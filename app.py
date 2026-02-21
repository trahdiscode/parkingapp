import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime, date, timedelta
import pytz
import base64

# ---------- LOGO ----------
# This is a base64 encoded transparent PNG of a simple parking icon with a subtle gradient.
# It's intended to blend well with a dark theme.
LOGO_B64_DATA = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAADmPMawAAACuElEQVR4Xu2Zz0pDQRSFPxV3B1Uf4QJKQXBx4U5y4s38zCduxIX/JbS4cBIuDpy7yN0JtLhQXCkXg0Fw2F0302o4C+d9h8yZk9nZzJy392bMmy/TZrM+JzPfzBkiEAIkgQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkAQEkASgX/JkSg/bC6QAAAAASUVORK5CYII="

# Convert to base64 for embedding in CSS
LOGO_B64 = f"data:image/png;base64,{base64.b64encode(open('logo.png', 'rb').read()).decode()}"

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="ParkOS", layout="wide", page_icon="🅿️", initial_sidebar_state="collapsed")

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
html, body,.stApp {
    background: var(--bg)!important;
    font-family: var(--font);
    color: var(--text-1);
}

/* ── Kill Streamlit's rerun fade/flicker ── */
.stApp > div,.main,.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="element-container"],
iframe,.stMarkdown,.stButton,
.stTextInput,.stSelectbox,.stDateInput {
    animation: none!important;
    transition: none!important;
    opacity: 1!important;
}
/* Streamlit skeleton loader — hide it */
[data-testid="stSkeleton"] { display: none!important; }
/* Remove the white flash on rerun */
.stApp [data-stale="true"] { opacity: 1!important; }
.stApp [data-stale="true"] * { opacity: 1!important; }
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: var(--bg-grad);
    pointer-events: none;
    z-index: 0;
}
.main.block-container {
    padding: 2rem 1.25rem 4rem!important;
    max-width: 480px!important;
    margin: 0 auto!important;
    position: relative;
    z-index: 1;
}
/* Streamlit injects 6rem top padding internally — kill it */
.block-container { padding-top: 2rem!important; }
section.main > div.block-container { padding-top: 2rem!important; }
div[data-testid="stAppViewBlockContainer"] { padding-top: 2rem!important; }

/* Desktop layout */
@media (min-width: 769px) {
   .main.block-container {
        padding: 2rem 2rem 4rem!important;
        max-width: 900px!important;
    }
}

p, li { color: var(--text-1); font-size: 0.9rem; line-height: 1.6; }

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 9999px; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton, div[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
div[data-testid="stToolbar"] { display: none; }
div[data-testid="stHeader"] { display: none!important; height: 0!important; }
div[data-testid="stStatusWidget"] { display: none; }
div[data-testid="collapsedControl"] { display: none; }

h1, h2, h3, h4 { font-family: var(--font); letter-spacing: -0.02em; }

/* ── Section label ── */
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── App Header ── */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 0.5rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.app-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.app-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    box-shadow: var(--shadow-accent);
}
.app-brand-name {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-1);
    letter-spacing: -0.04em;
    line-height: 1;
}
.app-brand-sub {
    font-size: 0.58rem;
    font-weight: 600;
    color: var(--text-3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    line-height: 1;
    margin-top: 2px;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
/* Sign Out — compact power icon button */
[data-testid="column"]:last-child.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(239,68,68,0.07) 100%)!important;
    border: 1px solid rgba(239,68,68,0.4)!important;
    color: #FCA5A5!important;
    -webkit-text-fill-color: #FCA5A5!important;
    font-size: 1.1rem!important;
    font-weight: 400!important;
    min-height: 36px!important;
    max-height: 36px!important;
    width: 36px!important;
    border-radius: 10px!important;
    box-shadow: 0 2px 12px rgba(239,68,68,0.15), inset 0 1px 0 rgba(255,255,255,0.05)!important;
    transition: all 0.18s ease!important;
    padding: 0!important;
    line-height: 1!important;
    display: flex!important;
    align-items: center!important;
    justify-content: center!important;
}
[data-testid="column"]:last-child.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(135deg, rgba(239,68,68,0.28) 0%, rgba(239,68,68,0.15) 100%)!important;
    border-color: rgba(239,68,68,0.7)!important;
    color: #fff!important;
    -webkit-text-fill-color: #fff!important;
    box-shadow: 0 4px 20px rgba(239,68,68,0.3)!important;
    transform: translateY(-1px)!important;
}
.user-pill {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 99px;
    padding: 5px 12px 5px 6px;
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--text-2);
}
.user-avatar {
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6rem;
    font-weight: 700;
    color: white;
}

