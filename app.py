import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Parking Slot Booking", layout="wide")

from streamlit_autorefresh import st_autorefresh
import sqlite3
import hashlib
from datetime import datetime, date, timedelta

# ---------- AUTO REFRESH ----------
# st_autorefresh(interval=5000, key="refresh") # Commenting out for cleaner testing, uncomment if needed

# ---------- HIGHLY PROFESSIONAL UI STYLESHEET ----------
st.markdown("""
<style>
/* Import Google Font: Inter - A clean, professional font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* --- Root Variables for a Cohesive Design System --- */
:root {
    --color-bg: #111317;
    --color-bg-secondary: #1A1D23;
    --color-text-primary: #E0E6F1;
    --color-text-secondary: #A0AEC0;
    --color-border: #2A2F3B;
    --color-accent: #367BFA; /* Professional Blue */
    --color-accent-hover: #2F6AD5;
    --color-green: #28a745;
    --color-red: #dc3545;
    
    --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --border-radius: 8px;
}

/* --- Base App Styling --- */
.stApp {
    background-color: var(--color-bg);
    color: var(--color-text-primary);
    font-family: var(--font-family-sans);
}

/* --- Custom Title and Header Classes --- */
.main-title {
    font-family: var(--font-family-sans);
    font-weight: 700;
    font-size: 2.5rem; /* Large, but not comical */
    color: var(--color-text-primary);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--color-border);
}

.dashboard-title {
    font-family: var(--font-family-sans);
    font-weight: 600;
    font-size: 1.8rem;
    color: var(--color-text-secondary);
    margin-top: 3rem;
    margin-bottom: 1.5rem;
}

/* Override default Streamlit subheader */
h3 {
    font-family: var(--font-family-sans);
    font-weight: 600;
    font-size: 1.25rem;
    color: var(--color-text-primary);
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}

/* --- UI Elements: Inputs, Buttons, Selects --- */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
    background-color: var(--color-bg-secondary);
    color: var(--color-text-primary);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius);
    padding: 12px 14px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus,
.stTimeInput > div > div > input:focus {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 2px rgba(54, 123, 250, 0.3);
    outline: none;
}

.stButton > button {
    font-family: var(--font-family-sans);
    font-weight: 600;
    background-color: var(--color-bg-secondary);
    color: var(--color-text-primary);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius);
    padding: 12px 24px;
    transition: background-color 0.2s, border-color 0.2s;
}
.stButton > button:hover {
    background-color: #2A2F3B;
    border-color: var(--color-text-secondary);
}
.stButton > button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(54, 123, 250, 0.3);
    border-color: var(--color-accent);
}

/* Primary Button Style */
.stButton > button.primary {
    background-color: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}
.stButton > button.primary:hover {
    background-color: var(--color-accent-hover);
    border-color: var(--color-accent-hover);
}

/* --- Modern Card Design --- */
.card {
    background-color: var(--color-bg-secondary);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    height: 100%;
}

/* --- Slot Grid Display --- */
.slot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(85px, 1fr));
    gap: 12px;
    margin-top: 1rem;
    margin-bottom: 2.5rem;
}
.slot {
    padding: 1rem 0;
    text-align: center;
    border-radius: var(--border-radius);
    font-weight: 700;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}
.slot:hover {
    transform: translateY(-3px);
}
.free { background: linear-gradient(145deg, #2ecc71, #28a745); }
.busy { background: linear-gradient(145deg, #e74c3c, #c0392b); }
.mine { background: linear-gradient(145deg, #3498db, #2980b9); }
small {
    font-weight: 500;
    opacity: 0.85;
    font-size: 0.75rem;
    display: block;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
# (Database code remains the same)
conn = sqlite3.connect("parking_v4.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, vehicle_number TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, slot_number TEXT NOT NULL, start_datetime TEXT NOT NULL, end_datetime TEXT NOT NULL)")
conn.commit()

# ---------- HELPERS ----------
# (Helper functions remain the same)
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def get_user(u, p):
    cur.execute("SELECT id, vehicle_number FROM users WHERE username=? AND password_hash=?", (u, hash_password(p)))
    return cur.fetchone()
def create_user(u, p):
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (u, hash_password(p)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: return False

# ---------- SESSION ----------
# (Session state remains the same)
for k in ("user_id", "vehicle_number"):
    if k not in st.session_state: st.session_state[k] = None

# ---------- AUTH PAGE ----------
if st.session_state.user_id is None:
    st.markdown("<h1 class='main-title'>🅿️ Parking Slot Booking System</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            user = get_user(u, p)
            if user:
                st.session_state.user_id, st.session_state.vehicle_number = user[0], user[1]
                st.rerun()
            else: st.error("Invalid credentials")
    with tab2:
        u = st.text_input("New Username", key="reg_user")
        p = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register", use_container_width=True):
            if create_user(u, p): st.success("Account created. Login now.")
            else: st.error("Username already exists")
    st.stop()

# ---------- MAIN APP LAYOUT ----------

# --- HEADER ---
col1, col2, col3 = st.columns([7, 2, 1])
with col1:
    st.markdown("<h1 class='main-title' style='margin-bottom: 0; border: none; font-size: 2rem;'>🅿️ Parking Slot Booking</h1>", unsafe_allow_html=True)
with col2:
    st.caption(f"Vehicle: **{st.session_state.vehicle_number or 'Not set'}**")
with col3:
    if st.button("Logout", use_container_width=True):
        st.session_state.user_id, st.session_state.vehicle_number = None, None
        st.rerun()

st.divider()

# --- VEHICLE NUMBER INPUT ---
if st.session_state.vehicle_number is None:
    v = st.text_input("Enter Vehicle Number (one time requirement)")
    if st.button("Save Vehicle Number", type="primary"):
        cur.execute("UPDATE users SET vehicle_number=? WHERE id=?", (v.upper(), st.session_state.user_id))
        conn.commit()
        st.session_state.vehicle_number = v.upper()
        st.rerun()
    st.stop()

# --- DASHBOARD SECTION ---
st.markdown("<h2 class='dashboard-title'>Dashboard Overview</h2>", unsafe_allow_html=True)

# --- STATUS CARDS ---
col1, col2 = st.columns(2)
with col1:
    now_dt = datetime.now()
    cur.execute("SELECT slot_number, start_datetime, end_datetime FROM bookings WHERE user_id=? AND? BETWEEN start_datetime AND end_datetime", (st.session_state.user_id, now_dt.strftime("%Y-%m-%d %H:%M")))
    active = cur.fetchone()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if active:
        slot, start, end = active
        end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
        remaining = end_time - now_dt
        st.success(f"""
        🚗 **Currently Parked**\n
        **Slot:** {slot}\n
        **Until:** {end_time.strftime("%I:%M %p")}\n
        **Time Remaining:** {str(remaining).split('.')[0]}
        """)
    else:
        st.info("🟢 No active parking session.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    cur.execute("SELECT COUNT(*) FROM bookings")
    total = cur.fetchone()[0]
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Total Lifetime Bookings", total)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LIVE AVAILABILITY SECTION ---
st.subheader("Live Slot Availability")
slots = [f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 11)]
now = datetime.now().strftime("%Y-%m-%d %H:%M")
cur.execute("SELECT slot_number FROM bookings WHERE? BETWEEN start_datetime AND end_datetime", (now,))
occupied = {r[0] for r in cur.fetchall()}
cur.execute("SELECT slot_number FROM bookings WHERE user_id=? AND? BETWEEN start_datetime AND end_datetime", (st.session_state.user_id, now))
mine = {r[0] for r in cur.fetchall()}

grid = "<div class='slot-grid'>"
for s in slots:
    cls, label = ("mine", "YOURS") if s in mine else (("busy", "BUSY") if s in occupied else ("free", "FREE"))
    grid += f"<div class='slot {cls}'>{s}<br><small>{label}</small></div>"
grid += "</div>"
st.markdown(grid, unsafe_allow_html=True)

# --- BOOKING SECTION ---
st.subheader("Book a New Parking Slot")
booking_date = st.date_input("Date", min_value=date.today())
col1, col2 = st.columns(2)
with col1:
    entry_time = st.time_input("Entry Time", value=datetime.now().replace(second=0, microsecond=0).time())
with col2:
    exit_time = st.time_input("Exit Time")

start_dt, end_dt = datetime.combine(booking_date, entry_time), datetime.combine(booking_date, exit_time)
if exit_time <= entry_time:
    end_dt += timedelta(days=1)
    st.warning("Exit time is before or same as entry time. Booking will automatically extend to the next day.")

cur.execute("SELECT slot_number FROM bookings WHERE NOT (end_datetime <=? OR start_datetime >=?)", (start_dt.strftime("%Y-%m-%d %H:%M"), end_dt.strftime("%Y-%m-%d %H:%M")))
blocked = {r[0] for r in cur.fetchall()}
available = [s for s in slots if s not in blocked]

if available:
    slot = st.selectbox("Available Slots for Selected Time", available)
else:
    st.error("No slots available for the selected time frame.")
    slot = None

if st.button("Confirm Booking", type="primary", use_container_width=True):
    if slot:
        cur.execute("SELECT id FROM bookings WHERE user_id=? AND NOT (end_datetime <=? OR start_datetime >=?)", (st.session_state.user_id, start_dt.strftime("%Y-%m-%d %H:%M"), end_dt.strftime("%Y-%m-%d %H:%M")))
        if cur.fetchone():
            st.error("You already have an overlapping booking. Only one car is allowed per user at a time.")
        else:
            cur.execute("INSERT INTO bookings (user_id, slot_number, start_datetime, end_datetime) VALUES (?,?,?,?)", (st.session_state.user_id, slot, start_dt.strftime("%Y-%m-%d %H:%M"), end_dt.strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            st.success(f"Slot {slot} booked successfully from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}.")
            st.rerun()
    else:
        st.error("No slot selected or available to book.")
