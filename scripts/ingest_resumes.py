import os
from tqdm import tqdm

from src.embed import embed_text
from src.pinecone_client import ensure_index, get_index
from src.docx_parser import extract_text_from_docx
from src.tools import classify_resume_category
from src.chunker import chunk_text

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

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = embed_text(chunk)

            index.upsert([
                {
                    "id": f"{file}_chunk_{i}",
                    "values": vector,
                    "metadata": {
                        "text": chunk,
                        "file_name": file,
                        "category": category
                    }
                }
            ])


if __name__ == "__main__":
    ingest_resumes()