from pptx import Presentation
from pathlib import Path


def parse_pptx(file_path):
    """
    Extract text from a PowerPoint presentation slide by slide.

    Returns:
        {
            "metadata": {
                "source": filename,
                "slide_count": number_of_slides
            },
            "slides": [
                {
                    "slide": slide_number,
                    "text": slide_text
                }
            ]
        }
    """

    try:
        presentation = Presentation(file_path)

        

        data = []

        for slide_number, slide in enumerate(
            presentation.slides,
            start=1
        ):
            slide_text = []

            for shape in slide.shapes:

                if hasattr(shape, "text"):
                    text = shape.text.strip()

                    if text:
                        slide_text.append(text)

            combined_text = "\n".join(slide_text)

            if not combined_text:
                continue

            data.append({
                "location": {
                    "type": "slide",
                    "number": slide_number
                },
                "text": combined_text
            })
        metadata = {
            "source": Path(file_path).name,
            "file_type": "pptx",
            "slide_count": len(data)
        }

        return {
            "metadata": metadata,
            "data": data
        }

    except Exception as e:
        raise ValueError(f"Could not parse PPTX: {e}")