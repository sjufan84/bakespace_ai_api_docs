# This is a streamlit representation of the documentation related to the Bakespace AI API.  It is a work in progress.

# Initial imports
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Create buttons that link to the different pages
st.markdown("### BakeSpace AI API Documentation")
st.markdown("#### Select a page to view the documentation for the related endpoints for the BakeSpace AI API.\
             These options are also available on the sidebar to the left.  Click on 'ReadME'\
             to get a broad overview of the API, its endpoints, and the desired functionality of the API.")

st.markdown("---")

chat_button = st.button("Chat Endpoints", type='primary', use_container_width=True)
if chat_button:
    switch_page('Chat Endpoints')

extraction_button = st.button("Extraction Endpoints", type='primary', use_container_width=True)
if extraction_button:
    switch_page('Extraction Endpoints')

recipe_button = st.button("Recipe Endpoints", type='primary', use_container_width=True)
if recipe_button:
    switch_page('Recipe Endpoints')

readme_button = st.button("ReadME", type='primary', use_container_width=True)
if readme_button:
    switch_page('ReadME')

image_and_pairing_button = st.button("Image Generation and Pairing Endpoints", type='primary', use_container_width=True)
if image_and_pairing_button:
    switch_page('Pairing and Image Endpoints')


# Set up page links
