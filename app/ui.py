# import streamlit as st

# def pdf_uploader():
#     return st.file_uploader("Upload a PDF file", type=["pdf"],accept_multiple_files=True,
#                             help="Upload one or more PDF files to process.")


import streamlit as st

def pdf_upload():
    """
    Returns a list of uploaded PDF files (Streamlit UploadedFile objects).
    """
    return st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload medical PDFs. Scanned/image-only PDFs may extract little or no text."
    )