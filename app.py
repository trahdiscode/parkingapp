import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime, date, timedelta
from streamlit_autorefresh import st_autorefresh
import pytz
import base64
import time as _time
import re
import streamlit.components.v1 as components

# ---------- LOGO ----------
@st.cache_data
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

logo_base64 = get_image_base64("parking_logo_flat.png")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="ParkOS", layout="wide", page_icon="🅿️", initial_sidebar_state="collapsed")

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=30000, key="refresh")  # Refresh every 30s

# ---------- OPENING ANIMATION ----------
# ---------- OPENING ANIMATION ----------
st.markdown(f"""
<style>
/* Base Splash Container with deep radial gradient */
#splash-screen {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at center, #11131A 0%, var(--bg) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    animation: splashExit 1s cubic-bezier(0.65, 0, 0.35, 1) forwards;
    animation-delay: 2.8s;
    pointer-events: none;
    overflow: hidden;
}}

/* Cinematic Film Grain Overlay */
#splash-screen::after {{
    content: "";
    position: absolute;
    inset: -50%;
    width: 200%;
    height: 200%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 1;
    animation: grainShift 8s steps(10) infinite;
}}

/* Ambient Indigo Backlight */
.splash-glow {{
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(40px);
    z-index: 2;
    animation: breathGlow 4s ease-in-out infinite alternate;
}}

/* Content Wrapper to sit above grain and glow */
.splash-content {{
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Logo Focus & Float Reveal */
#splash-logo {{
    width: 120px;
    height: 120px;
    object-fit: contain;
    opacity: 0;
    filter: blur(12px) drop-shadow(0 0 0 rgba(99,102,241,0));
    transform: scale(0.9) translateY(10px);
    animation: 
        lensFocus 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards,
        premiumFloat 3s ease-in-out infinite alternate;
    animation-delay: 0.1s, 1.3s;
}}

/* Typography Tracking Reveal */
#splash-text {{
    font-family: var(--font);
    font-size: 3rem;
    font-weight: 800;
    color: var(--text-1);
    letter-spacing: -0.1em; /* Starts compressed */
    margin-top: 1.5rem;
    opacity: 0;
    filter: blur(8px);
    transform: translateY(15px);
    background: linear-gradient(180deg, #FFFFFF 0%, #9397B0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textTrackingReveal 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    animation-delay: 0.5s;
}}

/* Keyframes */
@keyframes lensFocus {{
    0% {{ opacity: 0; filter: blur(12px) drop-shadow(0 0 0 rgba(99,102,241,0)); transform: scale(0.9) translateY(10px); }}
    100% {{ opacity: 1; filter: blur(0px) drop-shadow(0 8px 24px rgba(99,102,241,0.3)); transform: scale(1) translateY(0); }}
}}

@keyframes premiumFloat {{
    0% {{ transform: translateY(0); filter: blur(0px) drop-shadow(0 8px 24px rgba(99,102,241,0.3)); }}
    100% {{ transform: translateY(-6px); filter: blur(0px) drop-shadow(0 12px 32px rgba(99,102,241,0.5)); }}
}}

@keyframes textTrackingReveal {{
    0% {{ opacity: 0; filter: blur(8px); transform: translateY(15px); letter-spacing: -0.1em; }}
    100% {{ opacity: 1; filter: blur(0px); transform: translateY(0); letter-spacing: -0.04em; }}
}}

@keyframes breathGlow {{
    0% {{ transform: scale(0.8); opacity: 0.5; }}
    100% {{ transform: scale(1.1); opacity: 1; }}
}}

@keyframes grainShift {{
    0%, 100% {{ transform: translate(0, 0); }}
    10% {{ transform: translate(-5%, -5%); }}
    30% {{ transform: translate(5%, -10%); }}
    50% {{ transform: translate(-10%, 5%); }}
    70% {{ transform: translate(10%, 10%); }}
    90% {{ transform: translate(-5%, 15%); }}
}}

/* App zoom-in effect on exit */
@keyframes splashExit {{
    0% {{ opacity: 1; transform: scale(1); visibility: visible; }}
    100% {{ opacity: 0; transform: scale(1.05); visibility: hidden; z-index: -1; }}
}}
</style>

<div id="splash-screen">
    <div class="splash-glow"></div>
    <div class="splash-content">
        <img id="splash-logo" src="data:image/png;base64,{logo_base64}" alt="ParkOS">
        <div id="splash-text">ParkOS</div>
    </div>
</div>
""", unsafe_allow_html=True)
# ---------- STYLESHEET ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #080A0F;
    --bg-grad: radial-gradient(ellipse 80% 60% at 50% -20%, rgba(99,102,241,0.15) 0%, transparent 70%);
    --surface: #0F1117;
    --surface-2: #161923;
    --surface-3: #1E2230;
    --border: rgba(255,255,255,0.06);
    --border-hover: rgba(255,255,255,0.12);
    --border-active: rgba(99,102,241,0.4);
    --text-1: #F1F2F6;
    --text-2: #9397B0;
    --text-3: #4B5068;
    --accent: #6366F1;
    --accent-2: #818CF8;
    --accent-soft: rgba(99,102,241,0.1);
    --green: #10B981;
    --green-soft: rgba(16,185,129,0.08);
    --green-border: rgba(16,185,129,0.2);
    --red: #EF4444;
    --red-soft: rgba(239,68,68,0.08);
    --amber: #F59E0B;
    --amber-soft: rgba(245,158,11,0.1);
    --radius: 14px;
    --radius-sm: 8px;
    --radius-xs: 5px;
    --font: 'Outfit', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
    --shadow-lg: 0 8px 40px rgba(0,0,0,0.5);
    --shadow-accent: 0 4px 20px rgba(99,102,241,0.25);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, .stApp { background: var(--bg)!important; font-family: var(--font); color: var(--text-1); }

/* Kill Streamlit's rerun fade/flicker */
.stApp > div, .main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"], [data-testid="element-container"], iframe, .stMarkdown, .stButton, .stTextInput, .stSelectbox, .stDateInput { animation: none!important; transition: none!important; opacity: 1!important; }
[data-testid="stSkeleton"] { display: none!important; }
.stApp [data-stale="true"], .stApp [data-stale="true"] * { opacity: 1!important; }

.stApp::before { content: ''; position: fixed; inset: 0; background: var(--bg-grad); pointer-events: none; z-index: 0; }
.main.block-container { padding: 1.5rem 1.25rem 4rem!important; max-width: 480px!important; margin: 0 auto!important; position: relative; z-index: 1; }
@media (min-width: 769px) { .main.block-container { padding: 2rem 2rem 4rem!important; max-width: 900px!important; } }
.main.block-container { max-width: 900px !important; }

p, li { color: var(--text-1); font-size: 0.9rem; line-height: 1.6; }
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 9999px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton, div[data-testid="stDecoration"] { display: none; }
h1, h2, h3, h4 { font-family: var(--font); letter-spacing: -0.02em; }

.section-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-3); margin-bottom: 0.875rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.app-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 0 0.75rem; margin-bottom: 0.25rem; border-bottom: 1px solid var(--border); }
.app-brand { display: flex; align-items: center; gap: 0.75rem; }
.app-brand-name { font-size: 2.75rem; font-weight: 800; color: var(--text-1); letter-spacing: -0.04em; line-height: 1; }
.app-brand-sub { font-size: 1.3rem; font-weight: 600; color: var(--text-3); letter-spacing: 0.08em; text-transform: uppercase; line-height: 1; margin-top: 2px; }