/* ── Active session card ── */
.active-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, var(--surface) 60%);
    border: 1px solid var(--green-border);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.active-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--green), transparent 60%);
}
.active-card-glow {
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.active-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    background: var(--green-soft);
    border: 1px solid var(--green-border);
    padding: 3px 8px;
    border-radius: 99px;
    margin-bottom: 0.75rem;
}
.active-dot {
    width: 6px; height: 6px;
    background: var(--green);
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px var(--green);
}
.active-slot-display {
    display: flex;
    align-items: flex-end;
    gap: 0.75rem;
    margin: 0.5rem 0 0.75rem;
}
.active-slot-label {
    font-size: 0.65rem;
    color: var(--text-3);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.active-slot-num {
    font-family: var(--font-mono);
    font-size: 3rem;
    font-weight: 600;
    color: var(--text-1);
    line-height: 1;
}
.active-time-block {
    flex: 1;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.5rem 0.75rem;
}
.active-time-label { font-size: 0.6rem; color: var(--text-3); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
.active-time-val { font-family: var(--font-mono); font-size: 0.95rem; color: var(--text-1); font-weight: 500; }
.active-remaining-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 0.875rem;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    margin-top: 0.25rem;
}
.remaining-label { font-size: 0.7rem; color: var(--text-3); font-weight: 500; flex: 1; }
.remaining-val { font-family: var(--font-mono); font-size: 0.9rem; color: var(--green); font-weight: 600; }
.vehicle-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 3px 8px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-2);
    margin-bottom: 0.75rem;
}

/* ── Stats row ── */
.stats-row {
    margin-bottom: 0.875rem;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.625rem;
    margin-bottom: 1.25rem;
}
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.125rem;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 40px; height: 40px;
    border-radius: 50%;
    background: var(--accent-soft);
    transform: translate(10px, 10px);
}
.stat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 0.35rem;
}
.stat-value {
    font-family: var(--font-mono);
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--text-1);
    line-height: 1;
}
.stat-value.accent { color: var(--accent-2); }
.stat-value.green { color: var(--green); }

/* ── Empty state ── */
.empty-card {
    background: var(--surface);
    border: 1px dashed var(--border-hover);
    border-radius: var(--radius);
    padding: 2rem 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.empty-title { font-size: 0.9rem; font-weight: 600; color: var(--text-2); margin-bottom: 0.25rem; }
.empty-sub { font-size: 0.78rem; color: var(--text-3); }

/* ── Booking items ── */
.booking-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 0.625rem;
    transition: border-color 0.2s;
}
.booking-card:hover { border-color: var(--border-hover); }
.booking-card-inner {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 0.875rem;
    padding: 0.875rem 1rem;
}
.slot-badge {
    width: 48px;
    height: 48px;
    background: var(--surface-3);
    border: 1px solid var(--border);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-1);
    flex-shrink: 0;
}
.slot-badge.active { background: var(--green-soft); border-color: var(--green-border); color: var(--green); }
.booking-info { min-width: 0; }
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 7px;
    border-radius: 99px;
    margin-bottom: 4px;
}
.pill-active { background: var(--green-soft); color: var(--green); border: 1px solid var(--green-border); }
.pill-upcoming { background: var(--accent-soft); color: var(--accent-2); border: 1px solid rgba(99,102,241,0.2); }
.pill-completed { background: var(--surface-2); color: var(--text-3); border: 1px solid var(--border); }
.booking-time-text {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-2);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.booking-date-text {
    font-size: 0.7rem;
    color: var(--text-3);
    margin-top: 1px;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Step header ── */
.step-wrap {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    margin-bottom: 1rem;
}
.step-num {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--accent-soft);
    border: 1px solid rgba(99,102,241,0.25);
    color: var(--accent-2);
    font-size: 0.7rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-title { font-size: 0.875rem; font-weight: 600; color: var(--text-2); }

/* ── Time pickers ── */
.time-form {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin-bottom: 1rem;
}

/* ── Slot legend ── */
.slot-legend {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.875rem;
    flex-wrap: wrap;
}
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 0.72rem; color: var(--text-2); }
.legend-dot { width: 8px; height: 8px; border-radius: 3px; flex-shrink: 0; }
.legend-free { background: var(--green); }
.legend-busy { background: var(--red); }
.legend-selected { background: var(--accent); }

/* ── Row label ── */
.row-label {
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-3);
    font-weight: 700;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.row-label::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 10px;
    background: var(--accent);
    border-radius: 99px;
}

