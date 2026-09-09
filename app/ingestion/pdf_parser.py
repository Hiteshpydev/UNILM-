import pymupdf as fitz
from pathlib import Path


def parse_pdf(file_path):
    """
    Extract text and tables from a PDF.

    Returns:
        {
            "metadata": {
                "source": filename,
                "file_type": "pdf",
                "page_count": number_of_pages,
                "table_count": number_of_tables
            },
            "data": [
                {
                    "location": {
                        "type": "page",
                        "number": page_number
                    },
                    "content": {
                        "type": "text",
                        "text": page_text
                    }
                },
                {
                    "location": {
                        "type": "page",
                        "number": page_number
                    },
                    "content": {
                        "type": "table",
                        "data": table_data
                    }
                }
            ]
        }
    """

    pdf = None

    try:
        pdf = fitz.open(file_path)

        data = []

        table_count = 0

        # ----------------------------------------
        # Process every page
        # ----------------------------------------

        for page_number, page in enumerate(
            pdf,
            start=1
        ):

            # ------------------------------------
            # Extract text
            # ------------------------------------

            text = page.get_text().strip()

            if text:

                data.append({
                    "location": {
                        "type": "page",
                        "number": page_number
                    },
                    "content": {
                        "type": "text",
                        "text": text
                    }
                })

            # ------------------------------------
            # Extract tables
            # ------------------------------------

            try:
                tables = page.find_tables()

                for table in tables.tables:

                    table_data = table.extract()

                    # Skip empty tables
                    if not table_data:
                        continue

                    if not any(
                        any(
                            cell is not None and str(cell).strip()
                            for cell in row
                        )
                        for row in table_data
                    ):
                        continue

                    table_count += 1

                    data.append({
                        "location": {
                            "type": "page",
                            "number": page_number
                        },
                        "content": {
                            "type": "table",
                            "data": table_data
                        }
                    })

            except Exception:
                # If table detection fails on a page,
                # continue processing the remaining content.
                continue

        # ----------------------------------------
        # Metadata
        # ----------------------------------------

        metadata = {
            "source": Path(file_path).name,
            "file_type": "pdf",
            "page_count": len(pdf),
            "table_count": table_count
        }

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:

        raise ValueError(
            f"Could not parse PDF: {e}"
        )

    finally:

        if pdf is not None:
            pdf.close()