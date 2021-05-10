import altair as alt
import pandas as pd
import scipy.sparse
import streamlit as st

from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD


@st.cache()
def load_data_matrix(fn: str):
    # data here is a sparse matrix saved as .npz
    return scipy.sparse.load_npz(fn)


def cluster():
    st.subheader("Visualize workshop clusters after tf-idf vectorization")
    st.write(
        "This visualization uses truncatedSVD and t-SNE for dimensionality reduction."
    )

    X = load_data_matrix("models/tfidf_workshops.npz")
    svd = TruncatedSVD(n_components=50)
    svd_embed = svd.fit_transform(X)
    X_svd_tsne_embedded = TSNE(n_components=2, perplexity=30).fit_transform(svd_embed)
    df_tsne = pd.DataFrame(X_svd_tsne_embedded, columns=["x", "y"])

    c = alt.Chart(df_tsne).mark_circle().encode(x="x", y="y")

    st.altair_chart(c, use_container_width=True)
