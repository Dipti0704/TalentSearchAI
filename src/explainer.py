from openai import OpenAI

client = OpenAI()

def generate_highlights(query, resume_text):

    prompt = f"""
You are a recruiter assistant.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Extract ONLY the most important highlights.

Return:
- 4–5 bullet points
- Focus on:
  - key skills
  - best projects
  - relevant experience
  - standout achievements

Keep it SHORT and SCANNABLE.
No paragraphs.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content