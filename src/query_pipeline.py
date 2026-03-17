from src.embed import embed_text
from src.pinecone_client import get_index


def retrieve_resumes(query: str, top_k: int = 5):

    # Convert query to embedding
    query_vector = embed_text(query)

    index = get_index()

    # Search Pinecone
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    resumes = []

    for match in results["matches"]:
        resumes.append({
            "score": match["score"],
            "text": match["metadata"]["text"],
            "file_name": match["metadata"]["file_name"],
            "category": match["metadata"].get("category", "Unknown")
        })

    return resumes