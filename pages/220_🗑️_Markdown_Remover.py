# Import block
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

# Main content
pass