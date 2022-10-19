from viz import *
from ast import literal_eval

review_df = pd.read_csv('data/nyc_reviews_final.csv')
cleaned_review_df = pd.read_csv('data/reviews_cleaned.csv')
cleaned_review_df.dropna(inplace=True)

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
        'Brooklyn, Brooklyn, NY': 'Brooklyn, NY',
        'Manhattan, NY': 'New York, NY'})
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
st.subheader("Word Cloud")
st.write("A word cloud of all words from the reviews after text preprocessing. Update the word cloud by entering any words to remove.")

words = set(nltk.corpus.words.words()) # all english words
cleaned_review_df['cleaned'] = cleaned_review_df['cleaned'].apply(literal_eval)
all_words = [word for review in cleaned_review_df['cleaned'] for word in review]
ok_words = [w for w in all_words if w.lower() in words or not w.isalpha()]
corpus_wc = " ".join(ok_words)
unique_words = set(ok_words)
my_stopwords = stopwords.words('english')
corpus_wordcloud = " ".join(str(review) for review in cleaned_review_df.cleaned_text)

if 'user_stopwords' not in st.session_state:
    st.session_state.user_stopwords = []

def handle_submit(new_stopwords):
    st.session_state.user_stopwords = new_stopwords

with st.form(key="Selecting words to remove from the word cloud"):
    user_stopwords = st.multiselect(label="Enter stopwords:", options=unique_words, help="Enter words to remove from the word cloud.")
    submit_button = st.form_submit_button(label="Submit", on_click=handle_submit, args=[user_stopwords])
    if submit_button:
        st.write('A word cloud without the words:', ", ".join(w for w in st.session_state.user_stopwords))
        for s in user_stopwords:
            st.session_state.user_stopwords.append(s)
        wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=st.session_state.user_stopwords).generate(corpus_wordcloud)
        fig, ax = plt.subplots(figsize = (8,8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=st.session_state.user_stopwords).generate(corpus_wordcloud)
        fig, ax = plt.subplots(figsize = (8,8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

# plot n-grams
if 'user_ngram' not in st.session_state:
    st.session_state.user_ngram = "Unigram"
if 'user_rating' not in st.session_state:
    st.session_state.user_rating = "⭐️"

def run_rating():
    if st.session_state["selected_rating"]:
        st.session_state["user_rating"] = st.session_state.selected_rating

def run_ngrams():
    st.session_state["user_ngram"] = st.session_state.selected_ngram

st.subheader("N-gram Analysis")
col1, col2 = st.columns(2)
with col1: 
    user_select_rating = st.selectbox("Select a star rating (1-5):", options=("⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"), on_change=run_rating, key="selected_rating")
with col2:
    user_select_ngram = st.radio("Select a n-gram:", options=("Unigram", "Bigram", "Trigram"), on_change=run_ngrams, key="selected_ngram", horizontal=True)

one_rating_corpus = [review for review in cleaned_review_df[cleaned_review_df['rating'] == '1 star rating']['cleaned_text']]
two_rating_corpus = [review for review in cleaned_review_df[cleaned_review_df['rating'] == '2 star rating']['cleaned_text']]
three_rating_corpus = [review for review in cleaned_review_df[cleaned_review_df['rating'] == '3 star rating']['cleaned_text']]
four_rating_corpus = [review for review in cleaned_review_df[cleaned_review_df['rating'] == '4 star rating']['cleaned_text']]
five_rating_corpus = [review for review in cleaned_review_df[cleaned_review_df['rating'] == '5 star rating']['cleaned_text']]

star_dict = {"⭐️": one_rating_corpus,
             "⭐️⭐️": two_rating_corpus,
             "⭐️⭐️⭐️": three_rating_corpus,
             "⭐️⭐️⭐️⭐️": four_rating_corpus,
             "⭐️⭐️⭐️⭐️⭐️": five_rating_corpus}

ngram_dict = {"Unigram": 1, 
              "Bigram": 2,
              "Trigram": 3}

create_ngram(star_dict[st.session_state["user_rating"]], ngram_dict[st.session_state["user_ngram"]])
