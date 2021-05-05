import pandas as pd
import spacy
import spacy_streamlit
import streamlit as st


@st.cache()
def load_data(fn):
    df = pd.read_csv(fn)
    df = df.drop(columns=["Unnamed: 0"])

    df.drop_duplicates(subset=["title"], keep="last", inplace=True)
    return df


def single():
    df = load_data("all-workshops-2021-02-04.csv")
    titles = df["title"].to_list()

    st.sidebar.subheader("Single workshop options")
    selected_workshop = st.sidebar.selectbox("Select workshop", titles)

    st.subheader(
        "Select a workshop in the sidebar to analyze token properties and named entities with spaCy."
    )

    st.write("Selected workshop: ", selected_workshop)
    selected_description = df[df.title == selected_workshop].body.to_list()[0]

    nlp = spacy.load("en_core_web_md")
    ner_labels = nlp.get_pipe("ner").labels

    doc = spacy_streamlit.process_text("en_core_web_md", selected_description)
    spacy_streamlit.visualize_tokens(doc, title="Token attributes")

    spacy_streamlit.visualize_ner(doc, labels=ner_labels, title="Named entities")