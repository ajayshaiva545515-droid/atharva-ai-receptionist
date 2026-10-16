import streamlit as st
from backend.db.session import init_db
from backend.db.models import create_call,list_calls
from backend.services.conversation import reply_to_caller
from backend.services.handoff import queue_handoff
from frontend.components.call_card import render_call_card
init_db(); st.title("📞 Live Calls / Demo Simulator")
st.warning("This page simulates a call using typed text. It does not connect to a real telephone line.")
with st.form("demo_call"):
    number=st.text_input("Caller phone number",value="+91 90000 00000")
    name=st.text_input("Caller name",value="Demo caller")
    message=st.text_area("What did the caller say?",placeholder="Example: I want to book an appointment")
    submitted=st.form_submit_button("Process demo call")
if submitted and message.strip():
    result=reply_to_caller(message)
    call=create_call(number,name,message,result["reply"],result["emergency"],"completed")
    if result["handoff"]: queue_handoff(result.get("reason") or "AI requested human handoff",call["id"])
    st.success("Demo call saved")
    st.markdown("**AI response**"); st.write(result["reply"]); st.caption("AI provider: "+result["provider"])
    if result["handoff"]: st.error("Human handoff queued. A staff member must act on the queue.")
for call in list_calls(30): render_call_card(call)
