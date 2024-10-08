import os
import subprocess
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path

# Function to clear existing OCR (if needed)
def clear_existing_ocr(file_path):
    # This function would typically require more complex logic to manipulate existing OCR
    # For simplicity, we will assume that we are creating a new file without OCR instead
    return file_path.suffix.lower() in ['.pdf', '.tiff', '.tif', '.jpeg', '.jpg']

# Function to perform OCR on the image or PDF file
def perform_ocr(input_file, output_file):
    # Call Tesseract OCR
    try:
        # If output is a PDF, add .pdf extension
        if output_file.suffix.lower() == '.pdf':
            output_file = output_file.with_suffix('.pdf')

        subprocess.run(['tesseract', str(input_file), str(output_file.stem), '--oem', '3', '--psm', '6'], check=True)
        print(f"OCR completed for {input_file} and saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error during OCR: {e}")

# Function to process files in folder A and output to folder B
def process_files(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    for file in input_path.glob('*'):
        if clear_existing_ocr(file):
            # Create an output filename
            output_file = output_path / (file.stem + '_ocr' + file.suffix)

            # If the file is a PDF, convert it to images before OCR
            if file.suffix.lower() == '.pdf':
                images = convert_pdf_to_images(file)
                for img in images:
                    perform_ocr(img, output_file)
            else:
                perform_ocr(file, output_file)

def convert_pdf_to_images(pdf_file):
    # Use Pillow to convert PDF to images
    images = convert_from_path(pdf_file)
    image_files = []

    # Save each image for processing
    for i, img in enumerate(images):
        img_path = Path(pdf_file.stem + f'_page_{i + 1}.png')
        img.save(img_path, 'PNG')
        image_files.append(img_path)

    return image_files

if __name__ == "__main__":
    # Define your input and output folders
    base_folder = Path("OCR")
    input_folder = base_folder / "A"
    output_folder = base_folder / "B"

    process_files(input_folder, output_folder)
