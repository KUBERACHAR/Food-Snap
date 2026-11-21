from google import genai
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=GEMINI_API_KEY)

genai_client = get_genai_client()
MODEL_NAME = "gemini-3.8-flash"

# Onboarding
if 'onboarded' not in st.session_state:
    st.title("I'm MacroSnap 🥗")
    st.caption("Snap it, track it, know it")

with st.form("onboarding_form"):
    name = st.text_input("Your name")
    whatsapp_number = st. text_input("WhatsApp number (with country code)", placeholder="+91XXXXXXXXXX", help="This is the number MacroSnap will text")

    submited = st.form_submit_button("Let's go!")

if submited:
    if not name.strip() or not whatsapp_number.strip():
        st.error("Please fill in both fields.")
    else:
        st.session_state.name = name.strip()
        st.session_state.whatsapp_number = whatsapp_number.strip()
        st.success("Onboarding complete! You can now start using MacroSnap.")

        # Activating AI 
        st.session_state.chat = genai_client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(system_instructions=SYSTEM_PROMPT),
        )
        st.session_state.messages = []
        st.session_state.onboarded = True
        st.rerun()
st.stop()

# Chat interface
header_col, btn_col = st.columns([5, 2], vertical_alignment="center")
with header_col:
    st.title("MacroSnap 🥗")

# with button_col:
#     send_disabled = len(st.session_state.messages) <= 2
#     if st.button("📤 Send to WhatsApp", disabled=send_disabled, use_container_width=True):
#         with st.spinner("Summarizing your day..."):
#             summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
#         success, info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary)
#         if success:
#             st.success("Sent! Check your WhatsApp 📲")
#         else:
#             st.error(f"Couldn't send that: {info}")
