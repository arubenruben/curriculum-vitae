from environs import Env

env = Env(eager=True)
env.read_env()

import streamlit as st
from sidebar import sidebar
from dropzone import dropzone


if 'api_key' not in st.session_state:
    st.session_state.api_key = None

if 'cv' not in st.session_state:
    st.session_state.cv = None

if 'pending' not in st.session_state:
    st.session_state.pending = False

st.set_page_config(
    page_title="Demo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

sidebar()

st.header("Extração de Informação de Curriculum Vitae")

dropzone()
