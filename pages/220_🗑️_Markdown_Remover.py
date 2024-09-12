# Import block
import re # Regular expressions
import streamlit as st # UI
import random # Select a random meme
import json # Read the master json file with all the memes
import asset_director # For asset management
import hashlib # For generating SHA256 hashes of the image urls
import requests # For downloading the images
import os # For cache management


# Configure assets
src = asset_director.Asset("Markdown Remover", 220)
# src.clear_cache() # Clear the cache on page load

# Page setup
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # This page will be wide because the image needs room to display
    initial_sidebar_state="expanded")

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Configure session states
if "phase220220" not in st.session_state:
    st.session_state["phase220"] = 0

# Functions
def remove_markdown(text):
    # Remove markdown syntax but keep list markers
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)  # Bold
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)  # Italics
    text = re.sub(r'~~(.*?)~~', r'\1', text)  # Strikethrough
    text = re.sub(r'`{1,2}([^`]+)`{1,2}', r'\1', text)  # Inline code
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)  # Images
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'>\s*', '', text)  # Blockquotes
    text = re.sub(r'\n{2,}', '\n\n', text)  # Remove extra newlines
    return text

# Main content
st.title("Markdown Remover")
with st.form("md_rmv"):
    text = st.text_area("Enter some markdown text here:", height=300)
    if st.form_submit_button("Remove Markdown"):
        st.session_state["phase220"] = 1
        # st.rerun()

        
        st.write("Here is the text with the markdown removed:")
        with st.container(border=True):
            st.write(remove_markdown(text))
        
        # if st.button("Try again", key="try_again", use_container_width=True):
        #     st.session_state["phase220"] = 0
        #     st.rerun()