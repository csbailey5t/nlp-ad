import pandas as pd
import streamlit as st

# import nltk and download stopwords for use
import nltk

nltk.download("stopwords")

from nltk.corpus import stopwords

from pandas import DataFrame
from typing import List


# should just save a cleaned version to disk to load rather than reclean
# since we're now also cleaning the query string, could probably skip cleaning data
@st.cache()
def load_data(fn: str) -> DataFrame:
    data = pd.read_csv(fn, usecols=["title", "body"])
    clean_data = data.assign(
        clean_title=data["title"].apply(lowercase_and_clean_string),
        clean_body=data["body"].apply(lowercase_and_clean_string),
    )
    return clean_data


def lowercase_and_clean_string(phrase: str) -> str:
    return " ".join(
        [
            word.lower()
            for word in phrase.split(" ")
            if not word.lower() in stopwords.words("english")
        ]
    )


def match_single_word_title(query: str, data: DataFrame) -> List[str]:
    words = query.split(" ")
    titles = [title for title in data["title"].to_list()]
    idxs = [
        i
        for (i, title) in enumerate(data["clean_title"].tolist())
        for word in words
        if word.lower() in title
    ]
    return [titles[i] for i in idxs]


def match_single_word_description(query: str, data: DataFrame) -> List[str]:
    words = query.split(" ")
    idxs = [
        i
        for (i, des) in enumerate(data["clean_body"])
        for word in words
        if word.lower() in des
    ]
    return [data["title"][i] for i in idxs]


def simple_search():
    st.subheader("Match a query with text in a workshop title or description")

    query = st.text_input(label="Query", value="Python")

    data = load_data("all-workshops-2021-02-04.csv")

    st.write("Title matches")
    title_matches = match_single_word_title(lowercase_and_clean_string(query), data)
    st.write(title_matches)

    st.write("Description matches")
    desc_matches = match_single_word_description(
        lowercase_and_clean_string(query), data
    )
    st.write(desc_matches)
