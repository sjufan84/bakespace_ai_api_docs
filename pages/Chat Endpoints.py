# Docs for the chat endpoints

import streamlit as st

st.title("Chat Service API Documentation")

st.markdown("#### Overview:")
display_container = st.container()
with display_container:
    st.success("""
    The general structure of the chat service allows for the initialization of a chat with some sort of context, i.e. a recipe, pairing, etc.
    and then the ability for the user to ask a question, receive a response, and to have the chat history maintained in state throughout.
    This chat history can be accessed at any time to be used as context for the model to answer the user's question, saving to a database, etc.
    
    **Right now my thought was to use some sort of Redis store to maintain the chat history in state, but if you think there is a better / more elegant\
    solution, please let me know!**
               

    To drill down on specific endpoints with descriptions as well as
    example JavaScript implementations, please choose an endpoint below.  You can also select "Streamlit Example" to view an example implentation of the overall
    class structure in Streamlit.  **This will obviously look different with the updated session state.**  
               
    Right now a chat_session object is created that manages the session state via Redis.  Each session is initialized with a unique identifier,\
        which I think would make sense to initiate with the user's id from the existing database and then tacking on an identifier that marks each chat session, recipe, etc.
    """)

    st.markdown('**Here is an example of the class implementation in Streamlit:**')
    
endpoints = {
    "Streamlit Example": {
        "description": """
    This is an example of the class implementation in Streamlit.  The class is initialized in the session state and then the user can
    initialize the chat with some context, ask a question, and receive a response.  The chat history is maintained in state and can be
    accessed at any time.
    """,
        "code_example": """
    class ChatMessage:
        def __init__(self, role, content):  
            self.role = role
            self.content = content
    class ChatService:
        def __init__(self):
            self.baseUrl = "http://localhost:8000"  # Replace with your FastAPI server's URL
            self.chat_history = []
            self.initial_message = {}

        
        # Initialize the chat @TODO: convert the initial message and the chat history to a dictionary with the same keys to be iterated over
        # For context to feed the model when answering questions
        def initialize_chat(self, context):
            response = requests.post(f"{self.baseUrl}/initialize_chat", params={"context": context})
            data = response.json()
            st.session_state.initial_message = data
            st.session_state.chat_service.chat_history.append(data)
            return st.session_state.initial_message
        
        def add_user_message(self, message):
            response = requests.post(f"{self.baseUrl}/add_user_message", params={"message": message})
            data = response.json()
            # Convert the response to a Message object
            message = ChatMessage(role = "user", content = data[0]['data']['content'])

            # Append the message to the chat history
            st.session_state.chat_service.chat_history.append({"role": message.role, "content": message.content})

            # Return the chat history
            return st.session_state.chat_service.chat_history

        def add_chef_message(self, message):
            response = requests.post(f"{self.baseUrl}/add_chef_message", params={"message": message})
            data = response.json()        
            # Convert the response to a Message object
            message = ChatMessage(role = "ai", content = data[0]['data']['content'])
            # Append the message to the chat history
            st.session_state.chat_service.chat_history.append({"role": message.role, "content": message.content})
            # Return the chat history
            return st.session_state.chat_service.chat_history
        
        def get_chef_response(self, question, chat_messages):
            data = {"question": question, "chat_messages": chat_messages}
            response = requests.post(f"{self.baseUrl}/get_chef_response", json=data)
            data = response.json()
            return data


        def clear_chat_history(self):
            self.chat_history = []

    
    """,
    },
    "POST /initialize_chat": {
        "description": """
    Initialize the chat with the initial context. The context could be a recipe to reference or some other
    information that we want to provide to the model to start the conversation.  This will return the appropriately 
    formatted message to the frontend to display to the user as a json object with the role and content keys.
    """,
        "code_example": """
    fetch('http://localhost:8000/initialize_chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context: 'context_string_here' })
    })
    .then(response => response.json())
    .then(data => console.log(data));""",
    },
    "POST /add_user_message": {
        "description": """
        
    Add a user message to the chat. This will return the chat history to the frontend as a json object
    that can be parsed and added to the chat history.
    
    """,
        "code_example": """
        fetch('http://localhost:8000/add_user_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'user_message_here' })
    })
    .then(response => response.json())
    .then(data => console.log(data));""",
    },

    "POST /add_chef_message": {
        "description": """
    Add a chef message to the chat. This will return the chat history to the frontend as a json object
    that can be parsed and added to the chat history.
    """,
        "code_example": """
        fetch('http://localhost:8000/add_chef_message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'chef_message_here' })
})
.then(response => response.json())
.then(data => console.log(data));

    """,
    },
    "POST /get_chef_response": {
        "description": """
    Get a response from the chef from a user question. This will be the primary function that we use to get a response
    as it will automatically add the user question and chef response to the chat history automatically. It takes in
    the user question and the chat history formatted as a dictionary or list of dictionaries with the keys "role" and "content". 
    The data is parsed based on the ChefRequest object, which is a list of ChatMessage objects. This will return the chef response 
    to the frontend as a string and update the chat history.
    """,
        "code_example": """
        fetch('http://localhost:8000/get_chef_response', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        question: 'user_question_here',
        chat_messages: [
            { role: 'role_here', content: 'content_here' },
            // other messages...
        ]
    })
})
.then(response => response.json())
.then(data => console.log(data));
    """,
    },

    "GET /view_chat_history": {
        "description": """
    Create a route to view the chat history. This takes in the chat service and returns the chat history as a json object.
    """,
        "code_example": """
        fetch('http://localhost:8000/view_chat_history', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
})
.then(response => response.json())
.then(data => console.log(data));
    """,
    },
    "DELETE /clear_chat_history": {
        "description": """
    Create a route to clear the chat history.
    """,
        "code_example": """
        fetch('http://localhost:8000/clear_chat_history', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
})
.then(response => response.json())
.then(data => console.log(data));
    """,
    },
}

selected_endpoint = st.selectbox("Select an endpoint:", list(endpoints.keys()))
st.markdown("**Description:**")
st.markdown(endpoints[selected_endpoint]["description"])
# Check to see if the selected endpoint is the Streamlit Example.  If so the code will be displayed as python.
# Otherwise, it will be displayed as javascript.
if selected_endpoint == "Streamlit Example":
    st.markdown("**Code Example:**")
    st.code(endpoints[selected_endpoint]["code_example"], language="python")
else:
    st.markdown("**Code Example:**")
    st.code(endpoints[selected_endpoint]["code_example"], language="javascript")
