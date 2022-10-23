from viz import *

store_df = pd.read_csv('data/nyc_boba_store50.csv')
review_df = pd.read_csv('data/nyc_reviews_final.csv')
cleaned_review_df = pd.read_csv('data/reviews_cleaned.csv')
cleaned_review_df.dropna(inplace=True)

st.set_page_config(
    page_title="EDA",
    page_icon="📊",
)

st.title("Yelp Reviews - NYC Boba Shops🧋")
st.subheader('🔎 EDA')
st.markdown("The dataset has a total of **13,211 reviews** from **50 boba stores** in NYC.")

# preview of df
st.dataframe(cleaned_review_df)

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

# plot map of store location
plot_map(store_df)

# plot ratings
ratings = review_df['rating'].value_counts().reset_index()
ratings.columns = ['rating','num of reviews']
fig = px.pie(ratings, values='num of reviews', names='rating', title='Rating Distribution')
st.plotly_chart(fig, use_container_width=True)