/* ── Confirm banner ── */
.confirm-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, var(--surface) 60%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.confirm-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent 60%);
}
.confirm-slot-big {
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 600;
    color: var(--text-1);
    line-height: 1;
    margin: 0.25rem 0;
}
.confirm-time {
    font-size: 0.78rem;
    color: var(--text-2);
    font-family: var(--font-mono);
}

/* ── Warning / note ── */
.warn-note {
    font-size: 0.78rem;
    color: var(--amber);
    background: var(--amber-soft);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: var(--radius-sm);
    padding: 0.625rem 1rem;
    margin-top: 0.625rem;
}
.lock-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 1.25rem;
    text-align: center;
}
.lock-icon { font-size: 1.75rem; margin-bottom: 0.5rem; }
.lock-title { font-size: 0.95rem; font-weight: 600; color: var(--text-2); margin-bottom: 0.375rem; }
.lock-sub { font-size: 0.78rem; color: var(--text-3); line-height: 1.5; }

/* ── Login page ── */
.login-wrap {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
}
.login-card {
    width: 100%;
    max-width: 380px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: calc(var(--radius) * 1.5);
    padding: 2rem;
    box-shadow: var(--shadow-lg);
}
.login-logo {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    margin-bottom: 0.25rem;
}
.login-logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    box-shadow: var(--shadow-accent);
}
.login-logo-text {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: var(--text-1);
}
.login-tagline { font-size: 0.78rem; color: var(--text-3); margin-bottom: 1.75rem; }

/* ── Streamlit overrides ── */
.stTextInput > label,.stDateInput > label,.stTimeInput > label,.stSelectbox > label {
    font-family: var(--font)!important;
    font-size: 0.7rem!important;
    font-weight: 700!important;
    letter-spacing: 0.08em!important;
    text-transform: uppercase!important;
    color: var(--text-3)!important;
    margin-bottom: 4px!important;
}
.stTextInput input,.stDateInput input,.stTimeInput input {
    background: var(--surface-2)!important;
    border: 1px solid var(--border)!important;
    border-radius: var(--radius-sm)!important;
    color: var(--text-1)!important;
    font-family: var(--font-mono)!important;
    font-size: 0.9rem!important;
    padding: 0.625rem 0.875rem!important;
    transition: border-color 0.2s, box-shadow 0.2s!important;
    min-height: 44px!important;
}
.stTextInput input:focus,.stDateInput input:focus {
    border-color: var(--accent)!important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important;
    outline: none!important;
}
/* Override BaseWeb's red/pink focus ring on input containers */
.stTextInput > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--accent)!important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important;
    outline: none!important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within {
    border-color: var(--accent)!important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important;
    outline: none!important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="base-input"] input:focus {
    outline: none!important;
    box-shadow: none!important;
}
/* Kill any red/pink coming from BaseWeb theme */
[data-baseweb="input"] { border-color: var(--border)!important; }
[data-baseweb="input"]:focus-within { border-color: var(--accent)!important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15)!important; }

/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--surface-2)!important;
    border: 1px solid var(--border)!important;
    border-radius: var(--radius-sm)!important;
    color: var(--text-1)!important;
    min-height: 44px!important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent)!important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12)!important;
}
div[data-baseweb="popover"] { background: var(--surface-2)!important; border: 1px solid var(--border)!important; border-radius: var(--radius)!important; }
[data-baseweb="menu"] { background: var(--surface-2)!important; }
[data-baseweb="option"] { background: var(--surface-2)!important; color: var(--text-1)!important; font-size: 0.88rem!important; }
[data-baseweb="option"]:hover, [aria-selected="true"] { background: var(--surface-3)!important; }

/* Buttons */
.stButton > button {
    font-family: var(--font)!important;
    font-size: 0.88rem!important;
    font-weight: 600!important;
    border-radius: var(--radius-sm)!important;
    transition: all 0.18s ease!important;
    min-height: 44px!important;
    letter-spacing: 0.01em!important;
    touch-action: manipulation!important;
    -webkit-tap-highlight-color: transparent!important;
}
.stButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--accent) 0%, #818CF8 100%)!important;
    border: none!important;
    color: #fff!important;
    box-shadow: var(--shadow-accent)!important;
    -webkit-tap-highlight-color: transparent!important;
    touch-action: manipulation!important;
}
[data-testid="stFormSubmitButton"] > button:active {
    transform: scale(0.97)!important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3)!important;
    transition: transform 0.08s ease, box-shadow 0.08s ease!important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 24px rgba(99,102,241,0.4)!important;
    transform: translateY(-1px)!important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface)!important;
    border: 1px solid var(--border)!important;
    color: var(--text-2)!important;
    font-size: 0.78rem!important;
    min-height: 34px!important;
    padding: 0 0.75rem!important;
    text-decoration: none!important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent)!important;
    color: var(--accent)!important;
    background: var(--accent-soft)!important;
    text-decoration: none!important;
}

