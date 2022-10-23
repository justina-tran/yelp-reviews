import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import creds
nltk.download('stopwords')
nltk.download('words')

stop_words = stopwords.words('english')

def plot_ngram(text, n):
  # ngrams counts
  count_vect = CountVectorizer(ngram_range = (n,n),
                               max_features=500,
                               stop_words=stop_words)
  cv_matrix = count_vect.fit_transform(text) 
  features = (count_vect.get_feature_names_out())

  cv_df = pd.DataFrame(cv_matrix.toarray(), columns=features)

  # ngrams tfidf
  tfidf = TfidfVectorizer(ngram_range = (n,n),
                          max_features=500,
                          # max_df=0.2,
                          # min_df=1, 
                          stop_words=stop_words)
  tfidf_matrix = tfidf.fit_transform(text)
  scores = (tfidf_matrix.toarray())
  tfidf_df = pd.DataFrame(scores, columns=tfidf.get_feature_names_out())

  # Getting top relevant ngrams based on tfidf
  tfidf_score = tfidf_matrix.sum(axis=0) # sum of the tfidf score
  counts = cv_matrix.sum(axis=0) # frequency count
  data = []
  for i, term in enumerate(features):
    data.append( (term, tfidf_score[0,i], counts[0,i]))
  ranking = pd.DataFrame(data, columns = ['term','tfidf', 'counts'])
  
  # plot ngram freq ordered by tfidf score
  words = ranking.sort_values('tfidf', ascending = False).head(10)
  fig = px.bar(words, x="term", y="counts", hover_data=["tfidf"], title="N-gram Frequency Using TF-IDF")
  st.plotly_chart(fig, use_container_width=True)

def plot_map(df):
  px.set_mapbox_access_token(creds.mapbox_token)
  fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", 
                          hover_data=['avg_rating','review_count'],
                          color='avg_rating', color_continuous_scale=px.colors.sequential.Sunset, 
                          size_max=15, zoom=10, title="Store Location")
  st.plotly_chart(fig, use_container_width=True)