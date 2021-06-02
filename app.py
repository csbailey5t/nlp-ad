import random
import re
import requests
import spacy
import pytextrank

from fastapi import FastAPI
from spacy.language import Language

from typing import Any, List, Tuple


app = FastAPI()

workshops_url = "https://www.lib.ncsu.edu/rest_workshops/master-workshops-feed.json"


async def get_json_api_data(url: str):
    """
    Given a url to a JSON api, return the JSON
    """
    r = requests.get(url)
    return r.json()


def extract_keywords(text: str, model: Language) -> List[Tuple]:
    doc = model(text)
    return [(phrase.text, phrase.rank) for phrase in doc._.phrases[:10]]


def strip_html_tags(text: str) -> str:
    tag = re.compile("<.*?>")
    return re.sub(tag, "", text)


def match_single_word(query: str, keywords: List[List[Tuple[Any, Any]]]) -> List[int]:
    words = query.split(" ")
    idxs = []
    for (i, keyword_list) in enumerate(keywords):
        kws = [keyword.lower().strip() for (keyword, score) in keyword_list]
        for word in words:
            if any(word.lower() in k for k in kws):
                idxs.append(i)
    return idxs


@app.get("/")
async def root():
    data = await get_json_api_data(workshops_url)
    random_workshop = random.choices(data, k=1)
    return {"workshops": random_workshop}


nlp = spacy.load("en_core_web_md")
nlp.add_pipe("textrank")


@app.get("/keyword")
async def keyword(q: str):
    data = await get_json_api_data(workshops_url)
    workshop_keywords = [
        extract_keywords(desc, nlp)
        for desc in [strip_html_tags(item["description"]) for item in data]
    ]
    matching_indices = match_single_word(q, workshop_keywords)
    return [data[i] for i in matching_indices]
