import spacy
import streamlit as st

from match_titles import build_corpus
from ui_pages.single import single
from ui_pages.all import all
from ui_pages.home import home
from ui_pages.title_similarity import query_section
from ui_pages.tfidf import query_tfidf
from ui_pages.simple_keyword import simple_search
from ui_pages.cluster import cluster


def main():

    # We'll go ahead and do this load and compute while the user selects a page
    nlp = spacy.load("en_core_web_md")
    docs = build_corpus("all-workshops-2021-02-04.csv", "title", nlp)

    # Sidebar area
    st.sidebar.title("Options")
    st.sidebar.subheader("Select page")
    selected_level = st.sidebar.selectbox(
        "Pages",
        [
            "Home",
            "Single workshop",
            "All workshops",
            "Title similarity search",
            "Tf-idf keyword search",
            "Simple query search",
            "Cluster workshops",
        ],
    )

    # Main app area
    st.title("Experiments with NC State University Libraries Catalog and Workshop Data")

    if selected_level == "Home":
        home()
    elif selected_level == "Single workshop":
        single()
    elif selected_level == "All workshops":
        all()
    elif selected_level == "Title similarity search":
        query_section(nlp, docs)
    elif selected_level == "Tf-idf keyword search":
        query_tfidf()
    elif selected_level == "Simple query search":
        simple_search()
    elif selected_level == "Cluster workshops":
        cluster()


if __name__ == "__main__":
    main()
