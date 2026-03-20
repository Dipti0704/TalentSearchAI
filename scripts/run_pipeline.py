import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.google_sheets import get_candidates
from src.google_drive import get_file_bytes
from src.pdf_parser import extract_text_from_pdf_bytes
from src.embed import embed_text
from src.chunker import chunk_text
from src.pinecone_client import ensure_index, get_index

print("🚀 FILE IS RUNNING")

def run_pipeline():
    print("🚀 RUN PIPELINE STARTED")

    ensure_index()
    index = get_index()

    candidates = get_candidates()

    print("TOTAL CANDIDATES:", len(candidates))
    print("SAMPLE:", candidates[:2])

    for c in candidates:

        name = c["name"]
        email = c["email"]
        resume_link = c["resume_link"]

        print("Processing:", name)

        file_bytes = get_file_bytes(resume_link)

        if not file_bytes:
            print("Failed to fetch file")
            continue

        text = extract_text_from_pdf_bytes(file_bytes)

        if not text.strip():
            print("Empty text")
            continue

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = embed_text(chunk)

            index.upsert([
                {
                    "id": f"{email}_chunk_{i}",
                    "values": vector,
                    "metadata": {
                        "name": name,
                        "email": email,
                        "resume_link": resume_link,
                        "text": chunk
                    }
                }
            ])

        print("Indexed:", name)
        
if __name__ == "__main__":
    run_pipeline()