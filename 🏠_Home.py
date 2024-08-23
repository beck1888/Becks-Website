# Use this command to run the app locally:
"""
streamlit run 🏠_Home.py
"""

# Import necessary libraries
import streamlit as st
import asset_director
import os

# Configure assets
src = asset_director.Asset("Home", 0)
loading = src.under_construction()

# Configure the Streamlit app
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Page content
# st.title("Beck's Site")
# st.text("This page is still under construction, so please see the README below for now...")

# st.markdown("""<a href="https://github.com/beck1888/Becks-Website" target="_blank"><u>https://github.com/beck1888/Becks-Website</u></a>""", unsafe_allow_html=True)

# st.divider()

# Header
st.title("Beck's Website")

# About
st.markdown("Hi! Welcome to my website. This is a collection of tools I have built. Please combe back often because I'm always adding new stuff! Feel free to check them out, or read the README below for more info and the GitHub repo.")

# Functions
def count_python_lines(directory: str) -> int:
    total_lines = 0
    
    for root, dirs, files in os.walk(directory):
        # Exclude the 'venv' directory
        if '.venv' in dirs:
            dirs.remove('.venv')
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
    
    return total_lines

def add_commas(number: int) -> str:
    return "{:,}".format(number)

# Show how many lines of code I have written
with st.spinner("Reading codebase..."):
    lines = count_python_lines(".")
    lines = add_commas(lines)

st.markdown(f"Current lines of code in project: {lines}")

services = [
    {
        "AI": [
            {"YouTube Summarizer": "http://beck.asuscomm.com/YouTube_Summarizer"},
            {"Chat with an AI about a YouTube video": "http://beck.asuscomm.com/YouTube_Chat"},
            {"Summarize the news": "http://beck.asuscomm.com/AI_News_Reader"}
        ],
        "Entertainment": [
            {"Computer Science Memes": "http://beck.asuscomm.com/Comp_Sci_Memes"}
        ],
        "Tools": [
            {"YouTube Video Downloader": "http://beck.asuscomm.com/YouTube_Downloader"}
        ],
        "Site info": [
            {"Change Log": "http://beck.asuscomm.com/Changelog"},
            {"Contact me/ feedback": "http://beck.asuscomm.com/Contact"}
        ]
    }
]

# Display the services

a1, a2, a3 = st.columns(3)
b1, b2, b3 = st.columns(3)
for service in services:
    with a1:
        with st.container(border=True):
            st.markdown("#### 🤖 AI Tools")
            for tool in service["AI"]:
                for name, link in tool.items():
                    st.markdown(f'<a href="{link}" target="_self" allow_unsafe_html="true">{name}</a>', unsafe_allow_html=True)

    with a2:
        with st.container(border=True):
            st.markdown("#### 🍿 Entertainment")
            for tool in service["Entertainment"]:
                for name, link in tool.items():
                    st.markdown(f'<a href="{link}" target="_self" allow_unsafe_html="true">{name}</a>', unsafe_allow_html=True)

    with a3:
        with st.container(border=True):
            st.markdown("#### 📦 Other Things")
            for tool in service["Tools"]:
                for name, link in tool.items():
                    st.markdown(f'<a href="{link}" target="_self" allow_unsafe_html="true">{name}</a>', unsafe_allow_html=True)

    with b1:
        with st.container(border=True):
            st.markdown("#### ℹ️ Site")
            for tool in service["Site info"]:
                for name, link in tool.items():
                    st.markdown(f'<a href="{link}" target="_self" allow_unsafe_html="true">{name}</a>', unsafe_allow_html=True)

st.markdown("*NOTE: You can also use the sidebar to navigate!*")
st.markdown("*NOTE: This site works best on a laptop or tablet. A mobile phone works, but it's best to use a laptop.*")

st.divider()

# # Render the Lottie animation
# st.markdown(loading[0], unsafe_allow_html=True)

# # Render the Lottie animation
# streamlit_lottie.st_lottie(loading[1], speed=1, height=300)