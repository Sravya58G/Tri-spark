import fitz
import re

def extract_text_from_pdf(file_path):
    """Extract clean text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        text = page.get_text("text")
        # basic normalization
        text = re.sub(r'\s+', ' ', text).strip()
        pages.append(text)
    return '\n\n'.join(pages)
