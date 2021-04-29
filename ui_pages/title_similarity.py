import streamlit as st

from match_titles import get_similar_titles


def query_section(nlp, docs):
    query = st.text_input(label="query string", value="Python")
    matches = get_similar_titles(query, docs, nlp)
    st.subheader("Match titles")
    st.write(matches)