.active-card { background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, var(--surface) 60%); border: 1px solid var(--green-border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1rem; position: relative; overflow: hidden; }
.active-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--green), transparent 60%); }
.active-card-glow { position: absolute; top: -30px; right: -30px; width: 100px; height: 100px; background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, transparent 70%); pointer-events: none; }
.active-badge { display: inline-flex; align-items: center; gap: 5px; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--green); background: var(--green-soft); border: 1px solid var(--green-border); padding: 3px 8px; border-radius: 99px; margin-bottom: 0.75rem; }
.active-dot { width: 6px; height: 6px; background: var(--green); border-radius: 50%; display: inline-block; box-shadow: 0 0 6px var(--green); }
.active-slot-display { display: flex; align-items: flex-end; gap: 0.75rem; margin: 0.5rem 0 0.75rem; }
.active-slot-label { font-size: 0.65rem; color: var(--text-3); font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px; }
.active-slot-num { font-family: var(--font-mono); font-size: 3rem; font-weight: 600; color: var(--text-1); line-height: 1; }
.active-time-block { flex: 1; background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 0.5rem 0.75rem; }
.active-time-label { font-size: 0.6rem; color: var(--text-3); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
.active-time-val { font-family: var(--font-mono); font-size: 0.95rem; color: var(--text-1); font-weight: 500; }
.active-remaining-bar { display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 0.875rem; background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-top: 0.25rem; }
.remaining-label { font-size: 0.7rem; color: var(--text-3); font-weight: 500; flex: 1; }
.remaining-val { font-family: var(--font-mono); font-size: 0.9rem; color: var(--green); font-weight: 600; }
.vehicle-chip { display: inline-flex; align-items: center; gap: 5px; background: var(--surface-2); border: 1px solid var(--border); border-radius: 6px; padding: 3px 8px; font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-2); margin-bottom: 0.75rem; }

.stats-row { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.625rem; margin-bottom: 1.25rem; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.125rem; position: relative; overflow: hidden; }
.stat-card::after { content: ''; position: absolute; bottom: 0; right: 0; width: 40px; height: 40px; border-radius: 50%; background: var(--accent-soft); transform: translate(10px, 10px); }
.stat-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-3); margin-bottom: 0.35rem; }
.stat-value { font-family: var(--font-mono); font-size: 1.75rem; font-weight: 600; color: var(--text-1); line-height: 1; }
.stat-value.accent { color: var(--accent-2); }
.stat-value.green { color: var(--green); }

.empty-card { background: var(--surface); border: 1px dashed var(--border-hover); border-radius: var(--radius); padding: 2rem 1.5rem; text-align: center; margin-bottom: 1rem; }
.empty-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.empty-title { font-size: 0.9rem; font-weight: 600; color: var(--text-2); margin-bottom: 0.25rem; }
.empty-sub { font-size: 0.78rem; color: var(--text-3); }

.booking-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; margin-bottom: 0.625rem; transition: border-color 0.2s; }
.booking-card:hover { border-color: var(--border-hover); }
.booking-card-inner { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 0.875rem; padding: 0.875rem 1rem; }
.slot-badge { width: 48px; height: 48px; background: var(--surface-3); border: 1px solid var(--border); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-family: var(--font-mono); font-size: 0.88rem; font-weight: 600; color: var(--text-1); flex-shrink: 0; }
.slot-badge.active { background: var(--green-soft); border-color: var(--green-border); color: var(--green); }
.booking-info { min-width: 0; }
.status-pill { display: inline-flex; align-items: center; gap: 4px; font-size: 0.6rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 2px 7px; border-radius: 99px; margin-bottom: 4px; }
.pill-active { background: var(--green-soft); color: var(--green); border: 1px solid var(--green-border); }
.pill-upcoming { background: var(--accent-soft); color: var(--accent-2); border: 1px solid rgba(99,102,241,0.2); }
.pill-completed { background: var(--surface-2); color: var(--text-3); border: 1px solid var(--border); }
.booking-time-text { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.booking-date-text { font-size: 0.7rem; color: var(--text-3); margin-top: 1px; }

.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }
.step-wrap { display: flex; align-items: center; gap: 0.625rem; margin-bottom: 1rem; }
.step-num { width: 24px; height: 24px; border-radius: 50%; background: var(--accent-soft); border: 1px solid rgba(99,102,241,0.25); color: var(--accent-2); font-size: 0.7rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
.step-title { font-size: 0.875rem; font-weight: 600; color: var(--text-2); }
.time-form { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1rem; }
.slot-legend { display: flex; gap: 1rem; margin-bottom: 0.875rem; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 0.72rem; color: var(--text-2); }
.legend-dot { width: 8px; height: 8px; border-radius: 3px; flex-shrink: 0; }
.legend-free { background: var(--green); }
.legend-busy { background: var(--red); }
.legend-selected { background: var(--accent); }
.row-label { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-3); font-weight: 700; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.4rem; }
.row-label::before { content: ''; display: inline-block; width: 3px; height: 10px; background: var(--accent); border-radius: 99px; }

.confirm-banner { background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, var(--surface) 60%); border: 1px solid rgba(99,102,241,0.25); border-radius: var(--radius); padding: 1rem 1.25rem; margin: 1rem 0; position: relative; overflow: hidden; }
.confirm-banner::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent), transparent 60%); }
.confirm-slot-big { font-family: var(--font-mono); font-size: 2rem; font-weight: 600; color: var(--text-1); line-height: 1; margin: 0.25rem 0; }
.confirm-time { font-size: 0.78rem; color: var(--text-2); font-family: var(--font-mono); }
.warn-note { font-size: 0.78rem; color: var(--amber); background: var(--amber-soft); border: 1px solid rgba(245,158,11,0.2); border-radius: var(--radius-sm); padding: 0.625rem 1rem; margin-top: 0.625rem; }
.lock-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem 1.25rem; text-align: center; }
.lock-icon { font-size: 1.75rem; margin-bottom: 0.5rem; }
.lock-title { font-size: 0.95rem; font-weight: 600; color: var(--text-2); margin-bottom: 0.375rem; }
.lock-sub { font-size: 0.78rem; color: var(--text-3); line-height: 1.5; }

