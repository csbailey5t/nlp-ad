import pandas as pd
import streamlit as st

from pandas import DataFrame
from typing import List

# Given a query of one or more words, we want to determine whether a combination of those words
# appears in the keywords extracted by tfidf


@st.cache()
def load_data(fn: str) -> DataFrame:
    return pd.read_csv(fn)


def match_single_word(query: str, data: DataFrame) -> List[str]:
    words = query.split(" ")
    keywords = data["term"].to_list()
    idxs = [
        i for (i, ks) in enumerate(keywords) for word in words if word.lower() in ks
    ]
    return [data["title"][i] for i in idxs]


def query_tfidf():
    tfidf_data = load_data("workshops_tfidf.csv")

    st.subheader("Match a workshop based on keywords extracted through tf-idf")

    query = st.text_input(label="query string", value="Python")

    matches = match_single_word(query, tfidf_data)
    st.write(matches)