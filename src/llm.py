from openai import OpenAI

client = OpenAI()


def generate_answer(query: str, resumes: list):

    context = ""

    for r in resumes:
        context += f"\nResume: {r['file_name']}\n"
        context += r["text"][:1500] + "\n"

    prompt = f"""
You are an AI recruiter assistant.

A recruiter asked the following query:

{query}

Below are some candidate resumes.

{context}

Identify the most relevant candidates and summarize why they are suitable.
Return the answer in a recruiter-friendly format.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content