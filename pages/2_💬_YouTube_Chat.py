# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import openai # For using AI to ask questions about YouTube videos
from youtube_transcript_api import YouTubeTranscriptApi # For getting the transcript
from youtube_transcript_api.formatters import TextFormatter # For formatting the transcript
from pytubefix import YouTube # Fixed library to download YouTube videos (titles only in this case) (PyTube Fix)

# Configure assets
src = asset_director.Asset("YouTube Chat", 2)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # This page will be wide because the chat
    initial_sidebar_state="expanded")

# # Hide the Streamlit UI
# for config in src.clear_st_ui():
#     st.markdown(config, unsafe_allow_html=True)

# Configure the session state
if "phase" not in st.session_state:
    st.session_state["phase"] = 0

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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

def ask_question(question: str, transcript: str, chat_history: list) -> str:
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Create the prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Read this video transcript: {transcript}. Read the history of this chat you're having: {chat_history}. Now answer this following question (return ONLY your answer):"},
                    {"role": "user", "content": question}],
        stream=False,
    ).choices[0].message.content

    return response

def get_video_title(url: str) -> str:
    # Retrieve the video ID from the URL
    yt = YouTube(url)
    video_name = yt.title

    return video_name

# Streamlit app interface
if st.session_state["phase"] == 0:
    st.title("YouTube Chat")
    st.markdown("**How it works:** You will enter a video URL. The AI will go and watch that video. Then you can ask it questions about the video. If you just need a summary of the video instead of asking questions, please use the summary page instead.")
    st.markdown("**Note:** Because of the way this web framework is, it may look like the AI is not responding, but I assure you that it is! After asking a question, please wait a few seconds for it to reply, even if it looks like it's not doing anything. Most importantly, avoid spamming requests or refreshing.")


    with st.form("chat_form"):
        url = st.text_input("Enter a YouTube video URL")
        submit_button = st.form_submit_button("Submit")

    if submit_button and url is not None and url != "":
        st.session_state["phase"] = 1
        st.session_state["url"] = url
        st.rerun()

# Get the transcript and title of the video
if st.session_state["phase"] == 1:
    with st.spinner("Fetching transcript..."):
        st.session_state["transcript"] = get_transcription(st.session_state["url"])
        st.session_state.video_title = get_video_title(st.session_state["url"])

    st.session_state["phase"] = 2
    st.rerun()

# Chat interface
if st.session_state["phase"] == 2:
    st.markdown("## Chat about: [" + st.session_state.video_title + "](" + st.session_state["url"] + ")")

    msg = st.chat_input("Ask a question about the video")

    if msg is not None and msg != "":
        st.session_state["chat_history"].append({
            "user": msg,
            "ai": ask_question(msg, st.session_state["transcript"], st.session_state["chat_history"])
        })

    # Display the chat 
    for message in st.session_state["chat_history"]:
        st.chat_message("human").write(message["user"])
        st.chat_message("ai").write(message["ai"])