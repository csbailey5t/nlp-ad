"""
Goal: given a search string, find the most similar title
"""

import pandas as pd
import spacy
import typer

from spacy.tokens import Doc
from spacy.language import Language
from typing import List, Tuple
from pandas import DataFrame


def load_data(fn: str, title_col: str) -> DataFrame:
    """
    Takes a path to csv file, loads data from title col
    Parameters:
    fn (string): path/to/file
    title_col (string): string title of column containing workshop titles
    """
    return pd.read_csv(fn, usecols=[f"{title_col}"])


def build_corpus(fn: str, title_col: str, model: Language) -> List[Doc]:

    df = load_data(fn, title_col)
    docs = list(model.pipe(title for title in df[f"{title_col}"]))

    return docs


def get_similar_titles(
    query: str, docs: List[Doc], model: Language, threshold: float = 0.8
) -> List[Tuple]:
    """
    Find workshop titles with cosine similarity >= threshold to the submitted query
    """
    query_doc = model(query)

    simils = [query_doc.similarity(title_doc) for title_doc in docs]

    # similarity will throw errors due to words without vectors
    # best to check those first, or disable the warning
    # https://stackoverflow.com/questions/55921104/spacy-similarity-warning-evaluating-doc-similarity-based-on-empty-vectors
    matches = [(docs[i].text, val) for i, val in enumerate(simils) if val >= threshold]
    return matches


def main(query: str, threshold: float = 0.8):
    fn = "all-workshops-2021-02-04.csv"
    title_col = "title"
    nlp = spacy.load("en_core_web_lg")
    docs = build_corpus(fn, title_col, nlp)
    matches = get_similar_titles(query, docs, nlp, threshold)
    typer.echo(matches)


if __name__ == "__main__":
    typer.run(main)
