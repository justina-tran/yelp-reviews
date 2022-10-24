from viz import *

store_df = pd.read_csv('data/nyc_boba_store50.csv')
review_df = pd.read_csv('data/nyc_reviews_final.csv')
cleaned_review_df = pd.read_csv('data/reviews_cleaned.csv')
cleaned_review_df.dropna(inplace=True)

st.set_page_config(
    page_title="Classification",
    page_icon="🎯",
)

st.title("📝 Classification")

def get_prediction(user_text):
    """
    Input: any string
    Returns: model predictions
    """
    import pickle
    # get model and vectorizer from pickle file
    with open('models/logreg.pkl', 'rb') as file:  
        logreg = pickle.load(file)
    with open('models/tfidf.pkl', 'rb') as file:
        vec = pickle.load(file)
    # get predictions
    text = vec.transform([user_text])
    preds = logreg.predict(text)
    proba = logreg.predict_proba(text)
    return preds, proba[0]

# get user to enter news
default_text = st.selectbox(
        "Select one sample review:",
        (
            "I ordered a unsweetened jasmine green tea with lychee jelly which was just the right amount of sweetness. Price wise, it's on the more expensive side.",
            "The wait was long! I got the taro milk tea with boba but unfortunately when I got the drink it didn't have any boba in it!",
            "Ordered an iced tea with 50% sugar, less ice, and herbal jelly for to go through their website. It was exactly what I wanted and am craving for more. Will come again when in the area.",
            "Smells a little weird and stuffy inside, but they have lots of drink options.",
            "The drinks didn't really taste that good. I think I might go to some other place for boba next time considering the price."
        ),
    )

if default_text:
    st.write("You selected: ", default_text)
    results, proba = get_prediction(default_text)
    plot_proba(proba)

st.markdown("**or** input any review:")

user_input = st.text_area("Enter review: ", "", 
    help="Enter some text here to find out what star rating is likely given.", height=60)
classify_button = st.button("Submit")

if classify_button:
    results, proba = get_prediction(user_input)
    plot_proba(proba)
    

