"""
Goal: given a search string, find the most similar title
"""

import pandas as pd
import spacy
import typer

from pandas import DataFrame


def load_data(fn: str, title_col: str) -> DataFrame:
    """
    Takes a path to csv file, loads data from title col
    Parameters:
    fn (string): path/to/file
    title_col (string): string title of column containing workshop titles
    """
    return pd.read_csv(fn, usecols=[f"{title_col}"])


def main(query: str):
    """
    Find workshop titles with >= .8 similarity to the submitted query
    """
    fn = "all-workshops-2021-02-04.csv"
    title_col = "title"

    nlp = spacy.load("en_core_web_lg")

    df = load_data(fn, title_col)
    docs = list(nlp.pipe(title for title in df[f"{title_col}"]))

    query_doc = nlp(query)

    simils = [query_doc.similarity(title_doc) for title_doc in docs]

    # similarity will throw errors due to words without vectors
    # best to check those first, or disable the warning
    # https://stackoverflow.com/questions/55921104/spacy-similarity-warning-evaluating-doc-similarity-based-on-empty-vectors
    matches = [(docs[i], val) for i, val in enumerate(simils) if val >= 0.8]

    typer.echo(matches)


if __name__ == "__main__":
    typer.run(main)
