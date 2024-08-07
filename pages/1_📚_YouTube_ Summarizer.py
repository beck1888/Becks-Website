# Import necessary libraries
import openai # For generating summaries
from youtube_transcript_api import YouTubeTranscriptApi # For getting the transcript
from youtube_transcript_api.formatters import TextFormatter # For formatting the transcript
import streamlit as st # Web framework
import streamlit_lottie # For rendering the Lottie animation
from asset_director import Asset # For asset management

# Configure assets
src = Asset("YouTube Summarizer", 1)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide",
    initial_sidebar_state="expanded")

if "phase" not in st.session_state:
    st.session_state["phase"] = 0

# Define the function to get the transcript
def get_transcription(url: str) -> str:
    # Retrieve the video ID from the URL for desktop links
    video_id = url.removeprefix("https://www.youtube.com/watch?v=") # Removes the 'https://www.youtube.com/watch?v=' prefix
    second_parameter = video_id.find("&")
    if second_parameter != -1:
        video_id = video_id[:second_parameter] # Removes everything after the '&'

    # Retrieve the video ID from the URL for mobile links
    video_id = video_id.removeprefix("https://youtu.be/") # Removes the 'https://youtu.be/' prefix
    second_parameter = video_id.find("?")
    if second_parameter != -1:
        video_id = video_id[:second_parameter] # Removes everything after the '?'


    # Retrieve the transcript
    json_transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Format the transcript into plain text
    formatter = TextFormatter()
    transcript = formatter.format_transcript(json_transcript)

    # Return the transcript
    return transcript

# Define the function to get the transcript
def summarize(transcript: str, use_emojis: bool, mention_sponsors: bool) -> str:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if use_emojis:
        emoji_flag = "Use emojis to make the summary more engaging and clear."
    else:
        emoji_flag = "Do not use any emojis anywhere in the summary."

    if mention_sponsors:
        sponsor_flag = "If the transcript mentions any sponsors, mention them in the summary and include info about any possible deals from it."
    else:
        sponsor_flag = "Do not mention anything about sponsors in the summary, even if the transcript mentions them."


    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Summarize this Youtube video. Crate multiple sections for the key points. Use markdown formatting. {emoji_flag} {sponsor_flag}"},
                  {"role": "user", "content": transcript}],
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response

# Streamlit app
if st.session_state["phase"] == 0:
    # Preload the Lottie animation
    st.session_state["animation_data"] = src.load_lottie_animation_data()

    st.title("YouTube Summarizer")

    st.session_state.url = st.text_input("Enter a YouTube video URL")

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.use_emojis = st.checkbox("Use emojis", value=False)

    with col2:
        st.session_state.sponsors = st.checkbox("Mention sponsors", value=False)

    button_holder = st.empty()

    if button_holder.button("✨ Summarize", use_container_width=True) and st.session_state.url is not None and st.session_state.url != "":
        st.session_state["phase"] = 1
        button_holder.empty()
        st.rerun()

if st.session_state["phase"] == 1:
        st.markdown("# Summarizing...")
        st.text("(This may take a moment, please stay on this page.)")

        loader = streamlit_lottie.st_lottie(
            animation_source=st.session_state.animation_data,
            quality="high",
            height=400,
            key="loader"
        )
        # loader.start("loader")

        transcript = get_transcription(st.session_state.url)
        st.session_state.summary = summarize(transcript, st.session_state.use_emojis, st.session_state.sponsors)
        st.session_state["phase"] = 2
        st.rerun()


if st.session_state["phase"] == 2:
    st.markdown(st.session_state.summary)

    st.divider() # Add a divider between the summary and the buttons for visual separation

    col1_p2, col2_p2, col3_p2, col4_p2 = st.columns(4)

    with col1_p2:
        st.button("📦 Download Summary", key="download_summary", disabled=True, help="Button functionality not yet implemented.", use_container_width=True)

    with col2_p2:
        st.link_button("📺 Visit Source", url=st.session_state.url, use_container_width=True)

    with col3_p2:
        if st.button("❌ Try Again", key="summarize_again", use_container_width=True, disabled=True, help="Button functionality not yet implemented."):
            pass
            # st.session_state["phase"] = 1
            # st.rerun()

    with col4_p2:
        if st.button("🔄 Summarize Another", key="summarize_another", use_container_width=True):
            st.session_state["phase"] = 0
            st.rerun()