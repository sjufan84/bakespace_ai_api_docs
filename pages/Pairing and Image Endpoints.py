import streamlit as st

st.subheader("Image Generation and Pairings API Documentation")

st.success("""
At a very basic level, the image generation endpoint takes in a prompt as a string and then generates an image url based on that prompt
    utilizing StabilityAI's API.  Generally I have been using the recipe name as the initial prompt, but you can use any prompt you want.
        The pairing endpoint takes in a recipe text and a pairing type and returns a pairing object.  The pairing object contains the pairing text
        as well as the reasoning behind the pairing.  The pairing type can be any general type of pairing, such as wine,
        beer, cocktail, etc.  The pairing endpoint passes these parameters to the LLM API and returns the results.  **My thought is this is tied
        to a recipe id or perhaps to a separate line in the database, and the session state will need to be managed on these as well.**
           
        To view more specifics about the endpoints as well as code examples in javascript, please see below.  You can also view an example
        Streamlit implementation for reference.
""")
endpoints = {
    "Streamlit Example": {
        "description": """
            This is a Streamlit example of how to implement the endpoints.  You can use this as a reference for how to implement the endpoints in your own code.
        """,
        "example": """
        class Pairing:
    # Pairing implementation
    def __init__(self, pairing_text, pairing_reason):
        self.pairing_text = pairing_text
        self.pairing_reason = pairing_reason
    
    class PairingService:
    def __init__(self):
        self.baseUrl = "http://localhost:8000"
        self.pairing_type = ""
        self.recipe = ""
        self.pairing = Pairing("", "")

    def get_pairing(self, pairing_type, recipe_text):
        response = requests.post(f"{self.baseUrl}/generate_pairing", params={"pairing_type": pairing_type, "recipe_text": recipe_text})
        data = response.json()
        # Populate the pairing service with the pairing data
        self.pairing.pairing_text = data['pairing_text']
        self.pairing.pairing_reason = data['pairing_reason']
        return data

    # Image Generation implementation
    class ImageService:
    def __init__(self):
        self.baseUrl = "http://localhost:8000"
        self.prompt = ""
        self.image_url = ""

    def get_image(self, prompt):
        response = requests.post(f"{self.baseUrl}/generate_image_url", params={"prompt": prompt})
        data = response.json()
        return data
        """,
    },
    "POST /generate_image_url": {
        "description": """
            Takes in a string prompt and returns an image url. The image url is generated based on the provided prompt that is passed to the StabilityAI API.
        """,
        "example": """
            ```javascript
            const prompt = "a scenic mountain view";
            fetch('http://localhost:8000/generate_image_url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            })
            .then(response => response.json())
            .then(data => console.log(data));
            ```
            Replace 'http://localhost:8000' with the actual server URL if different.
        """
    },
    "POST /generate_pairing": {
        "description": """
            Takes in a recipe text and pairing type as input and returns a Pairing object. The Pairing object includes details about a recommended pairing based on the provided recipe and pairing type.
        """,
        "example": """
            ```javascript
            const recipeText = "pasta with tomato sauce";
            const pairingType = "wine";
            fetch('http://localhost:8000/generate_pairing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ recipe_text: recipeText, pairing_type: pairingType })
            })
            .then(response => response.json())
            .then(data => console.log(data));
            ```
            Replace 'http://localhost:8000' with the actual server URL if different.
        """
    },
}

selected_endpoint = st.selectbox("Select an endpoint", options=list(endpoints.keys()))
# If the selected endpoint is "Streamlit Example", then display the code snippet in python
st.markdown(endpoints[selected_endpoint]["description"])
if selected_endpoint == "Streamlit Example":
    st.code(endpoints[selected_endpoint]["example"], language="python")
else:
    st.code(endpoints[selected_endpoint]["example"], language="javascript")