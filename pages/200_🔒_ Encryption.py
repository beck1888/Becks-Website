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
    if str(key)[0] == "0":
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

def calculate_english_density(message: str) -> float:
    # Convert the message to lowercase
    message = message.lower() # The list is all lowercase

    # Sanitize the message of all non-alphabetical characters
    alphabet = "abcdefghijklmnopqrstuvwxyz" + " " # Don't forget about the space!!!
    tmp = ""
    for char in message:
        if char in alphabet:
            tmp += char
    message = tmp # Overwrite the original message with the sanitized message

    # Get all the top 10,000 English words
    words = src.fetch_local_json("words.json")

    is_english = 0

    for word in message.split(" "):
        if word in words:
            is_english += 1

    del words # Free up memory

    density = is_english / len(message.split(" "))

    return round(density, 3)

def crack(encrypted: str) -> dict:
    # Initialize
    highest_score = 0
    best_key = ""
    best_guess_of_original_message = ""

    # Create a list of all possible keys
    all_possible_keys = []
    for i in range(1, 27):
        all_possible_keys.append(str(i))

    # Loop through all possible keys
    for key in all_possible_keys:
        # Decrypt the message
        decrypted = rotate(encrypted, str(key), -1)

        # Calculate the score
        score = calculate_english_density(decrypted)

        # Debug
        # print(f"Key: {key} | Score: {score}")

        # Update the best key
        if score > highest_score:
            highest_score = score
            best_key = key
            best_guess_of_original_message = decrypted

    return {
        "key": best_key,
        "message": best_guess_of_original_message,
        "confidence": highest_score
    }


# Streamlit app entry point
col1, col2 = st.columns(2)

with col1:
    with st.form(key="encryption_controller", border=False):
        with st.container(border=True, height=550):
            st.subheader("Encrypt or Decrypt:")
            st.divider()

            text = st.text_area("Your message: ", placeholder="Enter your message here...")
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
    with st.container(border=True, height=550):
        st.subheader("Result:")
        st.divider()

        try:
            st.markdown(st.session_state["encrypted_or_decrypted_text"])
        except:
            st.markdown("*No text has been encrypted or decrypted yet. Use the form to the left and try again!*")

# Message cracker
with st.container(border=True):
    st.subheader("Message Cracker")
    st.divider()

    with st.form(key="message_cracker", border=False):
        message = st.text_area("Message: ", placeholder="Enter an encrypted message here...")

        if st.form_submit_button("Crack"):
            if not message:
                st.error("Please enter some text before continuing!")
                st.stop()

            st.divider()

            with st.spinner("Cracking..."):
                original_message = crack(message)

            st.markdown("**Best Guess of Original Message:** " + original_message["message"])
            st.markdown("**Lowest Possible Key:** " + str(original_message["key"]))
            st.markdown("**Confidence Score:** " + str(original_message["confidence"]))