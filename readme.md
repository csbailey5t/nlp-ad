# Using NLP to fuel library discovery

This is an experimental project to discover ways that natural language processing and machine learning can provide different forms of discovery for library collections, workshops, and events.

The initial version attempts to surface relevant workshops on various types of catalog and Libraries' website pages, beyond the limitations of existing keyword searches.

## Running the project code

The project includes necessary environment files for [`poetry`](https://python-poetry.org/) and `venv`/`virtualenv`.

After you've cloned this repository, run `poetry install` or `pip install -r requirements.txt` as appropriate to install dependencies into a new virtual environment.

Analysis code using `spaCy` requires an installed language model. The current code uses the small and medium English language models. Within an activated virtual environment, run `python -m spacy download en_core_web_lg` and `python -m spacy download en_core_web_md`.

The project uses Jupyter notebooks. `poc.ipynb` is a running experimentation file. As chunks settle, they'll be abstracted out into individual notebooks or scripts. `data.ipynb` is one example, which covers downloading json data from a Drupal endpoint for Libraries workshops, and doing a bit of cleaning before writing to a dated csv file.

## Scripts

- `match_titles.py` is a brief CLI to return the workshop titles similar to the submitted query according to vectors from the spaCy `en_core_web_lg` model. It's currently hardcoded with a cutoff of >= 0.8. To run the script, within the active virtual environment, run `python match_titles.py query`, where the query is a string.

## Streamlit app

This project uses Streamlit to provide a front end for exploration of our data and experiments. To run the Streamlit app, within an active virtual environment:

`streamlit run streamlit_app.py`

The top-level script of the app is at the root of the project directory. Individual pages are separate Python files in the `ui_pages` directory, and expose functions imported into the top-level script for use.

The Streamlit app contains a page, API POC, that integrates the Libraries' catalog search with the API server detailed below. Given a search query, the page will return the top catalog API results for the query, the results from the keyword extraction endpoint of the workshops API for the same query, and workshop titles that match based on similarity. This page of the app currently works only locally, and requires the FastAPI server to be running locally as well. 

## FastAPI app

This project includes an API app as a POC for how this work could be incorporated into existing, non-Python library applications. The main file for the API is `app.py`.

To run the API app locally, within an active virtual environment:

`uvicorn app:app --reload`

The app will run, by default, at `http://localhost:8000`. This endpoint simply returns a random, upcoming NC State University Libraries workshop.

The second endpoint, at `http://localhost:8000/keyword`, accepts a query parameter, `q`, and returns upcoming workshops that match based on keywords extracted from the workshop descriptions. For instance, `http://localhost:8000/keyword?q=data+visualization` returns a JSON list of workshops where either `data` or `visualization` is in an extracted keyword.

The third endpoint, at `http://localhost:8000/titlesimilarity`, accepts a query parameter, `q`, and returns upcoming workshops whose titles meet a sufficient threshhold according to vector similarity, determined by the spaCy `en_core_web_md` model. 
