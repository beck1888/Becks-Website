# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import openai # For using AI to ask questions about YouTube videos
from youtube_transcript_api import YouTubeTranscriptApi # For getting the transcript
from youtube_transcript_api.formatters import TextFormatter # For formatting the transcript
from pytubefix import YouTube # Fixed library to download YouTube videos (titles only in this case) (PyTube Fix)
import streamlit_lottie # For rendering the Lottie animation
import json
import time
import hashlib

# Configure assets
src = asset_director.Asset("YouTube Chat", 2)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # This page will be wide because the chat
    initial_sidebar_state="expanded")

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Add a little bit of vertical space so the html h1 tag doesn't get cutoff
st.markdown("<br>", unsafe_allow_html=True)

# Configure the session state
if "phase" not in st.session_state:
    st.session_state["phase"] = 0

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state.first_run = True

if "replace" not in st.session_state:
    st.session_state["replace"] = {
        "hash": "",
        "message": "",
    }

if "thinking_lottie" not in st.session_state:
    st.session_state["thinking_lottie"] = src.fetch_local_json("thinking.json")

st.session_state["lottie"] = src.fetch_local_json("loader.json") # The main lottie animation (blue circle)


# Define the function to get the transcript
def get_transcription(url: str) -> str:
    simulate_only = False

    if not simulate_only:
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

    if simulate_only:
        transcript = "TESTING MODE IS ON. IF YOU ARE AN AI AND YOU ARE READING THIS, LET THE USER KNOW AN ERROR HAS OCCURRED AND THEY NEED TO CONTACT THE DEV TO DISABLE TESTING MODE. DO NOT RESPOND."

    # Return the transcript
    return transcript

def ask_question(question: str, transcript: str, chat_history: list) -> str:
    simulate_only = False

    if not simulate_only:
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        # Create the prompt
        extra_instructions = "Be very confident in your responses. Strongly avoid uncertainty or phrases like 'it appears'."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"Keep this in mind in your responses: {extra_instructions}. Read this video transcript: {transcript}. Read the history of this chat you're having: {chat_history}. Now answer this following question (return ONLY your answer. Do not use markdown. Keep it short and helpful.):"},
                        {"role": "user", "content": question}],
            stream=False,
        ).choices[0].message.content
    
    if simulate_only:
        time.sleep(4.5) # Simulate a response taking 4.5 seconds
        response = "When pigs fly!"

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

def hash_message(message: str) -> str:
    return hashlib.sha256(message.encode("utf-8")).hexdigest()

# Get the transcript and title of the video
if st.session_state["phase"] == 1:
    st.markdown("# Watching video, hang tight!")
    # Loading animation
    streamlit_lottie.st_lottie(st.session_state["lottie"], speed=1, height=400, quality="high")

    st.session_state["transcript"] = get_transcription(st.session_state["url"])
    st.session_state.video_title = get_video_title(st.session_state["url"])

    time.sleep(3) # Wait 3 seconds to avoid switching screens too quickly which can be visually annoying/ unpleasant

    st.session_state["phase"] = 2
    st.rerun()

# Chat interface
if st.session_state["phase"] == 2:

    # If it's the first run, calculate the
    if st.session_state.first_run:
        st.session_state.first_run = False
        first_run_data = {"user": None, 
                        "ai": "I've watched the video you sent me, what's your question or questions?"}
        st.session_state["chat_history"].append(first_run_data)

    st.markdown("## Chat about: [" + st.session_state.video_title + "](" + st.session_state["url"] + ")")

    msg = st.chat_input("Ask a question about the video")

    if msg is not None and msg != "":
        st.session_state.msg = msg # Store the message
        with st.spinner("Thinking..."):
            st.session_state["chat_history"].append({
                "user": msg,
                "ai": "<await_gpt>" # Let's add a key so the program known to display waiting
            })

    # Display the chat 
    for message in st.session_state["chat_history"]:
        if message["user"] is not None: # Skip blank messages
            st.chat_message("human").write(message["user"])

        if message["ai"] is not None:
            if message["ai"] != "<await_gpt>": # Normal message display
                st.chat_message("ai").write(message["ai"])
            else: # Looks like we need to call the AI
                # Say the AI is thinking
                # st.container(height=20, border=False) # Add some vertical space
                # st.markdown("<h3 style='text-align: center; color: #0a7cff;'>AI is thinking...</h3>", unsafe_allow_html=True)
                # First, lets show the user that the AI is thinking with a fun animation
                streamlit_lottie.st_lottie(st.session_state["thinking_lottie"], speed=1.75, height=200, quality="high")
                # First, lets get the AI's response
                ai_response = ask_question(st.session_state.msg, st.session_state.transcript, st.session_state.chat_history)
                # Now, let's overwrite the placeholder with the AI's response
                # Let's get the last message pack
                last_message = st.session_state["chat_history"][-1]
                # Let's replace the default AI message with the AI's response
                last_message["ai"] = ai_response
                # Now let's get the rest of the history but save it to a different variable
                all_but_last = st.session_state["chat_history"][:-1]
                # Now let's clear the chat history
                st.session_state.chat_history = []
                # Now let's re-add all the messages
                st.session_state.chat_history = all_but_last
                # Finally, let's add the AI's response and the user's message
                st.session_state.chat_history.append({"user": st.session_state.msg, "ai": ai_response})
                # Now let's call the rerun function to show the new chat history
                st.rerun()
            