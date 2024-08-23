# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import subprocess # For running commands
import time # For adding a delay so the toast messages can be read before running the action
import http.client, urllib # For sending HTTP requests to Pushover
import os # i forgot lmao
import json # For reading inbox

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

## This page is not allowed to be locked because then it would be impossible to access it from the web

# Check if the page is locked
pass # This page will never be locked

# Set up session state
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "sudo_mode" not in st.session_state: # Sudo mode is a checkbox on login to allow destructive actions from the web interface
    st.session_state["sudo_mode"] = False # Off by default

if st.session_state["sudo_mode"] is True: # Sudo mode is on
    st.session_state["block_destructive_actions"] = False # Will NOT disable destructive action buttons
else: # Sudo mode is off
    st.session_state["block_destructive_actions"] = True # Will disable destructive action buttons

if "bash_history" not in st.session_state:
    st.session_state["bash_history"] = []

# Functions
def create_file_tree(start_path: str, skip_folders: list=None) -> str:
    if skip_folders is None:
        skip_folders = []
    
    tree = []
    
    for root, dirs, files in os.walk(start_path):
        # Skip any folders in the skip_folders list
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in [os.path.join(start_path, sf) for sf in skip_folders]]
        
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level + '├── ' if level > 0 else '' # '.\n'
        tree.append(f"{indent}{os.path.basename(root)}")
        
        sub_indent = ' ' * 4 * (level + 1) + '└── '
        for i, f in enumerate(files):
            if i == len(files) - 1:
                tree.append(f"{sub_indent}{f}")
            else:
                file_indent = ' ' * 4 * (level + 1) + '├── '
                tree.append(f"{file_indent}{f}")

    return "\n".join(tree)

def validate_command(command: str) -> dict:
    # Check for prohibited actions
    blocked = ["sudo", "apt", "shutdown", "reboot", "rm"]

    for b in blocked:
        if b in command:
            return {
                "can_run": False,
                "error": f"The action is not allowed: {b}"
            }

    return {
        "can_run": True
    }

