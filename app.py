import streamlit as st

from src.query_pipeline import retrieve_resumes
from src.llm import generate_answer


st.title("TalentSearchAI")
st.write("AI-powered resume search for recruiters")

query = st.text_input("Enter recruiter query")

if st.button("Search"):

    if query:

        with st.spinner("Searching resumes..."):

            resumes = retrieve_resumes(query)

            answer = generate_answer(query, resumes)

        st.subheader("Results")

        st.write(answer)