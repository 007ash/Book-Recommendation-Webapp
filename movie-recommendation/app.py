import streamlit as st
import pickle
import requests

with open("artifact/movie.pkl", 'rb') as f:
    movie_train, cosine_sim = pickle.load(f)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movie_train[movie_train['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie_train[['title', 'movie_id']].iloc[movie_indices]

def featch_poster(movie_id):
    api_key = '16ee0a07d4e100ede5aa60ff91c3a721'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    respond = requests.get(url)
    data = respond.json()
    poster_path = data['poster_path']
    full_path = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return full_path

st.title('Movie Recommendation System')
st.markdown('''<h3 style='text-align: center; color: blue;'>Find your next favorite movie!</h3>''', unsafe_allow_html=True)
selected_movie = st.selectbox('Select a movie:', movie_train['title'].values)
if st.button('Recommend'):
    recommendation = get_recommendations(selected_movie)
    st.subheader('Recommended Movies:')
    for i in range(0,10,5):
        col = st.columns(5)
        for col,j in zip(col, range(i,i+5)):
            if j < len(recommendation):
                movie_train = recommendation.iloc[j]
                movie_id = recommendation.iloc[j]['movie_id']
                poster = featch_poster(movie_id)
        
                with col:
                    st.image(poster, width=150)
                    st.text(movie_train['title'])
