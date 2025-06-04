import os
from dotenv import load_dotenv
import streamlit as st
import subprocess

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Function to capture user inputs and respond with local selected LLM
def ollama_api_response(model_name: str, question: str) -> str | None:
    """
    Connects to a local Ollama LLM, sends a question, and returns the response.

    Args:
        model_name: The name of the Ollama model to use (e.g., "llama3", "mistral").
                    This model must be downloaded and available locally via Ollama.
        question: The question to ask the LLM.

    Returns:
        The LLM's response as a string, or None if an error occurs.
    """
    try:
        # Initialize the Ollama LLM
        # By default, it connects to http://localhost:11434
        llm = Ollama(model=model_name)

        # Create a simple prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
             As a seasoned Python Software Architect and Developer, your mission is to design and implement robust, modular, and maintainable Python programs. Every code snippet or application you generate must strictly follow PEP 8 style guidelines, incorporate clear variable and function naming, and utilize docstrings for comprehensive documentation. You are expected to design for readability, reusability, and efficient resource management. Implement robust error handling (try-except blocks) and consider dependency management. You are adept at creating solutions involving REST APIs, database interactions, data manipulation, and cloud integrations, utilizing libraries such as 'requests', 'SQLAlchemy', 'FastAPI', 'Pandas', and 'NumPy' where appropriate.
            IMPORTANT: If a user requests code or solutions in a programming language other than Python (e.g., C#, C++, .NET, Java, JavaScript, Go, etc.), you must politely inform them that your expertise is focused on Python. Then, ask if they would like to proceed with a Python-based solution for their request instead.
             """),
            ("user", "{question}")
        ])

        # Create a chain to process the input, pass to LLM, and parse output
        chain = prompt | llm | StrOutputParser()

        # Invoke the chain with the question
        print(f"Asking {model_name}...")
        response = chain.invoke({"question": question})

        return response.strip()  # .strip() to remove leading/trailing whitespace

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure Ollama is running and the model is downloaded locally.")
        return None


def ollama_llm_response_cli(model_name, prompt):
    try:
        # Run the ollama CLI command
        result = subprocess.run(
            ['ollama', 'run', model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30  # seconds
        )
        # The output should be the response
        response = result.stdout.strip()
        return response
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"

# Function to list installed LLMs via Ollama CLI


def list_installed_llms_via_cli():
    try:
        result = subprocess.run(
            ['ollama', 'ls'], capture_output=True, text=True)
        output_lines = result.stdout.strip().splitlines()
        models = []
        for line in output_lines[1:]:
            parts = line.split()
            if parts:
                model_name = parts[0]
                models.append(model_name)
        return models
    except Exception:
        return []


load_dotenv()

# Load credentials and configs
skip_login = os.getenv("SKIP_LOGIN", "False")
admin_user_name = os.getenv("ADMIN_USER_NAME", "Guest")
admin_password = os.getenv("ADMIN_PASSWORD", "Guest123$")
guest_user_name = os.getenv("GUEST_USER_NAME", "Guest")
guest_password = os.getenv("GUEST_PASSWORD", "Guest123$")

# --- Styling (custom CSS for soothing colors) ---
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
        color: #333;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1, h2 {
        color: #4A90E2;
    }
    .stTextInput {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stButton {
        border-radius: 8px;
        padding: 10px;
    }
    .stMarkdown {
        margin: 0 0 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App title ---
st.markdown("> # 🛠️ BuildBuddy - Your AI Project Builder")
st.write("Welcome! BuildBuddy helps you kickstart Python projects seamlessly.")

if 'input_counter' not in st.session_state:
    st.session_state['input_counter'] = 0

# --- Authentication & Login ---
if 'logged_in' not in st.session_state:
    if skip_login.lower() == "true":
        st.session_state['logged_in'] = True
        st.session_state['username'] = guest_user_name
        st.session_state['ROLE'] = 'Guest'
    else:
        st.session_state['logged_in'] = False


def login():
    st.header("Login to BuildBuddy")
    if not all([admin_user_name, admin_password, guest_user_name, guest_password]):
        st.error("Some credentials are missing in environment variables.")
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


if not st.session_state['logged_in']:
    login()
    st.stop()

# --- Main Logged-in Area ---
# Sidebar for Logout Button
with st.sidebar:
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# Fetch and display LLMs in sidebar
llm_list = list_installed_llms_via_cli()

st.sidebar.markdown("## Available LLMs")

if llm_list:
    selected_llm = st.sidebar.selectbox("Available Models", llm_list)
else:
    selected_llm = None
    st.sidebar.write("No models found.")

# Welcome message
st.success(
    f"👋 Hello, {st.session_state['username']}! You logged in as {st.session_state['ROLE']}.")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Fetch available LLMs
llm_list = list_installed_llms_via_cli()

# Chat history display
st.markdown("### Conversation")
chat_container = st.container()
with chat_container:
    for role, msg in st.session_state['messages']:
        if role == 'user':
            # User message with icon/emojis
            st.markdown(f"> 🧑 **You:** {msg}")
        else:
            # Bot message with icon/emojis
            st.markdown(f"> 🤖 **BuildBuddy:** {msg}")

# User input area
st.markdown("### Ask BuildBuddy")
input_key = f"chat_input_{st.session_state['input_counter']}"
user_input = st.text_input("Type your message here:", key=input_key)

# Send button (placed next to input)
if st.button("Send") and user_input:
    # Save user message
    st.session_state['messages'].append(('user', user_input))

    # Add this response to the chat history
    response = ollama_api_response(selected_llm, user_input)

    # Append the response to chat history
    st.session_state['messages'].append(('bot', response))

    st.session_state['input_counter'] += 1

    # Reset input box
    st.rerun()
