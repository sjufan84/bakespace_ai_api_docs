import streamlit as st

st.title("Extraction Service API Documentation")

st.success("""
The broad overview for these endpoints is the ability to upload image, pdf, or text files and extract the raw recipe text from them.
This text can then be passed to the "format-recipe" endpoint to get a formatted recipe object that aligns with the Recipe model in the
models folder.  **These will also need to be inititated with some sort of unique identifier that is tied to the user's id in the database,\
or perhaps we can just use the user_id itself to manage these extractions.**
           
This object's fields should line up with the existing bakespace database schema for easy insertion into the database.
To see more details and code examples for the specific endpoints, as well as an example implementation of the extraction service in a
streamlit app, choose an endpoint from the dropdown below.  **Some of the endpoints related to file uploads do not have javascript code examples
due to the variance in implementation methods. We will also need to work on integrating the unique ids. Refer back to the Streamlit example for reference to a pythonic application.**
""")



endpoints = {
    "Streamlit Example": {
        "description": """
            This is an example of how to call the extraction service from a Streamlit app. This is not an endpoint on the extraction service itself.
        """,
        "example": """
        # This is a streamlit front end to interact with our fastapi backend endpoints
# related to text extraction and recipe editing from various file types.

# Initial imports
import streamlit as st
import requests
import json
import os
from pydantic import BaseModel
from typing import List, Optional


class Recipe(BaseModel):
    #recipeid: int -- this could be generated by the database
    name: str
    #author: str
    #foodimg: str -- @TODO populate the foodimg field from the image generated by the image service
    #fullimg: str
    desc: Optional[str]
    preptime: int
    cooktime: int
    totaltime: int
    servings: int
    directions: List[str]
    ingredients: List[str]
    calories: Optional[int]
    recipe_text: str
    # created_on: date.today()

# Create an extraction service class
class ExtractionService:
    def __init__ (self):
        self.baseUrl = "http://localhost:8000"
        self.raw_text = ""
        self.formatted_recipe = Recipe
        
    # Define a function to allow the user to upload an image file and send it to the backend
    # for text extraction
    def extract_image_text(self, files):
        # Prepare the files for the request
        prepared_files = [("images", (file.name, file.getvalue())) for file in files]

        # Send the files to the backend
        response = requests.post(f"{self.baseUrl}/extract-text-from-images", files=prepared_files)
        # Get the response data
        data = response.json()
        # Convert the returned list of strings to a single string
        data = " ".join(data)
        # Set the raw text
        self.raw_text = data
        # Return the data
        return data
    
    # Define a function to extract text from a pdf file or files
    def extract_pdf_text(self, files):
        # Convert each file to bytes and then append to a list
        pdf_files = [("pdfs", (file.name, file.getvalue())) for file in files]

        # Create a list of files
        response = requests.post(f"{self.baseUrl}/extract-pdf", files=pdf_files)

        # Get the response data
        data = response.json()
        # Convert the returned list of strings to a single string
        data = " ".join(data)
        # Set the raw text
        self.raw_text = data
        # Return the data
        return data
    
    def extract_txt_text(self, files):
        # Prepare the files for the request
        prepared_files = [("text_files", (file.name, file.getvalue())) for file in files]

        # Send the files to the backend
        response = requests.post(f"{self.baseUrl}/extract-text-from-txt", files=prepared_files)

        # Get the response data
        data = response.json()

        # Convert the returned list of strings to a single string
        data = " ".join(data)

        # Set the raw text
        self.raw_text = data

        # Return the data
        return data

    
    # Define a function to pass the raw text to the backend for formatting
    def format_recipe(self, raw_text):
        params = {"raw_text" : raw_text}
        # Send the raw text to the backend
        response = requests.post(f"{self.baseUrl}/format-recipe", params = params)
        st.write(response)
        # Get the response data
        if response:
            data = response.json()
            # Set the formatted recipe
            self.formatted_recipe = Recipe(**data)
            # Set the is_recipe and is_formatted_recipe flags
            st.session_state.is_recipe = True
            st.session_state.is_formatted_recipe = True
            

        # Return the data
        return data
    

# Initialize the session state
if "extraction_service" not in st.session_state:
    st.session_state.extraction_service = ExtractionService()
if "recipe_text" not in st.session_state:
    st.session_state.recipe_text = ""
if "is_recipe" not in st.session_state:
    st.session_state.is_recipe = False
if "is_formatted_recipe" not in st.session_state:
    st.session_state.is_formatted_recipe = False
    

# Create a title for the app
st.title("Text Extraction and Recipe Editing")




uploaded_files = st.file_uploader("Choose an image file to upload", type=["png", "jpg", "jpeg", "txt", "pdf"], accept_multiple_files=True)

# Perform a check to ensure that the user has uploaded a file and that if they have uploaded multiple files,
# that they are all of the same type 
if uploaded_files:
   
    # Check to make sure that all of the files are of the same type
    file_types = []
    for file in uploaded_files:
        file_types.append(file.type)   
    
    # Check to see if the user has uploaded multiple files of different types
    if len(set(file_types)) > 1:
        st.write("Please upload files of the same type")
    else:
        # Check to see if the file type is an image
        if file_types[0] == "image/jpeg" or file_types[0] == "image/png" or file_types[0] == "image/jpg":
            # Create a button to upload the file
            if st.button("Upload files"):
                with st.spinner("Extracting text from image..."):
                    try:
                        st.session_state.extraction_service.raw_text = st.session_state.extraction_service.extract_image_text(uploaded_files)
                        st.session_state.is_recipe = True
                    except Exception as e:
                        st.write("Error extracting text from image")
                        st.write(e)

        # Check to see if the file type is a pdf
        elif file_types[0] == "application/pdf":
            # Create a button to upload the file
            if st.button("Upload files"):
                with st.spinner("Extracting text from pdf..."):
                    try:
                        st.session_state.extraction_service.raw_text = st.session_state.extraction_service.extract_pdf_text(uploaded_files)
                        st.session_state.is_recipe = True
                    except Exception as e:
                        st.write("Error extracting text from pdf")
                        st.write(e)

        # Check to see if the file type is a txt file
        elif file_types[0] == "text/plain":
            # Create a button to upload the file
            if st.button("Upload files"):
                with st.spinner("Extracting text from txt file..."):
                    try:
                        st.session_state.extraction_service.raw_text = st.session_state.extraction_service.extract_txt_text(uploaded_files)
                        st.session_state.is_recipe = True
                    except Exception as e:
                        st.write("Error extracting text from txt file")
                        st.write(e)
        else:
            st.write("Please upload a file of type .png, .jpg, .jpeg, .txt, or .pdf")


# Test out the formatting endpoint using the returned raw text
#st.write(st.session_state.extraction_service.raw_text)

# Create a button to format the recipe
if st.button("Format recipe"):
    with st.spinner("Formatting recipe..."):
        try:
            st.session_state.extraction_service.formatted_recipe = st.session_state.extraction_service.format_recipe(st.session_state.extraction_service.raw_text)
            st.session_state.is_formatted_recipe = True
        except Exception as e:
            st.write("Error formatting recipe")
            st.write(e)

# Write out the formatted recipe
if st.session_state.is_formatted_recipe == True:
    st.write("Recipe name: ", st.session_state.extraction_service.formatted_recipe['name']
            , "Ingredients: ", st.session_state.extraction_service.formatted_recipe['ingredients']
            , "Directions: ", st.session_state.extraction_service.formatted_recipe['directions']
            , "Prep time: ", st.session_state.extraction_service.formatted_recipe['preptime']
            , "Cook time: ", st.session_state.extraction_service.formatted_recipe['cooktime']
            , "Total time: ", st.session_state.extraction_service.formatted_recipe['totaltime']
            , "Servings: ", st.session_state.extraction_service.formatted_recipe['servings']
            , "Calories: ", st.session_state.extraction_service.formatted_recipe['calories']
            )
if st.session_state.is_recipe == True and st.session_state.is_formatted_recipe == False:
    st.write("Raw text: ", st.session_state.extraction_service.raw_text)
    """
    },
    "POST /extract-pdf": {
        "description": """
            Upload pdf files and pass them to the extraction service. Returns a list of strings containing the extracted text from each pdf.
            Example of how to call this endpoint using JavaScript's Fetch API is not provided, as it depends heavily on the specific application and environment you're working in.
            Please refer to the Streamlit example above for an example implementation in Python as a reference.
        """,
        "example": """
        n/a
        """
    },
    "POST /spellcheck-text": {
        "description": """
            Takes in a string of text and returns a version of that text with spelling corrections. Mostly used internally but can be used for testing.
        """,
        "example": """
            ```javascript
            const textData = { text: "misspelled text" };
            fetch('http://localhost:8000/spellcheck-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(textData)
            })
            .then(response => response.json())
            .then(data => console.log(data));
            ```
            Replace 'http://localhost:8000' with the actual server URL if different.
        """
    },
    "POST /extract-text-from-txt": {
        "description": """
            Extract the text from the uploaded .txt files.
        """,
        "example": """
            Example of how to call this endpoint using JavaScript's Fetch API is not provided, as it depends heavily on the specific application and environment you're working in.
            Please refer to the Streamlit example above for an example implementation in Python as a reference.
        """,
         "example": """
        n/a
        """
    },
    "POST /extract-text-from-images": {
        "description": """
            Upload images and pass them to the extraction service. Uses the Google Vision API to extract the text from images.
            Example of how to call this endpoint using JavaScript's Fetch API is not provided, as it depends heavily on the specific application and environment you're working in.  Please refer to the Streamlit example above for an example implementation in Python as a reference.
        """,
         "example": """
        n/a
        """
    },
    "POST /format-recipe": {
        "description": """
            Pass the raw text to the extraction service. This intakes a string of text that is the raw extracted text from the extraction service and returns a formatted recipe object.
        """,
        "example": """
            ```javascript
            const rawText = "raw recipe text";
            fetch('http://localhost:8000/format-recipe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ raw_text: rawText })
            })
            .then(response => response.json())
            .then(data => console.log(data));
            ```
            Replace 'http://localhost:8000' with the actual server URL if different.
        """
    },
}

selected_endpoint = st.selectbox("Select an endpoint", options=list(endpoints.keys()))
# If the selected endpoint is "Streamlit Example", display the code as python code
if selected_endpoint == "Streamlit Example":
    st.markdown(endpoints[selected_endpoint]["description"])
    st.code(endpoints[selected_endpoint]["example"], language="python")
# Otherwise, display the code as javascript code
else:
    st.markdown(endpoints[selected_endpoint]["description"])
    st.code(endpoints[selected_endpoint]["example"], language="javascript")
