import os
import json
import PyPDF2
from docx import Document
import openpyxl

def extract_pdf_data(file_path):
    """Extract full text data from a PDF file."""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text  # Return entire extracted text

def extract_docx_data(file_path):
    """Extract full text data from a DOCX file."""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text  # Return entire extracted text

def extract_excel_data(file_path):
    """Extract full text data from an Excel file."""
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    text = ""
    for row in sheet.iter_rows(values_only=True):
        for cell in row:
            text += str(cell) + " "
    return text  # Return entire extracted text

def process_files(upload_folder):
    """Process all files in the upload folder."""
    file_data = []

    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        file_info = {
            'file_name': filename,
            'file_description': '',
            'tags': [],
            'keywords': [],
            'full_text': ''  # Store full extracted text
        }

        full_text = ""  # Initialize full_text to avoid UnboundLocalError

        if filename.lower().endswith('.pdf'):
            full_text = extract_pdf_data(file_path)

        elif filename.lower().endswith('.docx'):
            full_text = extract_docx_data(file_path)

        elif filename.lower().endswith('.xlsx'):
            full_text = extract_excel_data(file_path)

        file_info['full_text'] = full_text  # Store extracted text in dictionary

        # Extract a simple description (first 500 characters) for the file
        file_info['file_description'] = full_text[:500]  # First 500 chars as description

        # Simple keywords based on the first 100 words from full text
        file_info['keywords'] = full_text.split()[:100]  # Use first 100 words as keywords

        # Optional: Automatically generate tags based on file type
        file_info['tags'] = [filename.split('.')[-1], 'extracted']

        file_data.append(file_info)

    return json.dumps(file_data, indent=4)
