# agent.py

from openai import OpenAI
import json

from src.query_pipeline import retrieve_resumes, rank_candidates
from src.sheet_highlighter import highlight_candidate

client = OpenAI()

# Memory
memory = {
    "last_results": [],
    "job_description": None
}

# ---------------- TOOLS ---------------- #

def search_candidates(query):
    resumes = retrieve_resumes(query, top_k=10)
    ranked = rank_candidates(query, resumes)

    memory["last_results"] = ranked

    results = []

    for i, c in enumerate(ranked[:5]):
        results.append({
            "rank": i + 1,
            "name": c["file_name"],
            "score": c["score"],
            "email": c.get("email"),
            "resume_link": c.get("resume_link")
        })

    return results


def get_resume(index):
    try:
        c = memory["last_results"][index - 1]
        return c.get("resume_link", "Not available")
    except:
        return "Invalid index"


def shortlist_candidates(top_k):
    selected = memory["last_results"][:top_k]

    for c in selected:
        if c.get("email"):
            highlight_candidate(c["email"])

    return f"Shortlisted top {top_k} candidates."


# ---------------- AGENT ---------------- #

SYSTEM_PROMPT = """
You are an AI recruiter assistant.

You MUST respond ONLY in JSON format when performing actions.

Available tools:

1. search_candidates
   args: { "query": string }

2. get_resume
   args: { "index": number }

3. shortlist_candidates
   args: { "top_k": number }

Rules:
- If user asks to find candidates → call search_candidates
- If user asks for resume → call get_resume
- If user asks to shortlist → call shortlist_candidates

STRICT:
- Output ONLY JSON
- No explanation
- No text outside JSON

Example:
{
  "tool": "search_candidates",
  "args": { "query": "machine learning engineer" }
}
"""


def handle_query(user_query):

    # Use JD if available
    effective_query = memory["job_description"] or user_query

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )

    reply = response.choices[0].message.content
    
    print("LLM RAW RESPONSE:", reply)


    # Try parsing tool call
    try:
        tool_call = json.loads(reply)
    except:
        print("⚠️ JSON parse failed, fallback triggered")

        # 🔥 FORCE SEARCH (important)
        result = search_candidates(user_query)
        return format_candidates(result)

    tool = tool_call.get("tool")
    args = tool_call.get("args", {})

    # Execute tool
    if tool == "search_candidates":
        result = search_candidates(args.get("query", effective_query))
        return format_candidates(result)

    elif tool == "get_resume":
        return get_resume(args.get("index", 1))

    elif tool == "shortlist_candidates":
        return shortlist_candidates(args.get("top_k", 3))
    

    return reply


# ---------------- FORMAT ---------------- #

def format_candidates(candidates):

    if not candidates:
        return "No relevant candidates found."

    text = "### Top Candidates:\n\n"

    for c in candidates:
        text += (
            f"{c['rank']}. {c['name']} "
            f"(Score: {c['score']})\n"
            f"Resume: {c['resume_link']}\n\n"
        )

    return text


# ---------------- JD ---------------- #

def set_job_description(jd):
    memory["job_description"] = jd
    
    
def get_last_candidates():
    return memory["last_results"]

