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

    st.subheader("EDA")
    st.markdown("""
        * how many reviews per stores, how many star ratings, user location
        * viz of word cloud
        * n-grams for each star rating
        * sentiment analysis for each star rating
    """)

if __name__ == "__main__":
    run()