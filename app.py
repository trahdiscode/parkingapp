import streamlit as st
import pandas as pd
from datetime import date

# ---------- Page configuration ----------
st.set_page_config(page_title="Appointment Manager", layout="centered")

st.title("📅 Simple Appointment Manager")

# ---------- Session state initialization ----------
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# ---------- Add Appointment ----------
st.subheader("Add Appointment")

with st.form("appointment_form", clear_on_submit=True):
    title = st.text_input("Title")
    app_date = st.date_input("Date", min_value=date.today())
    app_time = st.time_input("Time")
    description = st.text_area("Description")

    submit = st.form_submit_button("Add Appointment")

    if submit:
        if title.strip() == "":
            st.error("Title cannot be empty")
        else:
            st.session_state.appointments.append({
                "Title": title,
                "Date": app_date,
                "Time": app_time,
                "Description": description
            })
            st.success("Appointment added successfully")

# ---------- Display Appointments ----------
st.subheader("Appointments")

if not st.session_state.appointments:
    st.info("No appointments added yet")
else:
    df = pd.DataFrame(st.session_state.appointments)

    # Sort BEFORE formatting
    df = df.sort_values(by=["Date", "Time"]).reset_index(drop=True)

    # Format date as DD/MM/YYYY
    df["Date"] = df["Date"].apply(lambda d: d.strftime("%d/%m/%Y"))

    # Add numbering and FORCE it to string (left aligned)
    df.insert(0, "No", [str(i) for i in range(1, len(df) + 1)])

    st.dataframe(df, hide_index=True)
