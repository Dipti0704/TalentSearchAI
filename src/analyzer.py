from openai import OpenAI

client = OpenAI()

def analyze_candidate(query, resume_text):

    prompt = f"""
You are a recruiter assistant.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Return JSON:

{{
  "score": number (0–100),
  "highlights": ["point1", "point2"]
}}

Rules:

- DO NOT give same scores
- Use full range (60–95)
- Better candidates must have higher scores
- Be highly discriminative
- Use different scores for different candidates
- Be concise and focus on key skills, projects, and relevant experience.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # ✅ cheap
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    import json
    return json.loads(response.choices[0].message.content)