import streamlit as st
from backend.db.session import init_db
from backend.db.models import list_appointments,book_appointment,cancel_appointment
from backend.tools.find_slots import find_slots
init_db(); st.title("🗓️ Appointments")
with st.form("book"):
    name=st.text_input("Caller name"); phone=st.text_input("Phone number",value="unknown"); service=st.selectbox("Service",["General consultation","Follow-up","Dental consultation","Other"]); when=st.text_input("Appointment date/time",placeholder="2026-10-20 10:00")
    ok=st.form_submit_button("Book demo appointment")
if ok:
    if name.strip() and when.strip(): book_appointment(name.strip(),phone.strip() or "unknown",service,when.strip()); st.success("Appointment saved in local demo database.")
    else: st.error("Enter caller name and appointment date/time.")
with st.expander("Show sample available slots (not a live calendar)"):
    service_for_slots=st.text_input("Service for slots",value="General consultation")
    st.dataframe(find_slots(service_for_slots),use_container_width=True,hide_index=True)
st.subheader("Existing appointments")
for x in list_appointments():
    with st.container(border=True):
        st.write(f"**#{x['id']} — {x['caller_name']}** | {x['service']} | {x['appointment_at']} | {x['status']}")
        if x['status']=="booked" and st.button("Cancel",key=f"cancel_{x['id']}"):
            cancel_appointment(x['id']); st.rerun()
