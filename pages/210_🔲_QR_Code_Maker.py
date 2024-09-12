# Import necessary libraries
import streamlit as st # Web framework
import asset_director # For asset management
import segno
import hashlib
import streamlit_lottie as st_lottie
import json

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

c1, c2, c3 = st.columns(3)

with c2:
    st.markdown(src.under_construction()[0], unsafe_allow_html=True)
    st_lottie.st_lottie(src.under_construction()[1], speed=1, width=400, key="under_construction", quality="high")
    st.stop()

# Check if the page is locked
if src.is_locked()[0]:
        st.error(src.is_locked()[1])
        st.stop()

# Functions
def sanitize_text(text: str) -> str:
    hold = ""
    for char in text:
        if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
            if char == " ":
                hold += "_"
            else:
                hold += char

    return hold
        

    # text = hold
    
    text = text.replace(" ", "_")
    text = text.replace(".", "-")
    text = text.replace("/", "-")
    # text = text.lower()

    # if "www." in text:
    #     try:
    #         text = text.replace("https://", "")
    #         text = text.replace("http://", "")
    #         text = text.replace("www.", "")
    #         text.split(".")[0]
    #     except:
    #         pass

    # text = text.replace(".", "")
    # text = text.replace("-", "")
    # text = text.replace("_", "")
    # text = text.replace(" ", "_")
    

    # if (len(text) > 10):
    #     text = text[:10]

    return text


def generate_qr_code(text: str) -> str:
    """
    Generates a QR code image from the given text.

    Args:
        text (str): The text to encode in the QR code.

    Returns:
        The image path of the generated QR code.
    """
    qrcode = segno.make_qr(text)
    qrcode.save(f"cache/210/{sanitize_text(text)}.png", scale=10)
    return f"cache/210/{sanitize_text(text)}.png"


# Page setup
st.title("🔲 QR Code Maker")

st.divider() # Readability on page

col1, col2 = st.columns(2)

with col1:
    text = st.text_area("Enter text to use in QR code")
    go = st.button("Generate QR Code", use_container_width=True)

    if go and text is not None and text != "":
        fp = generate_qr_code(text)

    try:
        st.download_button("Save QR Code", fp, file_name=f"{sanitize_text(text)}.png", use_container_width=True, disabled=True)
    except NameError:
        st.button("Save QR Code", disabled=True, use_container_width=True)

    st.markdown("*To save, right click on the QR code and click 'Save Image As'.*")

with col2:
    try:
        st.image(fp, caption=text, use_column_width=True)
    except NameError:
        pass

