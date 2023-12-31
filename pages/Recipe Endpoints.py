import streamlit as st

st.title("Recipe Service API Documentation")

st.markdown("#### Overview:")
st.success("""
    The general structure of the recipe service allows for the generation of a recipe based on some specifications i.e. restrictions, preferences, etc.
    The current implementation is that all the specifications are passed as a single string, but we can certainly revisit this if needed.  This utilizes a 
    Recipe class that is the structure of the returned JSON object, and the RecipeService class that is the structure of the API itself.  To chat about a recipe,
    the context should be set as recipe and the recipe will be passed to initialize the chat for context.  The recipe will be held in state using
    Redis or something similar and tied to the user's id.
""")

endpoints = {
    "POST /generate_recipe": {
        "description": """
            This is the core recipe generating endpoint. It takes in a string, 'specifications', which can be any preferences, restrictions, etc. concatenated into a single string. It can be in natural language as the model will be able to parse it.
            The generated recipe is returned as a JSON object, which conforms to the 'Recipe' model.
        """,
        "code_example": """
            Here is an example of how to call this endpoint using JavaScript's Fetch API:
            ```javascript
            const specifications = "vegetarian pizza with extra cheese";
            fetch('http://localhost:8000/generate_recipe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ specifications })
            })
            .then(response => response.json())
            .then(data => console.log(data));
            ```
            Replace 'http://localhost:8000' with the actual server URL if different.
        """
    },
    "GET /get_recipe_by name": {
        "description": """
        This endpoint allows you to retrieve the recipe by name.  It accesses the recipe via the Redis store.
        """,
        "code_example": """
        """
    },
    "POST /save_recipe_by_name": {
        "description": """
        Similar to the get_recipe_by_name endpoint, this endpoint allows you to save a recipe by name to the Redis store.
        """,
        "code_example": """
        """
    },
    "DELETE /delete_recipe_by_name": {
        "description": """
        Similar to the get_recipe_by_name endpoint, this endpoint allows you to delete a recipe by name from the Redis store.
        """,
        "code_example": """
        """
    },
    "GET /view_recipe_history": {
        "description": """
        Pulls up the current session's recipes for the user.  This should be stored as multiple JSON recipe objects in the Redis store.
        """,
        "code_example": """
        """
    },
    "DELETE /clear_recipe_history": {
        "description": """
        Clears the current session's recipe history.
        """,
        "code_example": """
        """
    },
    "POST /save_recipe_history": {
        "description": """
        Saves the current session's recipe history to the Redis store.
        """,
        "code_example": """
        """
    },
    "Streamlit Example": {
        "description": """
        This is an example implementation of the RecipeService and Recipe models in Streamlit for reference.
        """,
        "code_example": """
        class Recipe:
        def __init__(self, name, ingredients, directions, servings, cooktime, preptime, calories, recipe_text):
            self.name = name
            self.ingredients = ingredients
            self.directions = directions
            self.servings = servings
            self.cooktime = cooktime
            self.preptime = preptime
            self.calories = calories
            self.recipe_text = recipe_text

    class RecipeService:
        def __init__(self):
            self.baseUrl = "http://localhost:8000"
            self.recipe = Recipe("", [], [], 0, 0, 0, 0, "")

        def get_recipe(self, specifications):
            response = requests.post(f"{self.baseUrl}/generate_recipe", params={"specifications": specifications})
            data = response.json()
            # Populate the recipe service with the recipe data
            self.recipe.name = data["name"]
            self.recipe.ingredients = data["ingredients"]
            self.recipe.directions = data["directions"]
            self.recipe.servings = data["servings"]
            self.recipe.cooktime = data["cooktime"]
            self.recipe.preptime = data["preptime"]
            self.recipe.calories = data["calories"]
            self.recipe.recipe_text = data["recipe_text"]

            return data
        """
    }
}

selected_endpoint = st.selectbox("Select an endpoint", options=list(endpoints.keys()))
st.markdown(endpoints[selected_endpoint]["description"])
# if the Streamlit Example is selected, display the code example as python code
if selected_endpoint == "Streamlit Example":
    st.code(endpoints[selected_endpoint]["code_example"], language="python")
else:
    st.code(endpoints[selected_endpoint]["code_example"], language="javascript")