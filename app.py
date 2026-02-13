import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import date

# ---------- Database setup ----------
conn = sqlite3.connect("app.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    date TEXT,
    time TEXT,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()

# ---------- Helpers ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(email, password):
    cur.execute(
        "SELECT id FROM users WHERE email=? AND password_hash=?",
        (email, hash_password(password))
    )
    return cur.fetchone()

def create_user(email, password):
    try:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# ---------- Session ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.set_page_config(page_title="Appointment Manager")

st.title("📅 Appointment Manager")

# ---------- Authentication ----------
if st.session_state.user_id is None:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = get_user(email, password)
            if user:
                st.session_state.user_id = user[0]
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        st.subheader("Register")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if create_user(email, password):
                st.success("Account created. You can log in now.")
            else:
                st.error("Email already exists")

    st.stop()

# ---------- Logout ----------
if st.button("Logout"):
    st.session_state.user_id = None
    st.experimental_rerun()

# ---------- Add Appointment ----------
st.subheader("Add Appointment")

with st.form("appointment_form", clear_on_submit=True):
    title = st.text_input("Title")
    app_date = st.date_input("Date", min_value=date.today())
    app_time = st.time_input("Time")
    description = st.text_area("Description")
    submit = st.form_submit_button("Add")

    if submit:
        if title.strip() == "":
            st.error("Title cannot be empty")
        else:
            cur.execute(
                "INSERT INTO appointments (user_id, title, date, time, description) VALUES (?, ?, ?, ?, ?)",
                (
                    st.session_state.user_id,
                    title,
                    app_date.strftime("%d/%m/%Y"),
                    app_time.strftime("%H:%M"),
                    description
                )
            )
            conn.commit()
            st.success("Appointment added")

# ---------- Display Appointments ----------
st.subheader("Your Appointments")

cur.execute(
    "SELECT title, date, time, description FROM appointments WHERE user_id=?",
    (st.session_state.user_id,)
)
rows = cur.fetchall()

if not rows:
    st.info("No appointments yet")
else:
    df = pd.DataFrame(rows, columns=["Title", "Date", "Time", "Description"])
    df.insert(0, "No", [str(i) for i in range(1, len(df) + 1)])
    st.dataframe(df, hide_index=True)
