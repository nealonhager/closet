from google import genai
from PIL import Image
from io import BytesIO
from pathlib import Path
from typing import List, Optional
from flask import Flask, request, jsonify, send_file
import os
import uuid


# Initialize Flask app
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Initialize folders
INPUT_FOLDER = Path("images/input")
OUTPUT_FOLDER = Path("images/output")
ARCHIVE_FOLDER = Path("images/archive")


def assure_folders_exist(*folders: List[Path]) -> None:
    """
    Assure that the folders exist
    """
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def process_image_with_ai(image_path: Path, article: str) -> Optional[Path]:
    """
    Process a single image with AI to extract the clothing article.

    Args:
        image_path: Path to the input image
        article: Type of clothing article to extract

    Returns:
        Path to the processed image or None if processing failed
    """
    client = genai.Client()
    prompt = f"I'm going to send you a picture of a {article}, i want you to remove the rest of the image and only show the {article}. Remove any people, pets, or other objects that are not the {article}. I'm trying to make an app that will show all the things in your closet. If you can't find the article, don't return an image."

    try:
        image_prompt = Image.open(image_path)
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview", contents=[prompt, image_prompt]
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                new_file_name = f"{image_path.stem} - {article}.png"
                output_path = OUTPUT_FOLDER / new_file_name
                image.save(output_path)
                return output_path
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

    return None


@app.route("/health", methods=["GET"])
def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Status information about the API
    """
    return jsonify({"status": "healthy", "message": "Closet API is running"})


@app.route("/process", methods=["POST"])
def process_image() -> dict:
    """
    Process a single uploaded image to extract clothing article.

    Expected form data:
        - file: Image file to process
        - article: Type of clothing article to extract

    Returns:
        JSON response with processing results
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    if "article" not in request.form:
        return jsonify({"error": "No article type provided"}), 400

    file = request.files["file"]
    article = request.form["article"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return jsonify(
            {"error": "Invalid file type. Only PNG, JPG, and JPEG are supported"}
        ), 400

    # Ensure folders exist
    assure_folders_exist(INPUT_FOLDER, OUTPUT_FOLDER, ARCHIVE_FOLDER)

    # Save uploaded file temporarily
    filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = INPUT_FOLDER / filename
    file.save(temp_path)

    try:
        # Process the image
        result_path = process_image_with_ai(temp_path, article)

        if result_path and result_path.exists():
            return jsonify(
                {
                    "success": True,
                    "message": f"Successfully processed {article}",
                    "output_file": result_path.name,
                    "download_url": f"/download/{result_path.name}",
                }
            )
        else:
            return jsonify(
                {
                    "success": False,
                    "message": f"Could not extract {article} from the image",
                }
            ), 400

    except Exception as e:
        return jsonify({"success": False, "error": f"Processing failed: {str(e)}"}), 500

    finally:
        # Clean up temporary file
        if temp_path.exists():
            temp_path.unlink()


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename: str):
    """
    Download a processed image file.

    Args:
        filename: Name of the file to download

    Returns:
        The requested file or 404 if not found
    """
    file_path = OUTPUT_FOLDER / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/list-processed", methods=["GET"])
def list_processed_files() -> dict:
    """
    List all processed image files.

    Returns:
        JSON response with list of processed files
    """
    assure_folders_exist(OUTPUT_FOLDER)

    files = []
    for file_path in OUTPUT_FOLDER.glob("*.png"):
        files.append(
            {
                "filename": file_path.name,
                "download_url": f"/download/{file_path.name}",
                "size": file_path.stat().st_size,
                "created": file_path.stat().st_ctime,
            }
        )

    return jsonify({"files": files, "count": len(files)})


if __name__ == "__main__":
    # Ensure folders exist on startup
    assure_folders_exist(INPUT_FOLDER, OUTPUT_FOLDER, ARCHIVE_FOLDER)

    # Run the Flask app
    debug_mode = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
