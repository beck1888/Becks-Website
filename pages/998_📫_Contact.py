import streamlit as st
import asset_director
import streamlit_lottie

src = asset_director.Asset("Admin", 998)
loading = src.under_construction()

st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(loading[0], unsafe_allow_html=True)

streamlit_lottie.st_lottie(loading[1], speed=1, height=300)
