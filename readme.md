# Using NLP to fuel library discovery

This is an experimental project to discover ways that natural language processing can provide different forms of discovery for library collections, workshops, and events.

The initial version attempts to surface relevant workshops on various types of catalog and Libraries' website pages, beyond the limitations of existing keyword searches.

## Running the project code

The project currently manages libraries and virtual environments with [`poetry`](https://python-poetry.org/).

After you've cloned this repository, run `poetry install` to install dependencies into a new virtual environment.

Analysis code using `spaCy` requires an installed language model. For the current code, which uses v2 of `spaCy`, install the large English language model. Within an activated virtual environment, run `python -m spacy download en_core_web_lg`.

The project uses Jupyter notebooks. `poc.ipynb` is a running experimentation file. As chunks settle, they'll be abstracted out into individual notebooks or scripts.
