# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import json # For managing JSON data in the contact form
import http.client, urllib # For sending HTTP requests to Pushover
import hashlib # For generating hashes for the contact form
import datetime # For date formatting

# Configure assets
src = asset_director.Asset("Contact", 998)

# Configure the Streamlit app
st.set_page_config(
    page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded",
)

# Get the date
def get_date_and_time():
    """
    Gets the current date and time as MM/DD/YYYY HH:MM:SS AM/PM
    """
    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%I:%M:%S %p")
    full_datetime_stamp = date + " " + time

    return full_datetime_stamp

# Get the SHA256 hash of the contact form
def get_sha256_hash(subject, message, date_and_time):
    """
    Gets the SHA256 hash of the contact form
    """
    sha256_hash = hashlib.sha256((subject + message + date_and_time).encode("utf-8")).hexdigest()

    return sha256_hash

# Communication with Pushover
def send_pushover_notification(subject, message, is_urgent):
    if is_urgent:
        priority = 1
        sound = "Woop"
        emoji = "⚠️ "
    else:
        priority = 0
        sound = "Message"
        emoji = ""


    conn = http.client.HTTPSConnection("api.pushover.net:443") # Pushover API endpoint
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": st.secrets["PUSHOVER_APP_TOKEN"],
        "user": st.secrets["PUSHOVER_USER_KEY"],
        "priority": priority,
        "sound": sound,
        "title": emoji + "Server Alert: " + subject,
        "message": "New message: " + message
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse() # Sends the request

# Main content
st.title("Contact")

# Contact form
with st.form(key="contact_form", clear_on_submit=True):
    st.markdown("**Your Info:**")
    name = st.text_input("Name (required)", key="name", placeholder="Your Name", help="Your name helps me track where issues are coming from. I won't share it. Feel free to make up a name if you'd like, just please use the same name in each message.")
    email = st.text_input("Email (optional)", key="email", placeholder="example_email@example.com", help="Your email will help me get in contact with you if needed or to reply/ let you know when the issue is fixed. I cannot guarantee a response, but I will look at your message. Your email is stored locally and I won't share it.")
    st.divider()

    st.markdown("**Your Message:**")
    message_placeholder_text = "Type your message here. Include as much info possible, including where you found the issue, how to reproduce it, commit hashes, and other info as relevant."

    message_type = st.radio("Message Type (required)", options=["Bug Report", "Feature Request", "Other"], key="message_type", index=None, help="Selecting a message type helps me prioritize issues over requests.")

    subject = st.text_input("Subject (required)", key="subject", placeholder="Short Subject Headline", help="Please write a few words about your issue to help me classify it. Keep this to a few words, and put the details in the main message box below.")

    message = st.text_area("Message (required)", placeholder=message_placeholder_text, key="message", help="Please include as much info as possible.")

    urgent = st.checkbox("Urgent (optional)", value=False, key="urgent", help="Check this box only if you've found an urgent issue like leaked API keys, infinite loops, outages, etc.")

    submit_button = st.form_submit_button(label="Send Message")

    if submit_button:
        # Make sure all required fields are filled

        # Create the JSON data
        data = {
            "date_and_time": get_date_and_time(),
            "message_hash": get_sha256_hash(subject, message, get_date_and_time()),
            "name": name,
            "email": email,
            "subject": subject,
            "message_type": message_type,
            "message": message,
            "urgent": urgent
        }

        # Write the JSON data to the file
        with open("contact_form_responses.json", "r") as f:
            responses = json.load(f)

        responses.append(data)

        with open("contact_form_responses.json", "w") as f:
            json.dump(responses, f, indent=4)

        # Send Pushover notification
        send_pushover_notification(subject, message, urgent)

        st.info(f"Response received! Thank you for contacting me, {name}!")
