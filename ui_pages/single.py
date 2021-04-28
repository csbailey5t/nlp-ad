import streamlit as st
import spacy_streamlit


def single(selected_workshop, df, ner_labels):
    st.write("Selected workshop: ", selected_workshop)
    selected_description = df[df.title == selected_workshop].body.to_list()[0]

    doc = spacy_streamlit.process_text("en_core_web_md", selected_description)
    spacy_streamlit.visualize_tokens(doc, title="Token attributes")

    spacy_streamlit.visualize_ner(doc, labels=ner_labels, title="Named entities")