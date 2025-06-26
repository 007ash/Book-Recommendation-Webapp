import pickle
import numpy as np
import streamlit as st


st.markdown(f""" <h2 style="text-align:center; font-style:arial; color:#cccc">
            Books Recommender System
            </h2>""", unsafe_allow_html=True)

model = pickle.load(open('artifact\model.pkl', 'rb'))
books_name = pickle.load(open("artifact\\book_names.pkl", 'rb'))   
final_ratings = pickle.load(open('artifact\\final_rating.pkl', 'rb')) 
book_pivot = pickle.load(open('artifact\\book_pivot.pkl', 'rb'))

def fetch_poster(suggestions):
    book_name = []
    ids = []
    poster_url = []

    for i in suggestions:
        book_name.append(book_pivot.index[i])
    
    for i in book_name[0]:
        id = np.where(final_ratings['title'] == i)[0][0]
        ids.append(id)

    for i in ids:
        url = final_ratings.iloc[i]['image_url']
        poster_url.append(url)
    
    return poster_url
    

def recommend_books(selected_book_name):
    book_list = []
    book_id = np.where(book_pivot.index == selected_book_name)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
    poster_url = fetch_poster(suggestions)

    for i in range(len(suggestions)):
        books = book_pivot.index[suggestions[i]]
        for j in books:
            book_list.append(j)
    
    return book_list, poster_url    

selected_book_name = st.selectbox(
    "Type or select a book name from the dropdown",
    books_name
)

if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_books(selected_book_name)

    st.markdown("---")
    st.info("Find Your Next Favorite Book!")
    st.markdown("Here are some book recommendations based on your selection:")
    
    cols = st.columns(5)
    recommended_books = recommended_books[1:6]  
    poster_url = poster_url[1:6]  
    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <div style="text-align:center; height:300px; display:flex; flex-direction:column; justify-content:space-between;">
                    <img src="{poster_url[i]}" style="width:100%; height:100%; object-fit:cover; border-radius:8px;"/>
                    <p style=" color:#dddd; font-weight:bold; margin-top:10px;">{recommended_books[i]}</p>
                </div>
                """,unsafe_allow_html=True)

    