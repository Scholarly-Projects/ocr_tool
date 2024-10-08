import os
import subprocess
from pathlib import Path
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to clear existing OCR files
def clear_existing_ocr(output_file):
    if output_file.exists():
        output_file.unlink()  # Deletes the existing OCR output

# Function to convert PDF to images using Ghostscript
def convert_pdf_to_images(pdf_file):
    output_folder = pdf_file.parent
    output_pattern = str(output_folder / (pdf_file.stem + '_page_%03d.png'))

    # Ghostscript command to convert PDF to PNG images
    subprocess.run([
        'C:\\Program Files (x86)\\gs\\gs10.04.0\\bin\\gswin32c.exe',
        '-dNOPAUSE',
        '-dBATCH',
        '-sDEVICE=pngalpha',
        f'-sOutputFile={output_pattern}',
        str(pdf_file)
    ], check=True)  # Ensure subprocess raises an error if it fails

    return list(output_folder.glob(f"{pdf_file.stem}_page_*.png"))

# Function to perform OCR on images and create a single OCR PDF
def perform_ocr(images, output_file):
    try:
        c = canvas.Canvas(str(output_file), pagesize=letter)
        for img in images:
            text = pytesseract.image_to_string(str(img))  # Perform OCR

            # Draw the original image on the PDF
            c.drawImage(str(img), 0, 0, width=612, height=792)  # Adjust sizes as necessary
            # Add recognized text below the image
            c.drawString(10, 10, text)  # Position text; adjust as necessary
            c.showPage()  # Move to the next page

        c.save()  # Save the PDF
        print(f"OCR completed and saved to {output_file}.")
    except Exception as e:
        print(f"Error during OCR: {e}")

# Function to process files in folder A and output to folder B
def process_files(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    for file in input_path.glob('*'):
        output_file = output_path / (file.stem + '_ocr.pdf')
        clear_existing_ocr(output_file)

        if file.suffix.lower() == '.pdf':
            images = convert_pdf_to_images(file)
            perform_ocr(images, output_file)  # Pass all images at once for a single output PDF
        else:
            perform_ocr([file], output_file)  # Process images directly

if __name__ == "__main__":
    base_folder = Path("OCR")
    input_folder = base_folder / "A"
    output_folder = base_folder / "B"

    process_files(input_folder, output_folder)
