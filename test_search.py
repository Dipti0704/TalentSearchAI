from src.query_pipeline import retrieve_resumes
from src.llm import generate_answer

query = "Find machine learning engineers"

resumes = retrieve_resumes(query)

answer = generate_answer(query, resumes)

print(answer)