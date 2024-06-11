import streamlit as st
import pandas as pd
from cv_parsing.data.Dataloader import Dataloader
from cv_parsing.parser.Parser import Parser
from cv_parsing.parser.strategies.HuggingFaceApiStrategy import HuggingFaceApiStrategy
from cv_parsing.prompts.EnglishPrompt import ExtractPersonalInformationPrompt, ExtractEducationPrompt,  ExtractLanguagesPrompt, ExtractJobsPrompt
from cv_parsing.exceptions.PromptException import PromptException


def predicters():
    parser_non_jobs = Parser(parsing_strategy=HuggingFaceApiStrategy(
        prompts=[
            ExtractPersonalInformationPrompt(),
            ExtractEducationPrompt(),
            ExtractLanguagesPrompt(),
            ExtractJobsPrompt()
        ],
        model="google/gemma-1.1-7b-it",
        temperature=1.0,
        api_key=st.session_state['api_key']
    ))

    """
    parser_jobs = Parser(parsing_strategy=HuggingFaceApiStrategy(
        prompts=[
        ],
        model="meta-llama/Meta-Llama-3-8B",
        temperature=1.0,
        api_key=st.session_state['api_key']
    ))
    """

    return parser_non_jobs, None


def handle_uploaded_file(uploaded_file):
    with st.spinner("A Processar..."):
        parser_non_jobs, parser_jobs = predicters()

        raw_pdf_text = Dataloader._load_pdf(uploaded_file)

        response_non_jobs = parser_non_jobs.parse(
            raw_pdf_text=raw_pdf_text).serialize()

        """
        response_jobs = parser_jobs.parse(
            raw_pdf_text=raw_pdf_text).serialize()

        response_non_jobs.update({'jobs': response_jobs['jobs']})
        """

        df_personal_information = pd.DataFrame(
            response_non_jobs['personal_information'], index=[0])
        df_education = pd.DataFrame(response_non_jobs['education'])
        df_languages = pd.json_normalize(response_non_jobs['languages'])

        df_jobs = pd.DataFrame(response_non_jobs['jobs'])

        return df_personal_information, df_education, df_languages, df_jobs


def dropzone():

    if st.session_state['api_key']:
        file = st.file_uploader("Introduzir Ficheiro PDF", type=[
            "pdf"], accept_multiple_files=False, disabled=st.session_state['pending'])
    else:
        st.warning(
            "Por favor introduza a sua chave de segurança na barra lateral.")
        file = None

    if file and st.session_state['api_key'] is None:
        st.warning(
            "Por favor introduza a sua chave de segurança na barra lateral.")

    if file and st.session_state['api_key'] is not None:

        try:
            st.session_state['pending'] = True

            df_personal_information, df_education, df_languages, df_jobs = handle_uploaded_file(
                uploaded_file=file)

            st.session_state['pending'] = False

            st.subheader("Informação Pessoal")
            st.dataframe(df_personal_information, hide_index=True,
                         use_container_width=True)

            st.subheader("Educação")
            st.dataframe(df_education, hide_index=True,
                         use_container_width=True)

            st.subheader("Idiomas")
            st.dataframe(df_languages, hide_index=True,
                         use_container_width=True)

            st.subheader("Experiência Profissional")
            st.dataframe(df_jobs, hide_index=True, use_container_width=True)

        except OverflowError as e:
            st.error(
                "O CV é muito extenso para ser processado. Por favor tente com um CV mais curto.")
            st.error(e)
            st.error(
                "Se o problema persistir, por favor contacte Rúben Almeida (ruben.almeida@innovpoint.com)")
        except PromptException as e:
            st.error("Erro ao processar o CV. Por favor tente novamente.")
            st.error(e)
            st.error(
                "Se o problema persistir, por favor contacte Rúben Almeida (ruben.almeida@innovpoint.com)")
        finally:
            st.session_state['pending'] = False
