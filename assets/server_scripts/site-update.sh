#!/bin/bash

# Step 1: Kill the current terminal streamlit process
pkill -f streamlit

# Step 2: Navigate to the Documents directory
cd ~/Documents

# Step 3: Backup the contact_form_responses.json if it exists to Env
if [ -f Becks-Website/contact_form_responses.json ]; then
    mv Becks-Website/contact_form_responses.json Env/contact_form_responses.json.bak
fi

# Step 4: Remove the existing Becks-Website directory and clone the repository
rm -rf Becks-Website
git clone https://github.com/beck1888/Becks-Website.git

# Step 5: Restore the contact_form_responses.json file from Env
if [ -f Env/contact_form_responses.json.bak ]; then
    mv Env/contact_form_responses.json.bak Becks-Website/contact_form_responses.json
fi

# Step 6: Copy the secrets file without removing the original
mkdir -p Becks-Website/.streamlit
cp Env/secrets.toml Becks-Website/.streamlit/secrets.toml

# Step 7: Run the Streamlit application
cd Becks-Website
streamlit run 🏠_Home.py