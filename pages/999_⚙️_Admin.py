# Import necessary libraries
import streamlit as st
import asset_director
import subprocess

# Configure assets
src = asset_director.Asset("Admin", 999)
# loading = src.under_construction()

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="centered",
    initial_sidebar_state="expanded")

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True)

# Set up session state
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "sudo_mode" not in st.session_state: # Sudo mode is a checkbox on login to allow destructive actions from the web interface
    st.session_state["sudo_mode"] = False # Off by default

if st.session_state["sudo_mode"] is True: # Sudo mode is on
    st.session_state["block_destructive_actions"] = False # Will NOT disable destructive action buttons
else: # Sudo mode is off
    st.session_state["block_destructive_actions"] = True # Will disable destructive action buttons

## Page content
st.title("Admin Portal")

# Sign-in page
if st.session_state["auth"] is False:
    with st.form(key="login_form"):
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")

        sudo_mode = st.checkbox("Sudo Mode", key="sudo_mode_checkbox", value=False)

        login_button = st.form_submit_button(label="Login")
        st.markdown("*You might have to click the password field to get autofill to show up*")

        if login_button:
            if username == st.secrets["ADMIN_USERNAME"] and password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state["auth"] = True
                if sudo_mode is True:
                    st.session_state["sudo_mode"] = True
                st.rerun() # Rerun the script to display the admin portal
            else:
                st.error("Incorrect username or password")

# Admin portal
if st.session_state["auth"] is True:
    # Header
    if st.session_state["sudo_mode"] is True:
        st.warning("Sudo Mode Enabled - All destructive actions are disabled - Be careful!")
    else:
        st.text("Standard mode")
    st.divider()


    # Update server button
    if st.button("Update Server", key="update_server", disabled=st.session_state["block_destructive_actions"]):
        st.toast("Updating server...")
        subprocess.Popen(["bash", "/home/admin/Documents/Becks-Website/assets/server_scripts/site-update.sh"])
        # st.toast("Make sure to refresh in a minute!")
        # st.toast("Button broken", icon="❌")
        # st.toast("Use manual update script from server", icon="🖥️")
        # os.system("~/Documents/update_becks_website.sh")
    st.markdown("""<p style='color:orange;'>This button will only work on the server, not in a development environment.</p>""", unsafe_allow_html=True)
    st.markdown("""<p style='color:red;'>If you've updated, added, or changed any secrets, you will have to add those manually.</p>""", unsafe_allow_html=True)