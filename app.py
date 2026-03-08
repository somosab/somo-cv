"""
╔══════════════════════════════════════════════════════════════╗
║     EA SPORTS FC MOBILE — HAQIQIY O'YIN DIZAYNI             ║
║     Somosab | OVR 121 | Real Madrid                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import math
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════
st.set_page_config(
    page_title="FC Mobile – Somosab",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════
#  GLOBAL CSS — FC MOBILE DARK THEME
# ══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Barlow:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0c10 !important;
    color: #e8e8e8 !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="collapsedControl"] { display: none !important; }

/* ── TOP NAV BAR ── */
.fc-topbar {
    background: linear-gradient(180deg, #111520 0%, #0d1018 100%);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky; top: 0; z-index: 100;
}
.fc-profile-info { display: flex; align-items: center; gap: 12px; }
.fc-avatar {
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg, #1a6b2e, #0d4a1f);
    border: 2px solid #22c55e;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; color: white; font-weight: 900;
}
.fc-username { font-size: 15px; font-weight: 700; color: #f0f0f0; }
.fc-level-bar-wrap { display: flex; align-items: center; gap: 6px; }
.fc-level-num { font-size: 11px; color: #22c55e; font-weight: 700; }
.fc-level-bar {
    width: 80px; height: 5px; background: rgba(255,255,255,0.1);
    border-radius: 3px; overflow: hidden;
}
.fc-level-fill {
    height: 100%; border-radius: 3px;
    background: linear-gradient(90deg, #22c55e, #16a34a);
}
.fc-currencies { display: flex; gap: 14px; align-items: center; }
.fc-coin {
    display: flex; align-items: center; gap: 5px;
    background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25);
    border-radius: 20px; padding: 4px 10px;
}
.fc-gem {
    display: flex; align-items: center; gap: 5px;
    background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px; padding: 4px 10px;
}
.fc-coin-val { font-size: 12px; font-weight: 700; color: #fbbf24; }
.fc-gem-val { font-size: 12px; font-weight: 700; color: #ef4444; }

/* ── BOTTOM NAV ── */
.fc-bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
    background: linear-gradient(180deg, #0d1018, #111520);
    border-top: 1px solid rgba(255,255,255,0.1);
    display: flex; justify-content: space-around; align-items: center;
    padding: 8px 0 12px 0;
}
.fc-nav-item {
    display: flex; flex-direction: column; align-items: center;
    gap: 3px; cursor: pointer; padding: 4px 12px;
    border-radius: 8px; transition: all 0.2s;
    text-decoration: none;
}
.fc-nav-icon { font-size: 20px; }
.fc-nav-label { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; color: #6b7280; }
.fc-nav-label.active { color: #22c55e; }

/* ── PLAYER CARD ── */
.fc-card {
    position: relative;
    border-radius: 12px;
    padding: 12px 10px 10px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    overflow: hidden;
    min-height: 160px;
}
.fc-card:hover { transform: translateY(-4px); }

.fc-card-icon { border-color: #f59e0b; background: linear-gradient(145deg, #1a1209, #251a0a); }
.fc-card-hero { border-color: #a855f7; background: linear-gradient(145deg, #170d24, #1f0f30); }
.fc-card-gold { border-color: #d97706; background: linear-gradient(145deg, #1a1507, #221c08); }
.fc-card-silver { border-color: #9ca3af; background: linear-gradient(145deg, #111318, #161b22); }
.fc-card-special { border-color: #06b6d4; background: linear-gradient(145deg, #071820, #091f28); }

.fc-card-pos-badge {
    position: absolute; top: 7px; left: 8px;
    font-size: 10px; font-weight: 800;
    padding: 2px 5px; border-radius: 4px;
    letter-spacing: 0.5px;
}
.pos-att { background: rgba(239,68,68,0.85); color: white; }
.pos-mid { background: rgba(34,197,94,0.85); color: white; }
.pos-def { background: rgba(59,130,246,0.85); color: white; }
.pos-gk  { background: rgba(234,179,8,0.85); color: black; }

.fc-card-ovr {
    position: absolute; top: 5px; right: 8px;
    font-size: 18px; font-weight: 900;
    font-family: 'Barlow Condensed', sans-serif;
}
.ovr-icon   { color: #fbbf24; text-shadow: 0 0 10px rgba(251,191,36,0.6); }
.ovr-hero   { color: #d946ef; text-shadow: 0 0 10px rgba(217,70,239,0.6); }
.ovr-gold   { color: #f59e0b; text-shadow: 0 0 10px rgba(245,158,11,0.5); }
.ovr-silver { color: #9ca3af; }
.ovr-special{ color: #22d3ee; text-shadow: 0 0 10px rgba(34,211,238,0.6); }

.fc-card-emoji { font-size: 32px; margin: 22px 0 4px; display: block; }

.fc-card-name {
    font-size: 11px; font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    color: #f0f0f0;
}
.fc-card-club { font-size: 9px; color: #9ca3af; margin-top: 2px; }

.fc-card-rank { margin-top: 6px; font-size: 10px; color: #fbbf24; letter-spacing: 1px; }

.fc-card-border-icon   { border: 2px solid #f59e0b; box-shadow: 0 0 12px rgba(245,158,11,0.3); }
.fc-card-border-hero   { border: 2px solid #a855f7; box-shadow: 0 0 12px rgba(168,85,247,0.3); }
.fc-card-border-gold   { border: 2px solid #d97706; }
.fc-card-border-silver { border: 1px solid #4b5563; }
.fc-card-border-special{ border: 2px solid #06b6d4; box-shadow: 0 0 12px rgba(6,182,212,0.3); }

/* ── SECTION HEADERS ── */
.fc-section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px; font-weight: 800;
    color: #f0f0f0; letter-spacing: 1px;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
    padding: 14px 20px 8px;
}
.fc-section-line {
    height: 2px;
    background: linear-gradient(90deg, #22c55e 0%, rgba(34,197,94,0.1) 60%, transparent 100%);
    margin: 0 20px 14px;
    border-radius: 1px;
}

/* ── CONTENT WRAPPER ── */
.fc-page { padding: 0 0 80px 0; }
.fc-content { padding: 0 16px; }

/* ── OVR BADGE (big) ── */
.fc-ovr-badge {
    display: inline-flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #dc2626, #991b1b);
    color: white; font-weight: 900; font-size: 22px;
    font-family: 'Barlow Condensed', sans-serif;
    width: 56px; height: 56px; border-radius: 12px;
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 16px rgba(220,38,38,0.4);
}
.fc-ovr-label { font-size: 9px; letter-spacing: 1px; opacity: 0.7; margin-top: 1px; }

/* ── TEAM INFO PANEL ── */
.fc-team-panel {
    background: linear-gradient(135deg, #111520, #0d1520);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 16px;
    display: flex; flex-direction: column; gap: 10px;
}
.fc-team-row { display: flex; align-items: center; gap: 10px; }
.fc-formation-badge {
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 8px; padding: 4px 10px;
    font-size: 12px; font-weight: 700; color: #22c55e;
}
.fc-coins-row {
    display: flex; align-items: center; gap: 6px;
    color: #fbbf24; font-size: 13px; font-weight: 600;
}

/* ── PITCH FIELD ── */
.fc-pitch-wrap {
    background: linear-gradient(180deg, #1a3d1a 0%, #1e4a1e 40%, #1a3d1a 100%);
    border-radius: 12px; padding: 20px 10px;
    position: relative;
    min-height: 360px;
    border: 2px solid rgba(255,255,255,0.06);
    overflow: hidden;
}
.fc-pitch-lines {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    background:
        linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px) 0 50%/100% 1px,
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px) 0 20%/100% 1px,
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px) 0 80%/100% 1px;
}
.fc-field-player {
    display: flex; flex-direction: column;
    align-items: center; gap: 2px;
}
.fc-field-card {
    width: 54px; height: 62px;
    border-radius: 8px; border: 1.5px solid;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 1px; padding: 4px; position: relative;
    cursor: pointer; transition: transform 0.15s;
}
.fc-field-card:hover { transform: scale(1.08); }
.fc-field-card-ovr { font-size: 14px; font-weight: 900; font-family: 'Barlow Condensed', sans-serif; }
.fc-field-card-emoji { font-size: 18px; }
.fc-field-card-pos {
    position: absolute; top: 2px; left: 3px;
    font-size: 7px; font-weight: 800;
    padding: 1px 3px; border-radius: 2px;
}
.fc-field-name { font-size: 9px; font-weight: 700; color: #d1fae5; text-transform: uppercase; letter-spacing: 0.3px; text-align: center; max-width: 60px; }
.fc-field-pos-label { font-size: 8px; color: rgba(255,255,255,0.4); }

/* ── TRANSFER MARKET ── */
.fc-market-card {
    background: linear-gradient(145deg, #111520, #0d1218);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; padding: 12px;
    display: flex; flex-direction: column; gap: 8px;
    cursor: pointer; transition: border-color 0.2s;
}
.fc-market-card:hover { border-color: rgba(34,197,94,0.4); }
.fc-market-price {
    display: flex; align-items: center; gap: 4px;
    color: #fbbf24; font-size: 12px; font-weight: 700;
}
.fc-market-selected {
    background: linear-gradient(145deg, #1a2535, #111d2e);
    border: 2px solid rgba(34,197,94,0.5);
    border-radius: 12px; padding: 16px;
}
.fc-purchase-btn {
    background: linear-gradient(135deg, #ca8a04, #a16207);
    color: white; font-weight: 800; font-size: 14px;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 12px; border-radius: 8px;
    border: none; width: 100%; cursor: pointer;
    text-align: center;
}

/* ── TABS STYLING ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 0 !important; padding: 0 16px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 16px !important;
    font-size: 12px !important; font-weight: 700 !important;
    letter-spacing: 0.5px !important; text-transform: uppercase !important;
}
.stTabs [aria-selected="true"] {
    color: #22c55e !important;
    border-bottom-color: #22c55e !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #1e3a2f, #16302b) !important;
    color: #22c55e !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 8px !important;
    font-weight: 700 !important; letter-spacing: 0.5px !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    border-color: #22c55e !important;
    box-shadow: 0 0 12px rgba(34,197,94,0.3) !important;
}

/* Primary action button */
.btn-primary > button {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    color: white !important;
    border: none !important;
    font-size: 14px !important; font-weight: 800 !important;
    letter-spacing: 1px !important;
}

/* ── FORM INPUTS ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #111520 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e8e8e8 !important;
    border-radius: 8px !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #111520 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    padding: 14px !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #6b7280 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #22c55e !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #111520 !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0c10; }
::-webkit-scrollbar-thumb { background: #22c55e44; border-radius: 2px; }

/* ── INFO / WARNING / SUCCESS ── */
.stInfo    { background: rgba(34,197,94,0.08) !important; border: 1px solid rgba(34,197,94,0.2) !important; }
.stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.2) !important; }
.stSuccess { background: rgba(34,197,94,0.12) !important; border: 1px solid rgba(34,197,94,0.3) !important; }
.stError   { background: rgba(239,68,68,0.08) !important; border: 1px solid rgba(239,68,68,0.2) !important; }

/* ── DRAFT CARD ── */
.draft-pool-card {
    background: linear-gradient(145deg, #1a1409, #221c08);
    border: 2px solid #d97706;
    border-radius: 12px; padding: 14px;
    text-align: center; position: relative;
    cursor: pointer; transition: transform 0.2s;
    box-shadow: 0 0 15px rgba(217,119,6,0.2);
}
.draft-pool-card:hover { transform: scale(1.04); }

/* ── STORE CARD ── */
.store-card {
    background: linear-gradient(145deg, #111520, #0d1218);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 16px;
    text-align: center; position: relative;
}
.store-badge-sale {
    position: absolute; top: -8px; right: -8px;
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: white; font-size: 10px; font-weight: 800;
    padding: 4px 7px; border-radius: 20px;
    letter-spacing: 0.5px;
}
.store-limit-badge {
    background: rgba(107,114,128,0.3); color: #9ca3af;
    font-size: 9px; font-weight: 700;
    padding: 2px 7px; border-radius: 4px;
    display: inline-block; margin-bottom: 8px;
    letter-spacing: 0.5px; text-transform: uppercase;
}

/* ── EXCHANGE CARD ── */
.exchange-card {
    background: linear-gradient(145deg, #12100a, #1a1507);
    border: 2px solid rgba(217,119,6,0.4);
    border-radius: 14px; padding: 16px;
    cursor: pointer; transition: border-color 0.2s;
    position: relative;
}
.exchange-card:hover { border-color: #d97706; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 10px !important; overflow: hidden !important; }
iframe { border-radius: 8px !important; }

/* ── HOME BANNER ── */
.home-banner {
    background: linear-gradient(135deg, #0f1b2d 0%, #1a0a2e 50%, #0a1a0f 100%);
    border-radius: 14px; overflow: hidden;
    position: relative; padding: 24px;
    border: 1px solid rgba(255,255,255,0.06);
    margin: 0 16px 16px;
}
.home-banner-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px; font-weight: 900;
    color: #f0f0f0; letter-spacing: 1px;
    text-transform: uppercase;
    line-height: 1.1;
}
.home-banner-sub {
    font-size: 13px; color: #9ca3af;
    margin: 6px 0 16px;
}
.go-now-btn {
    background: linear-gradient(135deg, #d4a017, #a07010);
    color: #000; font-weight: 800; font-size: 13px;
    letter-spacing: 1.5px; padding: 10px 24px;
    border-radius: 24px; display: inline-block;
    cursor: pointer; text-transform: uppercase;
}
.club-card {
    background: linear-gradient(135deg, #1a2535, #111d2e);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px; padding: 14px;
    display: flex; align-items: center; gap: 12px;
}
.play-card {
    background: linear-gradient(135deg, #15803d, #166534);
    border-radius: 12px; padding: 14px;
    text-align: center; cursor: pointer;
}
.play-card-title {
    font-size: 22px; font-weight: 900;
    letter-spacing: 2px; color: white;
}

/* ── ACTIVITY ROW ── */
.activity-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 10px 14px;
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 8px; cursor: pointer;
    transition: background 0.2s;
}
.activity-item:hover { background: rgba(34,197,94,0.06); }

/* ── QUEST ITEM ── */
.quest-item {
    background: #111520;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 14px;
    margin-bottom: 8px;
}
.quest-progress-bar {
    height: 6px; background: rgba(255,255,255,0.1);
    border-radius: 3px; overflow: hidden; margin-top: 8px;
}
.quest-progress-fill {
    height: 100%; border-radius: 3px;
    background: linear-gradient(90deg, #22c55e, #16a34a);
    transition: width 0.3s;
}

/* ── LEAGUE TABLE ── */
.league-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.league-pos { font-size: 14px; font-weight: 700; color: #6b7280; min-width: 24px; }
.league-pos-top3 { color: #fbbf24; }
.league-team { display: flex; align-items: center; gap: 8px; font-size: 13px; }

/* ── SLIDER ── */
.stSlider > div > div { color: #22c55e !important; }
.stSlider [data-baseweb="slider"] > div:first-child { background: rgba(255,255,255,0.1) !important; }
.stSlider [data-baseweb="slider"] > div:last-child { background: #22c55e !important; }

/* ── RADIO BUTTONS ── */
.stRadio > div { flex-direction: row !important; gap: 8px !important; }
.stRadio [data-testid="stMarkdownContainer"] { display: none !important; }

/* ── CHECKBOX ── */
.stCheckbox label { color: #9ca3af !important; font-size: 13px !important; }

/* page wrapper padding */
.main .block-container { padding-bottom: 80px !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "home"
if "coins" not in st.session_state:
    st.session_state.coins = 1_102_246_695
if "gems" not in st.session_state:
    st.session_state.gems = 2476
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


# ══════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════

# --- ACTUAL TEAM (from screenshots) ---
MY_TEAM = {
    "name": "MY TEAM",
    "club": "Real Madrid",
    "club_emoji": "👑",
    "ovr": 121,
    "formation": "3-4-3 Diamond",
    "coins": 62_760_000_000,
    "badges": ["🥇", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🔷"],
    "players": [
        # GK
        {"name": "MUSLERA", "pos": "GK", "ovr": 119, "rank": 30, "type": "gold", "emoji": "🧤", "nationality": "🇺🇾", "club": "Galatasaray"},
        # CB x3
        {"name": "MARQUINHOS", "pos": "CB", "ovr": 117, "rank": 29, "type": "hero", "emoji": "🛡️", "nationality": "🇧🇷", "club": "PSG"},
        {"name": "NESTA",      "pos": "CB", "ovr": 120, "rank": 30, "type": "icon", "emoji": "🛡️", "nationality": "🇮🇹", "club": "ICON"},
        {"name": "SALIBA",     "pos": "CB", "ovr": 121, "rank": 30, "type": "hero", "emoji": "🛡️", "nationality": "🇫🇷", "club": "Arsenal"},
        # MID x4
        {"name": "HAGI",       "pos": "LM", "ovr": 120, "rank": 30, "type": "icon", "emoji": "🌟", "nationality": "🇷🇴", "club": "ICON"},
        {"name": "MCTOMINAY",  "pos": "CDM","ovr": 121, "rank": 30, "type": "special","emoji": "💜","nationality": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "club": "Napoli"},
        {"name": "OLISE",      "pos": "CAM","ovr": 122, "rank": 30, "type": "special","emoji": "🔥","nationality": "🇫🇷", "club": "Bayern"},
        {"name": "BECKHAM",    "pos": "RM", "ovr": 120, "rank": 30, "type": "icon", "emoji": "⚽", "nationality": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "ICON"},
        # ATT x3
        {"name": "HAZARD",     "pos": "LW", "ovr": 120, "rank": 30, "type": "icon", "emoji": "💛", "nationality": "🇧🇪", "club": "ICON"},
        {"name": "OWEN",       "pos": "ST", "ovr": 120, "rank": 30, "type": "icon", "emoji": "🎯", "nationality": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "ICON"},
        {"name": "L.YAMAL",    "pos": "RW", "ovr": 121, "rank": 30, "type": "special","emoji": "⭐","nationality": "🇪🇸", "club": "Barcelona"},
    ]
}

# --- TRANSFER MARKET PLAYERS ---
MARKET_PLAYERS = [
    {"name": "DOUE",           "pos": "LW", "ovr": 117, "type": "special", "price": 4_670_000_000, "low": 4_430_000_000, "high": 4_900_000_000, "emoji": "💫", "nat": "🇫🇷", "club": "PSG"},
    {"name": "AFONSO MOREIRA", "pos": "LM", "ovr": 116, "type": "hero",    "price": 2_410_000_000, "low": 2_200_000_000, "high": 2_600_000_000, "emoji": "⚡", "nat": "🇵🇹", "club": "Emirates"},
    {"name": "BENZEMA",        "pos": "ST", "ovr": 116, "type": "hero",    "price": 2_460_000_000, "low": 2_300_000_000, "high": 2_700_000_000, "emoji": "🎯", "nat": "🇫🇷", "club": "Al-Ittihad"},
    {"name": "DONNARUMMA",     "pos": "GK", "ovr": 116, "type": "special", "price": 3_050_000_000, "low": 2_800_000_000, "high": 3_200_000_000, "emoji": "🧤", "nat": "🇮🇹", "club": "PSG"},
    {"name": "RASHFORD",       "pos": "LW", "ovr": 116, "type": "special", "price": 4_670_000_000, "low": 4_400_000_000, "high": 4_900_000_000, "emoji": "🌪️", "nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "Man Utd"},
    {"name": "R.CARVALHO",     "pos": "CB", "ovr": 116, "type": "icon",    "price": 5_350_000_000, "low": 5_000_000_000, "high": 5_700_000_000, "emoji": "🛡️", "nat": "🇵🇹", "club": "ICON"},
    {"name": "ZAMORANO",       "pos": "ST", "ovr": 116, "type": "icon",    "price": 2_250_000_000, "low": 2_100_000_000, "high": 2_400_000_000, "emoji": "🔟", "nat": "🇨🇱", "club": "ICON"},
    {"name": "BARESI",         "pos": "CB", "ovr": 115, "type": "icon",    "price": 4_230_000_000, "low": 3_900_000_000, "high": 4_600_000_000, "emoji": "🏆", "nat": "🇮🇹", "club": "ICON"},
    {"name": "BARNES",         "pos": "LW", "ovr": 115, "type": "hero",    "price": 2_450_000_000, "low": 2_200_000_000, "high": 2_700_000_000, "emoji": "⚡", "nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "Liverpool"},
    {"name": "DIAZ",           "pos": "LW", "ovr": 115, "type": "special", "price": 3_470_000_000, "low": 3_200_000_000, "high": 3_700_000_000, "emoji": "🌟", "nat": "🇨🇴", "club": "Bayern"},
    {"name": "HAALAND",        "pos": "ST", "ovr": 115, "type": "hero",    "price": 4_100_000_000, "low": 3_800_000_000, "high": 4_400_000_000, "emoji": "💪", "nat": "🇳🇴", "club": "Man City"},
    {"name": "MBAPPE",         "pos": "ST", "ovr": 115, "type": "special", "price": 5_800_000_000, "low": 5_400_000_000, "high": 6_200_000_000, "emoji": "⚡", "nat": "🇫🇷", "club": "Real Madrid"},
    {"name": "SAKA",           "pos": "RW", "ovr": 114, "type": "hero",    "price": 1_980_000_000, "low": 1_800_000_000, "high": 2_200_000_000, "emoji": "🏃", "nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "Arsenal"},
    {"name": "BELLINGHAM",     "pos": "CM", "ovr": 114, "type": "hero",    "price": 3_200_000_000, "low": 2_900_000_000, "high": 3_500_000_000, "emoji": "💎", "nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "Real Madrid"},
    {"name": "VINICIUS JR",    "pos": "LW", "ovr": 114, "type": "hero",    "price": 2_750_000_000, "low": 2_500_000_000, "high": 3_000_000_000, "emoji": "🌪️", "nat": "🇧🇷", "club": "Real Madrid"},
]

# --- RESERVES ---
RESERVES = [
    {"name": "KANE",       "pos": "ST", "ovr": 119, "type": "hero", "emoji": "🎯", "nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "club": "Bayern"},
    {"name": "DUMFRIES",   "pos": "RB", "ovr": 118, "type": "gold", "emoji": "⚡", "nat": "🇳🇱", "club": "Inter"},
    {"name": "ROBERTSON",  "pos": "LB", "ovr": 118, "type": "gold", "emoji": "🌟", "nat": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "club": "Liverpool"},
    {"name": "ALISSON",    "pos": "GK", "ovr": 117, "type": "hero", "emoji": "🧤", "nat": "🇧🇷", "club": "Liverpool"},
    {"name": "KEANE",      "pos": "CDM","ovr": 117, "type": "icon", "emoji": "🛡️", "nat": "🇮🇪", "club": "ICON"},
    {"name": "ERIKSEN",    "pos": "CAM","ovr": 114, "type": "gold", "emoji": "🎼", "nat": "🇩🇰", "club": "Wolfsburg"},
    {"name": "DJENE",      "pos": "CB", "ovr": 112, "type": "gold", "emoji": "💪", "nat": "🇹🇬", "club": "Getafe"},
    {"name": "FABIANSKI",  "pos": "GK", "ovr": 112, "type": "gold", "emoji": "🧤", "nat": "🇵🇱", "club": "West Ham"},
    {"name": "KAMADA",     "pos": "CM", "ovr": 112, "type": "gold", "emoji": "🇯🇵", "nat": "🇯🇵", "club": "Dortmund"},
    {"name": "BAKAMBU",    "pos": "ST", "ovr": 111, "type": "gold", "emoji": "⚽", "nat": "🇨🇩", "club": "Marseille"},
    {"name": "HALLER",     "pos": "ST", "ovr": 111, "type": "gold", "emoji": "🎯", "nat": "🇨🇮", "club": "Dortmund"},
]

# --- DRAFT POOLS ---
DRAFT_POOLS = {
    "CAPPED LEGENDS": {
        "hot": True,
        "ends": "4 Days",
        "description": "Legendary players from football history",
        "pool_a": [
            {"name": "CANNAVARO","pos": "CB","ovr": 117,"type": "icon","emoji": "🛡️","nat": "🇮🇹"},
            {"name": "COLE",     "pos": "LB","ovr": 117,"type": "icon","emoji": "⚡","nat": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
            {"name": "MARADONA", "pos": "RW","ovr": 117,"type": "icon","emoji": "🤌","nat": "🇦🇷"},
            {"name": "LAUDRUP",  "pos": "CAM","ovr": 116,"type": "icon","emoji": "🌟","nat": "🇩🇰"},
            {"name": "DE ROSSI", "pos": "CDM","ovr": 116,"type": "icon","emoji": "💪","nat": "🇮🇹"},
            {"name": "KEANE",    "pos": "LW", "ovr": 116,"type": "icon","emoji": "🏃","nat": "🇮🇪"},
        ],
        "pool_b_guaranteed": 8,
        "pool_a_guaranteed": 43,
        "cost_single": 1,
        "cost_ten": 10,
    },
    "RAMADAN": {
        "hot": False,
        "ends": "Festive",
        "description": "Special Ramadan season players",
        "pool_a": [],
        "cost_single": 1, "cost_ten": 10,
    },
    "WELCOME": {
        "hot": False,
        "ends": "Kick Off",
        "description": "Welcome pack for new players",
        "pool_a": [],
        "cost_single": 1, "cost_ten": 10,
    }
}

# --- STORE ITEMS ---
STORE_ITEMS = [
    {"name": "Player Pack 65-74",  "icon": "📦", "price_coins": 1500,  "price_gems": 15000, "limit": "Weekly: 20", "sale": None,       "type": "featured"},
    {"name": "FC Draft Voucher",   "icon": "🎫", "price_coins": 200,   "price_gems": 3000,  "limit": None,         "sale": None,       "type": "featured"},
    {"name": "10 FC Points",       "icon": "🪙", "price_coins": 2000,  "price_gems": 30000, "limit": None,         "sale": None,       "type": "featured"},
    {"name": "10 FC Points SALE",  "icon": "🪙", "price_coins": 1000,  "price_gems": None,  "limit": "Weekly: 1",  "sale": "50% OFF",  "type": "featured"},
    {"name": "10 FC Points 20%",   "icon": "🪙", "price_coins": 1600,  "price_gems": None,  "limit": "Daily: 1",   "sale": "20% OFF",  "type": "featured"},
    {"name": "Daily Voucher",      "icon": "🎫", "price_coins": None,  "price_gems": None,  "limit": "Daily: 1",   "sale": "50% OFF",  "type": "festive"},
    {"name": "Voucher Bundle Mega","icon": "🎁", "price_coins": None,  "price_gems": None,  "limit": "Purchase: 1","sale": "40% OFF",  "type": "festive"},
    {"name": "Daily Resource",     "icon": "📦", "price_coins": None,  "price_gems": None,  "limit": "Daily: 1",   "sale": "LIMIT",    "type": "festive"},
    {"name": "Star Pass Premium",  "icon": "⭐", "price_coins": 5000,  "price_gems": 50000, "limit": None,         "sale": None,       "type": "star_pass"},
]

# --- EXCHANGE ITEMS ---
EXCHANGE_ITEMS = {
    "CAPPED LEGENDS": [
        {"name": "FC Draft Voucher",         "icon": "🎫", "target": "All Players", "limit": "No Limit",    "desc": "Exchange for draft voucher"},
        {"name": "Rank Up Point x100",       "icon": "⬆️", "target": "All Players", "limit": "0/10",        "expires": "4 Days", "desc": "Boost rank points"},
        {"name": "117 OVR CL Player B",      "icon": "👤", "target": "All Players", "limit": "0/1",         "desc": "50% OFF",  "sale": True},
        {"name": "117 OVR CL Player B x3",   "icon": "👥", "target": "All Players", "limit": "0/3",         "desc": "Regular price"},
        {"name": "117 OVR CL Selection",     "icon": "🌟", "target": "All Players", "limit": "0/5",         "desc": "Select your player"},
    ],
    "TEAM OF THE YEAR 2026": [
        {"name": "TOTY 26 Player A",         "icon": "🏆", "target": "All Players", "limit": "0/5",  "desc": "Top rated players"},
        {"name": "TOTY 26 Token",            "icon": "🎖️", "target": "All Players", "limit": "No Limit", "desc": "Exchange token"},
    ],
    "RAMADAN": [
        {"name": "Ramadan Player",           "icon": "🌙", "target": "All Players", "limit": "0/3",  "desc": "Special Ramadan player"},
    ],
    "LIVE EVENTS": [
        {"name": "Live Event Reward",        "icon": "📡", "target": "All Players", "limit": "0/10", "desc": "Complete live events"},
    ],
    "RANK UP & TRAINING": [
        {"name": "26 Phase 2 Token",         "icon": "🔑", "target": "All Items",   "limit": "No Limit", "desc": "Expires: 46 Days", "items_needed": ["Pack A", "Pack B", "Pack C"]},
        {"name": "Extra Time Token A",       "icon": "⏱️", "target": "108-117 OVR","limit": "0/100,000", "desc": "Refreshes daily"},
    ]
}

# --- QUESTS ---
DAILY_QUESTS = [
    {"name": "Score 5 Goals",        "icon": "⚽", "reward": "500 Coins",   "progress": 3, "total": 5,   "type": "daily"},
    {"name": "Win 2 VS Attack",      "icon": "⚔️", "reward": "1 Draft Voucher", "progress": 1, "total": 2, "type": "daily"},
    {"name": "Complete a Match",     "icon": "🏟️", "reward": "200 Gems",   "progress": 1, "total": 1,   "type": "daily"},
    {"name": "Use 3 Skill Moves",    "icon": "🔄", "reward": "300 Coins",   "progress": 2, "total": 3,   "type": "daily"},
    {"name": "Assist 3 Times",       "icon": "🅰️", "reward": "150 Coins",   "progress": 0, "total": 3,   "type": "daily"},
]
WEEKLY_QUESTS = [
    {"name": "Win 10 H2H Matches",   "icon": "🥊", "reward": "5,000 Coins", "progress": 7,  "total": 10,  "type": "weekly"},
    {"name": "Reach Top 100",        "icon": "📈", "reward": "10 Vouchers", "progress": 1,  "total": 1,   "type": "weekly"},
    {"name": "Complete 5 Draft",     "icon": "🎫", "reward": "50,000 Coins","progress": 3,  "total": 5,   "type": "weekly"},
    {"name": "Score 30 Goals",       "icon": "⚽", "reward": "25,000 Coins","progress": 22, "total": 30,  "type": "weekly"},
]

# --- LEAGUE MEMBERS ---
LEAGUE_MEMBERS = [
    {"rank": 1,  "name": "MasterFC",    "ovr": 123, "pts": 9850, "country": "🇧🇷"},
    {"rank": 2,  "name": "ProPlayer99", "ovr": 122, "pts": 9720, "country": "🇩🇪"},
    {"rank": 3,  "name": "Somosab",     "ovr": 121, "pts": 9600, "country": "🇺🇿"},
    {"rank": 4,  "name": "FCLegend",    "ovr": 120, "pts": 9480, "country": "🇫🇷"},
    {"rank": 5,  "name": "GoalMachine", "ovr": 119, "pts": 9350, "country": "🇪🇸"},
    {"rank": 6,  "name": "SkillKing",   "ovr": 118, "pts": 9200, "country": "🇦🇷"},
    {"rank": 7,  "name": "PaceMonster", "ovr": 117, "pts": 9050, "country": "🇵🇹"},
    {"rank": 8,  "name": "DribblePro",  "ovr": 117, "pts": 8900, "country": "🇮🇹"},
    {"rank": 9,  "name": "DefenseWall", "ovr": 116, "pts": 8750, "country": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"rank": 10, "name": "MetaMaster",  "ovr": 116, "pts": 8600, "country": "🇳🇱"},
]


# ══════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════

def fmt_price(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.3f}B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)

def get_card_class(card_type):
    return {
        "icon":    ("fc-card-icon",    "fc-card-border-icon",    "ovr-icon"),
        "hero":    ("fc-card-hero",    "fc-card-border-hero",    "ovr-hero"),
        "gold":    ("fc-card-gold",    "fc-card-border-gold",    "ovr-gold"),
        "silver":  ("fc-card-silver",  "fc-card-border-silver",  "ovr-silver"),
        "special": ("fc-card-special", "fc-card-border-special", "ovr-special"),
    }.get(card_type, ("fc-card-gold", "fc-card-border-gold", "ovr-gold"))

def get_pos_class(pos):
    atk = ["ST", "LW", "RW", "CF", "SS"]
    mid = ["CM", "CDM", "CAM", "LM", "RM", "LAM", "RAM"]
    dfn = ["CB", "LB", "RB", "LWB", "RWB"]
    if pos in atk: return "pos-att"
    if pos in mid: return "pos-mid"
    if pos in dfn: return "pos-def"
    return "pos-gk"

def get_card_colors(card_type):
    """Returns (border_color, bg_gradient, ovr_color) for field cards"""
    return {
        "icon":    ("#f59e0b", "linear-gradient(145deg,#1a1209,#251a0a)", "#fbbf24"),
        "hero":    ("#a855f7", "linear-gradient(145deg,#170d24,#1f0f30)", "#d946ef"),
        "gold":    ("#d97706", "linear-gradient(145deg,#1a1507,#221c08)", "#f59e0b"),
        "silver":  ("#4b5563", "linear-gradient(145deg,#111318,#161b22)", "#9ca3af"),
        "special": ("#06b6d4", "linear-gradient(145deg,#071820,#091f28)", "#22d3ee"),
    }.get(card_type, ("#d97706", "linear-gradient(145deg,#1a1507,#221c08)", "#f59e0b"))

def render_player_card(player, show_price=False):
    bg, border, ovr_cls = get_card_class(player["type"])
    pos_cls = get_pos_class(player["pos"])
    stars = "⭐" * min(3, (player["ovr"] - 100) // 5 + 1) if player["ovr"] >= 100 else "★"
    price_html = f'<div class="fc-market-price">🪙 {fmt_price(player.get("price", 0))}</div>' if show_price else ""
    nat = player.get("nat", player.get("nationality", ""))
    return f"""
