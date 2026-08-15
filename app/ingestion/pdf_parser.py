import pymupdf as fitz
from pathlib import Path


def parse_pdf(file_path):
    """
    Extract text from a PDF page by page.

    Returns:
        {
            "metadata": {
                "source": filename,
                "page_count": number_of_pages
            },
            "pages": [
                {
                    "page": page_number,
                    "text": page_text
                }
            ]
        }
    """

    try:
        pdf = fitz.open(file_path)

        

        data= []

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()

            # Skip pages with no extractable text
            if not text:
                continue

            data.append({
    "location": {
        "type": "page",
        "number": page_number
    },
    "text": text
})
        metadata = {
            "source": Path(file_path).name,
            "file_type": "pdf",
            "page_count": len(data)
        }

        pdf.close()

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:
        raise ValueError(f"Could not parse PDF: {e}")
    
    