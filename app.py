from google import genai
from PIL import Image
from io import BytesIO
from pathlib import Path
from typing import List
import click
from icecream import ic
from typing import Optional


def assure_folders_exist(*folders: List[Path]):
    """
    Assure that the folders exist
    """
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def get_input_files(input_folder: Path, input_file: Optional[Path]) -> List[Path]:
    """
    Get the input files from the input folder or the input file.

    Args:
        input_folder: The folder containing the input images
        input_file: The input image file

    Returns:
        A list of input files
    """
    if input_file is not None:
        input_files = [input_file]
    else:
        input_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"]:
            input_files.extend(input_folder.glob(ext))
        input_files = list(dict.fromkeys(input_files))

    for input_file in input_files:
        print(f"Found {input_file.name}")
    return input_files


@click.command()
@click.option("-a", "--article", type=str, required=True)
@click.option("--input_folder", type=Path, default="images/input")
@click.option("--input_file", type=Path, default=None)
@click.option("--output_folder", type=Path, default="images/output")
@click.option("--archive_folder", type=Path, default="images/archive")
@click.option("-d", "--debug", is_flag=True, default=False)
@click.option("--archive", is_flag=True, default=False)
def main(
    article, input_folder, input_file, output_folder, archive_folder, debug, archive
):
    """
    Process the images in the input folder or the input file.

    If input_file is provided, only process that file. Otherwise, process all files in the input folder.

    Args:
        article: The article of clothing to process
        input_folder: The folder containing the input images
        input_file: The input image file
        output_folder: The folder containing the output images
        archive_folder: The folder containing the archived images
        debug: Whether to print debug information
        archive: Whether to archive the input files
    """
    if debug:
        ic.enable()
    else:
        ic.disable()

    client = genai.Client()
    prompt = f"I'm going to send you a picture of a {article}, i want you to remove the rest of the image and only show the {article}. Remove any people, pets, or other objects that are not the {article}. I'm trying to make an app that will show all the things in your closet. If you can't find the article, don't return an image."
    ic(prompt)

    input_files = get_input_files(input_folder, input_file)

    if not input_files:
        print(f"No image files found in {input_folder}")
        return

    assure_folders_exist(input_folder, output_folder, archive_folder)

    for input_file in input_files:
        image_prompt = Image.open(input_file)

        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview", contents=[prompt, image_prompt]
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                new_file_name = f"{input_file.stem} - {article}.png"
                image.save(output_folder / new_file_name)
                print(f"Saved {new_file_name}")

        if archive:
            input_file.rename(archive_folder / f"{input_file.stem}.png")
            print(f"Archived {input_file}")


if __name__ == "__main__":
    main()
