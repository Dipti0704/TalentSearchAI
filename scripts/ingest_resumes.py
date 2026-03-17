import os
from tqdm import tqdm

from src.embed import embed_text
from src.pinecone_client import ensure_index, get_index
from src.docx_parser import extract_text_from_docx
from src.tools import classify_resume_category

RESUME_FOLDER = "resumes"


def ingest_resumes():

    ensure_index()
    index = get_index()

    for file in tqdm(os.listdir(RESUME_FOLDER)):

        print("Processing file:", file)

        if not file.endswith(".docx"):
            continue

        file_path = os.path.join(RESUME_FOLDER, file)

        # Extract resume text
        text = extract_text_from_docx(file_path)
        category = classify_resume_category(text)

        print("Predicted category:", category)

        print("Text length:", len(text))

        if not text.strip():
            print("Empty text for:", file)
            continue

        print("Generating embedding...")

        vector = embed_text(text)

        print("Upserting vector for:", file)

        index.upsert([
            {
                "id": file,
                "values": vector,
                "metadata": {
                    "text": text,
                    "file_name": file,
                    "category": category
                }
            }
        ])


if __name__ == "__main__":
    ingest_resumes()