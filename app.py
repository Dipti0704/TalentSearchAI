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

    from src.explainer import generate_highlights

    for i, c in enumerate(candidates):

        with st.container():
            st.markdown(f"## {i+1}. {c['file_name']}")
            st.write(f" Score: {c['score']}")

            # Resume link
            if c.get("resume_link"):
                st.markdown(f"[ Open Resume]({c['resume_link']})")
            else:
                st.write("No resume link")

            # 🔥 Highlights
            highlights = c.get("highlights", [])

            st.markdown("### 🔥 Strong Points")
            for point in highlights:
                st.markdown(f"- {point}")

            # Shortlist button
            if st.button(f"Shortlist {i}", key=f"s{i}"):
                from src.sheet_highlighter import highlight_candidate
                highlight_candidate(c["email"])
                st.success("Shortlisted!")

            st.divider()                    
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