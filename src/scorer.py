
from openai import OpenAI

client = OpenAI()


def score_candidate(query, resume_text):

    prompt = f"""
You are a strict recruiter AI.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Instructions:
- Score between 0 to 100
- DO NOT give same scores to multiple candidates
- Use full range (50–95)
- Be highly discriminative
- Compare depth of skills, projects, and relevance

Return ONLY a number.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    score = response.choices[0].message.content.strip()

    return score