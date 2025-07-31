import streamlit as st
import pandas as pd
import pickle
import requests

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_title):
    response=requests.get('https://omdbapi.com/?t={}&apikey=210aee2b'.format(movie_title))
    data=response.json()
    return data['Poster']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_list = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_title=movies.iloc[i[0]].title
        recommended_movies_posters.append(fetch_poster(movie_title))
        recommend_list.append(movies.iloc[i[0]].title)
    return recommend_list,recommended_movies_posters
st.title('Movie Recommender System')
option = st.selectbox(
    "What movie would you like to watch?",
    movies['title'].values,
    index=None,
    placeholder="Select your mood",
)
if st.button("Recommend"):
    names,posters=recommend(option)
    col1,col2,col3,col4,col5=st.columns(5)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div style='text-align: center; padding-top: 5px'><b>{names[i]}</b></div>",
                        unsafe_allow_html=True)
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])