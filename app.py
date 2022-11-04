import streamlit as st
from streamlit_option_menu import option_menu
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import redis.asyncio as redis
import config
from redis.commands.search.query import Query
from redis.commands.search.result import Result
#from embeddings import model


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Paper Recommendation", "Question & Answering", "Topic Identification"],  # required
        icons=["house", "diagram-2", "people"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )


if selected == "Paper Recommendation":
    st.markdown(
        """<h2 style='text-align: center; color: #EA047E;font-size:40px;margin-top:-50px;'>ArXiv Dataset Hackathon</h2>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<h6 style='text-align: left; color: #EEEEEE;font-size:12px;margin-top:-10px;'>This Webpage uses vector search of Redis Enterprise  to retrieve information based on arvix dataset.Searching over scholarly papers makes VSS retrieve a similar paper of interest
</h6>""",
        unsafe_allow_html=True,
    )


    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    redis_conn = redis.from_url(config.REDIS_URL)
    topK = 5

    paragraph_slot = st.empty()
    question = st.text_input("Enter a search query below to discover scholarly papers")


    if st.button("Discover Scholarly Papers"):
        if question is not None:
            query_vector = model.encode(question).astype(np.float32).tobytes()
            q = Query(f'*=>[KNN {topK} @vector $vec_param AS vector_score]').sort_by("vector_score").paging(0, topK).return_fields("title", "vector_score").dialect(2)

            params_dict = {"vec_param": query_vector}

            results = redis_conn.ft().search(q, query_params = params_dict)

            st.success(results)


if selected == "Question & Answering":
    st.markdown(
        """<h2 style='text-align: center; color: purple;font-size:60px;margin-top:-50px;'>Our Project Holistic View</h2>""",
        unsafe_allow_html=True,
    )
if selected == "Topic Identification":
    st.markdown(
        """<h2 style='text-align: center; color: purple;font-size:60px;margin-top:-50px;'>Meet Our Amazing Team</h2>""",
        unsafe_allow_html=True,
    )