def run_command(command: str) -> str:
    try:
        return subprocess.check_output(command, shell=True).decode("utf-8")
    except Exception as e:
        return f"❌ {str(e)}"

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
        if st.button("🔼 Update Server", key="update_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            # st.toast("Starting update in 5 seconds. Refresh the page if it doesn't automatically refresh in a bit.")
            # time.sleep(5)
            subprocess.Popen(["bash", "/home/admin/Documents/Becks-Website/assets/server_scripts/site-update.sh"])

    # Reboot server button
    with column_2_row_1:
        if st.button("🔄 Reboot Server", key="reboot_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            # st.toast("Rebooting in 5 seconds. Refresh the page if it doesn't automatically refresh in a bit.")
            # time.sleep(5)
            subprocess.Popen(["bash", "sudo reboot"])

    # Shutdown server button
    with column_3_row_1:
        if st.button("🔌 Shutdown Server", key="shutdown_server", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            # st.toast("Shutting down in 5 seconds. The page will no longer be available.")
            # time.sleep(5)
            subprocess.Popen(["bash", "sudo pkill -f streamlit"])
            os.system("sudo pkill -f streamlit")

    # Delete secrets file
    with column_4_row_1:
        if st.button("🗑️ Delete Secrets File", key="delete_secrets_file", disabled=st.session_state["block_destructive_actions"], use_container_width=True):
            st.toast("Deleting secrets file. Make sure to replace it manually.")
            subprocess.Popen(["bash", "rm /home/admin/Documents/Becks-Website/.streamlit/secrets.toml"])


    ## Non sudo buttons below

    # Clear cache button
    with column_1_row_2:
        # THIS ONLY WORKS ON THE PROD SERVER
        if st.button("🧹 Clear Cache [BROKEN]", key="clear_cache", disabled=False, use_container_width=True): # This is not a destructive action so it can stay enabled
            st.toast("Command broken - you need to manually clear the cache") # Not yet implemented
            # # Cache folders: cache/memes and cache/YT
            # folder_endpoints = ["memes", "YT"]

            # for folder_endpoint in folder_endpoints:
            #     # Keep the folder BUT remove all its contents
            #     subprocess.Popen(["bash", f"rm -rf /home/admin/Documents/Becks-Website/cache/{folder_endpoint}/*"])

            # st.toast("Cache cleared", icon="🗑️")

    with column_2_row_2:
        st.button("🌀 Refresh", key="refresh", use_container_width=True, on_click=st.rerun)

    with column_3_row_2:
        if st.button("🔒 Logoff", key="logoff", use_container_width=True):
            st.session_state["auth"] = False
            st.session_state["sudo_mode"] = False
            st.rerun()

    with column_4_row_2:
        if st.button("👤 Switch to SUDO", key="switch_to_sudo", use_container_width=True):
            st.session_state["sudo_mode"] = True
            st.rerun()

    with column_1_row_3:
        if st.button("❌ Stop SUDO", key="switch_to_user", use_container_width=True):
            st.session_state["sudo_mode"] = False
            st.rerun()

    # Bottom columns
    notes, file_tree = st.columns(2)
    messages, message_controller = st.columns(2)
    error_log, visitor_log = st.columns(2)

    # Notes
    with notes:
        with st.expander("📝 Notes", expanded=False):
            st.markdown("**Notes:**")
            st.markdown("- Make sure to replace the secrets file manually.")
            st.markdown("- Make sure to install new packages manually.")
            st.markdown("- Clear cache will only work on the production server.")
            st.markdown("- Clear the cache from time to time for better performance.")
            st.markdown("- Destructive commands will shutdown the server, and it can only be restarted manually or by another device on the same network.")
            st.markdown("- Install packages on the server's global environment by passing the --break-system-packages flag to pip install package.")
            st.markdown("- For now, the lock file will have to be manually edited.")

    # File tree
    with file_tree:
        # Display the file tree starting at the root directory of the Becks-Website folder
        with st.expander("📁 File tree", expanded=False):
            st.markdown("**File tree:**")
            raw_tree = create_file_tree(".", [".venv", "__pycache__", ".git"])
            st.text(raw_tree)

    # Messages
    with messages:
        with st.expander("📨 Mailbox", expanded=False):
            with open("contact_form_responses.json", "r") as f:
                inbox = json.load(f)

            if len(inbox) == 0:
                st.markdown("*No messages in the inbox.*")

            for message in inbox:
                if message["urgent"]:
                    flag = "🚨 "
                else:
                    flag = ""
                st.markdown(f"**{flag}{message['subject']}**")
                st.markdown(f"*Sent on: {message['date_and_time']}*")
                st.markdown(f"*From: {message['name']} ({message['email']})*")
                st.markdown("**Message:** " + message["message"])
                st.markdown(f"`{message['message_hash'][:6]}`")

                st.markdown("---")

    # Message controller
    with message_controller:
        with st.expander("🎛️ Message controller", expanded=False):
            # Load the messages from the JSON file
            with open("contact_form_responses.json", "r") as f:
                messages = json.load(f)

            # Create a list of target hashes
            targets = [message["message_hash"][:6] for message in messages]

            # Create the form for selecting targets
            with st.form(key="message_controller"):
                target = st.multiselect("Target:", targets)
                begin_archive = st.form_submit_button("Archive")
                st.container(height=20, border=False)

                if begin_archive:
                    with st.spinner("Archiving messages..."):
                        archive_path = "assets/page_admin/old.md"
                        updated_inbox = []

                        with open(archive_path, "a") as archive_file:
                            for message in messages:
                                if message["message_hash"][:6] in target:
                                    # Append the message details to the archive
                                    archive_file.write(f"## {message['subject']}\n")
                                    archive_file.write(f"{message['date_and_time']} - {message['name']} - {message['email']}\n\n")
                                    archive_file.write(f"{message['message']}\n\n")
                                    archive_file.write(f"`{message['message_hash'][:6]}`\n\n")
                                    archive_file.write("Was this message urgent? " + ("Yes" if message["urgent"] else "No") + "\n\n")
                                    archive_file.write("---\n\n")
                                else:
                                    # Keep the message in the inbox if it doesn't match the target hash
                                    updated_inbox.append(message)

                        # Save the updated inbox back to the JSON file
                        with open("contact_form_responses.json", "w") as f:
                            json.dump(updated_inbox, f, indent=4)

                        # st.success("Messages archived.")
                        time.sleep(1.5)
                        st.rerun()


    # Error log
    with error_log:
        with st.expander("🚨 Error log", expanded=False):
            st.markdown("*Not implemented yet*")


    # Visitor log
    with visitor_log:
        with st.expander("👥 Visitor log", expanded=False):
            st.markdown("**WARNING:** This log is really long and may take a while to load. Are you sure you want to see it?")

            vlcl1, vlcl2 = st.columns(2)

            with vlcl1:
                show_visitor_log = st.checkbox("Show visitor log")

            with vlcl2:
                delete_visitor_log = st.button("Delete visitor log", disabled=st.session_state.block_destructive_actions)

            if show_visitor_log:
                with open("visitor_log.txt", "r") as f:
                    visitor_log = f.readlines()

                for line in visitor_log:
                    st.markdown(line)

            if delete_visitor_log:
                with open("visitor_log.txt", "w") as f:
                    f.write("")
                
                st.toast("Dumped visitor log.")
                st.rerun()


    # Terminal
    with st.container(border=True):
        st.markdown("### Terminal")

        command = st.chat_input("Run command:")

        if command:
            command_is_valid = validate_command(command)

            if command_is_valid["can_run"]:
                output = (run_command(command))
            else:
                output = command_is_valid["error"]

            st.session_state.bash_history.append({
                "user": command,
                "rpi": output
            })

        for run in st.session_state.bash_history:
            st.markdown(run["user"])
            st.markdown("**➡** `" + run["rpi"] + "`")

            