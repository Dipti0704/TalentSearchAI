#  TalentSearch AI — Resume RAG + Agentic Hiring System

##  Overview

TalentSearch AI is an end-to-end AI-powered recruiter assistant that allows users to:

* Search candidates using natural language queries
* Retrieve resumes using RAG (Retrieval-Augmented Generation)
* Rank candidates intelligently
* View strong highlights instead of full resumes
* Shortlist candidates directly to Google Sheets

This project combines:

*  LLM Agent (decision making)
*  Vector Search (Pinecone)
*  Resume Parsing
*  Streamlit Dashboard UI

---

##  System Architecture

```

User → Streamlit UI → Agent (LLM)
↓
Pinecone (Vector DB)
↓
Ranked Candidates + Highlights
↓
UI (Cards + Shortlisting)

```

---

##  Features

###  Smart Candidate Search

* Natural language queries ("top 5 ML engineers")
* Dynamic `top_k` handling

###  Agentic Behavior

* LLM decides which tool to call
* Supports:

  * search_candidates
  * shortlist_candidates
  * get_resume

###  Resume Processing

* Fetch resumes from Google Drive
* Parse PDF content
* Chunk + embed using OpenAI embeddings

###  RAG Pipeline

* Store embeddings in Pinecone
* Retrieve relevant chunks
* Rank candidates using LLM + similarity

###  Candidate Highlights

* Each candidate shows:

  * Score
  * Resume link
  * Strong points (bullet format)

###  Shortlisting

* Individual shortlist button
* Bulk shortlist (Top K)
* Automatically updates Google Sheets (green highlight)

###  Logging

* All results stored in `logs.txt`

---

##  Project Structure

```
Resume-RAG/
│
├── app.py                  # Streamlit UI
├── agent.py               # Agent logic
│
├── scripts/
│   └── run_pipeline.py    # Ingestion pipeline
│
├── src/
│   ├── analyzer.py        # Score + highlights
│   ├── chunker.py
│   ├── embed.py
│   ├── google_drive.py
│   ├── google_sheets.py
│   ├── pdf_parser.py
│   ├── pinecone_client.py
│   ├── query_pipeline.py
│   ├── scorer.py
│   ├── sheet_highlighter.py
│
├── resumes/               # (optional local storage)
├── logs.txt               # query logs
├── requirements.txt
└── credentials.json       # Google Sheets access
```

---

##  Setup Instructions

### 1 Clone Repo

```bash
git clone <your-repo-url>
cd Resume-RAG
```

---

### 2️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️ Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX=resumes-index
```

---

### 4️ Google Sheets Setup

1. Create Service Account (Google Cloud)
2. Download `credentials.json`
3. Share your Google Sheet with:

```
<client_email from credentials.json>
```

---

### 5️ Run Ingestion Pipeline

```bash
python -m scripts.run_pipeline
```

 This will:

* Fetch resumes from Google Drive
* Extract text
* Create embeddings
* Store in Pinecone

 Run only once (avoid repeated indexing to save cost)

---

### 6 Run App

```bash
streamlit run app.py
```

---

##  Example Queries

* "give me top 5 ML candidates"
* "best frontend developers"
* "shortlist top 3 candidates"
* "show resume of candidate 2"

---

##  Key Design Decisions

###  Separation of Concerns

* Agent → decision making
* UI → rendering only

###  Cost Optimization

* Uses `gpt-4o-mini` (cheap model)
* Combined scoring + highlights in one call
* Avoids repeated LLM calls

###  Robust Pipeline

* Handles:

  * invalid PDFs
  * folder links
  * corrupted files

###  Dynamic Behavior

* Supports user-driven `top_k`
* No hardcoding

---

##  Known Limitations

* Resume parsing depends on PDF quality
* Google Drive folder links are skipped
* LLM scoring can vary slightly

---

##  Future Improvements

* JD upload (PDF)
* Skill-based filtering
* Candidate comparison dashboard
* Export shortlisted candidates
* Pagination / infinite scroll

---

##  Why This Project Stands Out

* Combines RAG + Agent + UI
* Real-world recruiter workflow
* Cost-optimized AI system
* Production-level thinking

---

##  Author

Dipti Hatwar

---

