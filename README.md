# Closet

A Python CLI tool that uses Google's Gemini AI to automatically process clothing images for your digital closet. The tool removes background elements and focuses only on the clothing item, making it perfect for creating a clean, organized digital wardrobe.

## Features

- **AI-powered image processing**: Uses Google's Gemini 2.5 Flash model to isolate clothing items
- **Batch processing**: Process multiple images at once or single files
- **Flexible input**: Support for PNG, JPG, and JPEG formats
- **Automatic organization**: Saves processed images with descriptive names
- **Archive functionality**: Option to move original images to an archive folder
- **Debug mode**: Detailed logging for troubleshooting

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed, then run:

```bash
poetry install
```

## Setup

1. **Get a Google AI API key**: Visit [Google AI Studio](https://aistudio.google.com/) to get your API key
2. **Set up environment**: Set the `GOOGLE_API_KEY` environment variable with your API key

## Usage

### Basic Usage

Process all images in the input folder:
```bash
poetry run python app.py -a "sweater"
```

Process a specific image:
```bash
poetry run python app.py -a "sweater" --input_file "path/to/your/image.jpg"
```

### Command Line Options

- `-a, --article`: **Required**. The type of clothing item (e.g., "sweater", "jeans", "dress")
- `--input_folder`: Input folder path (default: `images/input`)
- `--input_file`: Process a specific file instead of the entire input folder
- `--output_folder`: Output folder path (default: `images/output`)
- `--archive_folder`: Archive folder path (default: `images/archive`)
- `-d, --debug`: Enable debug mode for detailed logging
- `--archive`: Move processed images to archive folder

### Examples

```bash
# Process all sweaters in the input folder
poetry run python app.py -a "sweater"

# Process a specific dress with debug output
poetry run python app.py -a "dress" --input_file "my_dress.jpg" -d

# Process jeans and archive the originals
poetry run python app.py -a "jeans" --archive

# Use custom folders
poetry run python app.py -a "shirt" --input_folder "photos" --output_folder "processed"
```

## Project Structure

```
closet/
├── app.py                 # Main application
├── images/
│   ├── input/            # Place your clothing images here
│   ├── output/           # Processed images are saved here
│   └── archive/          # Original images (when using --archive)
├── pyproject.toml        # Poetry configuration
└── README.md
```

## How It Works

1. **Input**: The tool reads images from the specified input folder or file
2. **AI Processing**: Each image is sent to Google's Gemini AI with a prompt to isolate the clothing item
3. **Background Removal**: The AI removes people, pets, and other objects, keeping only the specified clothing item
4. **Output**: Clean images are saved to the output folder with descriptive names (e.g., `image - sweater.png`)


To set up development environment:
```bash
poetry install
pre-commit install
```

## License

MIT for now.
