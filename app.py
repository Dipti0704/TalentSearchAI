import streamlit as st
from agent import handle_query, set_job_description, get_last_candidates

st.set_page_config(layout="wide")

st.title("🤖 TalentSearch AI Dashboard")

# ---------------- JD PANEL ---------------- #

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📄 Job Description")

    jd = st.text_area("Paste JD")

    if st.button("Set JD"):
        set_job_description(jd)
        st.success("JD set successfully!")

# ---------------- CHAT PANEL ---------------- #

with col2:
    st.subheader("💬 Chat Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask about candidates...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        response = handle_query(user_input)
        st.session_state.chat_history.append(("bot", response))

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# ---------------- CANDIDATES TABLE ---------------- #

st.divider()
st.subheader("👥 Candidates")

candidates = get_last_candidates()

if candidates:

    for i, c in enumerate(candidates[:10]):

        col1, col2, col3, col4 = st.columns([2, 1, 2, 1])

        with col1:
            st.write(f"**{i+1}. {c['file_name']}**")

        with col2:
            st.write(f"Score: {c['score']}")

        with col3:
            st.write(c.get("resume_link", "No link"))

        with col4:
            if st.button(f"Shortlist {i}", key=i):
                from src.sheet_highlighter import highlight_candidate
                if c.get("email"):
                    highlight_candidate(c["email"])
                    st.success(f"{c['file_name']} shortlisted!")

else:
    st.info("No candidates yet. Run a search.")

# ---------------- BULK SHORTLIST ---------------- #

st.divider()
st.subheader("⭐ Bulk Actions")

top_k = st.number_input("Shortlist top K", min_value=1, max_value=10, value=3)

if st.button("Shortlist Top K"):
    from src.sheet_highlighter import highlight_candidate

    for c in candidates[:top_k]:
        if c.get("email"):
            highlight_candidate(c["email"])

    st.success(f"Top {top_k} candidates shortlisted!")