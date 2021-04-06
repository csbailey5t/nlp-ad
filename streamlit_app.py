import pandas as pd
import spacy
import spacy_streamlit
import streamlit as st

from match_titles import get_similar_titles, build_corpus

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


@st.cache()
def workshops_count(df, n):
    counts = df["title"].value_counts()
    return counts[:n]


@st.cache()
def tag_count(df):
    return df["field_workshop_user_activities"].value_counts()


def single(selected_workshop, df, ner_labels):
    st.write("Selected workshop: ", selected_workshop)
    selected_description = df[df.title == selected_workshop].body.to_list()[0]

    doc = spacy_streamlit.process_text("en_core_web_md", selected_description)
    spacy_streamlit.visualize_tokens(doc, title="Token attributes")

    spacy_streamlit.visualize_ner(doc, labels=ner_labels, title="Named entities")


def all(df, num_workshops, nlp, docs):
    st.subheader("Raw data")
    st.write(df)

    st.subheader("Most common workshops")
    st.write(workshops_count(df, num_workshops))

    st.subheader("Most common tags")
    st.write(tag_count(df))

    st.subheader("Similarity query")
    query_section(nlp, docs)


def query_section(nlp, docs):
    query = st.text_input(label="query string", value="Python")
    matches = get_similar_titles(query, docs, nlp)
    st.write(matches)


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
    selected_level = st.sidebar.selectbox("Level", ["Single workshop", "All workshops"])

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
    else:
        all(df_full, num_workshops, nlp, docs)


if __name__ == "__main__":
    main()
