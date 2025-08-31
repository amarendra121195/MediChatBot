# from pypdf import  PdfReader
# from typing import List, Optional
# from io import BytesIO
# from pypdf import  PdfReader

# def extract_text_from_pdf(file):
#     reader = PdfReader(file)
#     text = ' '
#     for page in reader.pages:
#         text = text + page.extract_text() or ''
#     return text


from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf(file) -> str:
    """
    Accepts a Streamlit UploadedFile, path-like, or bytes-like object and returns extracted text.
    Safely concatenates page text and ignores None returns from extractor.
    """
    # Streamlit's UploadedFile provides .read(), but PdfReader can take the file directly too.
    # To be robust across both cases, wrap bytes in BytesIO if needed.
    try:
        if hasattr(file, "read"):  # UploadedFile or file-like
            # Important: make a separate BytesIO, so repeated reads work
            raw = file.read()
            reader = PdfReader(BytesIO(raw))
        else:
            # Path or file-like already suitable
            reader = PdfReader(file)
    except Exception as e:
        # Return an empty string so caller can handle "no text" gracefully
        return ""

    texts = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            texts.append(page_text)

    return "\n".join(texts).strip()