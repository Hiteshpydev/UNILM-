import streamlit as st
from ingestion.pdf_parser import parse_pdf
import tempfile
import os

st.set_page_config(page_title="UNILLM", page_icon="📚")

st.title("📚 UNILLM")
st.write("Upload a PDF to extract its text.")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Parse the PDF
    pages = parse_pdf(temp_path)

    st.success(f"Extracted {len(pages)} pages.")

    for page in pages:
        st.subheader(f"Page {page['page']}")
        st.write(page["text"][:500])  # Show first 500 characters
        st.divider()

    os.remove(temp_path)