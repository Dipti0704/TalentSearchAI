from src.embed import embed_text
from src.pinecone_client import get_index
from src.scorer import score_candidate


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
            "file_name": match["metadata"].get("name"),
            "name": match["metadata"].get("name"),
            "email": match["metadata"].get("email"),
            "resume_link": match["metadata"].get("resume_link"),
        })

    return resumes

def group_by_resume(resumes):

    grouped = {}

    for r in resumes:

        file_name = r["file_name"]

        if file_name not in grouped:
            grouped[file_name] = ""

        grouped[file_name] += " " + r["text"]

    return grouped

def rank_candidates(query, resumes):

    grouped_resumes = group_by_resume(resumes)

    ranked = []

    for file_name, resume_text in grouped_resumes.items():

        score = score_candidate(query, resume_text)

        ranked.append({
            "file_name": file_name,
            "score": int(score),
            "resume_text": resume_text
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked

