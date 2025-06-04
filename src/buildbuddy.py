import os
from dotenv import load_dotenv

import streamlit as st

import subprocess

def list_installed_llms_via_cli():
    try:
        result = subprocess.run(['ollama', 'ls'], capture_output=True, text=True)
        output_lines = result.stdout.strip().splitlines()
        # Skip the header row and extract only model names
        models = []
        for line in output_lines[1:]:
            # Split line by whitespace and get the first item
            parts = line.split()
            if parts:
                model_name = parts[0]
                models.append(model_name)
        return models
    except Exception:
        return []
    
load_dotenv()

skip_login = os.getenv("SKIP_LOGIN")

admin_user_name = os.getenv("ADMIN_USER_NAME")
admin_password = os.getenv("ADMIN_PASSWORD")

guest_user_name = os.getenv("GUEST_USER_NAME")
guest_password = os.getenv("GUEST_PASSWORD")
 
# --- Styling (custom CSS for soothing colors) ---
st.markdown(
    """
    <style>
    /* Set soothing background color and font styles */
    body {
        background-color: #f0f4f8; /* light soothing background */
        color: #333; /* dark text for contrast */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Style headers */
    h1, h2 {
        color: #4A90E2; /* calming blue */
    }
    /* Style input boxes and buttons */
    .stTextbox, .stButton {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    /* Style success/error messages */
    .stSuccess, .stError {
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App title with branding ---
st.markdown("> # 🛠️ BuildBuddy - Your AI Project Creator")
st.write("Welcome to **BuildBuddy**! Your friendly assistant to kickstart your Python projects effortlessly.")

# --- User authentication ---
if 'logged_in' not in st.session_state:
    if(skip_login=="True"):
        st.session_state['logged_in'] = True
        st.session_state['logged_in'] = True
        st.session_state['username'] = guest_user_name
        st.session_state['ROLE'] = 'Guest'
    else:
        st.session_state['logged_in'] = False

def login():
    st.header("Login to BuildBuddy")
    username = st.text_input("USN")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if username == guest_user_name and password == guest_password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['ROLE'] = 'Guest'
        elif username == admin_user_name and password == admin_password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['ROLE'] = 'ADMIN'
        else:
            st.error("Invalid credentials!")

# --- Main interface ---
if not st.session_state['logged_in']:
    login()
else:
    # Welcome message
    st.success(f"👋 Hello, {st.session_state['username']}! You logged in as {st.session_state['ROLE']}! Ready to build something awesome?")

    # Chat interface
    st.markdown("## 🤖 Ask BuildBuddy for help or type your project details:")
    
    # Fetch models dynamically
    llm_list = list_installed_llms_via_cli()

    if not llm_list:
        st.warning("No LLMs found. Please install models using Ollama.")
    else:
        selected_llm = st.selectbox("Choose an LLM to use:", llm_list)
        st.write(f"Selected Model: {selected_llm}")

        user_input = st.text_area("As a BuildBuddy, I can assist you with any Python project creation, How can i help you today?:")
        if st.button("Run NLP"):
            # Add your connection to Ollama here
            # For example:
            # response = ollama_api_or_cli_call(selected_llm, user_input)
            response = f"Dummy response for model {selected_llm} with input: {user_input}"
            st.write("LLM Response:")
            st.write(response)
            
            # Here, connect to Ollama LLM for processing
            # Example placeholder:
            # response = ollama_llm_process(user_input)
            # For now, just echo:
            st.info(f"BuildBuddy understands your request: {user_input}")

            # Trigger your project creation logic based on user_input
            # create_project_files(project_name or based on NLP response)

            # After creation, provide download link (placeholder)
            st.success("Your project has been set up successfully!")
            # Add download button if files are ready

    # Options to logout
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()
