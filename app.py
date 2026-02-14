import streamlit as st
import sqlite3
import hashlib
import time
from datetime import datetime, date, timedelta

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Parking Slot Booking", layout="wide")

# ---------- DATABASE ----------
conn = sqlite3.connect("parking_v4.db", check_same_thread=False)
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
    slot_number TEXT NOT NULL,
    start_datetime TEXT NOT NULL,
    end_datetime TEXT NOT NULL
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

# ---------- SESSION ----------
for k in ("user_id", "vehicle_number"):
    if k not in st.session_state:
        st.session_state[k] = None

if "error_message" not in st.session_state:
    st.session_state.error_message = None

if "error_time" not in st.session_state:
    st.session_state.error_time = None

# ---------- AUTH ----------
if st.session_state.user_id is None:
    st.title("🅿 Parking Slot Booking")

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

# ---------- HEADER ----------
st.markdown("## Parking Dashboard")
st.divider()

# Show persistent error (7 seconds)
if st.session_state.error_message:
    elapsed = time.time() - st.session_state.error_time
    if elapsed < 7:
        st.error(st.session_state.error_message)
    else:
        st.session_state.error_message = None
        st.session_state.error_time = None

# ---------- SLOT LIST ----------
slots = [f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 11)]

now_dt = datetime.now()
now_str = now_dt.strftime("%Y-%m-%d %H:%M")

# ---------- ACTIVE BOOKING QUERY ----------
cur.execute("""
SELECT slot_number, start_datetime, end_datetime
FROM bookings
WHERE user_id=? AND ? BETWEEN start_datetime AND end_datetime
""", (st.session_state.user_id, now_str))

active = cur.fetchone()

# ---------- OCCUPIED SLOTS ----------
cur.execute("""
SELECT slot_number FROM bookings
WHERE ? BETWEEN start_datetime AND end_datetime
""", (now_str,))

occupied = {r[0] for r in cur.fetchall()}
available_count = len(slots) - len(occupied)

# ---------- DASHBOARD COLUMNS ----------
col1, col2 = st.columns([2, 1])

# Left Column (Active Booking)
with col1:
    if active:
        slot, start, end = active
        end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
        remaining = end_time - now_dt

        st.success(f"""
🚗 **Currently Parked**

**Slot:** {slot}  
**Until:** {end_time.strftime("%H:%M")}  
**Time Remaining:** {str(remaining).split('.')[0]}
""")

        if st.button("Cancel Booking", use_container_width=True):
            cur.execute("""
            DELETE FROM bookings
            WHERE user_id=? AND slot_number=? AND start_datetime=? AND end_datetime=?
            """, (
                st.session_state.user_id,
                slot,
                start,
                end
            ))
            conn.commit()
            st.success("Booking cancelled successfully.")
            st.rerun()
    else:
        st.info("🟢 No active parking session")

# Right Column (Metric)
with col2:
    st.metric("Available Slots", available_count)

st.divider()

# ---------- LIVE GRID ----------
st.subheader("Live Slot Overview")

grid = "<div style='display:grid;grid-template-columns:repeat(10,1fr);gap:10px;'>"
for s in slots:
    if s in occupied:
        color = "#ef4444"
        label = "BUSY"
    else:
        color = "#22c55e"
        label = "FREE"

    grid += f"<div style='padding:12px;text-align:center;background:{color};border-radius:6px;color:white;font-weight:600;'>{s}<br><small>{label}</small></div>"

grid += "</div>"
st.markdown(grid, unsafe_allow_html=True)

st.divider()

# ---------- BOOK SLOT ----------
st.subheader("Book Parking")

booking_date = st.date_input("Date", min_value=date.today())
entry_time = st.time_input("Entry Time", value=datetime.now().replace(second=0, microsecond=0).time())
exit_time = st.time_input("Exit Time")

start_dt = datetime.combine(booking_date, entry_time)
end_dt = datetime.combine(booking_date, exit_time)

if exit_time <= entry_time:
    end_dt += timedelta(days=1)
    st.caption("Overnight booking")

cur.execute("""
SELECT slot_number FROM bookings
WHERE NOT (end_datetime <= ? OR start_datetime >= ?)
""", (
    start_dt.strftime("%Y-%m-%d %H:%M"),
    end_dt.strftime("%Y-%m-%d %H:%M")
))

blocked = {r[0] for r in cur.fetchall()}
available = [s for s in slots if s not in blocked]

if available:
    slot = st.selectbox("Available Slots", available)
else:
    st.error("No slots available")
    slot = None

if st.button("Confirm Booking", use_container_width=True):

    if slot is None:
        st.stop()

    cur.execute("""
    SELECT id FROM bookings
    WHERE user_id=?
    AND NOT (end_datetime <= ? OR start_datetime >= ?)
    """, (
        st.session_state.user_id,
        start_dt.strftime("%Y-%m-%d %H:%M"),
        end_dt.strftime("%Y-%m-%d %H:%M")
    ))

    if cur.fetchone():
        st.session_state.error_message = "You already have a booking during this time."
        st.session_state.error_time = time.time()
    else:
        cur.execute("""
        INSERT INTO bookings (user_id, slot_number, start_datetime, end_datetime)
        VALUES (?, ?, ?, ?)
        """, (
            st.session_state.user_id,
            slot,
            start_dt.strftime("%Y-%m-%d %H:%M"),
            end_dt.strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        st.success(f"Slot {slot} booked successfully")
        st.rerun()
