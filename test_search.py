from src.query_pipeline import retrieve_resumes

query = "data science engineer"

results = retrieve_resumes(query)

for r in results:
    print("\nResume:", r["file_name"])
    print("Score:", r["score"])
    print("Category:", r["category"])
    print(r["text"][:200])