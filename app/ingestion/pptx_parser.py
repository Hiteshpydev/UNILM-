from pptx import Presentation
from pathlib import Path


def parse_pptx(file_path):
    """
    Extract text and tables from a PowerPoint presentation.

    Returns:
        {
            "metadata": {
                "source": filename,
                "file_type": "pptx",
                "slide_count": number_of_slides,
                "table_count": number_of_tables
            },
            "data": [
                {
                    "location": {
                        "type": "slide",
                        "number": slide_number
                    },
                    "content": {
                        "type": "text",
                        "text": slide_text
                    }
                },
                {
                    "location": {
                        "type": "slide",
                        "number": slide_number
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
        presentation = Presentation(file_path)

        data = []

        slide_count = 0
        table_count = 0

        for slide_number, slide in enumerate(
            presentation.slides,
            start=1
        ):

            slide_count += 1

            # ----------------------------------------
            # Extract text
            # ----------------------------------------

            slide_text = []

            for shape in slide.shapes:

                if hasattr(shape, "text"):
                    text = shape.text.strip()

                    if text:
                        slide_text.append(text)

            combined_text = "\n".join(slide_text)

            if combined_text:

                data.append({
                    "location": {
                        "type": "slide",
                        "number": slide_number
                    },
                    "content": {
                        "type": "text",
                        "text": combined_text
                    }
                })

            # ----------------------------------------
            # Extract tables
            # ----------------------------------------

            for table in slide.shapes:

                if not table.has_table:
                    continue

                table_data = []

                for row in table.table.rows:

                    row_data = []

                    for cell in row.cells:
                        row_data.append(
                            cell.text.strip()
                        )

                    table_data.append(row_data)

                # Skip empty tables
                if not any(
                    any(cell for cell in row)
                    for row in table_data
                ):
                    continue

                table_count += 1

                data.append({
                    "location": {
                        "type": "slide",
                        "number": slide_number
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
            "file_type": "pptx",
            "slide_count": slide_count,
            "table_count": table_count
        }

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:
        raise ValueError(
            f"Could not parse PPTX: {e}"
        )