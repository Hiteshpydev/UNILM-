import fitz  # PyMuPDF
from pathlib import Path


def parse_pdf(file_path):
    """
    Reads a PDF and extracts text page by page.

    Returns:
        List of dictionaries containing:
        - source (filename)
        - page number
        - extracted text
    """

    pdf = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text()

        pages.append({
            "source": Path(file_path).name,
            "page": page_number,
            "text": text.strip()
        })

    pdf.close()

    return pages