# This is a streamlit representation of the documentation related to the Bakespace AI API.  It is a work in progress.

# Initial imports
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Create buttons that link to the different pages
st.set_page_config(page_title="BakeSpace App", layout="wide", initial_sidebar_state="collapsed")

chat_button = st.button("Chat Endpoints", type='primary', use_container_width=True)
if chat_button:
    switch_page('Chat Endpoints')


# Set up page links
