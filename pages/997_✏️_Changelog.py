# Import necessary libraries
import streamlit as st # Web framework
import requests # For making HTTP requests to the GitHub API
import asset_director # For asset management
from datetime import datetime # For date formatting
import pytz # For timezone conversion
import time # For adding a delay to prevent spamming the API
from random import randint # For generating random numbers for the loading time

# Configure assets
src = asset_director.Asset("Changelog", 997)

# Configure the Streamlit app
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded",
)

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Function to get all commit messages from the repo
def get_commit_messages(repo_url):
    owner_repo = "/".join(repo_url.strip("/").split("/")[-2:])
    commits_url = f"https://api.github.com/repos/{owner_repo}/commits"
    # print(commits_url) # For debugging
    response = requests.get(commits_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Date formatting function
def convert_date_format(date_str):
    # Parse the date string into a datetime object
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    # Define the UTC and Los Angeles time zones
    utc_zone = pytz.utc
    la_zone = pytz.timezone('America/Los_Angeles')

    # Convert the datetime object from UTC to Los Angeles time
    dt_utc = utc_zone.localize(dt)
    dt_la = dt_utc.astimezone(la_zone)

    # Function to get the day suffix
    def get_day_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1]

    # Extract date components
    year = dt_la.year
    month = dt_la.strftime("%B")
    day = dt_la.day
    day_suffix = get_day_suffix(day)
    hour = dt_la.hour % 12 or 12  # Convert to 12-hour format
    minute = dt_la.minute
    am_pm = "AM" if dt_la.hour < 12 else "PM"

    # Create the desired formatted string
    formatted_date = f"{month} {day}{day_suffix}, {year} at {hour}:{minute} {am_pm}"

    return formatted_date

# Page content
st.title("Changelog")
st.markdown("Only the most recent 30-ish commits (changes/ updates) will be shown. To see a full changelog, please visit the [GitHub repository](https://github.com/beck1888/Becks-Website/commits/main/).")
st.divider()
page_loader_button = st.empty()

# Create a button to load the changelog
load_commits_go = page_loader_button.button("Load Changelog", key="load_changelog")

# Lock changelog from loading automatically to prevent spam to the github API
if load_commits_go:
    # Remove the button
    page_loader_button.empty()

    try:
        commits = get_commit_messages("https://github.com/beck1888/Becks-Website")
        # Go through each commit
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")  # Display error message for HTTP errors
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    # Add a delay to prevent spamming the API
    bar_hold = st.empty()
    bar = bar_hold.progress(0, text="Loading version history...")

    for i in range(100):
        time.sleep(randint(1, 5) / 100)
        bar.progress((i + 1)/100, text="Loading version history...")
    time.sleep(0.5)

    # Close the progress bar
    bar_hold.empty()

    # Initialize the counter for the number of commits
    # commit_count = 0

    # Display the changelog
    for commit in commits:
        try:
            # Simplify/ shorten the commit data variables
            commit_message: str = commit['commit']['message']
            commit_author = commit['commit']['author']['name']
            commit_date = commit['commit']['author']['date']

            # Get the commit number
            # commit_index = len(commits) - commit_count
            # commit_index = str(commit_index) # Convert to string for display
            # commit_index = f"Commit {commit_index} of {str(len(commits))}" # Add the number of commits into the index

            # Increment the counter
            # commit_count += 1

            # Capitalize the first letter of the commit message while leaving the rest as it is
            try:
                commit_message = commit_message[0].upper() + commit_message[1:] # IDK this could probably break
            except Exception as e:
                pass # So then just leave the message alone

            # Display commit data neatly
            with st.container(border=True):
                st.markdown(f"**{commit_message}**")
                # st.text(f"Author: {commit_author}") # No need to display author because I'm the only contributor
                st.markdown(f"*{convert_date_format(commit_date)}*")
                st.markdown(f"Commit ID: {commit['sha']}") # Display commit ID and index for reference in case there is an issue that needs to be reported so I can find which commit broke it
                # st.markdown(f"{commit_index}          |          Commit ID: {commit['sha']}") # Display commit ID and index for reference in case there is an issue that needs to be reported so I can find which commit broke it
        except Exception as e:
            with st.container(border=True):
                st.error("Error loading this commit")
                # st.error(e)

    # # End of changelog
    # st.markdown("---")
    # st.markdown("*End of changelog*")
    # st.markdown("---") # I love dividers, can ya tell? LMAO XD