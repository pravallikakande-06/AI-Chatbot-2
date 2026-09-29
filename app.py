import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

# ---------------- Load API key ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ---------------- Page config ----------------
st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    /* ---------- Page background ---------- */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #312e81 45%, #4f46e5 100%);
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    /* Hide default Streamlit header, menu and footer */
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    /* ---------- Main centered card ---------- */
    .block-container {
        max-width: 780px;
        margin: 2.5rem auto;
        padding: 2.5rem 2.5rem 1.5rem 2.5rem !important;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 28px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
    }

    /* ---------- Title ---------- */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-title {
        text-align: center;
        font-size: 1.05rem;
        font-weight: 500;
        color: #6366f1;
        margin: 0.3rem 0 0.8rem 0;
        letter-spacing: 0.5px;
    }
    .description {
        text-align: center;
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.8rem;
    }

    /* ---------- Prompt text area ---------- */
    div[data-testid="stTextArea"] label p {
        font-weight: 600;
        font-size: 1rem;
        color: #1e293b;
    }
    div[data-baseweb="textarea"] {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="textarea"]:focus-within {
        border-color: #6366f1 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.18);
    }
    div[data-baseweb="textarea"] textarea {
        background-color: transparent !important;
        color: #0f172a !important;
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        padding: 14px 16px !important;
    }
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1;
    }

    /* ---------- Generate button ---------- */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-top: 0.5rem;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.8rem 2.6rem;
        border: none;
        border-radius: 50px;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 28px rgba(79, 70, 229, 0.55);
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: #ffffff;
    }
    div.stButton > button:active {
        transform: translateY(0);
        color: #ffffff;
    }
    div.stButton > button:focus:not(:active) {
        color: #ffffff;
        border: none;
    }

    /* ---------- Spinner ---------- */
    div[data-testid="stSpinner"] {
        display: flex;
        justify-content: center;
        padding: 1rem 0;
    }
    div[data-testid="stSpinner"] p {
        color: #4f46e5 !important;
        font-weight: 600;
        font-size: 1.05rem;
    }

    /* ---------- Success / warning messages ---------- */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: none;
        font-weight: 500;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertSuccessIcon"]),
    div[data-testid="stAlert"][kind="success"] {
        background: linear-gradient(90deg, #d1fae5, #ecfdf5);
        color: #065f46;
    }
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertWarningIcon"]),
    div[data-testid="stAlert"][kind="warning"] {
        background: linear-gradient(90deg, #fef3c7, #fffbeb);
        color: #92400e;
    }

    /* ---------- AI response card ---------- */
    .st-key-response_card {
        background: #ffffff;
        border-left: 6px solid #6366f1;
        border-radius: 20px;
        padding: 1.5rem 1.8rem;
        margin-top: 1.2rem;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
    }
    .response-heading {
        font-size: 1.35rem;
        font-weight: 700;
        color: #4f46e5;
        margin: 0 0 0.8rem 0;
    }
    .st-key-response_card p,
    .st-key-response_card li {
        color: #1e293b;
        font-size: 1.02rem;
        line-height: 1.8;
    }
    .st-key-response_card h1,
    .st-key-response_card h2,
    .st-key-response_card h3 {
        color: #312e81;
    }
    .st-key-response_card code {
        background: #eef2ff;
        color: #4338ca;
        border-radius: 6px;
        padding: 2px 6px;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }

    /* ---------- Tablet ---------- */
    @media (max-width: 992px) {
        .block-container {
            max-width: 90%;
            padding: 2rem 1.8rem 1.2rem 1.8rem !important;
        }
        .main-title { font-size: 2.3rem; }
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 600px) {
        .block-container {
            max-width: 96%;
            margin: 1rem auto;
            padding: 1.4rem 1rem 1rem 1rem !important;
            border-radius: 20px;
        }
        .main-title { font-size: 1.75rem; }
        .sub-title, .description { font-size: 0.92rem; }
        div.stButton > button {
            width: 100%;
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        .st-key-response_card { padding: 1.1rem 1.1rem; }
        .response-heading { font-size: 1.15rem; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Title & description ----------------
st.markdown('<h1 class="main-title">🤖 Gemini AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Intelligent AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="description">Ask Gemini AI anything you want!</p>', unsafe_allow_html=True)

# ---------------- Prompt input ----------------
prompt = st.text_area(
    "Enter your prompt here:",
    placeholder="Explain Artifical Intelligence in simple terms."
)

# ---------------- Generate button ----------------
if st.button("Generate Response"):
    if prompt:
        with st.spinner("Gemini is thinking..."):
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
        st.success("Response generated successfully!")

        # Response card
        with st.container(key="response_card"):
            st.markdown('<p class="response-heading">🤖 Gemini Response</p>', unsafe_allow_html=True)
            st.write(response.text)
    else:
        st.warning("Please enter a prompt before generating a response.")

# ---------------- Footer ----------------
st.markdown('<div class="footer">Powered by Google Gemini + Streamlit 🤖</div>', unsafe_allow_html=True)