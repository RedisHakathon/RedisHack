import os
import streamlit as st

INDEX_NAME = "index"
REDIS_HOST = st.write("REDIS_HOST:", st.secrets["REDIS_HOST"])
REDIS_PORT = st.write("REDIS_PORT:", st.secrets["REDIS_PORT"])
REDIS_DB = st.write("REDIS_DB:", st.secrets["REDIS_DB"])
REDIS_PASSWORD = st.write("REDIS_PASSWORD:", st.secrets["REDIS_PASSWORD"])
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