<div class="fc-card {bg} {border}">
    <span class="fc-card-pos-badge {pos_cls}">{player['pos']}</span>
    <span class="fc-card-ovr {ovr_cls}">{player['ovr']}</span>
    <span class="fc-card-emoji">{player.get('emoji','⚽')}</span>
    <div class="fc-card-name">{player['name']}</div>
    <div class="fc-card-club">{nat} {player.get('club','')}</div>
    <div class="fc-card-rank">{stars}</div>
    {price_html}
</div>
"""

def render_field_card(player):
    bc, bg, ovr_c = get_card_colors(player["type"])
    pos_cls = get_pos_class(player["pos"])
    pos_colors = {"pos-att": "#ef4444", "pos-mid": "#22c55e", "pos-def": "#3b82f6", "pos-gk": "#eab308"}
    pos_bg = pos_colors.get(pos_cls, "#6b7280")
    return f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:2px;">
    <div class="fc-field-card" style="border-color:{bc};background:{bg};">
        <div class="fc-field-card-pos" style="background:{pos_bg};">{player['pos']}</div>
        <div class="fc-field-card-ovr" style="color:{ovr_c};">{player['ovr']}</div>
        <div class="fc-field-card-emoji">{player.get('emoji','⚽')}</div>
    </div>
    <div class="fc-field-name">{player['name']}</div>
    <div class="fc-field-pos-label">{player['pos']}</div>
</div>
"""


