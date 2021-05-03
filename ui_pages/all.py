import streamlit as st


@st.cache()
def workshops_count(df, n):
    counts = df["title"].value_counts()
    return counts[:n]


@st.cache()
def tag_count(df):
    return df["field_workshop_user_activities"].value_counts()


def all(df, num_workshops):
    st.subheader("Raw data")
    st.write(df)

    st.subheader("Most common workshops")
    st.write(workshops_count(df, num_workshops))

    st.subheader("Most common tags")
    st.write(tag_count(df))