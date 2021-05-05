import pandas as pd
import streamlit as st


@st.cache()
def workshops_count(df, n):
    counts = df["title"].value_counts()
    return counts[:n]


@st.cache()
def tag_count(df):
    return df["field_workshop_user_activities"].value_counts()


@st.cache()
def load_full_data(fn):
    return pd.read_csv(fn)


def all():
    df = load_full_data("all-workshops-2021-02-04.csv")

    st.subheader(
        "View raw data and calculated values on all workshop data for the last two years."
    )
    st.write(df)

    st.sidebar.subheader("All workshops options")
    num_workshops = st.sidebar.slider(
        "Number of most frequent workshops", 1, len(df["title"].unique()), value=30
    )

    st.subheader("Most frequent workshops")
    st.write(workshops_count(df, num_workshops))

    st.subheader("Most common tags")
    st.write(tag_count(df))