import re
import json
import requests
import pandas as pd
import urllib.request
import streamlit as st

# This script takes in a keyword from the user, retrieves the HTML of that
# search result, and isolates the catalog IDs using regex from the HTML of the search.
# It then generates valid .JSON urls of each individual item from the previous
# search and transforms them into one large .JSON file, named
# 'catalog_results_metadata.json', for further data transformation.

st.text('Input string you want to search the catalog for:')
string_input = st.text_input('Search')

if(st.button('Submit')):
    search_string = string_input.title()

# Replaces any spaces in a user input with '+' to make URL-friendly
search_string = search_string.replace(' ', '+')

    # Modify URL with search string input
catalogURL_search = ("https://catalog.lib.ncsu.edu/catalog?q=" + search_string +
    "&search_field=all_fields")

# Retrieve HTML of the modified URL and assign it to a decoded string
with urllib.request.urlopen(catalogURL_search) as res:
    catalogHTML = res.read().decode("utf-8")

# Use regex to find all catalog IDs from HTML results
pattern = "(?<=\/catalog\/)(.*?)(?=\/track)"
catalogIDs = re.findall(pattern, catalogHTML)

# Save catalog base URL to append with specific catalog IDs
catalogURL = 'https://catalog.lib.ncsu.edu/catalog/'

# Creates a list of valid .JSON urls for each catalog ID
catalogJSON_urls = [catalogURL + i + '.json' for i in catalogIDs]

# Parse all URLs from list and dump into a single JSON file
with open('catalog_results_metadata.json', 'w') as fp:
    json.dump([requests.get(url).json() for url in catalogJSON_urls], fp, indent=2)
