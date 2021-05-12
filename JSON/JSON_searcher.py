import JSON_scraper
import json
import streamlit as st
import pandas as pd

# Function to load JSON data, taking in # of rows for display
@st.cache
def load_data(nrows):
    data = pd.read_json('catalog_results_metadata.json')
    return data

data = load_data(50)
st.title('Catalog JSON Extraction')
st.subheader('Raw data')
st.dataframe(data)
