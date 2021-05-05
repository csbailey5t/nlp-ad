import streamlit as st

from match_titles import get_similar_titles


def query_section(nlp, docs):

    instructions = "Enter a search phrase to find any titles that match according to cosine similarity. This uses spaCy's English language model and similarity score."
    st.subheader(instructions)

    query = st.text_input(label="Search phrase", value="Python")
    threshold = st.slider(
        label="Similarity threshold", min_value=0.5, max_value=1.0, value=0.8, step=0.05
    )
    matches = get_similar_titles(query, docs, nlp, threshold)

    st.subheader("Matching titles")
    st.write(matches)
