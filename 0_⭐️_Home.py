import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="NLP",
        page_icon="⭐️",
    )
    st.title("Boba Reviews")
    st.sidebar.success("Select a demo above.")

    st.write(""" The goal of this project is to analyze reviews on Yelp from NYC boba shops and \
        find relationships between words and star ratings using NLP techniques. I gathered data from \
        webscraping reviews on Yelp from 50 boba stores in NYC. I performed EDA, text preprocessing steps, \
        and text analysis, including sentiment analysis, n-grams, and topic modeling. I also experimented \
        with building a classification model to predict the star rating of a review.
    """)
    st.subheader("📌 EDA")
    st.markdown("""
        * dataframe
        * how many reviews per store? 
        * where are reviewers coming from?
        * rating distribution
        * map of store location
    """)

    st.subheader("📌 Text Analysis")
    st.markdown("""
        * word cloud
        * n-gram for each star rating
        * sentiment analysis for each star rating
    """)

if __name__ == "__main__":
    run()