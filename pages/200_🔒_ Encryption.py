# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management


# Configure assets
src = asset_director.Asset("Encryption", 200)

# Configure the Streamlit app
st.set_page_config(page_title=src.tab_title(),
    page_icon=src.favicon(),
    layout="wide", # Needs more room (2 columns)
    initial_sidebar_state="collapsed") # Hide the sidebar because more room is needed for the 2 columns

# Hide the Streamlit UI
for config in src.clear_st_ui():
    st.markdown(config, unsafe_allow_html=True) 

# Add a little bit of vertical space so the html h1 tag doesn't get cutoff
with st.container(border=False, height=10):
    pass    

# Functions
def rotate(text: str, key: str, direction: int) -> str:
    """
    Encrypts the given text using the Caesar cipher algorithm.

    Args:
        text (str): The text to encrypt.
        key (str): The key to use for encryption.
        direction (int): The direction of encryption. 1 for encryption (forwards), -1 for decryption (backwards).

    Returns:
        str: The encrypted text.

    Raises:
        ValueError: If the key is not an integer or cannot be converted to one.
        ValueError: If the key has a leading zero.
        ValueError: If the direction is not 1 or -1.
    """
    # Checks

    # Check for empty key
    if not key:
        raise ValueError("Key cannot be empty.")
        
    # Check for leading zeros
    if key.startswith("0"):
        raise ValueError("Key cannot start with a leading zero.")

    # Convert the key to an integer
    try:
        key = int(key)
    except ValueError:
        raise ValueError("Key must be an integer.")
    
    # Check if the direction is 1 or -1
    if direction not in [1, -1]:
        raise ValueError("Direction must be 1 or -1.")

    # Normalize key within the range of the alphabet length
    key = key % 26

    # Main Logic
    # Define the alphabet (lowercase and uppercase handled separately)
    lowercase_alphabet = "abcdefghijklmnopqrstuvwxyz"
    uppercase_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    encrypted = ""  # Initialize an empty string to store the encrypted text

    # Loop through each character in the text
    for char in text:
        if char.islower():
            # Find the index of the character in the lowercase alphabet
            index = lowercase_alphabet.find(char)
            if index != -1:
                new_index = (index + direction * key) % 26
                encrypted += lowercase_alphabet[new_index]
            else:
                encrypted += char
        elif char.isupper():
            # Find the index of the character in the uppercase alphabet
            index = uppercase_alphabet.find(char)
            if index != -1:
                new_index = (index + direction * key) % 26
                encrypted += uppercase_alphabet[new_index]
            else:
                encrypted += char
        else:
            # Non-alphabet characters are added as is
            encrypted += char

    return encrypted

# Streamlit app entry point
col1, col2 = st.columns(2)

with col1:
    with st.form(key="encryption_controller", border=False):
        with st.container(border=True, height=600):
            st.subheader("Encrypt or Decrypt:")
            st.divider()

            text = st.text_area("Your message: ")
            key = st.text_input("Key:", placeholder="Such as 1234 or 9214")
            mode = st.radio("Mode:", ["Encrypt", "Decrypt"], None)
            direction = 1 if mode == "Encrypt" else -1 # 1 for encryption, -1 for decryption (single line if-else statement)
            submit = st.form_submit_button("Begin", use_container_width=True)

            if submit:
                if not text:
                    st.error("Please enter some text before continuing!")
                    st.stop()

                if not key:
                    st.error("Please type a key before continuing!")
                    st.stop()

                if not direction:
                    st.error("Please select a mode before continuing!")
                    st.stop()

                try:
                    st.session_state["encrypted_or_decrypted_text"] = rotate(text, key, direction)
                except ValueError as e:
                    st.error("Invalid key. Please try again.")

with col2:
    with st.container(border=True, height=600):
        st.subheader("Result:")
        st.divider()


        try:
            st.markdown("*" + st.session_state["encrypted_or_decrypted_text"] + "*")
        except:
            st.markdown("*No text has been encrypted or decrypted yet. Use the form to the left and try again!*")