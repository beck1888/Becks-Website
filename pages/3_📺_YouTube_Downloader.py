# Import necessary libraries
import os  # For cache management
import ssl  # For downloading YouTube videos with SSL certificates
from pytubefix import YouTube # Fixed library to download YouTube videos (PyTube Fix)
import streamlit as st  # Web framework
from asset_director import Asset  # For asset management
from streamlit_lottie import st_lottie  # For rendering the Lottie animation


# Configure assets
src = Asset("YouTube Downloader", 3)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded")

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# #### PAGE UNDER CONSTRUCTION ####
# construction = src.under_construction()
# st.markdown(construction[0], unsafe_allow_html=True)
# st_lottie(construction[1], height=300)
# st.stop()
# ####

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
    # Target the video
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()

    # Set up the download
    video_name = yt.title

    if "mp4" in file_type.lower():
        use_mp3 = False
        file_type_end = "mp4"
    elif "mp3" in file_type.lower():
        use_mp3 = True
        file_type_end = "mp3"

    # Download the video
    video_file_path = ys.download(
        output_path="cache/YT",
        filename=f"{video_name}.{file_type_end}",
        mp3=use_mp3,
    )

    return video_file_path

# Streamlit App

# Input page
if st.session_state["phase"] == 0:
    st.title("YouTube Downloader")

    with st.form("yt_download_form"):
        st.session_state.url = st.text_input("Enter a YouTube video URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.session_state.desired_file_type = st.radio("Please pick a file type", ["Audio (mp3)", "Video (mp4)"], index=None)

        download_button = st.form_submit_button(label="Download")

    if download_button:
        # Make sure both inputs are filled
        if st.session_state.url != "" and st.session_state.desired_file_type != "":
            st.session_state["phase"] = 1
            st.rerun()
        else:
            st.error("Please fill in both inputs before submitting!")

    # Preload the Lottie animations
    st.session_state.lottie_loader_data = src.fetch_local_json("loader")
    st.session_state.lottie_done_data = src.fetch_local_json("done")

# Download in progress page
if st.session_state["phase"] == 1:
    st.markdown("<h2 style='text-align: center; color: #0a7cff;'>Fetching media from YouTube</h2>", unsafe_allow_html=True) # Say media instead of video, because if the user selected audio they might get confused, but media could be either so it's less likely to be confusing and cause the user to refresh in panic which will cause the server to cache up a bunch of partially downloaded video streams (junk)
    st_lottie(st.session_state.lottie_loader_data, speed=1.5, height=500, quality="high")

    # Clear the cache of previously downloaded videos
    # src.clear_cache()

    # Download the YouTube video
    st.session_state.download_path = download_youtube_video(st.session_state.url, st.session_state.desired_file_type)

    st.session_state["phase"] = 2
    st.rerun()

# Download complete page
if st.session_state["phase"] == 2:
    st.markdown("<h1 style='text-align: center; color: #0a7cff; font-size: 50px;'>Done!</h1>", unsafe_allow_html=True)

    st.container(height=20, border=False) # Add some vertical space

    st_lottie(st.session_state.lottie_done_data, speed=0.7, height=200, quality="high", loop=False)

    # Load the file
    video = open(st.session_state.download_path, "rb")
    video_name = st.session_state.download_path.split("/")[-1]

    # Display a download button
    st.download_button("📥 Download", video, file_name=video_name, use_container_width=True, key="download_button_go")


    # Vertical space
    st.container(height=20, border=False)

    if st.button("Done", use_container_width=True, key="download_more"):
        os.remove(st.session_state.download_path) # Remove the downloaded file from the cache to save space
        st.session_state["phase"] = 0
        st.rerun()
    st.markdown("*Please click 'Done' after you have downloaded the video to let our servers clear up space!*")