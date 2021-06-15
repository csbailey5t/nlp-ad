import pandas as pd
import re
import requests
import streamlit as st

from JSON.JSON_scraper import search_catalog
from match_titles import get_similar_titles


@st.cache()
def get_catalog_results(query: str) -> pd.DataFrame:
    df = search_catalog(query)
    return df


def api_poc():
    st.subheader("POC for connecting catalog and API")

    with st.form(key="catalog_search"):
        query = st.text_input(label="Search the catalog")
        submit_button = st.form_submit_button(label="Submit catalog search")

    catalog_data = get_catalog_results(query)
    st.subheader("Results from the catalog are:")
    st.write(catalog_data)

    st.subheader("Results from the API")
    api_keyword_data = requests.get(f"http://localhost:8000/keyword?q={query}").json()
    api_keyword_data_df = pd.DataFrame(api_keyword_data)
    st.write(api_keyword_data_df)

    st.subheader("Results from title similiarity")
    title_query = " ".join(catalog_data["title"])
    api_similarity_data = requests.get(
        f"http://localhost:8000/titlesimilarity?q={title_query}"
    ).json()
    st.write(api_similarity_data)