# ══════════════════════════════════════════════════
#  TOP BAR
# ══════════════════════════════════════════════════
lvl = 80; xp_cur = 2510; xp_max = 6400
xp_pct = int(xp_cur / xp_max * 100)

st.markdown(f"""
<div class="fc-topbar">
    <div class="fc-profile-info">
        <div class="fc-avatar">S</div>
        <div>
            <div class="fc-username">Somosab</div>
            <div class="fc-level-bar-wrap">
                <span class="fc-level-num">Lv.{lvl}</span>
                <div class="fc-level-bar"><div class="fc-level-fill" style="width:{xp_pct}%"></div></div>
                <span class="fc-level-num">{xp_cur}/{xp_max}</span>
            </div>
        </div>
    </div>
    <div class="fc-currencies">
        <div class="fc-coin">
            <span style="font-size:14px;">🪙</span>
            <span class="fc-coin-val">{fmt_price(st.session_state.coins)}</span>
            <span style="color:#22c55e;font-size:12px;font-weight:700;">+</span>
        </div>
        <div class="fc-gem">
            <span style="font-size:14px;">💎</span>
            <span class="fc-gem-val">{st.session_state.gems:,}</span>
            <span style="color:#22c55e;font-size:12px;font-weight:700;">+</span>
        </div>
        <div style="font-size:18px;cursor:pointer;">⚙️</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  NAV BUTTONS (Streamlit)
# ══════════════════════════════════════════════════
nav_pages = [
    ("home",     "🏠", "HOME"),
    ("myteam",   "⚽", "CLUB"),
    ("market",   "💰", "MARKET"),
    ("draft",    "📦", "DRAFT"),
    ("exchange", "🔄", "EXCHANGE"),
    ("store",    "🛒", "STORE"),
    ("quests",   "🎯", "QUESTS"),
    ("leagues",  "🤝", "LEAGUES"),
]

nav_cols = st.columns(len(nav_pages))
for col, (p_key, icon, label) in zip(nav_cols, nav_pages):
    with col:
        is_active = st.session_state.page == p_key
        if st.button(
            f"{icon}\n{label}" if is_active else f"{icon}\n{label}",
            key=f"nav_{p_key}",
            help=label
        ):
            st.session_state.page = p_key
            st.rerun()

st.markdown("""
<style>
div[data-testid="column"] .stButton > button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: #6b7280 !important;
    border-radius: 0 !important;
    padding: 6px 4px !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    white-space: pre-line !important;
    line-height: 1.2 !important;
    width: 100% !important;
    box-shadow: none !important;
}
div[data-testid="column"] .stButton > button:hover {
    color: #22c55e !important;
    background: rgba(34,197,94,0.06) !important;
}
</style>
""", unsafe_allow_html=True)

# Highlight active nav
active_page = st.session_state.page
nav_idx = [p[0] for p in nav_pages].index(active_page) if active_page in [p[0] for p in nav_pages] else 0
st.markdown(f"""
<style>
div[data-testid="column"]:nth-child({nav_idx + 1}) .stButton > button {{
    color: #22c55e !important;
    border-bottom: 2px solid #22c55e !important;
    background: rgba(34,197,94,0.06) !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="fc-page">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  HOME PAGE
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    # Main banner
    st.markdown("""
    <div class="home-banner">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div>
                <div style="font-size:12px;color:#22c55e;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">
                    🔥 HOT EVENT
                </div>
                <div class="home-banner-title">CAPPED<br>LEGENDS</div>
                <div class="home-banner-sub">Legendary players. Iconic moments.<br>Draft now to build your dream squad.</div>
                <div class="go-now-btn">GO NOW →</div>
            </div>
            <div style="display:flex;gap:12px;">
                <div style="text-align:center;">
                    <div style="font-size:40px;">🏃</div>
                    <div style="font-size:10px;color:#9ca3af;font-weight:700;">117 LB</div>
                    <div style="font-size:11px;color:#f0f0f0;font-weight:800;">COLE</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:40px;">🤌</div>
                    <div style="font-size:10px;color:#fbbf24;font-weight:700;">117 RW</div>
                    <div style="font-size:11px;color:#f0f0f0;font-weight:800;">MARADONA</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:40px;">🛡️</div>
                    <div style="font-size:10px;color:#9ca3af;font-weight:700;">117 CB</div>
                    <div style="font-size:11px;color:#f0f0f0;font-weight:800;">CANNAVARO</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CLUB + PLAY cards
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="club-card" style="cursor:pointer;">
            <div>
                <div style="font-size:9px;color:#6b7280;font-weight:700;letter-spacing:1px;margin-bottom:2px;">CLUB</div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <div class="fc-ovr-badge">{MY_TEAM['ovr']}</div>
                    <div>
                        <div style="font-size:11px;color:#9ca3af;">OVR</div>
                        <div style="font-size:13px;font-weight:700;color:#f0f0f0;">{MY_TEAM['club']}</div>
                    </div>
                </div>
            </div>
            <div style="font-size:28px;margin-left:auto;">{MY_TEAM['club_emoji']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="play-card">
            <div class="play-card-title">PLAY</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-top:2px;">Start a Match</div>
            <div style="font-size:24px;margin-top:4px;">⚽</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fc-section-title">📋 ACTIVITIES</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

    activities = [
        ("🎫", "CAPPED LEGENDS DRAFT", "4 Days left", "#f59e0b"),
        ("⚔️", "VS ATTACK",            "Season 47",   "#3b82f6"),
        ("🌙", "RAMADAN SPECIAL",       "Festive Event","#a855f7"),
        ("⭐", "STAR PASS",             "Season ongoing","#22c55e"),
        ("⏱️", "EXTRA TIME",           "Phase 2",     "#06b6d4"),
        ("🏆", "BONUS REWARDS",         "Daily reset", "#fbbf24"),
    ]
    for icon, name, sub, color in activities:
        st.markdown(f"""
        <div class="activity-item">
            <div style="font-size:28px;min-width:40px;text-align:center;">{icon}</div>
            <div>
                <div style="font-size:13px;font-weight:700;color:#f0f0f0;">{name}</div>
                <div style="font-size:11px;color:#6b7280;">{sub}</div>
            </div>
            <div style="margin-left:auto;color:{color};font-size:16px;">›</div>
        </div>
        """, unsafe_allow_html=True)

    # Bottom bar items
    st.markdown('<div class="fc-section-title">🗓️ TODAY\'S SCHEDULE</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

    events_today = [
        ("🔄", "Division Rivals reset",  "12:00 UTC"),
        ("📊", "Team of the Week",        "Wednesday"),
        ("🏆", "League Tournament",       "19:00 UTC"),
        ("🎁", "Daily Login Bonus",       "Now"),
    ]
    cols_ev = st.columns(4)
    for col, (ico, name, time_) in zip(cols_ev, events_today):
        with col:
            st.markdown(f"""
            <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;">{ico}</div>
                <div style="font-size:11px;font-weight:700;color:#f0f0f0;margin:4px 0;">{name}</div>
                <div style="font-size:10px;color:#22c55e;">{time_}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  MY TEAM / CLUB PAGE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "myteam":

    tab_team, tab_reserves, tab_edit = st.tabs(["⚽ MY TEAM", "🔄 RESERVES", "✏️ TEAM EDITING"])

    with tab_team:
        # Left panel
        lc, rc = st.columns([1, 3])

        with lc:
            st.markdown(f"""
            <div class="fc-team-panel">
                <div style="font-size:11px;color:#6b7280;font-weight:700;letter-spacing:1px;">MY TEAM</div>
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <div style="font-size:28px;">{MY_TEAM['club_emoji']}</div>
                    <div class="fc-ovr-badge">
                        <div>
                            <div>{MY_TEAM['ovr']}</div>
                            <div class="fc-ovr-label">OVR</div>
                        </div>
                    </div>
                </div>
                <div style="font-size:13px;font-weight:700;color:#22c55e;">{MY_TEAM['formation']}</div>
                <div class="fc-coins-row">🪙 {fmt_price(MY_TEAM['coins'])}</div>
                <div style="display:flex;gap:6px;margin-top:4px;">
                    {"".join([f'<span style="font-size:18px;">{b}</span>' for b in MY_TEAM['badges']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            for btn_label in ["🔄 AUTO BUILD", "👥 RESERVES", "⚙️ TEAM EDITING"]:
                st.button(btn_label, key=f"team_btn_{btn_label}")

        with rc:
            # Pitch — 3-4-3 Diamond layout
            st.markdown("""
            <div style="font-size:12px;color:#6b7280;font-weight:700;letter-spacing:1px;padding:8px 0 4px;">
                3-4-3 DIAMOND FORMATION
            </div>
            """, unsafe_allow_html=True)

            # Formation rows: ATT(3) → MID(4) → DEF(3) → GK(1)
            layers = [
                ("⚔️ ATTACK",   [p for p in MY_TEAM["players"] if p["pos"] in ["LW","ST","RW"]]),
                ("🎯 MIDFIELD",  [p for p in MY_TEAM["players"] if p["pos"] in ["LM","CDM","CAM","RM"]]),
                ("🛡️ DEFENCE",  [p for p in MY_TEAM["players"] if p["pos"] in ["CB","LB","RB"]]),
                ("🧤 KEEPER",    [p for p in MY_TEAM["players"] if p["pos"] == "GK"]),
            ]

            for layer_name, layer_players in layers:
                if not layer_players:
                    continue
                st.markdown(f"""
                <div style="font-size:9px;color:rgba(255,255,255,0.2);text-align:center;
                            letter-spacing:2px;font-weight:700;margin:4px 0 2px;">{layer_name}</div>
                """, unsafe_allow_html=True)

                field_cols = st.columns(len(layer_players))
                for col, player in zip(field_cols, layer_players):
                    with col:
                        bc, bg, ovr_c = get_card_colors(player["type"])
                        pos_cls = get_pos_class(player["pos"])
                        pos_colors = {"pos-att": "#ef4444", "pos-mid": "#22c55e", "pos-def": "#3b82f6", "pos-gk": "#eab308"}
                        pos_bg = pos_colors.get(pos_cls, "#6b7280")

                        if st.button(
                            f"{player['emoji']}\n{player['ovr']}\n{player['name'][:8]}",
                            key=f"field_{player['name']}",
                            help=f"{player['name']} | {player['pos']} | OVR {player['ovr']}"
                        ):
                            st.session_state.selected_player = player
                            st.rerun()

                        st.markdown(f"""
                        <style>
                        div[data-testid="column"] button[title="{player['name']} | {player['pos']} | OVR {player['ovr']}"] {{
                            background: {bg} !important;
                            border: 1.5px solid {bc} !important;
                            color: {ovr_c} !important;
                            border-radius: 8px !important;
                            font-size: 10px !important;
                            padding: 4px !important;
                            white-space: pre-line !important;
                            line-height: 1.2 !important;
                            min-height: 64px !important;
                        }}
                        </style>
                        """, unsafe_allow_html=True)

            # Selected player panel
            if st.session_state.selected_player:
                p = st.session_state.selected_player
                bc, bg, ovr_c = get_card_colors(p["type"])
                st.markdown("<div class='fc-section-line' style='margin:12px 0 8px;'></div>", unsafe_allow_html=True)
                sel_c1, sel_c2 = st.columns([1, 2])
                with sel_c1:
                    st.markdown(f"""
                    <div style="background:{bg};border:2px solid {bc};border-radius:14px;
                                padding:20px 14px;text-align:center;
                                box-shadow:0 0 20px {bc}44;">
                        <div style="font-size:11px;font-weight:700;color:#9ca3af;letter-spacing:1px;">{p['pos']}</div>
                        <div style="font-size:44px;font-weight:900;color:{ovr_c};font-family:'Barlow Condensed',sans-serif;">{p['ovr']}</div>
                        <div style="font-size:48px;margin:8px 0;">{p.get('emoji','⚽')}</div>
                        <div style="font-size:16px;font-weight:800;color:#f0f0f0;text-transform:uppercase;">{p['name']}</div>
                        <div style="font-size:12px;color:#6b7280;margin-top:4px;">{p.get('nat','')} {p.get('club','')}</div>
                        <div style="font-size:13px;color:#fbbf24;margin-top:6px;">Rank {p.get('rank',30)} ⭐</div>
                    </div>
                    """, unsafe_allow_html=True)
                with sel_c2:
                    for action in ["⇄ SWAP", "ℹ️ DETAILS", "🏋️ TRAINING", "⬆️ RANK UP", "🔀 TRAINING TRANSFER"]:
                        st.button(action, key=f"player_action_{action}")

    with tab_reserves:
        st.markdown('<div class="fc-section-title">👥 RESERVES</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

        # Filter
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            reserve_search = st.text_input("🔍", placeholder="Search player...", label_visibility="collapsed")
        with f2:
            sort_res = st.selectbox("Sort", ["OVR ↓", "OVR ↑", "Name"], label_visibility="collapsed")
        with f3:
            pos_filter = st.selectbox("Position", ["All", "GK", "CB", "CM", "ST", "LW", "RW"], label_visibility="collapsed")

        filtered_reserves = RESERVES.copy()
        if reserve_search:
            filtered_reserves = [p for p in filtered_reserves if reserve_search.upper() in p["name"]]
        if pos_filter != "All":
            filtered_reserves = [p for p in filtered_reserves if p["pos"] == pos_filter]
        if sort_res == "OVR ↓":
            filtered_reserves.sort(key=lambda x: x["ovr"], reverse=True)
        elif sort_res == "OVR ↑":
            filtered_reserves.sort(key=lambda x: x["ovr"])
        else:
            filtered_reserves.sort(key=lambda x: x["name"])

        r_cols = st.columns(4)
        for i, player in enumerate(filtered_reserves):
            with r_cols[i % 4]:
                st.markdown(render_player_card(player), unsafe_allow_html=True)

    with tab_edit:
        st.markdown('<div class="fc-section-title">✏️ TEAM EDITING</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin:16px;">
            <div style="font-size:14px;color:#9ca3af;line-height:1.8;">
            ⚽ <b style="color:#f0f0f0;">Formation:</b> 3-4-3 Diamond<br>
            📋 <b style="color:#f0f0f0;">Instructions:</b> High Press, Short Passing<br>
            🏃 <b style="color:#f0f0f0;">Attacking:</b> Fast Build-Up, Width<br>
            🛡️ <b style="color:#f0f0f0;">Defending:</b> Press After Possession Loss<br>
            </div>
        </div>
        """, unsafe_allow_html=True)

        edit_c1, edit_c2 = st.columns(2)
        with edit_c1:
            st.selectbox("Formation", list(["3-4-3 Diamond","4-3-3","4-2-3-1","3-5-2","4-4-2"]))
            st.selectbox("Pressing Style", ["High Press","Mid Block","Low Block","Counter Press"])
            st.selectbox("Build-Up Play", ["Fast","Balanced","Slow"])
        with edit_c2:
            st.selectbox("Attacking Width", ["Wide","Normal","Narrow"])
            st.selectbox("Defensive Line", ["High","Medium","Low"])
            st.selectbox("Pressing Trigger", ["After Possession Loss","First Touch","Goalkeeper"])
        st.button("💾 SAVE TACTICS", key="save_tactics")


# ══════════════════════════════════════════════════════════════════
#  TRANSFER MARKET
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "market":

    mkt_tab1, mkt_tab2, mkt_tab3, mkt_tab4, mkt_tab5 = st.tabs([
        "⭐ RECOMMENDED", "👤 MY PLAYERS", "👁️ WATCHLIST", "📋 MY ORDERS", "🔍 SEARCH"
    ])

    with mkt_tab1:
        mc1, mc2 = st.columns([3, 1])

        with mc1:
            st.markdown('<div class="fc-section-title">📊 RECOMMENDED PLAYERS</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

            # Sort & filter row
            sf1, sf2, sf3 = st.columns([2, 1, 1])
            with sf1:
                mkt_search = st.text_input("🔍", placeholder="Search transfer market...", label_visibility="collapsed", key="mkt_search")
            with sf2:
                mkt_sort = st.selectbox("Sort", ["OVR ↓", "Price ↓", "Price ↑"], label_visibility="collapsed", key="mkt_sort")
            with sf3:
                mkt_pos = st.selectbox("Pos", ["All","GK","CB","CM","ST","LW","RW"], label_visibility="collapsed", key="mkt_pos")

            # Filter
            mkt_players = MARKET_PLAYERS.copy()
            if mkt_search:
                mkt_players = [p for p in mkt_players if mkt_search.upper() in p["name"]]
            if mkt_pos != "All":
                mkt_players = [p for p in mkt_players if p["pos"] == mkt_pos]
            if mkt_sort == "OVR ↓":
                mkt_players.sort(key=lambda x: x["ovr"], reverse=True)
            elif mkt_sort == "Price ↓":
                mkt_players.sort(key=lambda x: x["price"], reverse=True)
            else:
                mkt_players.sort(key=lambda x: x["price"])

            cols4 = st.columns(5)
            for i, p in enumerate(mkt_players):
                with cols4[i % 5]:
                    bg, border, ovr_cls = get_card_class(p["type"])
                    pos_cls = get_pos_class(p["pos"])

                    is_sel = (st.session_state.selected_player and
                              st.session_state.selected_player.get("name") == p["name"] and
                              st.session_state.selected_player.get("_from") == "market")

                    card_style = "border: 2px solid #22c55e !important;" if is_sel else ""

                    if st.button(
                        f"{p['emoji']} {p['ovr']}\n{p['name'][:10]}\n🪙{fmt_price(p['price'])}",
                        key=f"mkt_card_{p['name']}",
                        help=p['name']
                    ):
                        sel = dict(p); sel["_from"] = "market"
                        st.session_state.selected_player = sel
                        st.rerun()

                    st.markdown(f"""
                    <style>
                    button[title="{p['name']}"] {{
                        background: {('linear-gradient(145deg,#1a2535,#111d2e)' if is_sel else get_card_colors(p['type'])[1])} !important;
                        border: {"2px solid #22c55e" if is_sel else "1px solid rgba(255,255,255,0.08)"} !important;
                        color: {get_card_colors(p['type'])[2]} !important;
                        font-size: 10px !important;
                        white-space: pre-line !important;
                        line-height: 1.4 !important;
                        min-height: 70px !important;
                        border-radius: 10px !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)

            if st.button("🔄 REFRESH", key="mkt_refresh"):
                st.rerun()

        with mc2:
            # Selected player details
            sel = st.session_state.selected_player
            if sel and sel.get("_from") == "market":
                bc, bg, ovr_c = get_card_colors(sel["type"])
                in_wl = sel["name"] in st.session_state.watchlist

                st.markdown(f"""
                <div style="background:{bg};border:2px solid {bc};border-radius:14px;
                            padding:20px;text-align:center;margin-bottom:12px;
                            box-shadow:0 0 20px {bc}33;">
                    <div style="font-size:11px;font-weight:800;color:#9ca3af;letter-spacing:1px;">{sel['pos']} | {sel.get('nat','')}</div>
                    <div style="font-size:48px;font-weight:900;color:{ovr_c};font-family:'Barlow Condensed',sans-serif;">{sel['ovr']}</div>
                    <div style="font-size:36px;margin:6px 0;">{sel.get('emoji','⚽')}</div>
                    <div style="font-size:16px;font-weight:800;color:#f0f0f0;text-transform:uppercase;">{sel['name']}</div>
                    <div style="font-size:11px;color:#6b7280;margin-top:2px;">{sel.get('club','')}</div>
                </div>
                """, unsafe_allow_html=True)

                # Watch toggle
                wl_label = "👁️ Watching" if in_wl else "👁️ Watch Player"
                if st.button(wl_label, key="watch_btn"):
                    if in_wl:
                        st.session_state.watchlist.remove(sel["name"])
                    else:
                        st.session_state.watchlist.append(sel["name"])
                    st.rerun()

                # Price info
                st.markdown(f"""
                <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px;padding:14px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="color:#6b7280;font-size:12px;">Current Value</span>
                        <span style="color:#fbbf24;font-weight:700;font-size:12px;">{fmt_price(sel['price'])}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="color:#6b7280;font-size:12px;">Lowest Value</span>
                        <span style="color:#22c55e;font-weight:700;font-size:12px;">{fmt_price(sel['low'])}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#6b7280;font-size:12px;">Highest Value</span>
                        <span style="color:#ef4444;font-weight:700;font-size:12px;">{fmt_price(sel['high'])}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                can_afford = st.session_state.coins >= sel["price"]
                btn_label = f"🪙 PURCHASE\n{fmt_price(sel['price'])}"

                if st.button(btn_label, key="purchase_btn", disabled=not can_afford):
                    st.session_state.coins -= sel["price"]
                    st.success(f"✅ {sel['name']} sotib olindi!")
                    st.session_state.selected_player = None
                    st.rerun()

                if not can_afford:
                    st.markdown("""
                    <div style="color:#ef4444;font-size:11px;text-align:center;">
                    ⚠️ Yetarli coins yo'q
                    </div>
                    """, unsafe_allow_html=True)

                # Price trend chart
                days = list(range(7, 0, -1))
                base = sel["price"]
                prices = [base * (0.9 + random.uniform(0, 0.2)) for _ in days]
                prices[-1] = sel["price"]

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[f"Day -{d}" for d in days], y=prices,
                    mode='lines+markers',
                    line=dict(color='#fbbf24', width=2),
                    marker=dict(size=5, color='#f59e0b'),
                    fill='tozeroy', fillcolor='rgba(251,191,36,0.08)'
                ))
                fig.update_layout(
                    height=140, margin=dict(l=0,r=0,t=0,b=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, showticklabels=False, color='#6b7280'),
                    yaxis=dict(showgrid=False, showticklabels=False),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.markdown("""
                <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);
                            border-radius:12px;padding:30px;text-align:center;color:#4b5563;">
                    <div style="font-size:32px;margin-bottom:8px;">👆</div>
                    <div style="font-size:13px;font-weight:600;">Select a player to view details</div>
                </div>
                """, unsafe_allow_html=True)

    with mkt_tab2:
        st.markdown('<div class="fc-section-title">👤 MY PLAYERS</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
        my_pl_cols = st.columns(4)
        for i, player in enumerate(MY_TEAM["players"] + RESERVES[:4]):
            with my_pl_cols[i % 4]:
                st.markdown(render_player_card(player), unsafe_allow_html=True)

    with mkt_tab3:
        st.markdown('<div class="fc-section-title">👁️ MY WATCHLIST</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
        if st.session_state.watchlist:
            wl_players = [p for p in MARKET_PLAYERS if p["name"] in st.session_state.watchlist]
            wl_cols = st.columns(4)
            for i, p in enumerate(wl_players):
                with wl_cols[i % 4]:
                    st.markdown(render_player_card(p, show_price=True), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:40px;text-align:center;color:#4b5563;">
                <div style="font-size:40px;">👁️</div>
                <div style="font-size:14px;font-weight:600;margin-top:8px;">Watchlist bo'sh</div>
                <div style="font-size:12px;margin-top:4px;">O'yinchi kartasida Watch bosing</div>
            </div>
            """, unsafe_allow_html=True)

    with mkt_tab4:
        st.markdown('<div class="fc-section-title">📋 MY ORDERS</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:40px;text-align:center;color:#4b5563;">
            <div style="font-size:40px;">📋</div>
            <div style="font-size:14px;font-weight:600;margin-top:8px;">Faol buyurtmalar yo'q</div>
        </div>
        """, unsafe_allow_html=True)

    with mkt_tab5:
        st.markdown('<div class="fc-section-title">🔍 ADVANCED SEARCH</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.text_input("Player Name", placeholder="e.g. Maradona", key="adv_name")
        with s2:
            st.selectbox("Position", ["Any","GK","CB","LB","RB","CDM","CM","CAM","LW","RW","ST"], key="adv_pos")
        with s3:
            st.selectbox("Card Type", ["Any","ICON","HERO","GOLD","SPECIAL"], key="adv_type")
        with s4:
            st.number_input("Min OVR", 100, 130, 110, key="adv_ovr")

        max_price_b = st.slider("Max Price (Billions)", 0.5, 10.0, 5.0, 0.5, key="adv_price",
                                 format="%.1fB")

        if st.button("🔍 SEARCH NOW", key="adv_search"):
            results = [p for p in MARKET_PLAYERS if p["ovr"] >= st.session_state.adv_ovr
                       and p["price"] <= max_price_b * 1e9]
            st.markdown(f"**{len(results)} ta natija topildi:**")
            r_cols = st.columns(5)
            for i, p in enumerate(results):
                with r_cols[i % 5]:
                    st.markdown(render_player_card(p, show_price=True), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  DRAFT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "draft":

    d_col1, d_col2 = st.columns([1, 3])

    with d_col1:
        st.markdown('<div class="fc-section-title">📦 DRAFT</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

        for draft_name, draft_data in DRAFT_POOLS.items():
            is_hot = draft_data.get("hot", False)
            if "selected_draft" not in st.session_state:
                st.session_state.selected_draft = "CAPPED LEGENDS"

            is_sel = st.session_state.get("selected_draft") == draft_name
            border = "border-color: #22c55e;" if is_sel else ""

            if st.button(
                f"{'🔥 ' if is_hot else ''}{'✅ ' if is_sel else ''}{draft_name}\n{'HOT' if is_hot else draft_data['ends']}",
                key=f"draft_btn_{draft_name}"
            ):
                st.session_state.selected_draft = draft_name
                st.rerun()

    with d_col2:
        sel_draft_name = st.session_state.get("selected_draft", "CAPPED LEGENDS")
        sel_draft = DRAFT_POOLS.get(sel_draft_name, DRAFT_POOLS["CAPPED LEGENDS"])

        st.markdown(f"""
        <div style="padding:16px 16px 0;">
            <div style="font-size:18px;font-weight:900;color:#f0f0f0;text-transform:uppercase;letter-spacing:1px;">
                {sel_draft_name} DRAFT
            </div>
            <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
                <span style="color:#6b7280;font-size:12px;">⏱️ Ends in:</span>
                <span style="color:#22c55e;font-size:12px;font-weight:700;">{sel_draft.get('ends','Soon')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if sel_draft.get("pool_a"):
            st.markdown("""
            <div style="margin:12px 16px 6px;">
                <div style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);
                            border-radius:8px;padding:6px 12px;display:inline-block;">
                    <span style="font-size:12px;font-weight:800;color:#f59e0b;letter-spacing:1px;">POOL A</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            pool_cols = st.columns(3)
            for i, p in enumerate(sel_draft["pool_a"]):
                with pool_cols[i % 3]:
                    st.markdown(render_player_card(p), unsafe_allow_html=True)

        # Guaranteed info
        st.markdown(f"""
        <div style="padding:12px 16px;">
            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <div style="background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);
                            border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:8px;">
                    <span style="font-size:11px;font-weight:800;color:#a855f7;">POOL B</span>
                    <span style="color:#6b7280;font-size:11px;">or Higher Guaranteed in:</span>
                    <span style="color:#f0f0f0;font-weight:700;font-size:13px;">{sel_draft.get('pool_b_guaranteed','N/A')} Drafts</span>
                </div>
                <div style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);
                            border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:8px;">
                    <span style="font-size:11px;font-weight:800;color:#f59e0b;">POOL A</span>
                    <span style="color:#6b7280;font-size:11px;">Guaranteed in:</span>
                    <span style="color:#f0f0f0;font-weight:700;font-size:13px;">{sel_draft.get('pool_a_guaranteed','N/A')} Drafts</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Draft buttons
        btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 2])
        with btn_c1:
            if st.button(f"🎫 1 DRAFT\n{sel_draft['cost_single']} Voucher", key="draft_1x"):
                if st.session_state.gems >= 100:
                    pulled = random.choice(sel_draft["pool_a"]) if sel_draft.get("pool_a") else None
                    if pulled:
                        st.success(f"🎉 {pulled['name']} {pulled['ovr']} OVR tushdi!")
                    else:
                        st.info("Pack ochildi!")

        with btn_c2:
            if st.button(f"🎁 10 DRAFTS\n{sel_draft['cost_ten']} Vouchers", key="draft_10x"):
                results = []
                if sel_draft.get("pool_a"):
                    for _ in range(min(10, len(sel_draft["pool_a"]))):
                        results.append(random.choice(sel_draft["pool_a"]))
                if results:
                    st.success(f"🎉 10 pack ochildi! En yaxshi: {max(results, key=lambda x: x['ovr'])['name']} {max(results, key=lambda x: x['ovr'])['ovr']} OVR")

        with btn_c3:
            voucher_count = random.randint(0, 5)
            st.markdown(f"""
            <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;padding:10px;display:flex;gap:16px;">
                <div style="text-align:center;">
                    <div style="font-size:22px;">🎫</div>
                    <div style="color:#6b7280;font-size:10px;">Vouchers</div>
                    <div style="color:#f0f0f0;font-weight:700;">{voucher_count}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:22px;">💎</div>
                    <div style="color:#6b7280;font-size:10px;">Gems</div>
                    <div style="color:#f0f0f0;font-weight:700;">{st.session_state.gems:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  EXCHANGE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "exchange":

    exc_tabs = st.tabs(list(EXCHANGE_ITEMS.keys()))

    for tab, (exc_cat, items) in zip(exc_tabs, EXCHANGE_ITEMS.items()):
        with tab:
            sub_tab1, sub_tab2 = st.tabs(["📦 ITEM EXCHANGE", "👤 PLAYER EXCHANGE"])

            with sub_tab1:
                st.markdown(f'<div class="fc-section-title">{exc_cat}</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

                # Mr Manager intro (first category only)
                if exc_cat == "RANK UP & TRAINING":
                    st.markdown("""
                    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;
                                padding:16px;margin:0 16px 16px;display:flex;gap:14px;align-items:flex-start;">
                        <div style="font-size:36px;min-width:40px;">🤵</div>
                        <div>
                            <div style="font-size:14px;font-weight:700;color:#f0f0f0;">Mr. Manager ✓</div>
                            <div style="font-size:12px;color:#9ca3af;margin-top:4px;line-height:1.6;">
                                Welcome to the Item Exchange, where you can trade in Player Items for currencies.
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                cols3 = st.columns(3)
                for i, item in enumerate(items):
                    with cols3[i % 3]:
                        sale_badge = '<div style="position:absolute;top:-6px;right:-6px;background:linear-gradient(135deg,#dc2626,#b91c1c);color:white;font-size:9px;font-weight:800;padding:3px 7px;border-radius:10px;letter-spacing:0.5px;">50% OFF</div>' if item.get("sale") else ""
                        expires = f'<div style="color:#6b7280;font-size:10px;margin-top:4px;">⏱️ {item.get("expires","")}</div>' if item.get("expires") else ""
                        items_needed = ""
                        if item.get("items_needed"):
                            items_needed = '<div style="display:flex;justify-content:center;gap:4px;margin:8px 0;">' + "".join([f'<div style="background:rgba(255,255,255,0.05);border-radius:4px;padding:4px 6px;font-size:10px;color:#9ca3af;">{it}</div>' for it in item["items_needed"]]) + '</div>'

                        st.markdown(f"""
                        <div class="exchange-card" style="position:relative;margin-bottom:8px;">
                            {sale_badge}
                            <div style="font-size:32px;text-align:center;margin-bottom:8px;">{item['icon']}</div>
                            {items_needed}
                            <div style="font-size:13px;font-weight:700;color:#f0f0f0;text-align:center;">{item['name']}</div>
                            <div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.06);">
                                <div style="display:flex;justify-content:space-between;font-size:11px;color:#6b7280;margin:2px 0;">
                                    <span>Target:</span><span style="color:#9ca3af;">{item['target']}</span>
                                </div>
                                <div style="display:flex;justify-content:space-between;font-size:11px;color:#6b7280;margin:2px 0;">
                                    <span>Limit:</span><span style="color:#9ca3af;">{item['limit']}</span>
                                </div>
                            </div>
                            {expires}
                        </div>
                        """, unsafe_allow_html=True)

            with sub_tab2:
                st.markdown(f'<div class="fc-section-title">👤 PLAYER EXCHANGE — {exc_cat}</div><div class="fc-section-line"></div>', unsafe_allow_html=True)
                st.markdown("""
                <div style="padding:40px;text-align:center;color:#4b5563;">
                    <div style="font-size:40px;">🔄</div>
                    <div style="font-size:14px;font-weight:600;margin-top:8px;">Player Exchange items</div>
                    <div style="font-size:12px;margin-top:4px;">Trade players for exclusive rewards</div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  STORE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "store":

    st.markdown('<div class="fc-section-title">🛒 STORE</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

    str_tab1, str_tab2, str_tab3, str_tab4, str_tab5 = st.tabs([
        "⭐ RECOMMENDED", "🪙 FC POINTS & GEMS", "🔄 EXCHANGES", "💎 SILVER", "⭐ STAR PASS"
    ])

    def store_cat_tab(tab_obj, category, title):
        with tab_obj:
            items = [it for it in STORE_ITEMS if it["type"] == category]
            if not items:
                items = STORE_ITEMS[:6]

            st.markdown(f'<div class="fc-section-title">{title}</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

            s_cols = st.columns(4)
            for i, item in enumerate(items):
                with s_cols[i % 4]:
                    sale_html = f'<div class="store-badge-sale">{item["sale"]}</div>' if item.get("sale") else ""
                    limit_html = f'<div class="store-limit-badge">{item["limit"]}</div>' if item.get("limit") else ""
                    price_html = ""
                    if item.get("price_coins") and item["sale"] not in ["LIMIT"]:
                        price_html = f'<div class="fc-market-price" style="justify-content:center;">🪙 {item["price_coins"]:,}</div>'
                    if item.get("price_gems"):
                        price_html += f'<div style="color:#a855f7;font-size:11px;font-weight:700;text-align:center;">💎 {item["price_gems"]:,}</div>'
                    if item.get("sale") == "LIMIT":
                        price_html = '<div style="color:#6b7280;font-size:12px;font-weight:700;text-align:center;">LIMIT REACHED ✓</div>'

                    st.markdown(f"""
                    <div class="store-card" style="position:relative;margin-bottom:8px;">
                        {sale_html}
                        {limit_html}
                        <div style="font-size:36px;margin:8px 0;">{item['icon']}</div>
                        <div style="font-size:12px;font-weight:700;color:#f0f0f0;margin-bottom:8px;">{item['name']}</div>
                        {price_html}
                    </div>
                    """, unsafe_allow_html=True)

                    is_limited = item.get("sale") == "LIMIT"
                    if not is_limited:
                        if st.button(f"Buy {item['name'][:12]}", key=f"store_{i}_{item['name']}"):
                            cost = item.get("price_coins", 0) or 0
                            if st.session_state.coins >= cost:
                                st.session_state.coins -= cost
                                st.success(f"✅ {item['name']} sotib olindi!")
                            else:
                                st.error("Yetarli coins yo'q!")

    store_cat_tab(str_tab1, "featured",   "🌟 FEATURED ITEMS")
    store_cat_tab(str_tab2, "festive",    "🎉 FESTIVE ITEMS")
    store_cat_tab(str_tab3, "featured",   "🔄 EXCHANGES")
    store_cat_tab(str_tab4, "featured",   "💎 SILVER ITEMS")
    store_cat_tab(str_tab5, "star_pass",  "⭐ STAR PASS")


# ══════════════════════════════════════════════════════════════════
#  QUESTS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "quests":

    st.markdown('<div class="fc-section-title">🎯 QUESTS & MISSIONS</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

    q_tab1, q_tab2 = st.tabs(["📅 DAILY", "📆 WEEKLY"])

    def render_quests(quests_list):
        for q in quests_list:
            pct = int(q["progress"] / q["total"] * 100)
            done = q["progress"] >= q["total"]
            done_badge = '<span style="background:rgba(34,197,94,0.2);color:#22c55e;font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px;">✓ DONE</span>' if done else ""
            st.markdown(f"""
            <div class="quest-item">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="font-size:20px;">{q['icon']}</span>
                        <span style="font-size:13px;font-weight:700;color:#f0f0f0;">{q['name']}{done_badge}</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:11px;color:#fbbf24;font-weight:700;">{q['reward']}</div>
                        <div style="font-size:10px;color:#6b7280;">{q['progress']}/{q['total']}</div>
                    </div>
                </div>
                <div class="quest-progress-bar">
                    <div class="quest-progress-fill" style="width:{pct}%;background:{'linear-gradient(90deg,#22c55e,#16a34a)' if not done else 'linear-gradient(90deg,#fbbf24,#d97706)'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if done:
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("🎁 CLAIM", key=f"claim_{q['name']}"):
                        st.success(f"✅ {q['reward']} olindi!")

    with q_tab1:
        total_daily = len(DAILY_QUESTS)
        done_daily = sum(1 for q in DAILY_QUESTS if q["progress"] >= q["total"])
        st.markdown(f"""
        <div style="padding:12px 16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="color:#6b7280;font-size:12px;font-weight:700;">DAILY PROGRESS</span>
                <span style="color:#22c55e;font-size:12px;font-weight:700;">{done_daily}/{total_daily} complete</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:6px;height:8px;overflow:hidden;">
                <div style="width:{done_daily/total_daily*100:.0f}%;height:100%;background:linear-gradient(90deg,#22c55e,#16a34a);border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_quests(DAILY_QUESTS)

    with q_tab2:
        total_weekly = len(WEEKLY_QUESTS)
        done_weekly = sum(1 for q in WEEKLY_QUESTS if q["progress"] >= q["total"])
        st.markdown(f"""
        <div style="padding:12px 16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="color:#6b7280;font-size:12px;font-weight:700;">WEEKLY PROGRESS</span>
                <span style="color:#fbbf24;font-size:12px;font-weight:700;">{done_weekly}/{total_weekly} complete</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:6px;height:8px;overflow:hidden;">
                <div style="width:{done_weekly/total_weekly*100:.0f}%;height:100%;background:linear-gradient(90deg,#fbbf24,#d97706);border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_quests(WEEKLY_QUESTS)


# ══════════════════════════════════════════════════════════════════
#  LEAGUES
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "leagues":

    st.markdown('<div class="fc-section-title">🤝 LEAGUES</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

    lg_tab1, lg_tab2, lg_tab3 = st.tabs(["🏆 LEADERBOARD", "📊 STATS", "ℹ️ INFO"])

    with lg_tab1:
        # League header
        st.markdown("""
        <div style="background:linear-gradient(135deg,#111520,#0d1520);border:1px solid rgba(255,255,255,0.08);
                    border-radius:14px;padding:16px;margin:12px 16px;text-align:center;">
            <div style="font-size:24px;font-weight:900;color:#f0f0f0;text-transform:uppercase;letter-spacing:2px;">
                ⭐ ELITE MASTERS FC ⭐
            </div>
            <div style="color:#22c55e;font-size:12px;font-weight:700;margin-top:4px;">Division 1 • 10/100 Members</div>
            <div style="display:flex;justify-content:center;gap:20px;margin-top:12px;">
                <div style="text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#fbbf24;">121</div>
                    <div style="font-size:10px;color:#6b7280;">AVG OVR</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#22c55e;">98,350</div>
                    <div style="font-size:10px;color:#6b7280;">Total Pts</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#a855f7;">Rank #4</div>
                    <div style="font-size:10px;color:#6b7280;">Global</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Leaderboard
        st.markdown("""
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;margin:0 16px;">
            <div style="display:flex;justify-content:space-between;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.06);">
                <span style="font-size:10px;font-weight:800;color:#6b7280;letter-spacing:1px;">#</span>
                <span style="font-size:10px;font-weight:800;color:#6b7280;letter-spacing:1px;flex:1;margin-left:16px;">PLAYER</span>
                <span style="font-size:10px;font-weight:800;color:#6b7280;letter-spacing:1px;">OVR</span>
                <span style="font-size:10px;font-weight:800;color:#6b7280;letter-spacing:1px;margin-left:16px;">POINTS</span>
            </div>
        """, unsafe_allow_html=True)

        for member in LEAGUE_MEMBERS:
            is_me = member["name"] == "Somosab"
            rank_color = {"1": "#fbbf24", "2": "#9ca3af", "3": "#cd7f32"}.get(str(member["rank"]), "#6b7280")
            bg = "background:rgba(34,197,94,0.06);" if is_me else ""
            border = "border-left:3px solid #22c55e;" if is_me else "border-left:3px solid transparent;"

            st.markdown(f"""
            <div style="{bg}{border}display:flex;align-items:center;justify-content:space-between;
                        padding:12px 14px;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="font-size:14px;font-weight:800;color:{rank_color};min-width:20px;">{member['rank']}</span>
                <div style="flex:1;display:flex;align-items:center;gap:8px;margin-left:8px;">
                    <span style="font-size:16px;">{member['country']}</span>
                    <span style="font-size:13px;font-weight:{'800' if is_me else '600'};color:{'#22c55e' if is_me else '#f0f0f0'};">
                        {member['name']}{'  ← YOU' if is_me else ''}
                    </span>
                </div>
                <div style="background:linear-gradient(135deg,#dc2626,#991b1b);color:white;font-weight:800;
                            font-size:12px;padding:3px 8px;border-radius:6px;min-width:40px;text-align:center;">
                    {member['ovr']}
                </div>
                <div style="color:#fbbf24;font-weight:700;font-size:12px;margin-left:16px;min-width:50px;text-align:right;">
                    {member['pts']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with lg_tab2:
        st.markdown('<div class="fc-section-title">📊 LEAGUE STATISTICS</div><div class="fc-section-line"></div>', unsafe_allow_html=True)

        stat_cols = st.columns(4)
        lg_stats = [
            ("🏆", "League Rank",    "#4 Global",  "#fbbf24"),
            ("⭐", "Avg OVR",        "121",         "#22c55e"),
            ("⚽", "Goals Scored",   "2,847",       "#3b82f6"),
            ("🛡️", "Goals Conceded","1,203",       "#a855f7"),
        ]
        for col, (ico, lbl, val, clr) in zip(stat_cols, lg_stats):
            with col:
                st.markdown(f"""
                <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-top:3px solid {clr};
                            border-radius:10px;padding:14px;text-align:center;">
                    <div style="font-size:24px;">{ico}</div>
                    <div style="font-size:18px;font-weight:800;color:{clr};margin:4px 0;">{val}</div>
                    <div style="font-size:10px;color:#6b7280;font-weight:700;letter-spacing:0.5px;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

        # Chart
        members_df = pd.DataFrame(LEAGUE_MEMBERS)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=members_df["name"], y=members_df["pts"],
            marker=dict(
                color=["#22c55e" if n == "Somosab" else "#1e3a2f" for n in members_df["name"]],
                line=dict(color=["#22c55e" if n == "Somosab" else "#374151" for n in members_df["name"]], width=1)
            ),
            text=members_df["pts"].apply(lambda x: f"{x:,}"),
            textposition="outside", textfont=dict(color="#9ca3af", size=9)
        ))
        fig.update_layout(
            height=260, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='#6b7280', tickfont=dict(size=9), gridcolor='rgba(255,255,255,0.04)'),
            yaxis=dict(color='#6b7280', gridcolor='rgba(255,255,255,0.04)', tickfont=dict(size=9)),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with lg_tab3:
        st.markdown("""
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin:12px 16px;">
            <div style="font-size:16px;font-weight:800;color:#f0f0f0;margin-bottom:12px;">ℹ️ LEAGUE INFO</div>
            <div style="color:#9ca3af;font-size:13px;line-height:2;">
            🏟️ <b style="color:#f0f0f0;">Name:</b> Elite Masters FC<br>
            📊 <b style="color:#f0f0f0;">Division:</b> Division 1<br>
            👥 <b style="color:#f0f0f0;">Members:</b> 10/100<br>
            🌍 <b style="color:#f0f0f0;">Region:</b> Global<br>
            🏆 <b style="color:#f0f0f0;">Season:</b> Season 12<br>
            ⭐ <b style="color:#f0f0f0;">Min OVR:</b> 115 required<br>
            🎯 <b style="color:#f0f0f0;">Weekly target:</b> 5 matches<br>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE CLOSE
# ══════════════════════════════════════════════════════════════════
st.markdown('</div>', unsafe_allow_html=True)
