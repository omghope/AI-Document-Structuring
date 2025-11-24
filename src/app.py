"""
app.py
Streamlit-based UI for live demo of the PDF → Excel converter.
"""

import streamlit as st
from pathlib import Path

from extractor import extract_text_from_pdf
from parser import parse_document
from formatter import format_to_dataframe
from export_excel import export_to_excel


st.set_page_config(page_title="AI Document Structuring", layout="wide")

st.title("AI-Powered Document Structuring & Extraction")
st.write("Upload the PDF and generate the structured Excel output.")

uploaded_file = st.file_uploader("Upload PDF (Data Input.pdf)", type=["pdf"])

if uploaded_file is not None:

    # Save uploaded file
    temp_path = Path("temp_uploaded.pdf")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(str(temp_path))

    st.text_area("Extracted Raw Text", raw_text[:8000], height=250)

    st.info("Parsing document...")
    parsed = parse_document(raw_text)

    st.success("Parsed successfully!")

    st.write("### Structured Data")
    df = format_to_dataframe(parsed)
    st.dataframe(df, use_container_width=True)

    # Export to Excel
    output_file = "Output.xlsx"
    export_to_excel(df, raw_text, output_file)

    with open(output_file, "rb") as f:
        st.download_button(
            label="Download Output.xlsx",
            data=f,
            file_name="Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Please upload a PDF to begin.")
