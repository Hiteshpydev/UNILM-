from docx import Document
from pathlib import Path


def parse_docx(file_path):
    """
    Extract text from a Word document paragraph by paragraph.

    Returns:
        {
            "metadata": {
                "source": filename,
                "paragraph_count": number_of_paragraphs
            },
            "paragraphs": [
                {
                    "paragraph": paragraph_number,
                    "text": paragraph_text
                }
            ]
        }
    """

    try:
        document = Document(file_path)

        data = []

        for paragraph_number, paragraph in enumerate(
            document.paragraphs,
            start=1
        ):
            text = paragraph.text.strip()

            if not text:
                continue

            data.append({
    "location": {
        "type": "paragraph",
        "number": paragraph_number
    },
    "text": text
})

        metadata = {
    "source": Path(file_path).name,
    "file_type": "docx",
    "paragraph_count": len(data)
}

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:
        raise ValueError(f"Could not parse DOCX: {e}")
    