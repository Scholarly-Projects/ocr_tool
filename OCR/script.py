import os
import ocrmypdf

# Function to add OCR to PDFs in folder A and output to folder B
def add_ocr_to_pdfs(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)
            print(f"Processing {filename}...")

            # Run OCR on the PDF and output to the output folder
            ocrmypdf.ocr(input_pdf_path, output_pdf_path, deskew=True)
            print(f"Saved OCR'd PDF to {output_pdf_path}")

if __name__ == "__main__":
    # Input folder A and output folder B
    input_folder = "OCR/A"
    output_folder = "OCR/B"

    add_ocr_to_pdfs(input_folder, output_folder)
