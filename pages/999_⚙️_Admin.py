# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import subprocess # For running commands
import time # For adding a delay so the toast messages can be read before running the action
import http.client, urllib # For sending HTTP requests to Pushover

# Configure assets
src = asset_director.Asset("Admin", 999)
# loading = src.under_construction()

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # This page needs to be wide because there are a lot of buttons and text to display
    initial_sidebar_state="collapsed") # Hide the sidebar to give more room for the admin UI

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
        st.markdown("*If you are using Chrome's password manager, you might have to click on the password field first to get autofill to show up.*")

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
        st.markdown("**MODE:** SUDO")
        st.markdown("⚠️ *Use extreme caution while sudo mode is on. Sudo mode allows action that can break the server and cannot be resolved remotely!*")
    else:
        st.markdown("**MODE:** Standard")
        st.markdown("*Although inherently destructive actions are disabled, still proceed with caution.*")
    # st.divider()

    # Add some vertical space
    with st.container(border=False, height=20):
        pass

    # Create the columns and rows (as a 4x4 grid)
    column_1_row_1, column_2_row_1, column_3_row_1, column_4_row_1 = st.columns(4)
    column_1_row_2, column_2_row_2, column_3_row_2, column_4_row_2 = st.columns(4)
    column_1_row_3, column_2_row_3, column_3_row_3, column_4_row_3 = st.columns(4)
    column_1_row_4, column_2_row_4, column_3_row_4, column_4_row_4 = st.columns(4)

    # Update server button
    with column_1_row_1:
        if st.button("Update Server", key="update_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            st.toast("Starting update in 5 seconds. Refresh the page if it doesn't automatically refresh in a bit.")
            time.sleep(5)
            subprocess.Popen(["bash", "/home/admin/Documents/Becks-Website/assets/server_scripts/site-update.sh"])

    # Reboot server button
    with column_2_row_1:
        if st.button("Reboot Server", key="reboot_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            st.toast("Rebooting in 5 seconds. Refresh the page if it doesn't automatically refresh in a bit.")
            time.sleep(5)
            subprocess.Popen(["bash", "sudo reboot"])

    # Shutdown server button
    with column_3_row_1:
        if st.button("Shutdown Server", key="shutdown_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            st.toast("Shutting down in 5 seconds. The page will no longer be available.")
            time.sleep(5)
            subprocess.Popen(["bash", "pkill -f streamlit"])

    # Delete secrets file
    with column_4_row_1:
        if st.button("Delete Secrets File", key="delete_secrets_file", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            st.toast("Deleting secrets file. Make sure to replace it manually.")
            subprocess.Popen(["bash", "rm /home/admin/Documents/Becks-Website/.streamlit/secrets.toml"])

    # Clear cache button
    with column_1_row_2:
        # THIS ONLY WORKS ON THE PROD SERVER
        if st.button("Clear Cache", key="clear_cache", disabled=False, use_container_width=True): # This is not a destructive action so it can stay enabled
            # Cache folders: cache/memes and cache/YT
            folder_endpoints = ["memes", "YT"]

            for folder_endpoint in folder_endpoints:
                # Keep the folder BUT remove all its contents
                subprocess.Popen(["bash", f"rm -rf /home/admin/Documents/Becks-Website/cache/{folder_endpoint}/*"])

            st.toast("Cache cleared", icon="🗑️")

    with column_2_row_2:
        st.button("Refresh", key="refresh", use_container_width=True, on_click=st.rerun)

    # Notes
    with st.container(border=True):
        st.markdown("**Notes:**")
        st.markdown("- Make sure to replace the secrets file manually.")
        st.markdown("- Make sure to install new packages manually.")
        st.markdown("- Clear cache will only work on the production server.")
        st.markdown("- Clear the cache from time to time for better performance.")
        st.markdown("- Destructive commands will shutdown the server, and it can only be restarted manually or by another device on the same network.")
