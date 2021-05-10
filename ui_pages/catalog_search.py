from re import search
import streamlit as st

from JSON.JSON_scraper import search_catalog


def view_catalog_results():
    st.subheader("Search the Libraries' catalog")

    query = st.text_input("Search phrase", "data science")

    df = search_catalog(query)

    st.write(df)