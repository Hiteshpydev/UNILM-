from docx import Document
from pathlib import Path


def parse_docx(file_path):
    """
    Extract paragraphs and tables from a Word document.

    Returns:
        {
            "metadata": {
                "source": filename,
                "file_type": "docx",
                "paragraph_count": number_of_paragraphs,
                "table_count": number_of_tables
            },
            "data": [
                {
                    "location": {
                        "type": "paragraph",
                        "number": paragraph_number
                    },
                    "content": {
                        "type": "text",
                        "text": paragraph_text
                    }
                },
                {
                    "location": {
                        "type": "table",
                        "number": table_number
                    },
                    "content": {
                        "type": "table",
                        "data": table_data
                    }
                }
            ]
        }
    """

    try:
        document = Document(file_path)

        data = []

        # ----------------------------------------
        # Extract paragraphs
        # ----------------------------------------

        paragraph_count = 0

        for paragraph_number, paragraph in enumerate(
            document.paragraphs,
            start=1
        ):
            text = paragraph.text.strip()

            if not text:
                continue

            paragraph_count += 1

            data.append({
                "location": {
                    "type": "paragraph",
                    "number": paragraph_number
                },
                "content": {
                    "type": "text",
                    "text": text
                }
            })

        # ----------------------------------------
        # Extract tables
        # ----------------------------------------

        table_count = 0

        for table_number, table in enumerate(
            document.tables,
            start=1
        ):
            table_data = []

            for row in table.rows:
                row_data = []

                for cell in row.cells:
                    row_data.append(
                        cell.text.strip()
                    )

                table_data.append(row_data)

            # Skip completely empty tables
            if not any(
                any(cell for cell in row)
                for row in table_data
            ):
                continue

            table_count += 1

            data.append({
                "location": {
                    "type": "table",
                    "number": table_number
                },
                "content": {
                    "type": "table",
                    "data": table_data
                }
            })

        # ----------------------------------------
        # Metadata
        # ----------------------------------------

        metadata = {
            "source": Path(file_path).name,
            "file_type": "docx",
            "paragraph_count": paragraph_count,
            "table_count": table_count
        }

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:
        raise ValueError(
            f"Could not parse DOCX: {e}"
        )