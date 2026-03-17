import argparse
import pandas as pd
from tqdm import tqdm

from src.embed import embed_texts
from src.pinecone_client import ensure_index, get_index


def main(csv_path: str, batch_size: int = 100):
    # Read CSV
    df = pd.read_csv(csv_path)

    if "Resume" not in df.columns or "Category" not in df.columns:
        raise ValueError("CSV must contain 'Resume' and 'Category' columns")

    # Create Pinecone index if not exists
    ensure_index()
    index = get_index()

    vectors = []

    for i, row in tqdm(df.iterrows(), total=len(df)):
        text = str(row["Resume"])
        category = str(row["Category"])

        vectors.append({
            "id": f"row_{i}",
            "text": text,
            "category": category
        })

        if len(vectors) >= batch_size:
            upsert_batch(index, vectors)
            vectors = []

    if vectors:
        upsert_batch(index, vectors)


def upsert_batch(index, rows):
    texts = [r["text"] for r in rows]

    embeddings = embed_texts(texts)

    pinecone_vectors = []

    for r, vec in zip(rows, embeddings):
        pinecone_vectors.append({
            "id": r["id"],
            "values": vec,
            "metadata": {
                "text": r["text"],
                "category": r["category"]
            }
        })

    index.upsert(vectors=pinecone_vectors)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to Resume CSV"
    )

    args = parser.parse_args()

    main(args.csv)