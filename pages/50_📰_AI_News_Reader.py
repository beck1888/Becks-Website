# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import feedparser # For parsing RSS feeds
import openai # For using the OpenAI API to generate summaries of the news
import streamlit_lottie # For rendering the Lottie animation
import datetime # For getting the current date and time


# Configure assets
src = asset_director.Asset("News", 50)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded")

# # Hide the Streamlit UI
# for config in src.clear_st_ui():
#     st.markdown(config, unsafe_allow_html=True)

# # Add a little bit of vertical space so the html h1 tag doesn't get cutoff
# with st.container(border=False, height=10):
#     pass

# Functions
def get_news(site_rss_url):
    # Parse the feed
    feed = feedparser.parse(site_rss_url)

    result = {}

    # GET Head
    result["section"] = feed.feed.title

    # GET Entries (5)
    index = 0
    for entry in feed.entries[:5]:
        index += 1
        result[f"story_{str(index)}"] = {
            "title": entry.title,
            "summary": entry.summary
        }

    # Specify number of entries
    result["num_entries"] = index

    return result

def summarize_news(news: dict, style: str, use_emojis: bool) -> str:
    """
    Uses the OpenAI API to generate a summary of the news using the specified style. Returns the summary as a string using GitHub Flavored Markdown.
    
    Args:
        news (dict): The news data to summarize.
        style (str): The style of summary to generate.
        use_emojis (bool): Whether to use emojis in the summary.

    Returns:
        str: The summary of the news in GitHub Flavored Markdown format.
    """

    # Configure the OpenAI API
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Craft flags
    if use_emojis:
        emoji_flag = "Use emojis to make the summary more engaging and clear."

    # Query the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Create a {style} summary of the following news. {emoji_flag}"},
                  {"role": "user", "content": str(news)}], # Convert the dictionary to a string because OpenAI API only accepts strings for this parameter
        stream=False,
    ).choices[0].message.content

    return response

def get_timestamp() -> str:
    """
    Returns the current timestamp in the format Month_name day(day_suffix), Year at Hour AM/PM.
    """
    
    # Get the current date and time
    now = datetime.datetime.now()

    # Determine the day and its suffix
    day = now.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Format the timestamp
    timestamp = now.strftime(f"%B {day}{suffix}, %Y at %I:%M %p")

    return timestamp

# Set up session state
if "phase" not in st.session_state:
    st.session_state["phase"] = 0

# Preload the Lottie animation
st.session_state["animation_data"] = src.fetch_local_json("loader")


# Main app

# Cannot be defined in an if block
sites = {
    "The New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
}

if st.session_state["phase"] == 0:
    st.title("AI News Reader")

    with st.form("news_form"):
        st.session_state.site = st.selectbox("Select a site", options=list(sites.keys()), index=None, placeholder="News sites")
        st.session_state.focus = st.radio("Focus on", options=["Top Stories", "Upbeat"], index=None)
        st.session_state.use_emojis = st.checkbox("Use emojis", value=True)

        submit_button = st.form_submit_button(label="Read News")

        if submit_button:
            if st.session_state.site is None:
                st.error("Please select a site before continuing!")
                st.stop()

            if st.session_state.focus is None:
                st.error("Please select a focus before you continue!")
                st.stop()

            st.session_state["phase"] = 1
            st.rerun()

if st.session_state["phase"] == 1:
    st.markdown("# Reading news...")

    streamlit_lottie.st_lottie(st.session_state["animation_data"], speed=1, height=400, quality="high")

    st.session_state["news"] = get_news(sites[st.session_state.site])
    st.session_state.summary = summarize_news(st.session_state["news"], st.session_state.focus, st.session_state.use_emojis)

    st.session_state["phase"] = 2
    st.rerun()

if st.session_state["phase"] == 2:
    st.markdown(get_timestamp())
    st.container(height=5, border=False)
    st.markdown(st.session_state.summary)