# Import necessary libraries
import streamlit as st
import asset_director
import streamlit_lottie

# Configure assets
src = asset_director.Asset("Home", 0)
loading = src.under_construction()

# Configure the Streamlit app
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded",
)

# Page content
st.title("Beck's Site")
st.text("This page is still under construction, so please see the README below for now...")
st.page_link(page="https://github.com/beck1888/Becks-Website",label="GitHub")

st.divider()

with open("README.md", "r") as f:
    st.markdown(f.read())

# # Render the Lottie animation
# st.markdown(loading[0], unsafe_allow_html=True)

# # Render the Lottie animation
# streamlit_lottie.st_lottie(loading[1], speed=1, height=300)