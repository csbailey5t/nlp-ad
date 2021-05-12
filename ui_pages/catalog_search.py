from pandas.core.frame import DataFrame
import pandas as pd
import re
import spacy
from spacy.language import Language
from spacy.tokens import Doc
import streamlit as st
from typing import List

from match_titles import get_similar_titles
from JSON.JSON_scraper import search_catalog


@st.cache()
def get_catalog_results(query: str) -> DataFrame:
    df = search_catalog(query)
    return df


@st.cache()
def load_data(fn: str, title_col: str, body_col: str) -> DataFrame:
    """
    Takes a path to csv file, loads data from title and body cols
    Dedups data based on title

    Parameters:
    fn (string): path/to/file
    title_col (string): string title of column containing workshop titles
    body_col (string): string title of column containing wokshop descriptions
    """
    df = pd.read_csv(fn, usecols=[f"{title_col}", f"{body_col}"])
    df.drop_duplicates(subset=["title"], keep="last", inplace=True)
    return df


def build_corpus(fn: str, title_col: str, body_col: str, model: Language) -> List[Doc]:

    df = load_data(fn, title_col, body_col)
    # df_combined = df.assign(title_body=df[f"{title_col}"] + df[f"{body_col}"])
    # docs = list(model.pipe(content for content in df_combined["title_body"]))

    # for the moment, just use titles until we figure out data cleaning of summaries
    docs = list(model.pipe(content for content in df["title"]))
    return docs


def strip_html_tags(text: str) -> str:
    tag = re.compile("<.*?>")
    return re.sub(tag, "", text)


def extract_catalog_query(catalog_df: DataFrame, title_col: str, desc_col: str) -> str:
    """
    Given a DataFrame of catalog data:
    - combines the title and description columns
    - combines all of the combined titles and descriptions into a single string

    This string will be used as the query when matching against workshops.
    """
    df_combined = catalog_df.assign(
        title_desc=catalog_df[f"{title_col}"] + catalog_df[f"{desc_col}"]
    )

    # combined = df_combined["title_desc"].to_list()
    # return " ".join(
    #     [strip_html_tags(content) for content in combined if type(content) == str]
    # )

    # For now, just return a string of combined titles
    return " ".join(catalog_df[f"{title_col}"])


def match_workshops():
    st.write("Matching workshops per vector similiarty with titles + descriptions")

    st.subheader("Search the Libraries' catalog")
    query = st.text_input("Search phrase", "data science")

    catalog_data = get_catalog_results(query)
    st.subheader("Results from the catalog are:")
    st.write(catalog_data)

    catalog_query = extract_catalog_query(catalog_data, "title", "summary")
    st.subheader("The query passed to the similarity function:")
    st.write(catalog_query)
    nlp = spacy.load("en_core_web_md")
    fn = "all-workshops-2021-02-04.csv"
    docs = build_corpus(fn, "title", "body", nlp)

    matches = get_similar_titles(catalog_query, docs, nlp, 0.8)
    st.subheader("Matching workshops:")
    st.write(matches)
