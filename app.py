import streamlit as st
import google.generativeai as genai

load_dotenv()
# 🔐 Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 🌟 Streamlit UI settings
st.set_page_config(page_title="Gemini Q&A", layout="centered")

# 🌑 Custom CSS for dark theme
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
        }
        .stApp {
            background-color: #000000;
        }
        label, .stTextInput > div > label {
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: bold !important;
        }
        input, textarea {
            color: white !important;
            background-color: #1c1c1c !important;
        }
        input::placeholder {
            color: #888888 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 App Title
st.markdown("<h1 style='text-align: center; color: white;'>💬 AskAnything</h1>", unsafe_allow_html=True)

# 📥 User input
question = st.text_input("How can I help you?", placeholder="Type your question here...", label_visibility="visible")

if question:
    with st.spinner("Thinking..."):
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(question)
            st.markdown("---")
            st.markdown(f"### 📘 Answer:\n{response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
