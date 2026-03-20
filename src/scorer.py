
from openai import OpenAI

client = OpenAI()


def score_candidate(query, resume_text):

    prompt = f"""
You are a recruiter AI.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Give a match score between 0 and 100.

Only return the number.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    score = response.choices[0].message.content.strip()

    return score