# Import necessary libraries
import os  # For cache management
import ssl  # For downloading YouTube videos with SSL certificates
# from pytube import YouTube  # For downloading YouTube videos
# import yt_dlp
import streamlit as st  # Web framework
from asset_director import Asset  # For asset management
from streamlit_lottie import st_lottie  # For rendering the Lottie animation


# Configure assets
src = Asset("YouTube Downloader", 2)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded")

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

#### PAGE UNDER CONSTRUCTION ####
construction = src.under_construction()
st.markdown(construction[0], unsafe_allow_html=True)
st_lottie(construction[1], height=300)
st.stop()

# Add a little bit of vertical space so the html h1 tag doesn't get cutoff
with st.container(border=False, height=10):
    pass

# Establish SSL certificates
ssl._create_default_https_context = ssl._create_stdlib_context

# Set up session state
if "phase" not in st.session_state:
    st.session_state["phase"] = 0

# Define the function to download the YouTube video
def download_youtube_video(url, file_type):
    # Define the output directory
    output_dir = 'cache/YT'
    os.makedirs(output_dir, exist_ok=True)

    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best' if file_type.lower() == 'mp3' else 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if file_type.lower() == 'mp3' else []
    }

    # Download the video or audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)
    
    return file_name

# Streamlit App

# Input page
if st.session_state["phase"] == 0:
    st.title("YouTube Downloader")

    with st.form("yt_download_form"):
        st.session_state.url = st.text_input("Enter a YouTube video URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.session_state.desired_file_type = st.radio("Please pick a file type", ["Audio (mp3)", "Video (mp4)"], index=None)

        download_button = st.form_submit_button(label="Download")

    if download_button:
        st.session_state["phase"] = 1
        st.rerun()

    # Preload the Lottie animations
    st.session_state.lottie_loader_data = src.fetch_local_json("loader")
    st.session_state.lottie_done_data = src.fetch_local_json("done")

# Download in progress page
if st.session_state["phase"] == 1:
    st.markdown("<h2 style='text-align: center; color: #0a7cff;'>Fetching media from YouTube</h2>", unsafe_allow_html=True) # Say media instead of video, because if the user selected audio they might get confused, but media could be either so it's less likely to be confusing and cause the user to refresh in panic which will cause the server to cache up a bunch of partially downloaded video streams (junk)
    st_lottie(st.session_state.lottie_loader_data, speed=1.5, height=500, quality="high")

    # Clear the cache of previously downloaded videos
    src.clear_cache()

    # Download the YouTube video
    st.session_state.download_path = download_youtube_video(st.session_state.url, st.session_state.desired_file_type)

    st.session_state["phase"] = 2
    st.rerun()

# Download complete page
if st.session_state["phase"] == 2:
    st.markdown("<h1 style='text-align: center; color: #0a7cff; font-size: 50px;'>Done!</h1>", unsafe_allow_html=True)

    st.container(height=20, border=False) # Add some vertical space

    st_lottie(st.session_state.lottie_done_data, speed=0.7, height=200, quality="high", loop=False)

    # Display a download button
    st.download_button("📥 Download", open(st.session_state.download_path, "rb"), use_container_width=True, file_name="media", mime="video/mpeg")