.login-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem 0; }
.lp-card { background: #0F1117; border: 1px solid rgba(255,255,255,0.07); border-radius: 20px; padding: 2rem 2rem 1.5rem; margin-bottom: 1rem; position: relative; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.5); width: 100%; max-width: 420px; }
.lp-card::before { content: ''; position: absolute; top: -60px; right: -60px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 65%); pointer-events: none; }
.lp-title { font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 700; color: #F1F2F6; letter-spacing: -0.02em; margin-bottom: 0.2rem; }
.lp-sub { font-family: 'Outfit', sans-serif; font-size: 0.78rem; color: #4B5068; margin-bottom: 1.5rem; line-height: 1.5; }
.lp-divider { display: flex; align-items: center; gap: 0.75rem; margin: 1rem 0; }
.lp-divider-line { flex:1; height:1px; background: rgba(255,255,255,0.06); }
.lp-divider-text { font-size:0.65rem; color:#4B5068; font-family:'Outfit',sans-serif; letter-spacing:0.1em; text-transform:uppercase; }

/* Streamlit overrides */
.stTextInput > label, .stDateInput > label, .stTimeInput > label, .stSelectbox > label { font-family: var(--font)!important; font-size: 0.7rem!important; font-weight: 700!important; letter-spacing: 0.08em!important; text-transform: uppercase!important; color: var(--text-3)!important; margin-bottom: 4px!important; }
.stTextInput input, .stDateInput input, .stTimeInput input { background: var(--surface-2)!important; border: 1px solid var(--border)!important; border-radius: var(--radius-sm)!important; color: var(--text-1)!important; font-family: var(--font-mono)!important; font-size: 0.9rem!important; padding: 0.625rem 0.875rem!important; transition: border-color 0.2s, box-shadow 0.2s!important; min-height: 44px!important; }
.stTextInput input:focus, .stDateInput input:focus { border-color: var(--accent)!important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important; outline: none!important; }
div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within { border-color: var(--accent)!important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important; outline: none!important; }
div[data-baseweb="input"] input:focus, div[data-baseweb="base-input"] input:focus { outline: none!important; box-shadow: none!important; }
[data-baseweb="input"] { border-color: var(--border)!important; }
[data-baseweb="input"]:focus-within { border-color: var(--accent)!important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important; }

div[data-baseweb="select"] > div { background: var(--surface-2)!important; border: 1px solid var(--border)!important; border-radius: var(--radius-sm)!important; color: var(--text-1)!important; min-height: 44px!important; }
div[data-baseweb="select"] > div:focus-within { border-color: var(--accent)!important; box-shadow: 0 0 0 3px rgba(99,102,241,0.12)!important; }
div[data-baseweb="popover"] { background: var(--surface-2)!important; border: 1px solid var(--border)!important; border-radius: var(--radius)!important; }
[data-baseweb="menu"] { background: var(--surface-2)!important; }
[data-baseweb="option"] { background: var(--surface-2)!important; color: var(--text-1)!important; font-size: 0.88rem!important; }
[data-baseweb="option"]:hover, [aria-selected="true"] { background: var(--surface-3)!important; }

.stButton > button { font-family: var(--font)!important; font-size: 0.88rem!important; font-weight: 600!important; border-radius: var(--radius-sm)!important; transition: all 0.18s ease!important; min-height: 44px!important; letter-spacing: 0.01em!important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%)!important; border: none!important; color: #fff!important; box-shadow: var(--shadow-accent)!important; }
.stButton > button[kind="primary"]:hover { box-shadow: 0 6px 24px rgba(99,102,241,0.4)!important; transform: translateY(-1px)!important; }
.stButton > button[kind="secondary"] { background: transparent!important; border: 1px solid var(--border)!important; color: var(--text-3)!important; font-size: 0.78rem!important; min-height: 34px!important; padding: 0 0.75rem!important; }
.stButton > button[kind="secondary"]:hover { border-color: #3B82F6!important; color: #3B82F6!important; background: rgba(59,130,246,0.08)!important; }

.stButton > button[key*="slot_"] { height: 48px!important; font-family: var(--font-mono)!important; font-size: 0.8rem!important; font-weight: 600!important; padding: 0!important; }
.stButton > button[key*="slot_"]:hover { border-color: #3B82F6!important; color: #3B82F6!important; background: rgba(59,130,246,0.08)!important; }
.stButton > button[key*="slot_"]:disabled { border-color: #EF4444!important; color: #EF4444!important; background: rgba(239,68,68,0.08)!important; opacity: 1!important; cursor: not-allowed!important; }
div[data-testid="stAlert"] { background: var(--surface)!important; border-radius: var(--radius)!important; border: 1px solid var(--border)!important; font-size: 0.85rem!important; }
div[data-testid="stMetric"] { background: var(--surface)!important; border: 1px solid var(--border)!important; border-radius: var(--radius)!important; padding: 1rem 1.25rem!important; }
.stTabs [data-baseweb="tab-list"] { background: var(--surface)!important; border: 1px solid var(--border)!important; border-radius: var(--radius-sm)!important; padding: 3px!important; gap: 2px!important; }
.stTabs [data-baseweb="tab"] { background: transparent!important; border: none!important; color: var(--text-2)!important; font-size: 0.85rem!important; font-weight: 600!important; padding: 0.5rem 1rem!important; border-radius: var(--radius-xs)!important; transition: all 0.2s!important; flex: 1!important; text-align: center!important; justify-content: center!important; }
.stTabs [data-baseweb="tab"]:hover { color: var(--text-1)!important; }
.stTabs [aria-selected="true"] { background: var(--surface-3)!important; color: var(--text-1)!important; box-shadow: var(--shadow-sm)!important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.25rem!important; }
div[data-testid="stHorizontalBlock"] { gap: 0.4rem!important; }
details { border: 1px solid var(--border)!important; border-radius: var(--radius)!important; background: var(--surface)!important; }
summary { padding: 0.875rem 1rem!important; font-size: 0.85rem!important; color: var(--text-2)!important; font-weight: 600!important; }
div[data-baseweb="calendar"] { background: var(--surface-2)!important; border: 1px solid var(--border)!important; border-radius: var(--radius)!important; }
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# ---------- HELPERS ----------
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()

def get_user(u, p):
    res = supabase.table("users").select("id, vehicle_number").eq("username", u).eq("password_hash", hash_password(p)).execute()
    if res.data:
        row = res.data[0]
        return (row["id"], row["vehicle_number"])
    return None

def create_user(u, p):
    try:
        existing = supabase.table("users").select("id").eq("username", u).execute()
        if existing.data:
            return False
        supabase.table("users").insert({"username": u, "password_hash": hash_password(p)}).execute()
        return True
    except Exception:
        return False

ist_timezone = pytz.timezone('Asia/Kolkata')

def get_next_30min_slot_tz(dt_tz):
    minutes = dt_tz.minute
    if minutes == 0:
        return dt_tz.replace(second=0, microsecond=0)
    elif minutes <= 30:
        return dt_tz.replace(minute=30, second=0, microsecond=0)
    else:
        return (dt_tz + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def build_time_options(for_date, now_ist=None):
    standard_slots = [(datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").strftime("%I:%M %p"),
                       datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                      for h in range(24) for m in (0, 30)]
    if now_ist is not None and for_date == now_ist.date():
        now_time = now_ist.time().replace(second=0, microsecond=0)
        now_label = "Now (" + now_ist.strftime("%I:%M %p").lstrip("0") + ")"
        future_slots = [(label, t) for label, t in standard_slots if t > now_time]
        return [(now_label, now_time)] + future_slots
    return standard_slots

def parse_dt(s):
    dt_obj = datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")
    if dt_obj.tzinfo is None:
        return ist_timezone.localize(dt_obj)
    return dt_obj

# ---------- GLOBAL SESSION STATE INIT ----------
# Always declare these AT THE TOP so Streamlit never throws an AttributeError
if 'selected_slot' not in st.session_state:
    st.session_state.selected_slot = None

if 'show_booking_flow' not in st.session_state:
    st.session_state.show_booking_flow = False

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
    st.session_state.admin_role = None

# ── SECRET ADMIN ROUTING & UI ──
if "mode" in st.query_params and st.query_params["mode"] == "admin":
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { background-color: rgba(255,255,255,0.06) !important; }
    .stTabs [data-baseweb="tab-list"] { background: #0D0F14 !important; border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 12px !important; padding: 4px !important; gap: 2px !important; }
    .stTabs [data-baseweb="tab"] { color: #4B5563 !important; font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important; font-weight: 500 !important; border-radius: 8px !important; }
    .stTabs [aria-selected="true"] { background: #1A1D24 !important; color: #F9FAFB !important; box-shadow: 0 1px 3px rgba(0,0,0,0.4) !important; }
    .stTextInput > label { font-family: 'Inter', sans-serif !important; font-size: 0.68rem !important; font-weight: 500 !important; letter-spacing: 0.06em !important; color: #4B5563 !important; text-transform: uppercase !important; }
    .stTextInput input { background: #0A0C10 !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 10px !important; color: #F3F4F6 !important; font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important; min-height: 46px !important; }
    .stTextInput input:focus { border-color: rgba(99,102,241,0.5) !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important; }
    .stButton > button[kind="primary"] { background: #4F46E5 !important; border: none !important; color: #fff !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 0.85rem !important; min-height: 46px !important; border-radius: 10px !important; box-shadow: 0 4px 16px rgba(79,70,229,0.25) !important; }
    .stButton > button[kind="primary"]:hover { background: #4338CA !important; box-shadow: 0 6px 20px rgba(79,70,229,0.35) !important; }
    .stButton > button[kind="secondary"] { background: transparent !important; border: 1px solid rgba(255,255,255,0.07) !important; color: #4B5563 !important; border-radius: 10px !important; font-family: 'Inter', sans-serif !important; }
    .stButton > button[kind="secondary"]:hover { border-color: rgba(255,255,255,0.12) !important; color: #9CA3AF !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0 !important; }
    [data-testid="stHeader"] { display: none !important; }
    .main.block-container { padding-top: 0 rem !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if ANY admins exist
    admin_count_res = supabase.table("admins").select("id").neq("status", "removed").execute()
    admin_count = len(admin_count_res.data) if admin_count_res.data else 0

    st.markdown("""
    <div style="max-width:480px; margin: -2rem auto 3rem; background: linear-gradient(145deg, #0D0F14 0%, #111318 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 24px; padding: 2.5rem 2.5rem 2rem; box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 32px 64px rgba(0,0,0,0.6); text-align: center; position: relative; overflow: hidden;">
        <div style="display:inline-flex; align-items:center; gap:6px; padding:5px 14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:99px; color:#6B7280; font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:600; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:1.25rem;">
            <span style="width:5px; height:5px; background:#22C55E; border-radius:50%; display:inline-block; box-shadow:0 0 8px rgba(34,197,94,0.6);"></span>
            Secure Portal
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:2.4rem; font-weight:700; letter-spacing:-0.04em; color:#F9FAFB; margin-bottom:0.4rem; line-height:1.1;">Command Center</div>
        <div style="color:#4B5563; font-family:'Inter',sans-serif; font-size:0.82rem; line-height:1.5;">System Management & Access Control</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.admin_logged_in:
        
        # ── ROOT ONLY CONTROLS ──
        if st.session_state.admin_role == "root":
            st.markdown("#### Root Admin Controls")
            
            t_req, t_manage = st.tabs(["Pending Requests", "Manage Admins"])
            
            with t_req:
                pending = supabase.table("admins").select("*").eq("status", "pending").execute()
                if pending.data:
                    for req in pending.data:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1: st.markdown(f"**{req['username']}**<br><span style='font-size:0.7rem;color:gray;'>Requested Access</span>", unsafe_allow_html=True)
                        with col2:
                            if st.button("Approve", key=f"app_{req['id']}", type="primary"):
                                supabase.table("admins").update({"status": "active"}).eq("id", req["id"]).execute()
                                st.rerun()
                        with col3:
                            if st.button("Deny", key=f"den_{req['id']}"):
                                supabase.table("admins").delete().eq("id", req["id"]).execute()
                                st.rerun()
                else:
                    st.success("No pending requests at this time.")
                    
            with t_manage:
                all_other_admins = supabase.table("admins").select("*").in_("status", ["active", "removed"]).neq("status", "root").execute()
                if all_other_admins.data:
                    for adm in all_other_admins.data:
                        col_info, col_act = st.columns([3, 1])
                        with col_info: 
                            status_color = "green" if adm['status'] == "active" else "red"
                            st.markdown(f"**{adm['username']}**<br><span style='font-size:0.7rem;color:{status_color}; text-transform:uppercase;'>{adm['status']}</span>", unsafe_allow_html=True)
                        with col_act:
                            if adm['status'] == 'active':
                                if st.button("Remove", key=f"rm_{adm['id']}"):
                                    supabase.table("admins").update({"status": "removed"}).eq("id", adm['id']).execute()
                                    st.rerun()
                            elif adm['status'] == 'removed':
                                if st.button("Restore", key=f"res_{adm['id']}"):
                                    supabase.table("admins").update({"status": "active"}).eq("id", adm['id']).execute()
                                    st.rerun()
                else:
                    st.info("No other admins currently exist.")

            st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

        # ── GLOBAL ADMIN VIEWS (Root + Active) ──
        
        # 1. Recent Bookings (Last 24 Hours)
        st.markdown("#### System Activity (Last 24 Hours)")
        twenty_four_hours_ago = (datetime.now(ist_timezone) - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        recent_bookings = supabase.table("bookings").select("*").gte("start_datetime", twenty_four_hours_ago).order("start_datetime", desc=True).execute().data
        
        if recent_bookings:
            # Fetch usernames to match with user_id
            user_ids = list(set([b["user_id"] for b in recent_bookings]))
            users_res = supabase.table("users").select("id, username").in_("id", user_ids).execute().data
            user_map = {u["id"]: u["username"] for u in users_res} if users_res else {}

            for b in recent_bookings:
                u_name = user_map.get(b["user_id"], "Unknown User")
                s_time = parse_dt(b["start_datetime"]).strftime('%b %d, %I:%M %p')
                e_time = parse_dt(b["end_datetime"]).strftime('%I:%M %p')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #F3F4F6;">{u_name}</div>
                        <div style="font-size: 0.7rem; color: #9CA3AF; font-family: monospace;">{s_time} → {e_time}</div>
                    </div>
                    <div style="background: rgba(99,102,241,0.15); color: #818CF8; border: 1px solid rgba(99,102,241,0.3); padding: 4px 10px; border-radius: 6px; font-family: monospace; font-size: 0.8rem; font-weight: 600;">
                        {b["slot_number"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No bookings in the last 24 hours.")

        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # 2. System Settings
        st.markdown("#### System Settings")
        
        current_res = supabase.table("settings").select("setting_value").eq("setting_key", "sensor_interval_minutes").execute()
        current_interval = int(current_res.data[0]["setting_value"]) if current_res.data else 10
        
        col_set1, col_set2 = st.columns([3, 1])
        with col_set1:
            new_interval = st.number_input("Sensor Update Interval (Minutes)", min_value=1, max_value=120, value=current_interval)
        with col_set2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Save Settings", type="primary", use_container_width=True):
                try:
                    supabase.table("settings").upsert({"setting_key": "sensor_interval_minutes", "setting_value": str(new_interval)}).execute()
                    if 'get_sensor_interval' in st.session_state: del st.session_state['get_sensor_interval']
                    st.success("Saved!")
                except Exception:
                    st.error("Error saving.")

        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        if st.button("🔒 Exit Command Center", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.admin_role = None
            st.query_params.clear()
            st.rerun()

    else:
        if admin_count == 0:
            # STATE 1: NO ADMINS EXIST YET - CREATE ROOT
            st.markdown('<div style="text-align:center; color:#A0A0A0; margin-bottom:1rem;">Initialize the Root Admin Account</div>', unsafe_allow_html=True)
            u = st.text_input("Root Username", key="root_u")
            p = st.text_input("Root Password", type="password", key="root_p")
            if st.button("Initialize Root Admin", type="primary", use_container_width=True):
                if u and p:
                    # Note the status is set to 'root'
                    supabase.table("admins").insert({"username": u, "password_hash": hash_password(p), "status": "root"}).execute()
                    st.success("✅ Root Admin created! Please log in.")
                    st.rerun()
        else:
            # STATE 2: ADMINS EXIST - LOGIN OR REQUEST
            t1, t2 = st.tabs(["Secure Login", "Request Access"])
            
            with t1:
                u = st.text_input("Username", key="al_u")
                p = st.text_input("Password", type="password", key="al_p")
                if st.button("Authorize", type="primary", use_container_width=True):
                    # Check for both root and active statuses, explicitly excluding removed
                    res = supabase.table("admins").select("id, status").eq("username", u).eq("password_hash", hash_password(p)).in_("status", ["active", "root"]).execute()
                    if res.data:
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_role = res.data[0]["status"] # Will be 'root' or 'active'
                        st.rerun()
                    else:
                        st.error("Authentication failed, access pending, or account removed.")
            
            with t2:
                u_req = st.text_input("Desired Username", key="ar_u")
                p_req = st.text_input("Password", type="password", key="ar_p")
                
                if st.button("Submit Request", use_container_width=True):
                    if not u_req or not p_req:
                        st.error("Please fill in both fields.")
                    else:
                        # CHECK: Does this username already exist in ANY status (active, pending, or root)?
                        res = supabase.table("admins").select("id, status").eq("username", u_req).execute()
                        
                        if res.data:
                            status = res.data[0]["status"]
                            if status == "pending":
                                st.warning("You already have a request pending approval.")
                            elif status == "active" or status == "root":
                                st.error("This admin account already exists. Please log in.")
                            elif status == "removed":
                                st.error("This account has been deactivated. Contact Root Admin.")
                        else:
                            # PROCEED: Only if no record was found
                            try:
                                supabase.table("admins").insert({
                                    "username": u_req, 
                                    "password_hash": hash_password(p_req), 
                                    "status": "pending"
                                }).execute()
                                st.success("Request sent to the Root Admin.")
                            except Exception as e:
                                st.error("An error occurred. Please try again.")

    # Hide standard header & exit button if not logged in
    if not st.session_state.admin_logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("← Return to Faculty Portal"):
            st.query_params.clear()
            st.rerun()
    st.stop() # Prevents the rest of the standard app from loading!

# ── LIVE PARKING SENSOR FUNCTIONS ──
@st.cache_data(ttl=30, show_spinner=False)
def get_sensor_interval():
    """Fetches the global sensor interval from Supabase, updates every 30s"""
    try:
        res = supabase.table("settings").select("setting_value").eq("setting_key", "sensor_interval_minutes").execute()
        if res.data:
            return int(res.data[0]["setting_value"])
    except Exception:
        pass
    return 10  # Fallback to 10 minutes if DB fails

def _get_sensor_state(seed_offset=0):
    """Generate pseudo-random occupancy AND merge with real active bookings."""
    
    # 1. Fetch real active bookings from Supabase
    now_str = datetime.now(ist_timezone).strftime("%Y-%m-%d %H:%M")
    try:
        _res = supabase.table("bookings").select("slot_number, start_datetime, end_datetime").execute()
        # A slot is really occupied if the current time falls inside its booked window
        real_active_slots = {
            r["slot_number"] for r in _res.data 
            if r["start_datetime"] <= now_str <= r["end_datetime"]
        }
    except Exception:
        real_active_slots = set()

    # 2. Simulated pseudo-random generator based on DB Settings
    interval_seconds = get_sensor_interval() * 60
    bucket = int(_time.time() // interval_seconds) + seed_offset  
    
    def _is_occupied(hash_id, real_id):
        # Force RED if it is actively booked by a real user right now
        if real_id in real_active_slots:
            return True
            
        # Otherwise, fall back to the random sensor simulation
        h = int(hashlib.md5(f"{bucket}-{hash_id}".encode()).hexdigest(), 16)
        return (h % 100) < 45

    # 3. Build the zones
    zone_a = {f"A{r}{c}": _is_occupied(f"zA{r}{c}", f"A{r}{c}") for r in range(1, 4) for c in range(1, 5)}
    zone_b = {f"B{r}{c}": _is_occupied(f"zB{r}{c}", f"B{r}{c}") for r in range(1, 5) for c in range(1, 4)}
    zone_c = {f"C{r}{c}": _is_occupied(f"zC{r}{c}", f"C{r}{c}") for r in range(1, 3) for c in range(1, 7)}

    return zone_a, zone_b, zone_c

def _count(zone): 
    total = len(zone)
    occ = sum(zone.values())
    return total - occ, occ, total

def _slot_html(slot_id, occupied):
    color = "#EF4444" if occupied else "#10B981"
    bg = "rgba(239,68,68,0.12)" if occupied else "rgba(16,185,129,0.10)"
    border = "rgba(239,68,68,0.35)" if occupied else "rgba(16,185,129,0.35)"
    icon = "🔴" if occupied else "🟢"
    label = slot_id[1:]
    return f"""<div style="
        background:{bg};
        border:1.5px solid {border};
        border-radius:8px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:3px;
        padding:6px 4px;
        min-width:0;
    ">
        <span style="font-size:0.7rem;">{icon}</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;font-weight:700;color:{color};">{label}</span>
    </div>"""

def _zone_card(zone_name, zone_dict, rows, cols, description):
    free, occ, total = _count(zone_dict)
    pct_free = int(free / total * 100) if total > 0 else 0
    bar_color = "#10B981" if pct_free > 40 else ("#F59E0B" if pct_free > 15 else "#EF4444")
    slots_html = ""
    for r in range(1, rows + 1):
        slots_html += f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:6px;margin-bottom:6px;">'
        for c in range(1, cols + 1):
            sid = f"{zone_name[-1]}{r}{c}"
            slots_html += _slot_html(sid, zone_dict.get(sid, False))
        slots_html += "</div>"
    return f"""
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:1rem 1rem 0.875rem; flex:1; min-width:0;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.625rem;">
            <div>
                <div style="font-size:0.75rem;font-weight:800;color:var(--text-1);letter-spacing:-0.01em;">{zone_name}</div>
                <div style="font-size:0.6rem;color:var(--text-3);letter-spacing:0.05em;text-transform:uppercase;margin-top:1px;">{description}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700;color:{bar_color};">{free}<span style="font-size:0.65rem;color:var(--text-3);font-weight:400;">/{total}</span></div>
                <div style="font-size:0.58rem;color:var(--text-3);">free slots</div>
            </div>
        </div>
        <div style="height:3px;background:var(--surface-3);border-radius:99px;margin-bottom:0.75rem;">
            <div style="height:100%;width:{pct_free}%;background:{bar_color};border-radius:99px;transition:width 0.4s ease;"></div>
        </div>
        {slots_html}
        <div style="display:flex;gap:0.875rem;margin-top:0.5rem;padding-top:0.5rem;border-top:1px solid var(--border);">
            <span style="font-size:0.62rem;color:#10B981;">🟢 Available ({free})</span>
            <span style="font-size:0.62rem;color:#EF4444;">🔴 Occupied ({occ})</span>
        </div>
    </div>
    """

def render_live_parking():
    zone_a, zone_b, zone_c = _get_sensor_state()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(_zone_card("Zone A", zone_a, rows=3, cols=4, description="Block 3 × 4"), unsafe_allow_html=True)
    with col2:
        st.markdown(_zone_card("Zone B", zone_b, rows=4, cols=3, description="Block 4 × 3"), unsafe_allow_html=True)
    with col3:
        st.markdown(_zone_card("Zone C", zone_c, rows=2, cols=6, description="Block 2 × 6"), unsafe_allow_html=True)


# ---------- PUBLIC OR AUTH PAGE ----------
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'signin'

    # --- PUBLIC DASHBOARD HEADER ---
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; padding: 0.25rem 0 1rem; margin-bottom: 2rem; border-bottom: 1px solid var(--border);">
        <img src="data:image/png;base64,{logo_base64}" style="width: 56px; height: 56px; object-fit: contain; filter: drop-shadow(0 4px 16px rgba(99,102,241,0.4)); flex-shrink: 0;">
        <div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: var(--text-1); line-height: 1; letter-spacing: -0.04em;">ParkOS</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; color: var(--text-3); font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px;">Faculty Parking Portal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- RENDER VAST INTERFACE ---
    render_live_parking()
    st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

    # --- BOOKING CTA OR LOGIN FLOW ---
    if not st.session_state.show_booking_flow:
        st.markdown("""
        <div style="background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem; text-align: center; max-width: 600px; margin: 0 auto;">
            <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-1); margin-bottom: 0.5rem;">Need to reserve a slot?</div>
            <div style="font-size: 0.85rem; color: var(--text-3); margin-bottom: 1.5rem;">Faculty members can log in to securely book and manage parking spaces in advance.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the button nicely
        col_space1, col_btn, col_space2 = st.columns([1, 1.5, 1])
        with col_btn:
            # Move the button slightly up to overlap the container nicely
            st.markdown('<div style="margin-top: -1.5rem;"></div>', unsafe_allow_html=True)
            if st.button("Log In to Book a Slot →", type="primary", use_container_width=True):
                st.session_state.show_booking_flow = True
                st.rerun()
        st.stop()
    else:
        # --- LOGIN / REGISTER CARD ---
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)

        if st.session_state.auth_mode == 'signin':
            st.markdown("""
            <div class="lp-title">Welcome back</div>
            <div class="lp-sub">Sign in to manage your parking sessions</div>
            """, unsafe_allow_html=True)
            u = st.text_input("Username", key="login_user", placeholder="Enter your username", label_visibility="collapsed")
            p = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", type="primary", use_container_width=True):
                user = get_user(u, p)
                if user:
                    st.session_state.user_id = user[0]
                    st.session_state.vehicle_number = user[1]
                    st.session_state.username = u
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
            
            st.markdown("""<div class="lp-divider">
                <div class="lp-divider-line"></div>
                <div class="lp-divider-text">No account yet?</div>
                <div class="lp-divider-line"></div>
            </div>""", unsafe_allow_html=True)
            if st.button("Create a free account", type="secondary", use_container_width=True):
                st.session_state.auth_mode = 'register'
                st.rerun()

        else:
            st.markdown("""
            <div class="lp-title">Create your account</div>
            <div class="lp-sub">Join ParkOS and start parking smarter today</div>
            """, unsafe_allow_html=True)

            raw_u = st.text_input("Username", key="reg_user", placeholder="Choose a username", label_visibility="collapsed")
            u = re.sub(r'[^a-zA-Z0-9._]', '', raw_u.replace(' ', '_'))
            if u != raw_u and raw_u:
                st.caption(f"Username will be saved as: **{u}**")

            p = st.text_input("Password", type="password", key="reg_pass", placeholder="Choose a strong password", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", type="primary", use_container_width=True):
                if u.strip() and p.strip():
                    if create_user(u, p):
                        st.success("✅ Account created! Sign in to continue.")
                        st.session_state.auth_mode = 'signin'
                        st.rerun()
                    else:
                        st.error("That username is already taken.")
                else:
                    st.error("Please fill in all fields.")
            
            st.markdown("""<div class="lp-divider">
                <div class="lp-divider-line"></div>
                <div class="lp-divider-text">Already have an account?</div>
                <div class="lp-divider-line"></div>
            </div>""", unsafe_allow_html=True)
            if st.button("← Back to Sign In", type="secondary", use_container_width=True):
                st.session_state.auth_mode = 'signin'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()


# ---------- MAIN APP (LOGGED IN) ----------

# Fetch username if not set
if 'username' not in st.session_state:
    res = supabase.table("users").select("username").eq("id", st.session_state.user_id).execute()
    st.session_state.username = res.data[0]["username"] if res.data else "User"

username = st.session_state.get('username', 'User')
avatar_letter = username[0].upper() if username else "U"

# Initialize click tracker in session state
if 'admin_clicks' not in st.session_state:
    st.session_state.admin_clicks = []

# Header --- Left side HTML only
st.markdown(f"""
<div class="app-header">
    <div class="app-brand">
       <img src="data:image/png;base64,{logo_base64}" style="width:100px;height:100px;object-fit:contain;flex-shrink:0;">
        <div>
            <div class="app-brand-name">ParkOS</div>
            <div class="app-brand-sub">Smart Parking</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) {{ display: none; }}
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) + div[data-testid="stElementContainer"] {{
    position: fixed;
    top: 1.25rem;
    right: 1.5rem;
    z-index: 999;
    width: auto;
}}
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) + div[data-testid="stElementContainer"] button {{
    background: rgba(15,17,23,0.85) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 99px !important;
    padding: 4px 14px 4px 6px !important;
    font-family: var(--font) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--text-2) !important;
    height: 36px !important;
    min-height: 36px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.04) inset !important;
    backdrop-filter: blur(12px) !important;
}}
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) + div[data-testid="stElementContainer"] button:hover {{
    border-color: rgba(99,102,241,0.4) !important;
    color: var(--text-1) !important;
}}
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) + div[data-testid="stElementContainer"] button p {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin: 0 !important;
}}
div[data-testid="stElementContainer"]:has(#profile-pill-tracker) + div[data-testid="stElementContainer"] button p::before {{
    content: '{avatar_letter}';
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6rem;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}}
div[data-testid="stElementContainer"]:has(#signout-tracker) {{ display: none; }}
div[data-testid="stElementContainer"]:has(#signout-tracker) + div[data-testid="stElementContainer"] {{
    position: fixed;
    top: 1.25rem;
    right: 10rem;
    z-index: 999;
    width: auto;
}}
div[data-testid="stElementContainer"]:has(#signout-tracker) + div[data-testid="stElementContainer"] button {{
    background: rgba(15,17,23,0.85) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 99px !important;
    color: #4B5068 !important;
    font-family: var(--font) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 16px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(12px) !important;
}}
div[data-testid="stElementContainer"]:has(#signout-tracker) + div[data-testid="stElementContainer"] button:hover {{
    border-color: rgba(239,68,68,0.3) !important;
    color: #EF4444 !important;
    background: rgba(239,68,68,0.06) !important;
}}
</style>
<div id="profile-pill-tracker"></div>
""", unsafe_allow_html=True)

if st.button(username, key="secret_admin_btn"):
    now = _time.time()
    st.session_state.admin_clicks.append(now)
    st.session_state.admin_clicks = [t for t in st.session_state.admin_clicks if now - t <= 20]
    if len(st.session_state.admin_clicks) >= 10:
        st.query_params["mode"] = "admin"
        st.session_state.admin_clicks = []
        st.rerun()

st.markdown('<div id="signout-tracker"></div>', unsafe_allow_html=True)
if st.button("Sign Out", key="signout_btn"):
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

# Vehicle number gate
if 'vehicle_number' not in st.session_state or st.session_state.vehicle_number is None:
    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-top:1rem;">
        <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-3);margin-bottom:0.5rem;">One-time Setup</div>
        <div style="font-size:1.05rem;font-weight:700;color:var(--text-1);margin-bottom:0.375rem;">Register Your Vehicle</div>
        <div style="font-size:0.82rem;color:var(--text-2);margin-bottom:1.25rem;">Your vehicle number will be linked to all future bookings.</div>
    </div>
    """, unsafe_allow_html=True)
    v = st.text_input("Vehicle Number", placeholder="e.g., TN01 AB1234")
    if st.button("Save & Continue →", type="primary", use_container_width=True):
        if v.strip():
            supabase.table("users").update({"vehicle_number": v.upper()}).eq("id", st.session_state.user_id).execute()
            st.session_state.vehicle_number = v.upper(); st.rerun()
        else:
            st.error("Please enter a valid vehicle number.")
    st.stop()

# ── Current time & Booking Data Load ──
now_dt_fresh_ist = datetime.now(ist_timezone).replace(second=0, microsecond=0)
now_dt = now_dt_fresh_ist
earliest_allowed_dt_ist = get_next_30min_slot_tz(now_dt_fresh_ist)

@st.cache_data(ttl=30, show_spinner=False)
def fetch_bookings(user_id):
    res = supabase.table("bookings").select("id, slot_number, start_datetime, end_datetime").eq("user_id", user_id).order("start_datetime").execute()
    return [(r["id"], r["slot_number"], r["start_datetime"], r["end_datetime"]) for r in res.data]

all_user_bookings = fetch_bookings(st.session_state.user_id)

total_bookings = len(all_user_bookings)
user_current_future = [b for b in all_user_bookings if parse_dt(b[3]) > now_dt]
past_bookings_list = sorted(
    [b for b in all_user_bookings if parse_dt(b[3]) <= now_dt],
    key=lambda x: x[2], reverse=True
)
active_booking = next(
    (b for b in user_current_future if parse_dt(b[2]) <= now_dt <= parse_dt(b[3])), None
)
user_has_active_or_future = bool(user_current_future)
upcoming_count = len([b for b in user_current_future if parse_dt(b[2]) > now_dt])

# ── Overview ──
st.markdown('<div style="height:4rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

# Stats row
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Total Bookings</div>
        <div class="stat-value accent">{total_bookings}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Upcoming</div>
        <div class="stat-value green">{upcoming_count}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Active session
if active_booking:
    _, slot_num, start_str, end_str = active_booking
    end_dt = parse_dt(end_str)
    start_dt_active = parse_dt(start_str)
    remaining = end_dt - now_dt
    remaining_str = str(remaining).split('.')[0]
    end_ts_ms = int(end_dt.timestamp() * 1000)

    st.markdown(f"""
    <div class="active-card">
        <div class="active-card-glow"></div>
        <div class="active-badge"><span class="active-dot"></span> Active Session</div>
        <div class="vehicle-chip">&#128663; {st.session_state.vehicle_number}</div>
        <div class="active-slot-display">
            <div>
                <div class="active-slot-label">Slot</div>
                <div class="active-slot-num">{slot_num}</div>
            </div>
            <div class="active-time-block">
                <div class="active-time-label">Parked until</div>
                <div class="active-time-val">{end_dt.strftime('%I:%M %p')}</div>
                <div style="font-size:0.65rem;color:var(--text-3);margin-top:2px;">{end_dt.strftime('%b %d')}</div>
            </div>
        </div>
        <div class="active-remaining-bar">
            <span class="remaining-label">&#9201; Time remaining</span>
            <span class="remaining-val" id="parkos-countdown">{remaining_str}</span>
        </div>
    </div>
    <script>
    (function() {{
        var endMs = {end_ts_ms};
        function pad(n) {{ return String(n).padStart(2, "0"); }}
        function tick() {{
            var el = document.getElementById("parkos-countdown");
            if (!el) {{ setTimeout(tick, 100); return; }}
            var diff = Math.max(0, Math.floor((endMs - Date.now()) / 1000));
            var h = Math.floor(diff / 3600);
            var m = Math.floor((diff % 3600) / 60);
            var s = diff % 60;
            el.textContent = pad(h) + ":" + pad(m) + ":" + pad(s);
            el.style.color = diff < 300 ? "#EF4444" : "#10B981";
            if (diff === 0) {{ setTimeout(function(){{ window.parent.location.reload(); }}, 2000); return; }}
            setTimeout(tick, 1000);
        }}
        if (document.readyState === "loading") {{
            document.addEventListener("DOMContentLoaded", tick);
        }} else {{
            tick();
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-card">
        <div class="empty-icon">🅿️</div>
        <div class="empty-title">No Active Session</div>
        <div class="empty-sub">Park now using the booking section below</div>
    </div>
    """, unsafe_allow_html=True)

# ── Live Parking Sensor View ──
st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Live Parking Status</div>', unsafe_allow_html=True)

render_live_parking()

# ── Bookings ──
st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Your Bookings</div>', unsafe_allow_html=True)

if user_current_future:
    for booking_id, slot_number, start_dt_str, end_dt_str in user_current_future:
        start_dt_obj = parse_dt(start_dt_str)
        end_dt_obj = parse_dt(end_dt_str)
        is_active_b = (start_dt_obj <= now_dt <= end_dt_obj)

        badge_class = "pill-active" if is_active_b else "pill-upcoming"
        badge_text = "Active" if is_active_b else "Upcoming"
        slot_class = "slot-badge active" if is_active_b else "slot-badge"
        btn_label = "End Early" if is_active_b else "Cancel"
        btn_key = f"{'end' if is_active_b else 'cancel'}_booking_{booking_id}"

        col_info, col_btn = st.columns([4, 1])
        with col_info:
            st.markdown(f"""
            <div class="booking-card">
                <div class="booking-card-inner">
                    <div class="{slot_class}">{slot_number}</div>
                    <div class="booking-info">
                        <span class="status-pill {badge_class}">{badge_text}</span>
                        <div class="booking-time-text">{start_dt_obj.strftime('%I:%M %p')} → {end_dt_obj.strftime('%I:%M %p')}</div>
                        <div class="booking-date-text">{start_dt_obj.strftime('%b %d, %Y')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            if st.button(btn_label, key=btn_key, type="secondary", use_container_width=True):
                if st.session_state.get(f"confirm_{btn_key}", False):
                    supabase.table("bookings").delete().eq("id", booking_id).execute()
                    st.cache_data.clear()
                    del st.session_state[f"confirm_{btn_key}"]
                    st.session_state.selected_slot = None
                    st.rerun()
                else:
                    st.session_state[f"confirm_{btn_key}"] = True
                    st.warning("Tap again to confirm.")
else:
    st.markdown('<div class="empty-card" style="padding:1.25rem;"><div class="empty-sub">No current or upcoming bookings.</div></div>', unsafe_allow_html=True)

# Past bookings
if past_bookings_list:
    with st.expander(f"📋 Booking History ({len(past_bookings_list)})"):
        for _, slot_number, start_dt_str, end_dt_str in past_bookings_list:
            s = parse_dt(start_dt_str)
            e = parse_dt(end_dt_str)
            st.markdown(f"""
            <div class="booking-card" style="opacity:0.55;">
                <div class="booking-card-inner">
                    <div class="slot-badge" style="color:var(--text-3);">{slot_number}</div>
                    <div class="booking-info">
                        <span class="status-pill pill-completed">Completed</span>
                        <div class="booking-time-text">{s.strftime('%I:%M %p')} → {e.strftime('%I:%M %p')}</div>
                        <div class="booking-date-text">{s.strftime('%b %d, %Y')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Book New Slot ──
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if not user_has_active_or_future:
    st.markdown('<div class="section-label">New Booking</div>', unsafe_allow_html=True)

    # Step 1
    st.markdown("""
    <div class="step-wrap">
        <span class="step-num">1</span>
        <span class="step-title">Select parking window</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div>', unsafe_allow_html=True)
    booking_date = st.date_input("Date", min_value=now_dt_fresh_ist.date(), key="booking_date_input")

    entry_options = build_time_options(booking_date, now_ist=now_dt_fresh_ist)
    if not entry_options:
        st.warning("No available time slots for today. Please select a future date.")
        st.stop()

    entry_labels = [label for label, _ in entry_options]
    entry_times = [t for _, t in entry_options]

    col_en, col_ex = st.columns(2)
    with col_en:
        entry_label = st.selectbox("Entry Time", entry_labels, index=0, key="entry_select")
    selected_entry_time = entry_times[entry_labels.index(entry_label)]
    start_dt = ist_timezone.localize(datetime.combine(booking_date, selected_entry_time))

    # Exit: 30-min slots strictly after entry time
    all_exit_slots = [(datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").strftime("%I:%M %p"),
                       datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                      for h in range(24) for m in (0, 30)]
    exit_options = [(label, t) for label, t in all_exit_slots if t > selected_entry_time]
    if not exit_options:
        exit_options = all_exit_slots  # wrap to next day
    exit_labels = [label for label, _ in exit_options]
    exit_times = [t for _, t in exit_options]

    with col_ex:
        default_exit_idx = min(3, len(exit_labels) - 1)
        exit_label = st.selectbox("Exit Time", exit_labels, index=default_exit_idx, key="exit_select")
    st.markdown('</div>', unsafe_allow_html=True)

    selected_exit_time = exit_times[exit_labels.index(exit_label)]
    end_dt = ist_timezone.localize(datetime.combine(booking_date, selected_exit_time))

    next_day_note = False
    if selected_exit_time <= selected_entry_time:
        end_dt += timedelta(days=1)
        next_day_note = True

    if start_dt < now_dt_fresh_ist:
        st.markdown('<div class="warn-note">⚠️ Entry time is in the past. Please select a current or future time.</div>', unsafe_allow_html=True)
        st.stop()

    if next_day_note:
        st.markdown('<div class="warn-note">⚠️ Exit time is before entry --- booking extends to the next day.</div>', unsafe_allow_html=True)

    # Step 2 (Zone Selection)
    st.markdown("""
    <div class="step-wrap" style="margin-top:1.25rem;">
        <span class="step-num">2</span>
        <span class="step-title">Choose a Parking Zone</span>
    </div>
    """, unsafe_allow_html=True)

    selected_zone = st.radio("Select Zone", ["Zone A", "Zone B", "Zone C"], horizontal=True, label_visibility="collapsed")

    # Step 3 (Slot Selection)
    st.markdown("""
    <div class="step-wrap" style="margin-top:1.5rem;">
        <span class="step-num">3</span>
        <span class="step-title">Choose an available slot</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="slot-legend">
        <div class="legend-item"><div class="legend-dot legend-free"></div> Available</div>
        <div class="legend-item"><div class="legend-dot legend-busy"></div> Occupied</div>
        <div class="legend-item"><div class="legend-dot legend-selected"></div> Selected</div>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data(ttl=15, show_spinner=False)
    def fetch_blocked(start_str, end_str):
        _bl = supabase.table("bookings").select("slot_number, start_datetime, end_datetime").execute()
        return {r["slot_number"] for r in _bl.data
                if not (r["end_datetime"] <= start_str or r["start_datetime"] >= end_str)}

    # 1. Get real bookings from Supabase
    db_blocked = fetch_blocked(start_dt.strftime("%Y-%m-%d %H:%M"), end_dt.strftime("%Y-%m-%d %H:%M"))
    
    # 2. Get the current simulated "Occupied" (red) slots from the sensor
    z_a, z_b, z_c = _get_sensor_state()
    simulated_blocked = {slot for z in (z_a, z_b, z_c) for slot, is_occupied in z.items() if is_occupied}
    
    # 3. Combine them! Both Supabase bookings AND visual red slots are blocked.
    blocked = db_blocked.union(simulated_blocked)

    # Map the selected zone to its specific layout
    zone_configs = {
        "Zone A": {"prefix": "A", "rows": 3, "cols": 4},
        "Zone B": {"prefix": "B", "rows": 4, "cols": 3},
        "Zone C": {"prefix": "C", "rows": 2, "cols": 6},
    }
    
    current_conf = zone_configs[selected_zone]
    z_prefix = current_conf["prefix"]
    z_rows = current_conf["rows"]
    z_cols = current_conf["cols"]

    # Clear selected slot if the user switches zones
    if st.session_state.selected_slot and not st.session_state.selected_slot.startswith(z_prefix):
        st.session_state.selected_slot = None

    selected = st.session_state.selected_slot or ""

    def handle_slot_click(slot_name):
        if st.session_state.selected_slot == slot_name:
            st.session_state.selected_slot = None
        else:
            st.session_state.selected_slot = slot_name

    st.markdown("""<style>
/* Force slot columns horizontal */
[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) { flex-wrap: nowrap !important; overflow: hidden !important; }
[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) > div { min-width: 0 !important; flex: 1 !important; }
[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button { height: 36px !important; font-size: 0.62rem !important; padding: 0 !important; min-height: unset !important; white-space: nowrap !important; }
[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) { flex-wrap: nowrap !important; overflow: hidden !important; }
[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) > div { min-width: 0 !important; flex: 1 !important; }
[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) button { height: 36px !important; font-size: 0.62rem !important; padding: 0 !important; min-height: unset !important; }

/* Style the radio buttons to look like clickable boxes */
div[role="radiogroup"] { gap: 1rem; margin-bottom: 0.5rem; }
div[role="radiogroup"] label { background: var(--surface-2); border: 1px solid var(--border); padding: 0.5rem 1.25rem; border-radius: var(--radius-sm); transition: all 0.2s; cursor: pointer; }
div[role="radiogroup"] label:hover { border-color: var(--accent); }
div[role="radiogroup"] label[data-checked="true"] { background: rgba(99,102,241,0.1); border-color: var(--accent); }
</style>""", unsafe_allow_html=True)

    # Render only the slots for the currently selected zone
    for r in range(1, z_rows + 1):
        st.markdown(f'<div class="row-label">Row {r}</div>', unsafe_allow_html=True)
        cols = st.columns(z_cols)
        for c in range(1, z_cols + 1):
            s = f"{z_prefix}{r}{c}"
            with cols[c - 1]:
                is_blocked = s in blocked
                is_selected = (s == selected)
                if is_blocked:
                    st.markdown(f'<div style="height:36px;border-radius:8px;border:none;background:linear-gradient(135deg,#EF4444 0%,#F87171 100%);color:#fff;font-size:0.88rem;font-weight:600;display:flex;align-items:center;justify-content:center;font-family:Outfit,sans-serif;letter-spacing:0.01em;box-shadow:0 4px 20px rgba(239,68,68,0.25);">{s}</div>', unsafe_allow_html=True)
                elif is_selected:
                    st.button(s, key=f"slot_{s}", on_click=handle_slot_click, args=(s,), type="primary", use_container_width=True)
                else:
                    st.button(s, key=f"slot_{s}", on_click=handle_slot_click, args=(s,), use_container_width=True)
                    
    if st.session_state.selected_slot:
        current_blocked = fetch_blocked(start_dt.strftime("%Y-%m-%d %H:%M"), end_dt.strftime("%Y-%m-%d %H:%M"))
        if st.session_state.selected_slot in current_blocked:
            st.session_state.selected_slot = None
            st.rerun()
        else:
            st.markdown(f"""
            <div class="confirm-banner">
                <div style="font-size:0.65rem;color:var(--text-3);font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2px;">Selected Slot</div>
                <div class="confirm-slot-big">{st.session_state.selected_slot}</div>
                <div class="confirm-time">{start_dt.strftime('%b %d · %I:%M %p')} → {end_dt.strftime('%I:%M %p')}</div>
            </div>
            """, unsafe_allow_html=True)
            confirm_clicked = st.button("Confirm Booking →", type="primary", use_container_width=True)
            if confirm_clicked:
                if start_dt < now_dt_fresh_ist:
                    st.error("Your selected start time has just passed. Please pick a new time.")
                    st.session_state.selected_slot = None
                    st.rerun()
                else:
                    try:
                        supabase.table("bookings").insert({
                            "user_id": st.session_state.user_id,
                            "slot_number": st.session_state.selected_slot,
                            "start_datetime": start_dt.strftime("%Y-%m-%d %H:%M"),
                            "end_datetime": end_dt.strftime("%Y-%m-%d %H:%M")
                        }).execute()
                        st.cache_data.clear()
                        st.success(f"✅ Slot {st.session_state.selected_slot} booked successfully!")
                        st.session_state.selected_slot = None
                        st.rerun()
                    except Exception:
                        st.error(f"Failed to book slot {st.session_state.selected_slot}. It may have just been taken.")
                        st.session_state.selected_slot = None
                        st.rerun()
else:
    st.markdown("""
    <div class="lock-card">
        <div class="lock-icon">🔒</div>
        <div class="lock-title">Booking Locked</div>
        <div class="lock-sub">You have an active or upcoming booking.<br>Manage your existing sessions above to make a new booking.</div>
    </div>
    """, unsafe_allow_html=True)
