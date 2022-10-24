from viz import *
from ast import literal_eval

store_df = pd.read_csv('data/nyc_boba_store50.csv')
review_df = pd.read_csv('data/nyc_reviews_final.csv')
cleaned_review_df = pd.read_csv('data/reviews_cleaned.csv')
cleaned_review_df.dropna(inplace=True)

st.set_page_config(
    page_title="Text Analysis",
    page_icon="📝",
)

st.title("📝 Text Analysis")

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


with st.form(key="Selecting words to remove from the word cloud"):
    user_stopwords = st.multiselect(label="Enter stopwords:", options=unique_words, help="Enter words to remove from the word cloud.")
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.write('A word cloud without the words:', ", ".join(w for w in user_stopwords))
        wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=user_stopwords, random_state=12).generate(corpus_wordcloud)
        fig, ax = plt.subplots(figsize = (8,8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        wordcloud = WordCloud(width=1600, height=800, mode = "RGBA", background_color='white', stopwords=user_stopwords, random_state=12).generate(corpus_wordcloud)
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
st.write("Analyze the text frequencies by picking a star rating and a n-gram.")
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

plot_ngram(star_dict[st.session_state["user_rating"]], ngram_dict[st.session_state["user_ngram"]])

