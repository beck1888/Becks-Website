# Import block
import streamlit as st # UI
import random # Select a random meme
import json # Read the master json file with all the memes
import asset_director # For asset management
import hashlib # For generating SHA256 hashes of the image urls
import requests # For downloading the images
import os # For cache management


# Configure assets
src = asset_director.Asset("Comp Sci Memes", 100)
# src.clear_cache() # Clear the cache on page load

# Clear the cache on page load
cached_data_dir = "cache/memes"
# Remove all files in the directory but keep the directory
for file in os.listdir(cached_data_dir):
    if file != cached_data_dir:
        os.remove(os.path.join(cached_data_dir, file))

# Page setup
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # This page will be wide because the image needs room to display
    initial_sidebar_state="expanded")

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Add a little bit of vertical
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# Function for getting a meme
def get_a_meme():
    # Get the json data
    data = src.fetch_local_json("memes_data")

    # List to hold the paths
    paths = []

    # Extract 'path' from each dictionary in the list
    for item in data:
        paths.append(item['path'])

    # Pick a random path
    url_fragment = random.sample(paths, 1)[0]

    # Add start of url to the picked fragment
    full_url = f"https://raw.githubusercontent.com/deep5050/programming-memes/main/{url_fragment}"
    # import os; os.system(f"open -a \"Google Chrome\" {full_url}")
    
    # Return the random url in full
    return full_url

# Create columns for easier control and visualization (fit content)
col1, col2 =st.columns(2)

# Show the meme display column
with col1:
    found_meme_url = get_a_meme() # Save for the download button
    st.image(found_meme_url)

    # Hash the url
    sha256_hash = hashlib.sha256(found_meme_url.encode("utf-8")).hexdigest()
    
    # Short the hash
    short_hash = sha256_hash[0:6]

    # Try to cache the image
    try:
        with open(f"cache/memes/{short_hash}.png", "wb") as f:
            f.write(requests.get(found_meme_url).content)
    except:
        pass

# Show the page controls column
with col2:
    st.title("Programming Memes")

    st.divider() # Readability on page

    refresh = st.button("🔄 Refresh", use_container_width=True) # Button to get a new meme
    if refresh: # The button sets to true when clicked
        pass

    # Show the download button
    st.download_button(
        label="📥 Download and refresh",
        data=open(f"cache/memes/{short_hash}.png", "rb").read(),
        file_name=f"{short_hash}.png",
        mime="image/png",
        use_container_width=True
    )


    # st.markdown("*Right click the image, then click 'Save Image' to download it*")