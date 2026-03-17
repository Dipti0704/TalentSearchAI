from docx import Document


def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)

    text = []

    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)

    return "\n".join(text)