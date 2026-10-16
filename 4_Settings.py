import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv(); st.title("⚙️ Settings")
st.write("Environment settings are read from `.env`. Never paste secrets into screenshots or commit them to GitHub.")
for key,desc in [("GEMINI_API_KEY","Google Gemini API key"),("GEMINI_MODEL","Gemini model name"),("DATABASE_URL","Database connection string"),("PUBLIC_BASE_URL","Public HTTPS URL for telephony webhooks"),("TWILIO_PHONE_NUMBER","Phone number provisioned by telephony provider"),("HUMAN_HANDOFF_NUMBER","Human operator phone in E.164 format")]:
    value=os.getenv(key,"")
    if "KEY" in key or "TOKEN" in key: value="Configured" if value else "Not configured"
    st.write(f"**{key}** — {desc}: `{value or 'Not configured'}`")
st.info("To enable real calls, implement and test the provider webhook, speech recognition, speech synthesis, call transfer, authentication, consent, and monitoring. This starter does not claim to perform live phone transfers.")
