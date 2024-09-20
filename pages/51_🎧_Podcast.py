# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import feedparser
import dotenv
# import os
from openai import OpenAI
from datetime import datetime
from pathlib import Path
from pydub import AudioSegment

# Configure assets
src = asset_director.Asset("News", 50)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded")

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Add a little bit of vertical space so the html h1 tag doesn't get cutoff
with st.container(border=False, height=10):
    pass

# Functions
def get_news(site_rss_url, read_to=5):
    # Parse the feed
    feed = feedparser.parse(site_rss_url)

    result = {}

    # GET Head
    result["section"] = feed.feed.title

    # Find max entries
    result["max_entries"] = len(feed.entries)

    # Check how many entries are available
    max_entries = len(feed.entries)

    # Find how many entries to read
    if read_to > max_entries:
        read_to = max_entries
    else:
        read_to = read_to

    # GET Entries (5)
    index = 0
    for entry in feed.entries[:read_to]:
        index += 1
        result[f"story_{str(index)}"] = {
            "title": entry.title,
            "summary": entry.summary
        }

    # Specify number of entries
    result["num_entries"] = index

    r_value = ""

    for key, value in result.items():
        r_value += f"{key}: {value}\n"

    return result

def format_news(news) -> list:
    result = []

    for key, value in news.items():
        if key.startswith("story_"):
            headline = key.removeprefix("story_")
            title = value['title'].lstrip(".?")
            summary = value['summary']
            result.append(f"Headline {headline}: {title}: {summary}")

    return result

def get_api_key() -> str:
    return st.secrets["OPENAI_API_KEY"]

def expand_story(story: str) -> str:
    client = OpenAI(api_key=get_api_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Please expand this into a two sentences spoken like a news anchor. Start with the headline number such as 'First up' or 'Our second story'. Use your current knowledge to expand the story. Write no more that 50 words."},
            {
                "role": "user",
                "content": story
            }
        ]
    )

    return response.choices[0].message.content

def tidy_up_story(stories: list) -> str:
    story_string = "\n".join(stories)

    client = OpenAI(api_key=get_api_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Please make this into a coherent news broadcast script of about 200 words. Present it as a news anchor would, in a formal and direct manner. Do not add an intro. Do not add any placeholders. Do not add any cues. Do not add any other unnecessary text. This script is going to be fed into a TTS system directly. Do not add any cues or placeholders."},
            {
                "role": "user",
                "content": story_string
            }
        ]
    )

    return response.choices[0].message.content

def _get_time_of_day():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 21:
        return "evening"
    else:
        return "early morning"
    
def _get_formatted_date():
    now = datetime.now()
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day = now.strftime("%d").lstrip('0')
    year = now.strftime("%Y")

    # Convert day to ordinal
    if day == "1" or day.endswith("1") and not day.endswith("11"):
        day += "st"
    elif day == "2" or day.endswith("2") and not day.endswith("12"):
        day += "nd"
    elif day == "3" or day.endswith("3") and not day.endswith("13"):
        day += "rd"
    else:
        day += "th"

    return f"{day_name}, {month_name} {day}, {year}"

def complete_script(story_script, source):
    time_of_day = _get_time_of_day()
    # disclaimer = ""
    header = f"Good {time_of_day} from the 5 things podcast, powered by {source}. My name is Quantum, your AI host, and here are the top 5 things you need to know for {_get_formatted_date()}."
    footer = "That's all for now. Come tomorrow to catch our next show. This is Quantum, signing off."
    full_script = f"{header}\n\n{story_script}\n\n{footer}"
    return full_script

