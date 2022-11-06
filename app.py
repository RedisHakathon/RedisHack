import streamlit as st
from streamlit_option_menu import option_menu
from sentence_transformers import SentenceTransformer
import numpy as np
import redis
import config
from redis.commands.search.query import Query
from transformers import pipeline


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Paper Recommendation", "Topic Identification", "Question & Answering"],  # required
        icons=["house", "diagram-2", "people"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )

@st.cache(allow_output_mutation=True)
def load_qa_model():
    model = pipeline("question-answering")
    return model

if selected == "Paper Recommendation":
    st.markdown(
        """<h2 style='text-align: center; color: #EA047E;font-size:40px;margin-top:-50px;'>Paper Recommendation</h2>""",
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

    Search_query = st.text_input("Enter a search query below to discover scholarly papers")

    if st.button("Discover Scholarly Papers"):
        if Search_query is not None:
            query_vector = model.encode(Search_query).astype(np.float32).tobytes()
            query = Query(f'*=>[KNN {topK} @vector $vec_param AS vector_score]').sort_by("vector_score").paging(0, topK).return_fields("paper_id", "title", "categories", "vector_score").dialect(2)

            query_param = {"vec_param": query_vector}
            results =  redis_conn.ft(config.INDEX_NAME).search(query, query_params = query_param)

            for p in results.docs:
                p.title           
        

if selected == "Topic Identification":
    st.markdown(
        """<h2 style='text-align: center; color: #EA047E;font-size:40px;margin-top:-50px;'>Topic Identification</h2>""",
        unsafe_allow_html=True,
    )
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    redis_conn = redis.from_url(config.REDIS_URL)
    topK = 1

    Search_query = st.text_input("Enter a text below to Identify which Schoarly Topic it Falls under")

    if st.button("Discover Scholarly Papers Topic"):
        if Search_query is not None:
            query_vector = model.encode(Search_query).astype(np.float32).tobytes()
            query = Query(f'*=>[KNN {topK} @vector $vec_param AS vector_score]').sort_by("vector_score").paging(0, topK).return_fields("categories").dialect(2)

            query_param = {"vec_param": query_vector}
            results =  redis_conn.ft(config.INDEX_NAME).search(query, query_params = query_param)

            for p in results.docs:
                p.categories


if selected == "Question & Answering":
    st.markdown(
        """<h2 style='text-align: center; color: #EA047E;font-size:40px;margin-top:-50px;'>Question & Answering</h2>""",
        unsafe_allow_html=True,
    )

    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    redis_conn = redis.from_url(config.REDIS_URL)
    topK = 1

    Search_query = st.text_input("Enter your question")

    if st.button("Get an Answer"):
        if Search_query is not None:
            query_vector = model.encode(Search_query).astype(np.float32).tobytes()
            query = Query(f'*=>[KNN {topK} @vector $vec_param AS vector_score]').sort_by("vector_score").paging(0, topK).return_fields("abstract").dialect(2)

            query_param = {"vec_param": query_vector}
            results =  redis_conn.ft(config.INDEX_NAME).search(query, query_params = query_param)
            qa = load_qa_model()

            for p in results.docs:
                sentence  = p.abstract
                answers = qa(question=Search_query, context=sentence)
                st.write(answers['answer'])