import pandas as pd
import spacy
import streamlit as st

from match_titles import build_corpus
from ui_pages.single import single
from ui_pages.all import all
from ui_pages.title_similarity import query_section
from ui_pages.tfidf import query_tfidf

models = ["en_core_web_sm", "en_core_web_md"]


@st.cache()
def load_data(fn):
    df = pd.read_csv(fn)
    df = df.drop(columns=["Unnamed: 0"])

    df.drop_duplicates(subset=["title"], keep="last", inplace=True)
    return df


@st.cache()
def load_full_data(fn):
    return pd.read_csv(fn)


def main():
    df_dedup = load_data("all-workshops-2021-02-04.csv")
    titles = df_dedup["title"].to_list()

    df_full = load_full_data("all-workshops-2021-02-04.csv")

    nlp = spacy.load("en_core_web_md")
    ner_labels = nlp.get_pipe("ner").labels

    # for convenience, we'll repeat this chunk
    docs = build_corpus("all-workshops-2021-02-04.csv", "title", nlp)

    # Sidebar area
    st.sidebar.title("Options")
    st.sidebar.subheader("Select analysis level")
    selected_level = st.sidebar.selectbox(
        "Level", ["Single workshop", "Match title", "All workshops", "Tf-idf matching"]
    )

    st.sidebar.subheader("Single workshop options")
    selected_workshop = st.sidebar.selectbox("Select workshop", titles)

    st.sidebar.subheader("All workshops options")
    num_workshops = st.sidebar.slider(
        "Number of most frequent workshops", 1, len(titles), value=30
    )

    # Main app area
    st.title("NC State Libraries Workshop Data")

    if selected_level == "Single workshop":
        single(selected_workshop, df_dedup, ner_labels)
    elif selected_level == "Match title":
        query_section(nlp, docs)
    elif selected_level == "Tf-idf matching":
        query_tfidf()
    else:
        all(df_full, num_workshops)


if __name__ == "__main__":
    main()
