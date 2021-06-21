import streamlit as st
import pandas as pd
import yake
import numpy as np
import spacy 

#Import workshops file

@st.cache()
def get_workshops_df(fn): 
    workshops = pd.read_csv(fn)
    return workshops

#For reference this is the default yake function, which returns the top 20 keywords and their scores for a body of text
# def default_yake():
#     kw_extractor = yake.KeywordExtractor()
#     keywords = kw_extractor.extract_keywords(df["body"][0])
#     for kw in keywords:
#     return (kw)
 
#For reference this a custom Yake for just the top three keywords with their scores for a body of text
# def custom_kw_extractor(text):
#     custom_kw_extractor = yake.KeywordExtractor(top = 3)
#     top_three_keywords = custom_kw_extractor.extract_keywords(text)
#     return top_three_keywords

# This is the custom Yake function being used, which returns just the top three keywords without scores for a body of text
def get_top_three(description, custom_kw_extractor):
    top_three_keywords = custom_kw_extractor.extract_keywords(description)
    return [kw for (kw, _) in top_three_keywords]
    
# Main function to write everything onto the Streamlit page

# Pulling in the workshops file as a Pandas data frame
def extract_keywords():
    workshops_file = 'all-workshops-2021-02-04.csv'
    workshops_df = get_workshops_df(workshops_file)
    
# Writing the choose workshop prompt as a subheader to a list of workshop titles to choose from via a selection box    
    st.subheader("Choose a workshop title to see the top three Yake extracted keywords from the workshop's description")
    title_list = workshops_df["title"].to_list()
    selected_workshop = st.selectbox("Select workshop", title_list)
    
# Writing the title of the chosen workshop   
    st.write(selected_workshop)

# Go through the workshop data frame to find all workshops with the same title selected from the list above    
    filtered_workshops = workshops_df[workshops_df["title"] == selected_workshop]

# For the the workshops filtered by chosen title, apply the custom yake function to the body or descriptions of those workshops  
    custom_kw_extractor = yake.KeywordExtractor(top = 3)
    filtered_workshops["keywords_yake"] = filtered_workshops["body"].apply(get_top_three, args=(custom_kw_extractor,))
    #st.dataframe(filtered_workshops[["body","keywords_yake"]],width = 600)

 # Formatting the returned workshop descriptions with their keywords into two columns   
    col_description, col_keywords = st.beta_columns(2)
    with col_description: 
        st.write(filtered_workshops["body"])
    with col_keywords: 
        st.write(filtered_workshops["keywords_yake"])
        