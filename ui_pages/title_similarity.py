import streamlit as st

from match_titles import get_similar_titles


def query_section(nlp, docs):

    instructions = "Enter a search phrase to find any titles that match according to cosine similarity. This uses spaCy's English language model and similarity score, with a threshold of .80."
    st.subheader(instructions)

    query = st.text_input(label="Search phrase", value="Python")
    matches = get_similar_titles(query, docs, nlp)

    st.subheader("Matching titles")
    st.write(matches)
