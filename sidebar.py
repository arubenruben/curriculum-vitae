import streamlit as st


def sidebar():
    with st.sidebar:
        st.header('Chave de Segurança', '🔒')
        # Add horizontal line
        st.markdown('---')

        st.session_state.api_key = st.text_input(
            'Chave', placeholder='Introduza a sua chave de segurança aqui...')

        if st.session_state.api_key:
            st.text('🔑 Chave de Segurança: ' + st.session_state.api_key)
