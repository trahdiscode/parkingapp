import streamlit as st

# ---------- PAGE CONFIG (MUST BE FIRST) ----------
st.set_page_config(page_title="Parking Slot Booking", layout="centered")

from streamlit_autorefresh import st_autorefresh
import sqlite3
import hashlib
import pandas as pd
from datetime import date, datetime

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=5000, key="refresh")

st.title("🅿️ College Parking Slot Booking System")

# ---------- DARK MODE CSS ----------
st.markdown("""
<style>
.stApp {
    background-color: #0f1117;
    color: #e6e6e6;
    font-family: "Segoe UI", sans-serif;
}
section[data-testid="stVerticalBlock"] > div {
    background-color: #161b22;
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 16px;
}
.slot-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    max-width: 600px;
}
.slot-box {
    text-align: center;
    padding: 14px 0;
    border-radius: 6px;
    font-weight: 700;
}
.free { background-color: #238636; }
.busy { background-color: #da3633; }
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE (NEW VERSION) ----------
conn = sqlite3.connect("parking_v3.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    vehicle_number TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    parking_date TEXT NOT NULL,
    entry_time TEXT NOT NULL,
    exit_time TEXT NOT NULL,
    slot_number TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()

# ---------- HELPERS ----------
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_user(u, p):
    cur.execute(
        "SELECT id, vehicle_number FROM users WHERE username=? AND password_hash=?",
        (u, hash_password(p))
    )
    return cur.fetchone()

def create_user(u, p):
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (u, hash_password(p))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# ---------- SESSION STATE ----------
for key in ["user_id", "vehicle_number"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------- AUTH ----------
if st.session_state.user_id is None:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            user = get_user(u, p)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.vehicle_number = user[1]
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")
        if st.button("Register"):
            if create_user(u, p):
                st.success("Account created. Login now.")
            else:
                st.error("Username already exists")

    st.stop()

# ---------- LOGOUT ----------
if st.button("Logout"):
    st.session_state.user_id = None
    st.session_state.vehicle_number = None
    st.rerun()

# ---------- VEHICLE NUMBER ----------
if st.session_state.vehicle_number is None:
    v = st.text_input("Enter Vehicle Number (one time)")
    if st.button("Save Vehicle Number"):
        cur.execute(
            "UPDATE users SET vehicle_number=? WHERE id=?",
            (v.upper(), st.session_state.user_id)
        )
        conn.commit()
        st.session_state.vehicle_number = v.upper()
        st.rerun()
    st.stop()

# ---------- SLOTS ----------
slots = [f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 11)]

# ---------- REAL-TIME AVAILABILITY ----------
st.subheader("📊 Live Slot Availability (Now)")

now = datetime.now()
today = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M")

cur.execute("""
SELECT slot_number FROM bookings
WHERE parking_date=?
AND ? BETWEEN entry_time AND exit_time
""", (today, current_time))

occupied = {r[0] for r in cur.fetchall()}

grid = "<div class='slot-grid'>"
for s in slots:
    cls = "busy" if s in occupied else "free"
    grid += f"<div class='slot-box {cls}'>{s}</div>"
grid += "</div>"

st.markdown(grid, unsafe_allow_html=True)

# ---------- BOOK SLOT ----------
st.subheader("Book Parking Slot")

with st.form("book"):
    st.text_input("Vehicle Number", value=st.session_state.vehicle_number, disabled=True)
    d = st.date_input("Date", min_value=date.today())
    entry = st.time_input("Entry Time", value=datetime.now().time())
    exit_ = st.time_input("Exit Time")
    s = st.selectbox("Slot", slots)
    ok = st.form_submit_button("Book")

    if ok:
        if exit_ <= entry:
            st.error("Exit time must be after entry time")
        else:
            cur.execute("""
            SELECT 1 FROM bookings
            WHERE parking_date=?
            AND slot_number=?
            AND NOT (exit_time <= ? OR entry_time >= ?)
            """, (
                d.strftime("%d/%m/%Y"),
                s,
                entry.strftime("%H:%M"),
                exit_.strftime("%H:%M")
            ))

            if cur.fetchone():
                st.error("Slot is occupied during this time range")
            else:
                cur.execute("""
                INSERT INTO bookings (user_id, parking_date, entry_time, exit_time, slot_number)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    d.strftime("%d/%m/%Y"),
                    entry.strftime("%H:%M"),
                    exit_.strftime("%H:%M"),
                    s
                ))
                conn.commit()
                st.success("Slot booked successfully")
