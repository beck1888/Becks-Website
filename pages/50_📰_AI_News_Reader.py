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

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Add a little bit of vertical space so the html h1 tag doesn't get cutoff
with st.container(border=False, height=10):
    pass

# Functions
def get_news(site_rss_url, read_to):
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

    return result

def summarize_news(news: dict, focus: str, use_emojis: bool, style: str, language: str) -> str:
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
    else:
        emoji_flag = ""

    # Remove emojis from the language flag
    language = language[1:].removeprefix(" ").removesuffix(" ")

    # Query the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Create a summary of the following news using the news headline, the summary, and your own knowledge in {language} with the style of {style} and, if possible, focus on {focus}. {emoji_flag}"},
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
    "The Wall Street Journal": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "CBS News": "https://www.cbsnews.com/latest/rss/main",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "CNBC": "https://www.cnbc.com/id/10000108/device/rss/rss.xml",
    "The New York Post": "https://nypost.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "The United Nations": "https://news.un.org/feed/subscribe/en/news/all/rss.xml"
}

if st.session_state["phase"] == 0:
    st.title("AI News Reader")

    with st.form("news_form"):
        st.session_state.site = st.selectbox("Select a site", options=list(sites.keys()), index=None, placeholder="News sites")
        st.session_state.language = st.selectbox("Pick a language for the summary", options=["🇺🇸 English", "🇪🇸 Spanish", "🇫🇷 French", "🐈 Cat Noises", "🐶 Dog Noises", "🐷 Pig Latin"], index=0)
        st.session_state.max_stories = st.slider("How many headlines should I read?", min_value=1, max_value=10, value=5, step=1, help="Choose the number of headlines you want to read from the selected site. If that many headlines aren't available, the app will just read the max number of headlines available.")
        st.session_state.focus = st.radio("Focus on", options=["Breaking News", "Upbeat", "Lifestyle", "Wars and Conflicts", "Tech"], index=None)
        st.session_state.style = st.radio("Style", options=["News Anchor Script", "Shakespearian", "Joking", "Plain Summary"], index=None)
        st.session_state.use_emojis = st.checkbox("Use emojis", value=True)

        submit_button = st.form_submit_button(label="Read News")

        if submit_button:
            if st.session_state.site is None:
                st.error("Please select a site before continuing!")
                st.stop()

            if st.session_state.focus is None:
                st.error("Please select a focus before you continue!")
                st.stop()

            if st.session_state.style is None:
                st.error("Please select a style before you continue!")
                st.stop()

            if st.session_state.language is None:
                st.error("Please select a language before you continue!")
                st.stop()

            if st.session_state.max_stories is None:
                st.error("Please select a number of stories before you continue!")
                st.stop()

            st.session_state["phase"] = 1
            st.rerun()

if st.session_state["phase"] == 1:
    st.markdown("# Reading news...")

    streamlit_lottie.st_lottie(st.session_state["animation_data"], speed=1, height=400, quality="high")

    st.session_state["news"] = get_news(sites[st.session_state.site], st.session_state.max_stories)
    st.session_state.summary = summarize_news(st.session_state["news"], st.session_state.focus, st.session_state.use_emojis, st.session_state.style, st.session_state.language)

    st.session_state["phase"] = 2
    st.rerun()

if st.session_state["phase"] == 2:
    st.markdown(f"{st.session_state.site} | {get_timestamp()}")
    st.divider()
    st.container(height=5, border=False)
    st.markdown(st.session_state.summary)

st.container(height=20, border=False)
st.divider()
st.container(height=20, border=False)
st.markdown("*Reload the page to read another news article or select a new style*")