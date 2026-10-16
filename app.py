"""Atharva AI Receptionist — Streamlit dashboard entry point."""
import os
import streamlit as st
from dotenv import load_dotenv
from  import init_db
from backend.db.models import get_dashboard_stats, list_calls

load_dotenv()
st.set_page_config(page_title="Atharva AI Receptionist", page_icon="☎️", layout="wide")
init_db()
st.markdown("""<style>
.stApp {background:#0b1120;color:#f1f5f9} [data-testid="stMetric"]{background:#151f32;padding:16px;border-radius:12px;border:1px solid #26344d}
[data-testid="stSidebar"]{background:#101a2c} h1,h2,h3{color:#f8fafc}
</style>""", unsafe_allow_html=True)

def dashboard():
    st.title("☎️ Atharva AI Receptionist")
    st.caption("AI-assisted call handling • demo dashboard • human-first emergency escalation")
    if not os.getenv("GEMINI_API_KEY"):
        st.info("Demo mode: set GEMINI_API_KEY in .env to enable Gemini responses. Phone calls also need a telephony provider and public webhook URL.")
    stats=get_dashboard_stats()
    a,b,c,d=st.columns(4)
    a.metric("Total calls",stats["total_calls"]); b.metric("Active calls",stats["active_calls"]); c.metric("Escalations",stats["escalations"]); d.metric("Appointments",stats["appointments"])
    st.subheader("Recent call activity")
    calls=list_calls(limit=10)
    if calls:
        st.dataframe([{"ID":x["id"],"Caller":x["caller_number"],"Status":x["status"],"Emergency":x["emergency"],"Started":x["started_at"]} for x in calls],use_container_width=True,hide_index=True)
    else:
        st.write("No calls yet. Open **Live Calls** from the sidebar to create a demo call.")
    st.subheader("How to run")
    st.code("pip install -r requirements.txt\\nstreamlit run app.py", language="bash")
    st.caption("This starter project is not a medical device or emergency dispatch service. Always test with a human operator before handling real callers.")

pages=[
    st.Page(dashboard,title="Dashboard",icon="🏠",default=True),
    st.Page("frontend/pages/1_Live_Calls.py",title="Live Calls",icon="📞"),
    st.Page("frontend/pages/2_Appointments.py",title="Appointments",icon="🗓️"),
    st.Page("frontend/pages/3_Escalations.py",title="Escalations",icon="🚨"),
    st.Page("frontend/pages/4_Settings.py",title="Settings",icon="⚙️"),
]
selected=st.navigation(pages)
selected.run()
