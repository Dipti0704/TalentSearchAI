from openai import OpenAI

client = OpenAI()

CATEGORIES = [
    "DATA-SCIENCE",
    "INFORMATION-TECHNOLOGY",
   
]


def classify_resume_category(text: str) -> str:

    prompt = f"""
    You are a resume classifier.

    Classify the resume into one of the following categories:

    {CATEGORIES}

    Return ONLY the category name.

    Resume:
    {text[:2000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    category = response.choices[0].message.content.strip()

    return category