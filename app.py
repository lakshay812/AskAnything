import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

# ----------------------------
# Configuration
# ----------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=api_key)

# ----------------------------
# Page Settings
# ----------------------------
st.set_page_config(
    page_title="AskAnything",
    page_icon="💬",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }

    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #9CA3AF;
        margin-bottom: 30px;
    }

    .user-message {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        color: white;
    }

    .bot-message {
        background-color: #111827;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        color: white;
        border-left: 4px solid #3B82F6;
    }

    .stTextInput > div > div > input {
        background-color: #1F2937;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    model_name = st.selectbox(
        "Choose Gemini Model",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info(
        "AskAnything\n\n"
        "Powered by Google Gemini AI"
    )

# ----------------------------
# Header
# ----------------------------
st.markdown(
    "<div class='main-title'>💬 AskAnything</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Ask anything and get AI-powered answers instantly.</div>",
    unsafe_allow_html=True
)

# ----------------------------
# Display Chat History
# ----------------------------
for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        try:
            with st.spinner("Thinking..."):

                model = genai.GenerativeModel(model_name)

                response = model.generate_content(prompt)

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"

            st.error(error_msg)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_msg
                }
            )