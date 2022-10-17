import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

review_df = pd.read_csv('data/nyc_reviews_final.csv')
cleaned_review_df = pd.read_csv('data/reviews_cleaned.csv')

st.set_page_config(
    page_title="EDA",
    page_icon="📊",
)

st.title("Yelp Reviews - NYC Boba Shops🧋")
st.write("I created a dataset of Yelp reviews from NYC boba stores with the goal to perform text analysis.")
st.subheader('🔎 EDA')
st.markdown("The dataset has a total of **13,211 reviews** from **50 boba stores** in NYC.")

# plot reviews by store
store_reviews = review_df['store'].value_counts().reset_index()
store_reviews.columns = ['store','# of reviews']
fig = px.bar(store_reviews, x='store', y='# of reviews', title="Review Count for Each Store")
st.plotly_chart(fig, use_container_width=True)

# plot user location 
review_df = review_df.apply(
    lambda x: x.replace({
        'Manhattan, New York, NY':'New York, NY', 
        'Queens, Queens, NY':'Queens, NY',
        'Brooklyn, Brooklyn, NY': 'Brooklyn, NY'})
    )
store_reviews = review_df['user_loc'].value_counts().reset_index().head(10)
store_reviews.columns = ['location','# of reviews']
fig = px.bar(store_reviews, x='location', y='# of reviews', title="Where are the reviewers coming from?")
st.plotly_chart(fig, use_container_width=True)

# plot ratings
ratings = review_df['rating'].value_counts().reset_index()
ratings.columns = ['rating','num of reviews']
fig = px.pie(ratings, values='num of reviews', names='rating', title='Rating Distribution')
st.plotly_chart(fig, use_container_width=True)


# plot wordclouds
st.write("A word cloud of all words from the reviews after text preprocessing.")
my_stopwords = set(STOPWORDS)
corpus_wordcloud = " ".join(str(review) for review in cleaned_review_df.cleaned_text)
wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=my_stopwords).generate(corpus_wordcloud)
fig, ax = plt.subplots(figsize = (8,8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

st.write("Another word cloud but without the words: boba, bubble, place, tea, and drink.")
my_stopwords.update(["boba", "bubble", "place", "tea", "drink"])
wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=my_stopwords).generate(corpus_wordcloud)
fig, ax = plt.subplots(figsize = (8,8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)