/* Slot buttons */
.stButton > button[key*="slot_"] {
    height: 48px!important;
    font-family: var(--font-mono)!important;
    font-size: 0.8rem!important;
    font-weight: 600!important;
    padding: 0!important;
}
.stButton > button[key*="slot_"]:hover {
    border-color: #3B82F6!important;
    color: #3B82F6!important;
    background: rgba(59,130,246,0.08)!important;
}
.stButton > button[key*="slot_"]:disabled {
    border-color: #EF4444!important;
    color: #EF4444!important;
    background: rgba(239,68,68,0.08)!important;
    opacity: 1!important;
    cursor: not-allowed!important;
}

/* Alerts */
div[data-testid="stAlert"] {
    background: var(--surface)!important;
    border-radius: var(--radius)!important;
    border: 1px solid var(--border)!important;
    font-size: 0.85rem!important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: var(--surface)!important;
    border: 1px solid var(--border)!important;
    border-radius: var(--radius)!important;
    padding: 1rem 1.25rem!important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface)!important;
    border: 1px solid var(--border)!important;
    border-radius: var(--radius-sm)!important;
    padding: 3px!important;
    gap: 2px!important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent!important;
    border: none!important;
    color: var(--text-2)!important;
    font-size: 0.85rem!important;
    font-weight: 600!important;
    padding: 0.5rem 1rem!important;
    border-radius: var(--radius-xs)!important;
    transition: all 0.2s!important;
    flex: 1!important;
    text-align: center!important;
    justify-content: center!important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-1)!important; }
.stTabs [aria-selected="true"] {
    background: var(--surface-3)!important;
    color: var(--text-1)!important;
    box-shadow: var(--shadow-sm)!important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.25rem!important; }

div[data-testid="stHorizontalBlock"] { gap: 0.4rem!important; }
/* Tighten the default gap between Streamlit elements */
div[data-testid="stVerticalBlock"] { gap: 0.5rem!important; }
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlock"] > div[data-testid="element-container"] { margin-bottom: 0!important; }

/* Expander */
details { border: 1px solid var(--border)!important; border-radius: var(--radius)!important; background: var(--surface)!important; }
summary { padding: 0.875rem 1rem!important; font-size: 0.85rem!important; color: var(--text-2)!important; font-weight: 600!important; }

/* Date input */
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

@st.cache_data(ttl=30, show_spinner=False)
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
    if for_date == now_ist.date() and now_ist is not None:
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

# ---------- SESSION STATE ----------
if 'selected_slot' not in st.session_state:
    st.session_state.selected_slot = None

