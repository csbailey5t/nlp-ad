import streamlit as st

from match_titles import get_similar_titles


@st.cache()
def workshops_count(df, n):
    counts = df["title"].value_counts()
    return counts[:n]


@st.cache()
def tag_count(df):
    return df["field_workshop_user_activities"].value_counts()


def query_section(nlp, docs):
    query = st.text_input(label="query string", value="Python")
    matches = get_similar_titles(query, docs, nlp)
    st.write(matches)


def all(df, num_workshops, nlp, docs):
    st.subheader("Raw data")
    st.write(df)

    st.subheader("Most common workshops")
    st.write(workshops_count(df, num_workshops))

    st.subheader("Most common tags")
    st.write(tag_count(df))

    st.subheader("Similarity query")
    query_section(nlp, docs)