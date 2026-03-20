from io import BytesIO
from PyPDF2 import PdfReader


def extract_text_from_pdf_bytes(file_bytes):

    pdf = PdfReader(BytesIO(file_bytes))

    text = ""

    for page in pdf.pages:
        text += page.extract_text() or ""

    return text