# ---------- AUTH PAGE ----------
if 'user_id' not in st.session_state or st.session_state.user_id is None:

    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'signin'

    st.markdown(f"""
    <div class="login-wrap">
    <div class="lp-card">
        <div class="lp-top">
            <img class="lp-logo" src="{LOGO_B64}" />
            <div>
                <div class="lp-brand-name">ParkOS</div>
                <div class="lp-brand-sub">Smart Parking Management</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_mode == 'signin':
        st.markdown("""
        <div class="lp-title">Welcome back</div>
        <div class="lp-sub">Sign in to manage your parking sessions</div>
        """, unsafe_allow_html=True)

        @st.fragment
        def login_fragment():
            with st.form("login_form"):
                u = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
            if submitted:
                user = get_user(u, p)
                if user:
                    st.session_state.user_id = user[0]
                    st.session_state.vehicle_number = user[1]
                    st.session_state.username = u
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

        login_fragment()
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

        @st.fragment
        def register_fragment():
            import re
            with st.form("register_form"):
                raw_u = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Choose a strong password", label_visibility="collapsed")
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                reg_submitted = st.form_submit_button("Create Account →", type="primary", use_container_width=True)
            u = re.sub(r'[^a-zA-Z0-9._]', '', raw_u.replace(' ', '_'))
            if u!= raw_u and raw_u:
                st.caption(f"Username will be saved as: **{u}**")
            if reg_submitted:
                if u.strip() and p.strip():
                    if create_user(u, p):
                        st.success("✅ Account created! Sign in to continue.")
                        st.session_state.auth_mode = 'signin'
                        st.rerun()
                    else:
                        st.error("That username is already taken.")
                else:
                    st.error("Please fill in all fields.")

        register_fragment()

        st.markdown("""<div class="lp-divider">
            <div class="lp-divider-line"></div>
            <div class="lp-divider-text">Already have an account?</div>
            <div class="lp-divider-line"></div>
        </div>""", unsafe_allow_html=True)
        if st.button("← Back to Sign In", type="secondary", use_container_width=True):
            st.session_state.auth_mode = 'signin'
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Feature highlights below card
    st.markdown("""
    <div class="lp-features">
        <div class="lp-feature"><div class="lp-feature-dot"></div>Real-time slot availability across all rows</div>
        <div class="lp-feature"><div class="lp-feature-dot"></div>Instant booking with live countdown timer</div>
        <div class="lp-feature"><div class="lp-feature-dot"></div>Secure, private & IST timezone-aware sessions</div>
    </div>
    <div class="lp-footer">© 2025 ParkOS · All rights reserved</div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ---------- MAIN APP ----------

# Fetch username if not set
if 'username' not in st.session_state:
    res = supabase.table("users").select("username").eq("id", st.session_state.user_id).execute()
    st.session_state.username = res.data[0]["username"] if res.data else "User"

username = st.session_state.get('username', 'User')
avatar_letter = username[0].upper() if username else "U"

# Header: brand left, user pill + sign out right
col_hdr, col_pill, col_so = st.columns([5, 2, 1])
with col_hdr:
    st.markdown(f'''<div class="app-brand" style="padding:0.6rem 0 0.4rem;">
    <img src="{LOGO_B64}" style="width:36px;height:36px;object-fit:contain;flex-shrink:0;filter:drop-shadow(0 2px 8px rgba(99,102,241,0.3));" />
    <div><div class="app-brand-name">ParkOS</div><div class="app-brand-sub">Smart Parking</div></div>
</div>''', unsafe_allow_html=True)
with col_pill:
    st.markdown(f'''<div style="display:flex;align-items:center;justify-content:flex-end;padding:0.6rem 0 0.4rem;">
    <div class="user-pill"><div class="user-avatar">{avatar_letter}</div>{username}</div>
</div>''', unsafe_allow_html=True)
with col_so:
    st.markdown('<div style="padding-top:0.55rem;">', unsafe_allow_html=True)
    if st.button("⏻", key="signout_btn", type="secondary", use_container_width=True, help="Sign Out"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="border-bottom:1px solid var(--border);margin-bottom:0.875rem;"></div>', unsafe_allow_html=True)

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

# ── Current time ──
now_dt_fresh_ist = datetime.now(ist_timezone).replace(second=0, microsecond=0)
now_dt = now_dt_fresh_ist
earliest_allowed_dt_ist = get_next_30min_slot_tz(now_dt_fresh_ist)

# ── Fetch bookings (cached for 30s to reduce Supabase calls) ──
@st.cache_data(ttl=20, show_spinner=False)
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
st.markdown('<div class="section-label" style="margin-top:1.25rem;">Overview</div>', unsafe_allow_html=True)

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
    remaining_str = str(remaining).split(".")[0]
    end_ts_ms = int(end_dt.timestamp() * 1000)

    # Everything in one st.markdown — no iframe, no flash
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
            el.style.color = diff < 300? "#EF4444" : "#10B981";
            if (diff === 0) {{ setTimeout(function(){{ window.parent.location.reload(); }}, 2000); return; }}
            setTimeout(tick, 1000);
        }}
        // Wait for DOM then start
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

# ── Bookings ──
st.markdown('<hr class="divider" style="margin:1.25rem 0 1rem;">', unsafe_allow_html=True)
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
st.markdown('<hr class="divider" style="margin:1.25rem 0 1rem;">', unsafe_allow_html=True)

if not user_has_active_or_future:
    st.markdown('<div class="section-label">New Booking</div>', unsafe_allow_html=True)

    # Step 1
    st.markdown("""
    <div class="step-wrap">
        <span class="step-num">1</span>
        <span class="step-title">Select parking window</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="time-form">', unsafe_allow_html=True)
    today_ist = now_dt_fresh_ist.date()
    booking_date = st.date_input("Date", value=today_ist, min_value=today_ist, key="booking_date_input")

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
    # If entry is "Now" (current minute), build exits from next 30-min boundary onwards
    all_exit_slots = [(datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").strftime("%I:%M %p"),
                       datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                      for h in range(24) for m in (0, 30)]
    exit_options = [(label, t) for label, t in all_exit_slots if t > selected_entry_time]
    if not exit_options:
        exit_options = all_exit_slots # wrap to next day
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
        st.markdown('<div class="warn-note">⚠️ Entry time is in the