def translate(text, target_lang = "Spanish"):
    client = OpenAI(api_key=get_api_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Please translate this input to {target_lang}. Keep the news anchor like tone, but do not add any cues or placeholders. Do not add anything extra. Keep about the same length or shorter, but do not make it longer."},
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content

def _get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p").lstrip('0')

def say(text, lang, voice="nova") -> str:
    # Initialize the OpenAI API client
    client = OpenAI(api_key=get_api_key())

    # Structure the request
    response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=text
    )

    # # Create the cache directory if it doesn't exist
    # if not os.path.exists(Path(__file__).parent / "cache"/ "51"):
    #     os.makedirs(Path(__file__).parent / "cache"/ "51")

    file_id = _get_formatted_date() + f" at {_get_time()} 5 Things " + lang

    # # Save the audio file
    # file_name = speech_file_path = Path(__file__).parent / "cache" / f"{file_id}.mp3"
    # response.write_to_file(speech_file_path)

    speech_file_path =f"cache/51/{file_id}.mp3"
    response.write_to_file(speech_file_path)

    return speech_file_path

def append_intro_and_outro_music(file_path):
    # file_path = file_path.removeprefix("Your file is at: ")
    intro = "assets/page_51/intro.mp3"
    outro = "assets/page_51/outro.mp3"

    # Load the intro, outro, and main audio files
    intro_audio = AudioSegment.from_mp3(intro)
    outro_audio = AudioSegment.from_mp3(outro)
    main_audio = AudioSegment.from_mp3(file_path)

    # Concatenate the audio files
    final_audio = intro_audio + main_audio + outro_audio

    # Create the podcasts directory if it doesn't exist
    # podcasts_dir = Path(__file__).parent / "podcasts"
    podcasts_dir = "cache/51/finals"
    # if not podcasts_dir.exists():
    #     podcasts_dir.mkdir(parents=True)

    # Save the final audio file
    final_file_path = f"{podcasts_dir}/{Path(file_path).name}"
    final_audio.export(final_file_path, format="mp3")

    return final_file_path

# UI / Main Code for Streamlit view
with st.form(key="news_form", clear_on_submit=True, border=False):
    choices_of_news_source = {
        "The New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "CBS World News": "https://www.cbsnews.com/latest/rss/main",
        "CBS Politics": "https://www.cbsnews.com/latest/rss/politics",
    }

    news_source = st.selectbox("Select a news source", choices_of_news_source.keys(), index=None)
    LANG = st.selectbox(
        "Select Language",
        [
            "Arabic 🇸🇦", "Chinese 🇨🇳", "Dutch 🇳🇱", "English 🇺🇸", "French 🇫🇷",
            "German 🇩🇪", "Hebrew 🇮🇱", "Hindi 🇮🇳", "Italian 🇮🇹", "Japanese 🇯🇵",
            "Korean 🇰🇷", "Portuguese 🇵🇹", "Russian 🇷🇺", "Spanish 🇪🇸"
        ],
        index=3
    )
    st.markdown("*Due to pricing constraints, a password is required to use this service which has been rate limited.*")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Make Podcast")
    if submit:
        if password != st.secrets["ADMIN_PASSWORD"]:
            st.error("Incorrect password. Please try again.")
            st.stop()
        else:

            with st.status("Generating podcast...", expanded=True):

                st.write("Getting news...")
                news = get_news(news_source)

                st.write("Formatting news...")
                formatted_news = format_news(news)

                expanded_news = []

                i = 1

                for story_package in formatted_news:
                    st.write(f"Expanding story {str(i)} of 5...")
                    i += 1
                    expanded_news.append(expand_story(story_package))

                st.write("Condensing up the story...")
                story_only_script = tidy_up_story(expanded_news)

                st.write("Completing the script...")
                full_script = complete_script(story_only_script, news_source)

                # print(full_script)
                st.write("Translating the script...")
                if LANG != "English 🇺🇸":
                    full_script = translate(full_script, target_lang=LANG)
                else:
                    st.write("No translation needed...")
                    full_script = full_script

                st.write("Generating audio...")
                cache = say(full_script, lang=LANG)

                st.write("Appending intro and outro music...")
                final_fp = append_intro_and_outro_music(cache)

                st.write("Podcast generated successfully!")

            st.audio(final_fp, format="audio/mp3")
            st.markdown("*To download this podcast, click the three dots in the audio player then click on download*")
            # st.download_button("Download Podcast", final_fp, "Click here to download your podcast")
