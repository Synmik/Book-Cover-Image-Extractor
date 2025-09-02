# PDF and EPUB Cover Image Extractor
A simple application built with Python and Tkinter that allows extract cover images from PDF and EPUB files.
The application supports drag-and-drop functionality for easy file selection and saves extracted images as PNG files.

## Features
- **Dual Format Support**: Extract images from both PDF and EPUB files
- **Drag & Drop**: Intuitive drag-and-drop interface for file selection
- **Cover Image Extraction**: Extracts the first page (PDF) or first image (EPUB) as image
- **Output Directory Selection**: Choose where to save the extracted images

## Requirements
- PyMuPDF (for PDF processing)
- Pillow (for image handling)
- ebooklib (for EPUB processing)
- tkinterdnd2 (for drag-and-drop functionality)

## Installation
1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python book_image_extractor.py
   ```

2. Select a PDF or EPUB file using the "Select File" button or drag and drop it into the application window.
3. Choose an output directory where the image will be saved.
4. Click "Extract Image" to process the file and save the cover image.

The extracted image will be saved as a PNG file in the selected output directory with the filename format: `{original_filename}_cover.png`

## License
This project is available under the MIT License.
