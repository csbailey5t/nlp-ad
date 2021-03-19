"""
Goal: given a search string, find the most similar title
"""

import pandas as pd
import spacy


def load_data(fn, title_col):
    """
    Takes a path to csv file, loads data from title col
    Parameters:
    fn (string): path/to/file
    title_col (string): string title of column containing workshop titles
    """
    return pd.read_csv(fn, usecols=[f"{title_col}"])


def main(fn, title_col):
    """
    Entry function
    # Parameters:
    fn (string): path/to/file
    """
    nlp = spacy.load("en_core_web_lg")

    df = load_data(fn, title_col)
    docs = list(nlp.pipe(title for title in df["title"]))

    query = "R"
    query_doc = nlp(query)

    simils = [query_doc.similarity(title_doc) for title_doc in docs]

    # similarity will throw errors due to words without vectors
    # best to check those first, or disable the warning
    # https://stackoverflow.com/questions/55921104/spacy-similarity-warning-evaluating-doc-similarity-based-on-empty-vectors
    matches = [(docs[i], val) for i, val in enumerate(simils) if val >= 0.8]

    print(matches)


if __name__ == "__main__":
    fn = "all-workshops-2021-02-04.csv"
    title_col = "title"
    main(fn, title_col)
