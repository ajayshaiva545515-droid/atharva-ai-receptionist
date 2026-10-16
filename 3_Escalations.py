import streamlit as st
from backend.db.session import init_db
from backend.db.models import list_escalations,update_escalation
from backend.services.handoff import queue_handoff
init_db(); st.title("🚨 Escalations & Human Handover")
st.caption("This is a task queue, not an automatic telephone transfer. Connect a telephony provider to bridge calls to staff.")
with st.form("manual_escalation"):
    reason=st.text_area("Reason for handover",placeholder="Caller asked for a human / emergency detected")
    call_id=st.number_input("Related call ID (optional; 0 means none)",min_value=0,step=1,value=0)
    submit=st.form_submit_button("Create handover task")
if submit and reason.strip(): queue_handoff(reason.strip(),int(call_id) or None); st.success("Handover task added.")
for item in list_escalations():
    with st.container(border=True):
        st.write(f"**Escalation #{item['id']}** · Call: {item['call_id'] or '—'} · {item['status']}")
        st.write(item['reason']); st.caption(item['created_at'])
        c1,c2,c3=st.columns(3)
        if item['status']!="pending" and c1.button("Set pending",key=f"p{item['id']}"): update_escalation(item['id'],"pending");st.rerun()
        if item['status']!="assigned" and c2.button("Assign to staff",key=f"a{item['id']}"): update_escalation(item['id'],"assigned");st.rerun()
        if item['status']!="resolved" and c3.button("Resolve",key=f"r{item['id']}"): update_escalation(item['id'],"resolved");st.rerun()
