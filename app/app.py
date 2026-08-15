import streamlit as st
from ingestion.ingestion_manager import process_file
import tempfile
import os


st.set_page_config(
    page_title="UNILLM",
    page_icon="📚"
)


st.title("📚 UNILLM")

st.write(
    "Upload your study materials."
)


uploaded_files = st.file_uploader(
    "Upload your study materials",
    type=["pdf", "pptx", "docx"],
    accept_multiple_files=True
)


if uploaded_files:

    for uploaded_file in uploaded_files:

        file_extension = os.path.splitext(
            uploaded_file.name
        )[1].lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:

            temp_file.write(
                uploaded_file.read()
            )

            temp_path = temp_file.name

        try:

            result = process_file(temp_path)

            st.success(
                f"Processed "
                f"{result['metadata']['source']}"
            )

            st.write(
                f"Type: "
                f"{result['metadata']['file_type']}"
            )

            st.write(
                f"Extracted items: "
                f"{len(result['data'])}"
            )

            for item in result["data"]:

                location = item["location"]

                st.subheader(
                    f"{location['type'].title()} "
                    f"{location['number']}"
                )

                st.write(
                    item["text"][:500]
                )

                st.divider()

        except ValueError as e:

            st.error(
                f"Could not process "
                f"{uploaded_file.name}: {e}"
            )

        finally:

            os.remove(temp_path)