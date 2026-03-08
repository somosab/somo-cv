"""
╔══════════════════════════════════════════════════════════════╗
║         EA SPORTS FC MOBILE 25/26 - COMPANION APP           ║
║              Streamlit orqali to'liq boshqaruv               ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import math
from datetime import datetime, timedelta
import json

# ═══════════════════════════════════════════════════════════════
#  SAHIFA KONFIGURATSIYASI
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚽ FC Mobile 26 Companion",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "FC Mobile 26 Companion App - Barcha ma'lumotlar"
    }
)

# ═══════════════════════════════════════════════════════════════
#  CSS USLUB
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Asosiy ranglar */
    :root {
        --fc-green: #00B050;
        --fc-dark: #0a0a0a;
        --fc-gold: #FFD700;
        --fc-blue: #003087;
        --fc-red: #C41E3A;
    }

    /* Asosiy fon */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #0a1628 100%);
        color: #ffffff;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #051020 0%, #0a1628 100%);
        border-right: 2px solid #00B050;
    }

    /* Metrik kartalar */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0,176,80,0.15) 0%, rgba(0,48,135,0.15) 100%);
        border: 1px solid rgba(0,176,80,0.3);
        border-radius: 12px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }

    /* Tugmalar */
    .stButton > button {
        background: linear-gradient(135deg, #00B050, #007A35);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #00D060, #00B050);
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,176,80,0.4);
    }

    /* Kartalar */
    .player-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(0,48,135,0.2) 100%);
        border: 2px solid rgba(255,215,0,0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .player-card:hover {
        border-color: #FFD700;
        box-shadow: 0 10px 30px rgba(255,215,0,0.2);
        transform: translateY(-5px);
    }

    /* OVR badge */
    .ovr-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        font-weight: bold;
        font-size: 24px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        line-height: 60px;
        text-align: center;
        margin: 10px auto;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, rgba(0,176,80,0.2), rgba(0,48,135,0.2));
        border-left: 4px solid #00B050;
        border-radius: 0 10px 10px 0;
        padding: 15px 20px;
        margin: 20px 0;
        font-size: 22px;
        font-weight: bold;
        color: #00FF88;
    }

    /* Jadval uslubi */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Info boxlar */
    .info-box {
        background: rgba(0,176,80,0.1);
        border: 1px solid rgba(0,176,80,0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    /* Warning box */
    .warning-box {
        background: rgba(255,165,0,0.1);
        border: 1px solid rgba(255,165,0,0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    /* Formation field */
    .formation-cell {
        background: rgba(0,176,80,0.2);
        border: 1px solid rgba(0,176,80,0.4);
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        margin: 3px;
    }

    /* Title gradient */
    .main-title {
        background: linear-gradient(135deg, #00FF88, #FFD700, #00B0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Divider */
    .green-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #00B050, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }

    /* Progress bar */
    .stat-bar-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 12px;
        margin: 5px 0;
        overflow: hidden;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #aaaaaa;
        border-radius: 8px;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00B050, #007A35) !important;
        color: white !important;
    }

    /* Sidebar menu */
    .sidebar-menu-item {
        padding: 10px 15px;
        border-radius: 8px;
        margin: 3px 0;
        cursor: pointer;
        transition: all 0.2s;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        border-top: 1px solid rgba(0,176,80,0.2);
        margin-top: 40px;
    }

    /* Glassmorphism card */
    .glass-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }

    /* Gold text */
    .gold-text { color: #FFD700; font-weight: bold; }
    .green-text { color: #00FF88; font-weight: bold; }
    .red-text { color: #FF4444; font-weight: bold; }
    .blue-text { color: #00B0FF; font-weight: bold; }

    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  MA'LUMOTLAR BAZASI
# ═══════════════════════════════════════════════════════════════

# --- O'YINCHILAR MA'LUMOTLARI ---
PLAYERS_DATA = [
    # --- LEGENDLAR (109 OVR) ---
    {"name": "Ronaldo (R9)", "position": "ST", "ovr": 109, "team": "Brazil", "league": "ICON", "nationality": "Brazil",
     "pace": 95, "shooting": 99, "passing": 83, "dribbling": 97, "defending": 35, "physical": 91,
     "skill_moves": 5, "weak_foot": 5, "type": "ICON", "price": 15000000},
    {"name": "Ronaldinho", "position": "CAM", "ovr": 109, "team": "Brazil", "league": "ICON", "nationality": "Brazil",
     "pace": 88, "shooting": 91, "passing": 93, "dribbling": 99, "defending": 40, "physical": 79,
     "skill_moves": 5, "weak_foot": 4, "type": "ICON", "price": 14500000},
    {"name": "Zidane", "position": "CM", "ovr": 109, "team": "France", "league": "ICON", "nationality": "France",
     "pace": 83, "shooting": 87, "passing": 95, "dribbling": 97, "defending": 65, "physical": 85,
     "skill_moves": 5, "weak_foot": 5, "type": "ICON", "price": 14000000},
    {"name": "Gullit", "position": "CM", "ovr": 109, "team": "Netherlands", "league": "ICON", "nationality": "Netherlands",
     "pace": 85, "shooting": 89, "passing": 90, "dribbling": 94, "defending": 70, "physical": 88,
     "skill_moves": 4, "weak_foot": 4, "type": "ICON", "price": 13500000},
    {"name": "Thierry Henry", "position": "ST", "ovr": 109, "team": "France", "league": "ICON", "nationality": "France",
     "pace": 96, "shooting": 95, "passing": 82, "dribbling": 94, "defending": 42, "physical": 82,
     "skill_moves": 4, "weak_foot": 3, "type": "ICON", "price": 13000000},
    {"name": "Xabi Alonso", "position": "CM", "ovr": 109, "team": "Spain", "league": "ICON", "nationality": "Spain",
     "pace": 72, "shooting": 80, "passing": 96, "dribbling": 82, "defending": 85, "physical": 83,
     "skill_moves": 3, "weak_foot": 4, "type": "ICON", "price": 12000000},
    {"name": "Zlatan Ibrahimovic", "position": "ST", "ovr": 109, "team": "Sweden", "league": "ICON", "nationality": "Sweden",
     "pace": 80, "shooting": 97, "passing": 82, "dribbling": 91, "defending": 38, "physical": 96,
     "skill_moves": 5, "weak_foot": 4, "type": "ICON", "price": 12500000},
    {"name": "Marcelo", "position": "LB", "ovr": 109, "team": "Brazil", "league": "ICON", "nationality": "Brazil",
     "pace": 88, "shooting": 72, "passing": 87, "dribbling": 90, "defending": 85, "physical": 79,
     "skill_moves": 4, "weak_foot": 3, "type": "ICON", "price": 11000000},
    {"name": "Lilian Thuram", "position": "RB", "ovr": 109, "team": "France", "league": "ICON", "nationality": "France",
     "pace": 86, "shooting": 65, "passing": 81, "dribbling": 80, "defending": 95, "physical": 90,
     "skill_moves": 3, "weak_foot": 3, "type": "ICON", "price": 11000000},
    {"name": "Fernando Hierro", "position": "CB", "ovr": 109, "team": "Spain", "league": "ICON", "nationality": "Spain",
     "pace": 77, "shooting": 71, "passing": 80, "dribbling": 72, "defending": 97, "physical": 93,
     "skill_moves": 2, "weak_foot": 3, "type": "ICON", "price": 10500000},
    {"name": "Iker Casillas", "position": "GK", "ovr": 109, "team": "Spain", "league": "ICON", "nationality": "Spain",
     "pace": 58, "shooting": 40, "passing": 62, "dribbling": 45, "defending": 99, "physical": 80,
     "skill_moves": 1, "weak_foot": 3, "type": "ICON", "price": 10000000},
    {"name": "Pele", "position": "ST", "ovr": 109, "team": "Brazil", "league": "ICON", "nationality": "Brazil",
     "pace": 92, "shooting": 98, "passing": 86, "dribbling": 96, "defending": 40, "physical": 85,
     "skill_moves": 5, "weak_foot": 5, "type": "ICON", "price": 16000000},
    {"name": "Diego Maradona", "position": "CAM", "ovr": 109, "team": "Argentina", "league": "ICON", "nationality": "Argentina",
     "pace": 87, "shooting": 92, "passing": 91, "dribbling": 99, "defending": 45, "physical": 80,
     "skill_moves": 5, "weak_foot": 4, "type": "ICON", "price": 15500000},

    # --- HOZIRGI YULDUZLAR ---
    {"name": "Jude Bellingham", "position": "CM", "ovr": 107, "team": "Real Madrid", "league": "La Liga", "nationality": "England",
     "pace": 84, "shooting": 89, "passing": 89, "dribbling": 91, "defending": 79, "physical": 88,
     "skill_moves": 4, "weak_foot": 4, "type": "HERO", "price": 8500000},
    {"name": "Vinícius Jr.", "position": "LW", "ovr": 107, "team": "Real Madrid", "league": "La Liga", "nationality": "Brazil",
     "pace": 97, "shooting": 87, "passing": 81, "dribbling": 95, "defending": 30, "physical": 74,
     "skill_moves": 5, "weak_foot": 4, "type": "HERO", "price": 9000000},
    {"name": "Kylian Mbappé", "position": "ST", "ovr": 107, "team": "Real Madrid", "league": "La Liga", "nationality": "France",
     "pace": 99, "shooting": 94, "passing": 83, "dribbling": 95, "defending": 39, "physical": 83,
     "skill_moves": 5, "weak_foot": 4, "type": "HERO", "price": 9500000},
    {"name": "Erling Haaland", "position": "ST", "ovr": 107, "team": "Man City", "league": "Premier League", "nationality": "Norway",
     "pace": 89, "shooting": 97, "passing": 71, "dribbling": 81, "defending": 45, "physical": 97,
     "skill_moves": 3, "weak_foot": 3, "type": "HERO", "price": 8800000},
    {"name": "Jamal Musiala", "position": "CAM", "ovr": 106, "team": "Bayern München", "league": "Bundesliga", "nationality": "Germany",
     "pace": 88, "shooting": 84, "passing": 87, "dribbling": 93, "defending": 60, "physical": 76,
     "skill_moves": 4, "weak_foot": 3, "type": "HERO", "price": 7500000},
    {"name": "Bukayo Saka", "position": "RW", "ovr": 106, "team": "Arsenal", "league": "Premier League", "nationality": "England",
     "pace": 90, "shooting": 84, "passing": 85, "dribbling": 90, "defending": 64, "physical": 74,
     "skill_moves": 4, "weak_foot": 4, "type": "HERO", "price": 7000000},
    {"name": "Virgil van Dijk", "position": "CB", "ovr": 107, "team": "Liverpool", "league": "Premier League", "nationality": "Netherlands",
     "pace": 78, "shooting": 63, "passing": 76, "dribbling": 72, "defending": 97, "physical": 94,
     "skill_moves": 2, "weak_foot": 4, "type": "HERO", "price": 7200000},
    {"name": "Trent Alexander-Arnold", "position": "RB", "ovr": 106, "team": "Real Madrid", "league": "La Liga", "nationality": "England",
     "pace": 84, "shooting": 78, "passing": 93, "dribbling": 85, "defending": 79, "physical": 75,
     "skill_moves": 3, "weak_foot": 4, "type": "HERO", "price": 6800000},
    {"name": "Cole Palmer", "position": "CAM", "ovr": 106, "team": "Chelsea", "league": "Premier League", "nationality": "England",
     "pace": 83, "shooting": 87, "passing": 89, "dribbling": 91, "defending": 52, "physical": 72,
     "skill_moves": 4, "weak_foot": 4, "type": "HERO", "price": 7000000},
    {"name": "Lamine Yamal", "position": "RW", "ovr": 105, "team": "Barcelona", "league": "La Liga", "nationality": "Spain",
     "pace": 92, "shooting": 82, "passing": 84, "dribbling": 94, "defending": 30, "physical": 66,
     "skill_moves": 4, "weak_foot": 3, "type": "HERO", "price": 6500000},
    {"name": "Pedri", "position": "CM", "ovr": 106, "team": "Barcelona", "league": "La Liga", "nationality": "Spain",
     "pace": 79, "shooting": 78, "passing": 91, "dribbling": 91, "defending": 73, "physical": 72,
     "skill_moves": 4, "weak_foot": 3, "type": "HERO", "price": 6800000},
    {"name": "Rodri", "position": "CDM", "ovr": 107, "team": "Man City", "league": "Premier League", "nationality": "Spain",
     "pace": 73, "shooting": 75, "passing": 89, "dribbling": 83, "defending": 94, "physical": 87,
     "skill_moves": 3, "weak_foot": 4, "type": "HERO", "price": 7000000},
    {"name": "Mohamed Salah", "position": "RW", "ovr": 106, "team": "Liverpool", "league": "Premier League", "nationality": "Egypt",
     "pace": 94, "shooting": 90, "passing": 82, "dribbling": 93, "defending": 44, "physical": 79,
     "skill_moves": 4, "weak_foot": 3, "type": "HERO", "price": 7500000},
    {"name": "Harry Kane", "position": "ST", "ovr": 106, "team": "Bayern München", "league": "Bundesliga", "nationality": "England",
     "pace": 74, "shooting": 95, "passing": 84, "dribbling": 84, "defending": 48, "physical": 90,
     "skill_moves": 3, "weak_foot": 3, "type": "HERO", "price": 7200000},
    {"name": "Kevin De Bruyne", "position": "CM", "ovr": 107, "team": "Man City", "league": "Premier League", "nationality": "Belgium",
     "pace": 76, "shooting": 87, "passing": 97, "dribbling": 88, "defending": 65, "physical": 84,
     "skill_moves": 4, "weak_foot": 5, "type": "HERO", "price": 7800000},
    {"name": "Robert Lewandowski", "position": "ST", "ovr": 106, "team": "Barcelona", "league": "La Liga", "nationality": "Poland",
     "pace": 78, "shooting": 96, "passing": 81, "dribbling": 86, "defending": 42, "physical": 87,
     "skill_moves": 4, "weak_foot": 4, "type": "HERO", "price": 7000000},
    {"name": "Alisson Becker", "position": "GK", "ovr": 107, "team": "Liverpool", "league": "Premier League", "nationality": "Brazil",
     "pace": 62, "shooting": 42, "passing": 68, "dribbling": 52, "defending": 98, "physical": 82,
     "skill_moves": 1, "weak_foot": 3, "type": "HERO", "price": 6500000},
    {"name": "Thibaut Courtois", "position": "GK", "ovr": 107, "team": "Real Madrid", "league": "La Liga", "nationality": "Belgium",
     "pace": 65, "shooting": 44, "passing": 70, "dribbling": 54, "defending": 98, "physical": 92,
     "skill_moves": 1, "weak_foot": 3, "type": "HERO", "price": 6500000},

    # --- YULDUZ O'YINCHILAR ---
    {"name": "Marcus Rashford", "position": "LW", "ovr": 104, "team": "Man Utd", "league": "Premier League", "nationality": "England",
     "pace": 95, "shooting": 83, "passing": 76, "dribbling": 89, "defending": 40, "physical": 80,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 4500000},
    {"name": "Phil Foden", "position": "CAM", "ovr": 104, "team": "Man City", "league": "Premier League", "nationality": "England",
     "pace": 84, "shooting": 85, "passing": 88, "dribbling": 90, "defending": 54, "physical": 68,
     "skill_moves": 4, "weak_foot": 4, "type": "GOLD", "price": 4800000},
    {"name": "Bruno Fernandes", "position": "CAM", "ovr": 104, "team": "Man Utd", "league": "Premier League", "nationality": "Portugal",
     "pace": 77, "shooting": 84, "passing": 92, "dribbling": 87, "defending": 64, "physical": 75,
     "skill_moves": 4, "weak_foot": 4, "type": "GOLD", "price": 4500000},
    {"name": "Florian Wirtz", "position": "CAM", "ovr": 105, "team": "Bayer Leverkusen", "league": "Bundesliga", "nationality": "Germany",
     "pace": 82, "shooting": 83, "passing": 90, "dribbling": 92, "defending": 58, "physical": 74,
     "skill_moves": 4, "weak_foot": 4, "type": "GOLD", "price": 5500000},
    {"name": "Gavi", "position": "CM", "ovr": 104, "team": "Barcelona", "league": "La Liga", "nationality": "Spain",
     "pace": 83, "shooting": 78, "passing": 89, "dribbling": 89, "defending": 78, "physical": 74,
     "skill_moves": 4, "weak_foot": 3, "type": "GOLD", "price": 4500000},
    {"name": "Dani Carvajal", "position": "RB", "ovr": 104, "team": "Real Madrid", "league": "La Liga", "nationality": "Spain",
     "pace": 82, "shooting": 69, "passing": 84, "dribbling": 83, "defending": 91, "physical": 82,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 4200000},
    {"name": "Alphonso Davies", "position": "LB", "ovr": 104, "team": "Bayern München", "league": "Bundesliga", "nationality": "Canada",
     "pace": 97, "shooting": 69, "passing": 82, "dribbling": 87, "defending": 84, "physical": 78,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 4500000},
    {"name": "Ruben Dias", "position": "CB", "ovr": 105, "team": "Man City", "league": "Premier League", "nationality": "Portugal",
     "pace": 79, "shooting": 56, "passing": 75, "dribbling": 70, "defending": 95, "physical": 91,
     "skill_moves": 2, "weak_foot": 3, "type": "GOLD", "price": 4800000},
    {"name": "William Saliba", "position": "CB", "ovr": 104, "team": "Arsenal", "league": "Premier League", "nationality": "France",
     "pace": 82, "shooting": 52, "passing": 74, "dribbling": 69, "defending": 94, "physical": 88,
     "skill_moves": 2, "weak_foot": 3, "type": "GOLD", "price": 4500000},
    {"name": "Antony", "position": "RW", "ovr": 103, "team": "Man Utd", "league": "Premier League", "nationality": "Brazil",
     "pace": 91, "shooting": 81, "passing": 74, "dribbling": 87, "defending": 34, "physical": 74,
     "skill_moves": 5, "weak_foot": 3, "type": "GOLD", "price": 3500000},
    {"name": "Eduardo Camavinga", "position": "CM", "ovr": 103, "team": "Real Madrid", "league": "La Liga", "nationality": "France",
     "pace": 83, "shooting": 73, "passing": 83, "dribbling": 84, "defending": 82, "physical": 81,
     "skill_moves": 4, "weak_foot": 3, "type": "GOLD", "price": 3800000},
    {"name": "Fede Valverde", "position": "CM", "ovr": 104, "team": "Real Madrid", "league": "La Liga", "nationality": "Uruguay",
     "pace": 84, "shooting": 80, "passing": 84, "dribbling": 86, "defending": 83, "physical": 87,
     "skill_moves": 3, "weak_foot": 4, "type": "GOLD", "price": 4200000},
    {"name": "Rasmus Hojlund", "position": "ST", "ovr": 103, "team": "Man Utd", "league": "Premier League", "nationality": "Denmark",
     "pace": 88, "shooting": 86, "passing": 70, "dribbling": 82, "defending": 38, "physical": 87,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 3500000},
    {"name": "Ousmane Dembele", "position": "RW", "ovr": 104, "team": "PSG", "league": "Ligue 1", "nationality": "France",
     "pace": 95, "shooting": 82, "passing": 81, "dribbling": 93, "defending": 38, "physical": 75,
     "skill_moves": 4, "weak_foot": 3, "type": "GOLD", "price": 4300000},
    {"name": "Achraf Hakimi", "position": "RB", "ovr": 104, "team": "PSG", "league": "Ligue 1", "nationality": "Morocco",
     "pace": 95, "shooting": 71, "passing": 82, "dribbling": 86, "defending": 86, "physical": 80,
     "skill_moves": 3, "weak_foot": 4, "type": "GOLD", "price": 4200000},
    {"name": "Leandro Trossard", "position": "LW", "ovr": 103, "team": "Arsenal", "league": "Premier League", "nationality": "Belgium",
     "pace": 84, "shooting": 83, "passing": 81, "dribbling": 85, "defending": 52, "physical": 70,
     "skill_moves": 4, "weak_foot": 4, "type": "GOLD", "price": 3200000},
    {"name": "Ferran Torres", "position": "LW", "ovr": 102, "team": "Barcelona", "league": "La Liga", "nationality": "Spain",
     "pace": 91, "shooting": 82, "passing": 77, "dribbling": 84, "defending": 40, "physical": 72,
     "skill_moves": 3, "weak_foot": 4, "type": "GOLD", "price": 2800000},
    {"name": "Dominik Szoboszlai", "position": "CM", "ovr": 103, "team": "Liverpool", "league": "Premier League", "nationality": "Hungary",
     "pace": 79, "shooting": 82, "passing": 84, "dribbling": 85, "defending": 73, "physical": 82,
     "skill_moves": 3, "weak_foot": 4, "type": "GOLD", "price": 3500000},
    {"name": "Sandro Tonali", "position": "CM", "ovr": 103, "team": "Newcastle", "league": "Premier League", "nationality": "Italy",
     "pace": 75, "shooting": 78, "passing": 85, "dribbling": 82, "defending": 84, "physical": 83,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 3400000},
    {"name": "Gabriel Martinelli", "position": "LW", "ovr": 103, "team": "Arsenal", "league": "Premier League", "nationality": "Brazil",
     "pace": 95, "shooting": 83, "passing": 76, "dribbling": 87, "defending": 50, "physical": 80,
     "skill_moves": 3, "weak_foot": 3, "type": "GOLD", "price": 3500000},
    {"name": "Goncalo Ramos", "position": "ST", "ovr": 103, "team": "PSG", "league": "Ligue 1", "nationality": "Portugal",
     "pace": 82, "shooting": 88, "passing": 73, "dribbling": 82, "defending": 35, "physical": 80,
     "skill_moves": 3, "weak_foot": 4, "type": "GOLD", "price": 3300000},
    {"name": "Kim Min-jae", "position": "CB", "ovr": 104, "team": "Bayern München", "league": "Bundesliga", "nationality": "South Korea",
     "pace": 82, "shooting": 52, "passing": 70, "dribbling": 66, "defending": 94, "physical": 94,
     "skill_moves": 2, "weak_foot": 3, "type": "GOLD", "price": 4000000},
    {"name": "Antoine Griezmann", "position": "CAM", "ovr": 104, "team": "Atletico Madrid", "league": "La Liga", "nationality": "France",
     "pace": 80, "shooting": 88, "passing": 85, "dribbling": 88, "defending": 57, "physical": 76,
     "skill_moves": 4, "weak_foot": 4, "type": "GOLD", "price": 4500000},
]

# --- FORMATSIYALAR ---
FORMATIONS = {
    "4-3-3 Holding": {
        "tier": "S",
        "description": "Klassik hujum formatsiyasi. 3 ta winger bilan tez hujumlar.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CDM", "CM", "CM", "RW", "ST", "LW"],
        "pros": ["Tez kontr-hujumlar", "3 ta hujumchi", "O'rtamiyonni nazorat qilish"],
        "cons": ["CDM ustiga yuklanadi", "Yon tomonlarda zaif"],
        "style": "Hujum",
        "best_for": "VS Attack va Head-to-Head",
        "meta_rating": 95,
        "difficulty": "O'rta"
    },
    "4-2-3-1 Narrow": {
        "tier": "S",
        "description": "O'rtamiyonni egallash uchun eng yaxshi. CAM markazda ijodiy o'yin.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CDM", "CDM", "RAM", "CAM", "LAM", "ST"],
        "pros": ["O'rtamiyonni hukmronlik", "Ikki CDM himoyasi", "CAM erkin"],
        "cons": ["Keng tomonga zaiif", "Qanotlar yo'q"],
        "style": "Muvozanat",
        "best_for": "Division Rivals",
        "meta_rating": 93,
        "difficulty": "O'rta"
    },
    "3-5-2": {
        "tier": "S",
        "description": "2 ta striker + kuchli o'rtamiyonga ega. Hozirgi META formatsiyasi.",
        "positions": ["GK", "CB", "CB", "CB", "RM", "CM", "CDM", "CDM", "LM", "ST", "ST"],
        "pros": ["3 ta himoyachi mustahkam", "LM/RM ilgari itariladi", "2 ta striker xavfli"],
        "cons": ["Full-back yo'q", "Keng kontrga zaif"],
        "style": "Muvozanat",
        "best_for": "Barcha rejimlar",
        "meta_rating": 97,
        "difficulty": "Qiyin"
    },
    "4-1-2-1-2 Narrow": {
        "tier": "S",
        "description": "Markaziy o'yin. Tor ammo kuchli hujum chiziqli.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CDM", "CM", "CM", "CAM", "ST", "ST"],
        "pros": ["2 ta striker xavfli", "CAM ijodiy markaz", "CDM himoya qiladi"],
        "cons": ["Winger yo'q", "Keng hujumlarga zaif"],
        "style": "Hujum",
        "best_for": "VS Attack",
        "meta_rating": 91,
        "difficulty": "O'rta"
    },
    "4-4-2": {
        "tier": "A",
        "description": "Klassik va muvozanatli formatsiya. Boshlang'ich o'yinchilar uchun ideal.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "RM", "CM", "CM", "LM", "ST", "ST"],
        "pros": ["Muvozanatli", "Keng qanotlar", "Oson tushuniladi"],
        "cons": ["Hozirgi META uchun kuchsiz", "O'rtamiyonda bittaga kam"],
        "style": "Muvozanat",
        "best_for": "Yangi boshlovchilar",
        "meta_rating": 82,
        "difficulty": "Oson"
    },
    "4-3-2-1": {
        "tier": "A",
        "description": "Xmas daraxti formatsiyasi. Qalinlashtirilgan o'rtamiyonli.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CM", "CM", "CM", "RAF", "LAF", "ST"],
        "pros": ["O'rtamiyonda kuchli", "ST ga ko'p pas"],
        "cons": ["Keng zaif", "RM/LM yo'q"],
        "style": "Muvozanat",
        "best_for": "VS Attack",
        "meta_rating": 85,
        "difficulty": "O'rta"
    },
    "4-2-4": {
        "tier": "B",
        "description": "Ultra hujumchan. 4 ta hujumchi bilan xavfli ammo himoyasiz.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CDM", "CDM", "RW", "ST", "ST", "LW"],
        "pros": ["4 ta hujumchi", "Tezkor hujumlar", "Ko'p gol imkoniyati"],
        "cons": ["Juda himoyasiz", "Kontr-hujumlarga zaif"],
        "style": "Super Hujum",
        "best_for": "Tajribali o'yinchilar",
        "meta_rating": 75,
        "difficulty": "Juda qiyin"
    },
    "5-3-2": {
        "tier": "A",
        "description": "5 ta himoyachi bilan mustahkam mudofaa. Kontr-hujum taktikasi.",
        "positions": ["GK", "RWB", "CB", "CB", "CB", "LWB", "CM", "CM", "CM", "ST", "ST"],
        "pros": ["Juda mustahkam himoya", "RWB/LWB hujumda ham yordam beradi"],
        "cons": ["Kam hujum imkoniyati", "O'rtamiyonda bosim kerak"],
        "style": "Himoya",
        "best_for": "Manager Mode",
        "meta_rating": 80,
        "difficulty": "O'rta"
    },
    "4-3-3 Attack": {
        "tier": "A",
        "description": "Hujumchan 4-3-3. Keng qanotlar bilan kross o'yini.",
        "positions": ["GK", "RB", "CB", "CB", "LB", "CM", "CM", "CM", "RW", "ST", "LW"],
        "pros": ["Keng qanotlar", "Ko'p kross imkoniyati", "3 ta midfield"],
        "cons": ["CDM yo'q", "Kontr-hujumlarga zaif"],
        "style": "Hujum",
        "best_for": "VS Attack",
        "meta_rating": 88,
        "difficulty": "O'rta"
    },
}

# --- O'YIN REJIMLARI ---
GAME_MODES = {
    "VS Attack": {
        "icon": "⚔️",
        "description": "Asinxron PvP rejimi. Faqat hujum bosqichlarini o'ynaysiz.",
        "tips": [
            "Ikki CDM bilan kuchli formatsiya tanlang",
            "Tez wingerlarga ega bo'ling",
            "1-on-1 dribbling ustida mashq qiling",
            "Passing zanjirlarini takomillashtiring",
            "OVR oshirishga harakat qiling"
        ],
        "rewards": "Diamonds, Skill Boosts, Player Packs",
        "seasons": "Haftalik mavsumlar",
        "difficulty": "O'rta"
    },
    "Head to Head": {
        "icon": "🥊",
        "description": "To'liq real vaqt PvP. 90 daqiqalik to'liq o'yin.",
        "tips": [
            "3-5-2 yoki 4-2-3-1 ishlating",
            "Taktik o'zgarishlarga tayyor bo'ling",
            "Himoyada CDM/CB ni kuzating",
            "Skill moves kam ishlating",
            "Corner kick strategiyasini o'rganing"
        ],
        "rewards": "Division points, Weekly rewards, Event coins",
        "seasons": "Division tizimi",
        "difficulty": "Qiyin"
    },
    "Manager Mode": {
        "icon": "🧠",
        "description": "Taktik boshqaruv. O'yinchi harakatlari emas, jamoa taktikasi.",
        "tips": [
            "Futbolchilar ko'rsatkichlariga e'tibor bering",
            "Chemistry muhim",
            "To'g'ri pozitsiyalash",
            "Formatsiyani raqibga qarab o'zgartiring",
            "Player traits ni ko'rib chiqing"
        ],
        "rewards": "Manager tokens, Elite packs",
        "seasons": "Monthly seasons",
        "difficulty": "O'rta"
    },
    "Club Challenge": {
        "icon": "🏆",
        "description": "Litsenziyalangan klublar bilan o'ynash. EPL, La Liga, UCL.",
        "tips": [
            "Klub o'yinchilarining kuchli tomonlarini o'rganing",
            "Har bir liganing o'ziga xos o'yin uslubi bor",
            "Bonus OVR beradigan o'yinchilardan foydalaning",
            "Event o'yinchilarni to'plang"
        ],
        "rewards": "Club tokens, Exclusive player cards",
        "seasons": "Event-based",
        "difficulty": "O'rta"
    },
    "Division Rivals": {
        "icon": "🎯",
        "description": "Darajali reyting tizimi. Yulduz tizimi bilan yangilangan.",
        "tips": [
            "Haftada kamida 5 o'yin o'ynang",
            "Yuqori division = ko'p mukofot",
            "Lose streakdan keyin tanaffus oling",
            "Meta formatsiyalardan foydalaning"
        ],
        "rewards": "Division tokens, Pack rewards, Special cards",
        "seasons": "Haftalik divisions",
        "difficulty": "Juda qiyin"
    },
    "Tournament Mode": {
        "icon": "🌍",
        "description": "Real hayotdagi turnirlar: UCL, Euro, World Cup.",
        "tips": [
            "Turnirga mos o'yinchilar to'plang",
            "Group stage dan ehtiyot bo'ling",
            "Knockout roundda taktik o'zgartiring",
            "Special event o'yinchilarni ishlating"
        ],
        "rewards": "Tournament trophies, Special packs, Exclusive players",
        "seasons": "Real-world event based",
        "difficulty": "O'rta"
    },
    "Football Center": {
        "icon": "📡",
        "description": "Real hayot statistikasi asosida OVR yangilanadi.",
        "tips": [
            "Team of the Week o'yinchilarini kuzating",
            "Player of the Month ochko'zlik qiling",
            "Key Matches natijalarini kuzating",
            "OVR boost'lardan foydalaning"
        ],
        "rewards": "Live OVR updates, TOTW cards",
        "seasons": "Haftamahal yangilanadi",
        "difficulty": "Oson"
    },
    "Leagues": {
        "icon": "🤝",
        "description": "100 nafargacha o'yinchi bilan hamkorlik o'yini.",
        "tips": [
            "Faol liga a'zolari bilan kiriting",
            "Seasonal quests ni bajarish",
            "League vs League turnirlarida g'alaba qozonish",
            "League admin vositalaridan foydalaning"
        ],
        "rewards": "League coins, Co-op rewards, Special players",
        "seasons": "Mavsumiy",
        "difficulty": "Oson"
    },
}

# --- LIGALAR ---
LEAGUES = {
    "Premier League": {"country": "England", "teams": 20, "top_team": "Man City", "color": "#3D195B"},
    "La Liga": {"country": "Spain", "teams": 20, "top_team": "Real Madrid", "color": "#FF6600"},
    "Bundesliga": {"country": "Germany", "teams": 18, "top_team": "Bayern München", "color": "#D20515"},
    "Serie A": {"country": "Italy", "teams": 20, "top_team": "Inter Milan", "color": "#024494"},
    "Ligue 1": {"country": "France", "teams": 18, "top_team": "PSG", "color": "#003189"},
    "Champions League": {"country": "Europe", "teams": 32, "top_team": "Real Madrid", "color": "#0C2461"},
    "ICON": {"country": "Legends", "teams": 0, "top_team": "Various", "color": "#8B6914"},
    "HERO": {"country": "Heroes", "teams": 0, "top_team": "Various", "color": "#6B2E8E"},
}

# --- HODISALAR ---
EVENTS = [
    {"name": "Glorious Eras", "status": "Active", "type": "ICON Event",
     "description": "Real Madrid, Liverpool, Bayern va Juventus ICON o'yinchilari",
     "rewards": "ICON player cards, Special packs", "end_date": "2025-12-18", "icon": "🌟"},
    {"name": "Team of the Week", "status": "Active", "type": "Weekly",
     "description": "Haftalik real hayot statistikasi asosida eng yaxshi 11 ta o'yinchi",
     "rewards": "TOTW cards, Boosts", "end_date": "Ongoing", "icon": "📊"},
    {"name": "Club Challenge Season", "status": "Active", "type": "Seasonal",
     "description": "Premier League, La Liga va UCL klublari bilan musobaqa",
     "rewards": "Club tokens, Exclusive kits", "end_date": "Season end", "icon": "🏟️"},
    {"name": "Champions League Event", "status": "Coming Soon", "type": "Tournament",
     "description": "UEFA Champions League turniriga bag'ishlangan maxsus hodisa",
     "rewards": "UCL trophy, Exclusive players", "end_date": "2026-02-01", "icon": "🏆"},
    {"name": "Aqua vs Inferno", "status": "Seasonal", "type": "Team Event",
     "description": "Ikki jamoaga bo'linib musobaqa. Maxsus ko'rinishdagi o'yinchilar.",
     "rewards": "Special themed players, Exclusive packs", "end_date": "Seasonal", "icon": "🔥"},
    {"name": "Daily Training", "status": "Active", "type": "Daily",
     "description": "Kunlik vazifalar va maqsadlar bajarish",
     "rewards": "XP, Training tokens, Skill boosts", "end_date": "Daily reset", "icon": "💪"},
    {"name": "Division Rivals Season", "status": "Active", "type": "Weekly",
     "description": "Haftalik Division Rivals mavsumi",
     "rewards": "Division tokens, Pack rewards", "end_date": "Weekly reset", "icon": "⚡"},
    {"name": "MLS Live Games", "status": "Past", "type": "Live Event",
     "description": "MLS o'yinlarini jonli tomosha qilish va mukofotlar",
     "rewards": "MLS players, Coins", "end_date": "2025-09-27", "icon": "📺"},
]

# --- MASLAHATLAR ---
TIPS_AND_TRICKS = {
    "Yangi boshlovchilar": [
        "🎯 Avvalo Daily Quests ni bajaring - bu tekin resurslar beradi",
        "💎 Diamonds ni faqat muhim narsalarga sarflang",
        "📦 Pack ochishda shoshilmang - Events paytida oching",
        "⚽ Bir formatsiyada qoling va uni to'liq o'rganing",
        "🤝 Ligaga kiring - cooperative bonuslar muhim",
        "📈 OVR oshirishga e'tibor bering, kozmetikaga emas",
        "🏃 Pace (tezlik) eng muhim stat - tez o'yinchilar tanlang",
        "🔄 Chemistry ni to'g'rilang - bir millat/liga o'yinchilar",
    ],
    "O'rta daraja": [
        "🧪 Formatsiyani o'zgartirib ko'ring - 3-5-2 hozir META",
        "💰 Transfer marketda sotib oling - pack'dan ko'ra arzonroq",
        "📊 Football Center'ni kuzating - TOTW o'yinchilar qimmatli",
        "🎮 VS Attack'da CDM bilan o'yinchi blok qilishni o'rganing",
        "🌟 ICON o'yinchilarni maqsad qiling - eng yaxshi karta turi",
        "📋 Player traits ni o'qing - Long Shot, Dives Into Tackles muhim",
        "🔁 Rank Up tizimini tushuning - base OVR dan yuqoriga ko'taring",
        "⚔️ H2H'da Counter-attack taktikasi ishlating",
    ],
    "Ilg'or darajadagi": [
        "💡 Alternativ pozitsiyalar OVR boost beradi - RM ni CM'da o'ynating",
        "🎯 Penalty spot'larni yodlang - oldindan ko'rsatmasdan ur",
        "🔧 Taktik O'zgarishlarni real vaqtda qilishni o'rganing",
        "📈 Player ratings real hayot bilan o'zgaradi - Football Center tomosha",
        "🎭 Event o'yinchilari kelajakda OVR boostga ega bo'lishi mumkin",
        "💎 Diamond bundles'ni sale paytida oling",
        "🏆 Division Rivals'da Elite+/FC Champion maqsad qiling",
        "🤝 League vs League'da 100% ishtirok eting",
    ]
}

# --- STATISTIKA MA'LUMOTLARI ---
def get_global_stats():
    return {
        "total_players": "19,000+",
        "total_teams": 690,
        "total_leagues": 35,
        "game_modes": 8,
        "max_ovr": 109,
        "icon_count": "150+",
        "monthly_players": "100M+",
        "platform": "iOS & Android"
    }

# ═══════════════════════════════════════════════════════════════
#  YORDAMCHI FUNKSIYALAR
# ═══════════════════════════════════════════════════════════════

def get_ovr_color(ovr):
    """OVR ga qarab rang qaytaradi"""
    if ovr >= 109: return "#FFD700"
    elif ovr >= 107: return "#FF8C00"
    elif ovr >= 105: return "#9400D3"
    elif ovr >= 103: return "#0080FF"
    elif ovr >= 100: return "#00C000"
    else: return "#808080"

def get_ovr_label(ovr):
    """OVR ga qarab label qaytaradi"""
    if ovr >= 109: return "🔱 ELITE"
    elif ovr >= 107: return "⭐ YULDUZ"
    elif ovr >= 105: return "💜 LEGEND"
    elif ovr >= 103: return "💙 GOLD PLUS"
    elif ovr >= 100: return "💚 GOLD"
    else: return "⚪ SILVER"

def calculate_team_ovr(players_ovr_list):
    """Jamoaning umumiy OVR ni hisoblash"""
    if not players_ovr_list or len(players_ovr_list) == 0:
        return 0
    sorted_ovr = sorted(players_ovr_list, reverse=True)
    # Asosiy 11 ta o'yinchi (yoki mavjud bo'lganlar)
    main = sorted_ovr[:11]
    if len(main) == 0:
        return 0
    # Oddiy o'rtacha (soddalashtirilgan hisoblash)
    team_ovr = sum(main) / len(main)
    return round(team_ovr, 1)

def get_star_display(stars):
    """Yulduz ko'rinishi"""
    return "⭐" * stars + "☆" * (5 - stars)

def format_price(price):
    """Narxni formatlash"""
    if price >= 1_000_000:
        return f"{price/1_000_000:.1f}M"
    elif price >= 1_000:
        return f"{price/1_000:.0f}K"
    return str(price)

def get_position_color(pos):
    """Pozitsiyaga qarab rang"""
    attackers = ["ST", "LW", "RW", "CAM", "CF", "SS", "LAM", "RAM", "RAF", "LAF"]
    midfielders = ["CM", "CDM", "CAM", "LM", "RM"]
    defenders = ["CB", "LB", "RB", "LWB", "RWB"]
    keepers = ["GK"]
    if pos in attackers: return "#FF4444"
    elif pos in midfielders: return "#44FF88"
    elif pos in defenders: return "#4488FF"
    elif pos in keepers: return "#FFAA00"
    return "#FFFFFF"

def simulate_match(team1_ovr, team2_ovr):
    """Oddiy o'yin simulyatsiyasi"""
    diff = team1_ovr - team2_ovr
    # Win probability
    win_prob = 0.5 + (diff / 200)
    win_prob = max(0.1, min(0.9, win_prob))

    result = random.random()
    if result < win_prob:
        outcome = "G'ALABA"
        goals_for = random.randint(1, 5)
        goals_against = random.randint(0, goals_for - 1)
    elif result < win_prob + 0.15:
        outcome = "DURRANG"
        goals_for = random.randint(0, 3)
        goals_against = goals_for
    else:
        outcome = "MAG'LUBIYAT"
        goals_against = random.randint(1, 5)
        goals_for = random.randint(0, goals_against - 1)

    return outcome, goals_for, goals_against

# ═══════════════════════════════════════════════════════════════
#  ASOSIY NAVIGATSIYA
# ═══════════════════════════════════════════════════════════════

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-size: 50px;'>⚽</div>
        <div style='font-size: 22px; font-weight: bold; color: #00FF88;'>FC Mobile 26</div>
        <div style='font-size: 13px; color: #aaaaaa;'>Companion App</div>
        <div style='height: 2px; background: linear-gradient(90deg, transparent, #00B050, transparent); margin: 10px 0;'></div>
    </div>
    """, unsafe_allow_html=True)

    menu_options = {
        "🏠 Bosh Sahifa": "home",
        "👥 O'yinchilar Bazasi": "players",
        "🏗️ Jamoa Quruvchi": "squad_builder",
        "📐 Formatsiya Tahlilchisi": "formations",
        "🎮 O'yin Rejimlari": "game_modes",
        "🧮 OVR Kalkulyatori": "ovr_calc",
        "📊 Statistika va Tahlil": "stats",
        "📅 Hodisalar Taqvimi": "events",
        "💡 Maslahatlar": "tips",
        "💰 Transfer Marketi": "transfer",
        "⚽ O'yin Simulyatori": "simulator",
        "🏆 Ligalar va Jamoalar": "leagues",
        "🔧 Sozlamalar": "settings",
    }

    selected_page = st.selectbox(
        "📍 Sahifani tanlang:",
        list(menu_options.keys()),
        key="nav_select"
    )
    page = menu_options[selected_page]

    st.markdown("---")

    # Sidebar qo'shimcha info
    st.markdown("""
    <div style='background: rgba(0,176,80,0.1); border: 1px solid rgba(0,176,80,0.3);
                border-radius: 10px; padding: 12px; margin: 5px 0;'>
        <div style='color: #00FF88; font-weight: bold; margin-bottom: 8px;'>📊 O'yin Statistikasi</div>
        <div style='color: #aaa; font-size: 12px;'>19,000+ O'yinchi</div>
        <div style='color: #aaa; font-size: 12px;'>690 Jamoa</div>
        <div style='color: #aaa; font-size: 12px;'>35 Liga</div>
        <div style='color: #aaa; font-size: 12px;'>100M+ Oylik o'yinchilar</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.3);
                border-radius: 10px; padding: 12px; margin: 5px 0;'>
        <div style='color: #FFD700; font-weight: bold; margin-bottom: 8px;'>🎯 Joriy META</div>
        <div style='color: #aaa; font-size: 12px;'>Formatsiya: 3-5-2</div>
        <div style='color: #aaa; font-size: 12px;'>O'yin: Head to Head</div>
        <div style='color: #aaa; font-size: 12px;'>Muhim: Tezlik + CDM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 11px; padding: 10px;'>
        FC Mobile 26 Companion v2.6<br>
        {datetime.now().strftime('%Y-%m-%d')}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  BOS SAHIFA
# ═══════════════════════════════════════════════════════════════

if page == "home":
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <div style='font-size: 70px;'>⚽</div>
        <div class='main-title'>EA SPORTS FC MOBILE 26</div>
        <div style='color: #aaaaaa; font-size: 16px; margin-top: 5px;'>
            To'liq Hamroh Dastur | Barcha ma'lumotlar bir joyda
        </div>
        <div style='height: 3px; background: linear-gradient(90deg, transparent, #00B050, #FFD700, transparent);
                    margin: 15px auto; width: 60%; border-radius: 2px;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Asosiy metriklar
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    stats = get_global_stats()

    with col1:
        st.metric("⚽ O'yinchilar", stats["total_players"], "19,000+")
    with col2:
        st.metric("🏟️ Jamoalar", stats["total_teams"], "690 klub")
    with col3:
        st.metric("🏆 Ligalar", stats["total_leagues"], "35 liga")
    with col4:
        st.metric("🎮 Rejimlar", stats["game_modes"], "8 tur")
    with col5:
        st.metric("⭐ MAX OVR", stats["max_ovr"], "109 OVR")
    with col6:
        st.metric("👥 O'yinchilar", stats["monthly_players"], "Oylik")

    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

    # O'yin haqida
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class='section-header'>🎯 FC Mobile 26 Haqida</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card'>
        <p style='color: #cccccc; line-height: 1.8; font-size: 15px;'>
        <b style='color: #00FF88;'>EA Sports FC Mobile 26</b> — bu EA Sports'ning mobil futbol o'yinlarining eng yangi
        va eng mukammal versiyasidir. FIFA Mobile nomi bilan 2016 yildan mavjud bo'lgan bu o'yin,
        2023 yilda EA Sports FC Mobile nomini oldi.
        </p>

        <p style='color: #cccccc; line-height: 1.8; font-size: 15px;'>
        <b style='color: #FFD700;'>Yangi FC Mobile 26 Yangiliklari:</b><br>
        ✅ Yangi UI dizayni — zamonaviy va toza interfeys<br>
        ✅ 7 ta yangi formatsiya qo'shildi<br>
        ✅ Jamoaviy nishon tizimi (Team Badge)<br>
        ✅ Yaxshilangan futbolchilar AI harakati<br>
        ✅ Yangilangan Division Rivals tizimi<br>
        ✅ Yuzlar skaneri yangilandi (Face Scans)<br>
        ✅ Referees va Kickoff Rush yaxshilandi<br>
        ✅ Drafts yangi funksiyasi qo'shildi
        </p>

        <p style='color: #cccccc; line-height: 1.8; font-size: 15px;'>
        O'yin <b style='color: #00B0FF;'>iOS va Android</b> platformalarida bepul yuklab olinadi,
        ammo ichki xaridlar (in-app purchases) mavjud.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='section-header'>🔥 META Xabarlari</div>
        """, unsafe_allow_html=True)

        # META ma'lumotlari
        meta_items = [
            ("🥇", "Eng yaxshi formatsiya", "3-5-2", "#FFD700"),
            ("⚡", "Eng muhim stat", "Tezlik (Pace)", "#00FF88"),
            ("🎯", "Eng yaxshi mode", "Division Rivals", "#00B0FF"),
            ("💎", "Eng qimmat karta", "Pele ICON", "#FF8C00"),
            ("📈", "OVR chegarasi", "109 (ELITE)", "#FF4444"),
            ("🏆", "Joriy event", "Glorious Eras", "#FFD700"),
        ]

        for icon, label, value, color in meta_items:
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center;
                        background: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 12px;
                        margin: 5px 0; border-left: 3px solid {color};'>
                <span style='color: #aaaaaa; font-size: 13px;'>{icon} {label}</span>
                <span style='color: {color}; font-weight: bold; font-size: 13px;'>{value}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

    # Qo'shimcha ma'lumotlar
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='section-header'>🌍 Versiyalar</div>
        """, unsafe_allow_html=True)
        versions = [
            ("🌐", "Global", "EA Sports", "iOS & Android"),
            ("🇨🇳", "Xitoy", "Tencent Games", "iOS & Android"),
            ("🇯🇵🇰🇷", "Yaponiya/Koreya", "Nexon", "iOS & Android"),
            ("🇻🇳", "Vyetnam", "Garena", "iOS & Android"),
        ]
        for flag, region, publisher, platform in versions:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px;
                        margin: 5px 0; border: 1px solid rgba(255,255,255,0.1);'>
                <b style='color: #00FF88;'>{flag} {region}</b><br>
                <span style='color: #aaa; font-size: 12px;'>Nashriyot: {publisher}</span><br>
                <span style='color: #666; font-size: 12px;'>{platform}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='section-header'>📅 Muhim Sanalar</div>
        """, unsafe_allow_html=True)
        dates = [
            ("2016", "O'yin chiqarildi (FIFA Mobile)", "#666"),
            ("2023", "FC Mobile nomi olindi", "#888"),
            ("Sep 2024", "FC Mobile 25 chiqarildi", "#00B050"),
            ("Aug 2025", "FC Mobile 26 Beta test", "#FFD700"),
            ("Sep 2025", "FC Mobile 26 rasmiy chiqdi", "#00FF88"),
            ("2026", "FC Mobile 27 kutilmoqda", "#00B0FF"),
        ]
        for year, event, color in dates:
            st.markdown(f"""
            <div style='display: flex; align-items: center; margin: 5px 0;'>
                <span style='color: {color}; font-weight: bold; min-width: 80px; font-size: 13px;'>{year}</span>
                <span style='color: #aaaaaa; font-size: 13px;'>→ {event}</span>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='section-header'>🎮 Platformalar</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style='background: rgba(0,176,80,0.1); border-radius: 10px; padding: 15px;'>
            <div style='margin: 8px 0;'>
                <span style='color: #00FF88; font-size: 18px;'>📱</span>
                <span style='color: #ccc;'> iOS (iPhone & iPad)</span>
                <br><span style='color: #666; font-size: 12px; padding-left: 30px;'>App Store - Bepul</span>
            </div>
            <div style='margin: 8px 0;'>
                <span style='color: #00FF88; font-size: 18px;'>🤖</span>
                <span style='color: #ccc;'> Android</span>
                <br><span style='color: #666; font-size: 12px; padding-left: 30px;'>Google Play - Bepul</span>
            </div>
            <div style='margin: 8px 0; color: #888;'>
                <span style='color: #666; font-size: 16px;'>💻</span>
                <span style='color: #666;'> Windows (to'xtatilgan)</span>
                <br><span style='color: #555; font-size: 12px; padding-left: 30px;'>2017 yildan qo'llab quvvatlanmaydi</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pastki qism - Tezkor havolalar
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🚀 Tezkor Havolalar")

    quick_cols = st.columns(4)
    quick_links = [
        ("👥", "O'yinchilar Bazasiga o'tish", "players"),
        ("🏗️", "Jamoa qurish", "squad_builder"),
        ("📐", "Formatsiya tanlash", "formations"),
        ("💡", "Maslahatlar olish", "tips"),
    ]

    for i, (icon, text, target) in enumerate(quick_links):
        with quick_cols[i]:
            if st.button(f"{icon} {text}", key=f"quick_{target}"):
                st.info(f"Iltimos yuqoridan '{text}' ni tanlang")


# ═══════════════════════════════════════════════════════════════
#  O'YINCHILAR BAZASI
# ═══════════════════════════════════════════════════════════════

elif page == "players":
    st.markdown("""
    <div class='section-header'>👥 O'yinchilar Bazasi</div>
    """, unsafe_allow_html=True)

    # Filterlar
    with st.expander("🔍 Filterlar va Qidiruv", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            search_name = st.text_input("🔎 O'yinchi ismi", placeholder="Ronaldo, Messi...")

        with col2:
            positions = ["Hammasi"] + sorted(list(set([p["position"] for p in PLAYERS_DATA])))
            filter_pos = st.selectbox("📍 Pozitsiya", positions)

        with col3:
            leagues_list = ["Hammasi"] + sorted(list(set([p["league"] for p in PLAYERS_DATA])))
            filter_league = st.selectbox("🏆 Liga", leagues_list)

        with col4:
            types_list = ["Hammasi"] + sorted(list(set([p["type"] for p in PLAYERS_DATA])))
            filter_type = st.selectbox("⭐ Karta turi", types_list)

        with col5:
            min_ovr = st.slider("📊 Minimal OVR", 90, 109, 100)

    # Ma'lumotlarni filterlash
    filtered = PLAYERS_DATA.copy()

    if search_name:
        filtered = [p for p in filtered if search_name.lower() in p["name"].lower()]
    if filter_pos != "Hammasi":
        filtered = [p for p in filtered if p["position"] == filter_pos]
    if filter_league != "Hammasi":
        filtered = [p for p in filtered if p["league"] == filter_league]
    if filter_type != "Hammasi":
        filtered = [p for p in filtered if p["type"] == filter_type]
    filtered = [p for p in filtered if p["ovr"] >= min_ovr]

    # Saralash
    sort_col1, sort_col2 = st.columns([3, 1])
    with sort_col1:
        sort_by = st.selectbox("🔢 Saralash:", ["OVR (yuqoridan)", "OVR (pastdan)", "Narx (yuqoridan)", "Ismi (A-Z)", "Tezlik", "Shoot"])
    with sort_col2:
        st.metric("🔍 Natijalar", f"{len(filtered)} ta")

    # Saralash logikasi
    sort_map = {
        "OVR (yuqoridan)": ("ovr", True),
        "OVR (pastdan)": ("ovr", False),
        "Narx (yuqoridan)": ("price", True),
        "Ismi (A-Z)": ("name", False),
        "Tezlik": ("pace", True),
        "Shoot": ("shooting", True),
    }
    sk, sr = sort_map[sort_by]
    filtered = sorted(filtered, key=lambda x: x[sk], reverse=sr)

    # O'yinchilar ko'rinishi
    view_mode = st.radio("Korinish:", ["🃏 Karta", "📋 Jadval"], horizontal=True)

    if view_mode == "🃏 Karta":
        # Karta ko'rinishi
        cards_per_row = 4
        for i in range(0, min(len(filtered), 40), cards_per_row):
            cols = st.columns(cards_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered):
                    p = filtered[i + j]
                    ovr_color = get_ovr_color(p["ovr"])
                    pos_color = get_position_color(p["position"])
                    with col:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(30,30,50,0.9), rgba(10,20,40,0.9));
                                    border: 2px solid {ovr_color}44; border-radius: 15px; padding: 15px;
                                    text-align: center; margin: 5px 0;
                                    box-shadow: 0 4px 15px {ovr_color}22;
                                    transition: all 0.3s ease;'>

                            <!-- OVR Badge -->
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                                <div style='background: {ovr_color}; color: #000; font-weight: bold;
                                            font-size: 22px; width: 50px; height: 50px; border-radius: 50%;
                                            display: flex; align-items: center; justify-content: center;'>
                                    {p["ovr"]}
                                </div>
                                <div style='background: {pos_color}33; color: {pos_color}; font-weight: bold;
                                            padding: 4px 8px; border-radius: 5px; font-size: 13px;'>
                                    {p["position"]}
                                </div>
                            </div>

                            <!-- Ism -->
                            <div style='font-weight: bold; font-size: 14px; color: #ffffff;
                                        margin: 8px 0; min-height: 40px;'>{p["name"]}</div>

                            <!-- Jamoa va liga -->
                            <div style='color: #aaaaaa; font-size: 11px; margin: 3px 0;'>
                                🏟️ {p["team"]}
                            </div>
                            <div style='color: #888; font-size: 11px; margin: 3px 0;'>
                                🌍 {p["nationality"]}
                            </div>

                            <!-- Karta turi -->
                            <div style='background: {ovr_color}22; color: {ovr_color};
                                        border: 1px solid {ovr_color}44; border-radius: 5px;
                                        padding: 3px 8px; font-size: 11px; font-weight: bold;
                                        margin: 8px 0;'>
                                {get_ovr_label(p["ovr"])}
                            </div>

                            <!-- Stats mini bar -->
                            <div style='margin: 8px 0;'>
                                <div style='display: flex; justify-content: space-between; font-size: 10px; color: #888;'>
                                    <span>PAC</span><span>SHO</span><span>PAS</span><span>DRI</span>
                                </div>
                                <div style='display: flex; gap: 3px; margin-top: 3px;'>
                                    {"".join([f'<div style="flex:1; height:5px; border-radius:3px; background: linear-gradient(90deg, #00B050, #007A35); opacity: {stat/100};"></div>' for stat in [p["pace"], p["shooting"], p["passing"], p["dribbling"]]])}
                                </div>
                                <div style='display: flex; justify-content: space-between; font-size: 10px; color: #ccc; margin-top: 2px;'>
                                    <span>{p["pace"]}</span><span>{p["shooting"]}</span><span>{p["passing"]}</span><span>{p["dribbling"]}</span>
                                </div>
                            </div>

                            <!-- Narx -->
                            <div style='color: #FFD700; font-size: 12px; font-weight: bold; margin-top: 8px;'>
                                💰 {format_price(p["price"])} Coins
                            </div>

                            <!-- Skill & WF -->
                            <div style='display: flex; justify-content: center; gap: 10px; margin-top: 5px; font-size: 11px; color: #888;'>
                                <span>SM: {get_star_display(p["skill_moves"])}</span>
                                <span>WF: {get_star_display(p["weak_foot"])}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        # Jadval ko'rinishi
        df_players = pd.DataFrame(filtered)
        display_cols = ["name", "position", "ovr", "team", "league", "nationality",
                       "pace", "shooting", "passing", "dribbling", "defending", "physical", "type"]
        df_display = df_players[display_cols].copy()
        df_display.columns = ["Ism", "Pozitsiya", "OVR", "Jamoa", "Liga", "Millat",
                              "Tezlik", "Udarish", "Pas", "Dribbling", "Himoya", "Jismoniy", "Tur"]
        st.dataframe(df_display, use_container_width=True, height=600)

    # Statistika grafiklari
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 O'yinchilar Statistikasi")

    stat_col1, stat_col2 = st.columns(2)

    with stat_col1:
        # Pozitsiya bo'yicha taqsimot
        pos_counts = {}
        for p in PLAYERS_DATA:
            pos = p["position"]
            pos_counts[pos] = pos_counts.get(pos, 0) + 1

        fig_pos = px.pie(
            values=list(pos_counts.values()),
            names=list(pos_counts.keys()),
            title="Pozitsiyalar bo'yicha taqsimot",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pos.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="#00FF88"
        )
        st.plotly_chart(fig_pos, use_container_width=True)

    with stat_col2:
        # OVR taqsimoti
        ovr_values = [p["ovr"] for p in PLAYERS_DATA]
        fig_ovr = px.histogram(
            x=ovr_values,
            nbins=10,
            title="OVR Taqsimoti",
            color_discrete_sequence=["#00B050"],
            labels={"x": "OVR", "y": "O'yinchilar soni"}
        )
        fig_ovr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.3)",
            font_color="white",
            title_font_color="#00FF88"
        )
        st.plotly_chart(fig_ovr, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  JAMOA QURUVCHI
# ═══════════════════════════════════════════════════════════════

elif page == "squad_builder":
    st.markdown("""
    <div class='section-header'>🏗️ Jamoa Quruvchi</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card'>
        <b style='color: #00FF88;'>ℹ️ Qanday ishlaydi?</b><br>
        <span style='color: #aaa;'>Har bir pozitsiya uchun o'yinchi tanlang. Tizim avtomatik ravishda 
        jamoa OVR, kimyo va tavsiyalarni hisoblab beradi.</span>
    </div>
    """, unsafe_allow_html=True)

    # Formatsiya tanlash
    form_col1, form_col2 = st.columns([2, 1])
    with form_col1:
        selected_formation = st.selectbox(
            "📐 Formatsiyani tanlang:",
            list(FORMATIONS.keys()),
            key="squad_formation"
        )
    with form_col2:
        form_info = FORMATIONS[selected_formation]
        tier_colors = {"S": "#FFD700", "A": "#00B050", "B": "#0088FF", "C": "#FF4444"}
        tier_color = tier_colors.get(form_info["tier"], "#888")
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px;
                    border: 1px solid {tier_color}44; margin-top: 5px;'>
            <span style='color: {tier_color}; font-weight: bold;'>{form_info["tier"]} Tier</span>
            <span style='color: #aaa; font-size: 12px;'> — {form_info["style"]}</span><br>
            <span style='color: #888; font-size: 12px;'>{form_info["description"]}</span>
        </div>
        """, unsafe_allow_html=True)

    # Jamoa qurish
    positions = FORMATIONS[selected_formation]["positions"]
    player_names = ["— Tanlang —"] + sorted([p["name"] for p in PLAYERS_DATA])

    st.markdown("### 👨‍⚽ O'yinchilarni tanlang")

    # Saqlash uchun
    if "squad" not in st.session_state:
        st.session_state.squad = {}

    # Pozitsiyalar bo'yicha guruhlash
    gk_pos = [p for p in positions if p == "GK"]
    def_pos = [p for p in positions if p in ["CB", "LB", "RB", "LWB", "RWB"]]
    mid_pos = [p for p in positions if p in ["CDM", "CM", "CAM", "LM", "RM", "LAM", "RAM", "LAF", "RAF"]]
    att_pos = [p for p in positions if p in ["ST", "CF", "LW", "RW", "SS"]]

    # Ko'rsatish
    all_pos_groups = [
        ("⚡ Hujumchilar", att_pos),
        ("🎯 O'rtamiyonlar", mid_pos),
        ("🛡️ Himoyachilar", def_pos),
        ("🧤 Darvozabon", gk_pos),
    ]

    squad_ovr_list = []

    for group_name, group_positions in all_pos_groups:
        if group_positions:
            st.markdown(f"**{group_name}**")
            cols = st.columns(len(group_positions))
            for idx, (pos, col) in enumerate(zip(group_positions, cols)):
                key = f"pos_{pos}_{idx}"
                with col:
                    selected_player_name = st.selectbox(
                        pos,
                        player_names,
                        key=key
                    )
                    if selected_player_name != "— Tanlang —":
                        player_data = next((p for p in PLAYERS_DATA if p["name"] == selected_player_name), None)
                        if player_data:
                            ovr_color = get_ovr_color(player_data["ovr"])
                            st.markdown(f"""
                            <div style='text-align: center; background: {ovr_color}22;
                                        border: 1px solid {ovr_color}44; border-radius: 8px; padding: 8px; margin-top: -10px;'>
                                <div style='color: {ovr_color}; font-size: 20px; font-weight: bold;'>{player_data["ovr"]}</div>
                                <div style='color: #aaa; font-size: 10px;'>{player_data["type"]}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            squad_ovr_list.append(player_data["ovr"])
                            st.session_state.squad[key] = player_data

    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

    # Jamoa OVR va statistika
    if squad_ovr_list:
        team_ovr = calculate_team_ovr(squad_ovr_list)

        result_col1, result_col2, result_col3, result_col4 = st.columns(4)

        with result_col1:
            ovr_color = get_ovr_color(int(team_ovr))
            st.markdown(f"""
            <div style='text-align: center; background: {ovr_color}22; border: 2px solid {ovr_color};
                        border-radius: 15px; padding: 20px;'>
                <div style='font-size: 48px; font-weight: bold; color: {ovr_color};'>{team_ovr:.0f}</div>
                <div style='color: #aaa;'>Jamoa OVR</div>
                <div style='color: {ovr_color}; font-size: 12px;'>{get_ovr_label(int(team_ovr))}</div>
            </div>
            """, unsafe_allow_html=True)

        with result_col2:
            avg_pace = np.mean([p["pace"] for p in st.session_state.squad.values() if isinstance(p, dict)])
            st.markdown(f"""
            <div style='text-align: center; background: rgba(0,176,80,0.2); border: 2px solid #00B050;
                        border-radius: 15px; padding: 20px;'>
                <div style='font-size: 40px; font-weight: bold; color: #00FF88;'>{avg_pace:.0f}</div>
                <div style='color: #aaa;'>O'rtacha Tezlik</div>
            </div>
            """, unsafe_allow_html=True)

        with result_col3:
            total_price = sum([p["price"] for p in st.session_state.squad.values() if isinstance(p, dict)])
            st.markdown(f"""
            <div style='text-align: center; background: rgba(255,215,0,0.2); border: 2px solid #FFD700;
                        border-radius: 15px; padding: 20px;'>
                <div style='font-size: 32px; font-weight: bold; color: #FFD700;'>{format_price(total_price)}</div>
                <div style='color: #aaa;'>Jamoa Narxi</div>
            </div>
            """, unsafe_allow_html=True)

        with result_col4:
            selected_count = len(squad_ovr_list)
            st.markdown(f"""
            <div style='text-align: center; background: rgba(0,136,255,0.2); border: 2px solid #0088FF;
                        border-radius: 15px; padding: 20px;'>
                <div style='font-size: 40px; font-weight: bold; color: #00B0FF;'>{selected_count}/11</div>
                <div style='color: #aaa;'>Tanlangan O'yinchilar</div>
            </div>
            """, unsafe_allow_html=True)

        # Radar chart
        if len(st.session_state.squad) >= 3:
            team_stats = {
                "Tezlik": np.mean([p["pace"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
                "Udarish": np.mean([p["shooting"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
                "Passing": np.mean([p["passing"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
                "Dribbling": np.mean([p["dribbling"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
                "Himoya": np.mean([p["defending"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
                "Jismoniy": np.mean([p["physical"] for p in st.session_state.squad.values() if isinstance(p, dict)]),
            }

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=list(team_stats.values()),
                theta=list(team_stats.keys()),
                fill='toself',
                fillcolor='rgba(0,176,80,0.2)',
                line=dict(color='#00B050', width=2),
                name='Sizning jamoangiz'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], color="#666"),
                    angularaxis=dict(color="#aaa")
                ),
                showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title="Jamoa Statistikasi Radar",
                title_font_color="#00FF88"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # Savat tozalash tugmasi
    if st.button("🗑️ Jamoani tozalash", key="clear_squad"):
        st.session_state.squad = {}
        st.rerun()


# ═══════════════════════════════════════════════════════════════
#  FORMATSIYA TAHLILCHISI
# ═══════════════════════════════════════════════════════════════

elif page == "formations":
    st.markdown("""
    <div class='section-header'>📐 Formatsiya Tahlilchisi</div>
    """, unsafe_allow_html=True)

    # Formatsiyalar jadvali
    col1, col2 = st.columns([1, 2])

    with col1:
        selected_form = st.selectbox(
            "Formatsiyani tanlang:",
            list(FORMATIONS.keys()),
            key="form_select"
        )
        form_data = FORMATIONS[selected_form]
        tier_colors = {"S": "#FFD700", "A": "#00B050", "B": "#0088FF", "C": "#FF4444"}
        tier_color = tier_colors.get(form_data["tier"], "#888")

        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border: 2px solid {tier_color};
                    border-radius: 12px; padding: 20px; margin: 10px 0;'>
            <div style='color: {tier_color}; font-size: 28px; font-weight: bold; text-align: center;'>
                {selected_form}
            </div>
            <div style='text-align: center; margin: 5px 0;'>
                <span style='background: {tier_color}; color: #000; padding: 3px 12px;
                             border-radius: 15px; font-weight: bold;'>{form_data["tier"]} TIER</span>
            </div>
            <div style='color: #aaa; font-size: 13px; margin: 10px 0;'>{form_data["description"]}</div>
            <div style='color: #888; font-size: 12px;'>
                🎯 Maqsad: {form_data["best_for"]}<br>
                ⚽ Uslub: {form_data["style"]}<br>
                🎮 Qiyinchilik: {form_data["difficulty"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # META rating
        meta = form_data["meta_rating"]
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px;'>
            <div style='color: #aaa; font-size: 13px; margin-bottom: 5px;'>📊 META Rating</div>
            <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 20px; overflow: hidden;'>
                <div style='width: {meta}%; height: 100%;
                            background: linear-gradient(90deg, {"#00B050" if meta >= 90 else "#FFD700" if meta >= 80 else "#FF4444"}, transparent);
                            border-radius: 10px;'></div>
            </div>
            <div style='color: {"#00FF88" if meta >= 90 else "#FFD700" if meta >= 80 else "#FF4444"};
                        font-size: 18px; font-weight: bold; text-align: center;'>{meta}/100</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Maydon vizualizatsiyasi
        st.markdown("### ⚽ Maydon Joylashuvi")

        positions = form_data["positions"]

        # Formatsiyani maydon ko'rinishida chizish
        def draw_field(formation_name, positions):
            fig = go.Figure()

            # Maydon rangini o'rnatish
            fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=130,
                         fillcolor="#2D7A2D", line=dict(color="#1a5c1a", width=2))

            # O'rtadagi chiziq
            fig.add_shape(type="line", x0=0, y0=65, x1=100, y1=65,
                         line=dict(color="white", width=1, dash="dash"))

            # O'rtadagi doira
            fig.add_shape(type="circle", x0=40, y0=55, x1=60, y1=75,
                         line=dict(color="white", width=1))

            # Jazoga tashlanish joyi
            fig.add_shape(type="rect", x0=20, y0=0, x1=80, y1=20,
                         line=dict(color="white", width=1), fillcolor="rgba(0,0,0,0)")
            fig.add_shape(type="rect", x0=20, y0=110, x1=80, y1=130,
                         line=dict(color="white", width=1), fillcolor="rgba(0,0,0,0)")

            # Gol maydonlari
            fig.add_shape(type="rect", x0=35, y0=0, x1=65, y1=8,
                         line=dict(color="white", width=1), fillcolor="rgba(0,0,0,0)")
            fig.add_shape(type="rect", x0=35, y0=122, x1=65, y1=130,
                         line=dict(color="white", width=1), fillcolor="rgba(0,0,0,0)")

            # O'yinchilar joylashuvi
            pos_coords = {
                "GK": [(50, 5)],
                "CB": [(30, 25), (50, 25), (70, 25)] if positions.count("CB") == 3
                      else [(35, 25), (65, 25)] if positions.count("CB") == 2
                      else [(50, 25)],
                "LB": [(10, 30)], "RB": [(90, 30)],
                "LWB": [(10, 40)], "RWB": [(90, 40)],
                "CDM": [(35, 45), (65, 45)] if positions.count("CDM") == 2 else [(50, 45)],
                "CM": [], "LM": [(10, 60)], "RM": [(90, 60)],
                "CAM": [(50, 70)], "LAM": [(25, 70)], "RAM": [(75, 70)],
                "LAF": [(25, 75)], "RAF": [(75, 75)],
                "LW": [(15, 90)], "RW": [(85, 90)],
                "ST": [], "CF": [(50, 100)],
            }

            # CM o'yinchilar soni
            cm_count = positions.count("CM")
            if cm_count == 1: pos_coords["CM"] = [(50, 55)]
            elif cm_count == 2: pos_coords["CM"] = [(35, 55), (65, 55)]
            elif cm_count == 3: pos_coords["CM"] = [(25, 55), (50, 55), (75, 55)]

            # ST o'yinchilar soni
            st_count = positions.count("ST")
            if st_count == 1: pos_coords["ST"] = [(50, 110)]
            elif st_count == 2: pos_coords["ST"] = [(35, 110), (65, 110)]

            # CB 4 ta bo'lsa
            if positions.count("CB") == 4:
                pos_coords["CB"] = [(20, 25), (40, 25), (60, 25), (80, 25)]

            # Marker'larni chizish
            added_pos = {}
            for pos in positions:
                if pos not in added_pos:
                    added_pos[pos] = 0
                idx = added_pos[pos]
                coords = pos_coords.get(pos, [])
                if idx < len(coords):
                    x, y = coords[idx]
                    pos_color_map = {
                        "GK": "#FFB300", "CB": "#1565C0", "LB": "#1565C0",
                        "RB": "#1565C0", "LWB": "#0277BD", "RWB": "#0277BD",
                        "CDM": "#2E7D32", "CM": "#388E3C", "LM": "#43A047",
                        "RM": "#43A047", "CAM": "#F57F17", "LAM": "#F57F17",
                        "RAM": "#F57F17", "LAF": "#E65100", "RAF": "#E65100",
                        "LW": "#D32F2F", "RW": "#D32F2F", "ST": "#B71C1C",
                        "CF": "#C62828",
                    }
                    color = pos_color_map.get(pos, "#ffffff")

                    # Doira
                    fig.add_shape(type="circle",
                                 x0=x-6, y0=y-6, x1=x+6, y1=y+6,
                                 fillcolor=color, line=dict(color="white", width=2))
                    # Matn
                    fig.add_annotation(x=x, y=y, text=pos,
                                      font=dict(color="white", size=8, family="Arial Black"),
                                      showarrow=False)
                added_pos[pos] += 1

            fig.update_layout(
                width=400, height=500,
                xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[0, 130], showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=dict(text=f"{formation_name}", font=dict(color="#00FF88", size=16)),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            return fig

        field_fig = draw_field(selected_form, positions)
        st.plotly_chart(field_fig, use_container_width=True)

    # Formatsiya afzalliklari va kamchiliklari
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

    pro_con_col1, pro_con_col2 = st.columns(2)

    with pro_con_col1:
        st.markdown("**✅ Afzalliklari:**")
        for pro in form_data["pros"]:
            st.markdown(f"""
            <div style='background: rgba(0,176,80,0.15); border-left: 3px solid #00B050;
                        border-radius: 0 8px 8px 0; padding: 8px 12px; margin: 5px 0; color: #cccccc;'>
                ✅ {pro}
            </div>
            """, unsafe_allow_html=True)

    with pro_con_col2:
        st.markdown("**❌ Kamchiliklari:**")
        for con in form_data["cons"]:
            st.markdown(f"""
            <div style='background: rgba(255,68,68,0.15); border-left: 3px solid #FF4444;
                        border-radius: 0 8px 8px 0; padding: 8px 12px; margin: 5px 0; color: #cccccc;'>
                ❌ {con}
            </div>
            """, unsafe_allow_html=True)

    # Barcha formatsiyalar taqqoslama
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Barcha Formatsiyalar Reytingi")

    form_data_list = []
    for name, data in FORMATIONS.items():
        form_data_list.append({
            "Formatsiya": name,
            "Tier": data["tier"],
            "META Rating": data["meta_rating"],
            "Uslub": data["style"],
            "Eng yaxshi rejim": data["best_for"],
            "Qiyinchilik": data["difficulty"]
        })

    df_forms = pd.DataFrame(form_data_list).sort_values("META Rating", ascending=False)

    fig_bar = px.bar(
        df_forms,
        x="Formatsiya",
        y="META Rating",
        color="Tier",
        color_discrete_map={"S": "#FFD700", "A": "#00B050", "B": "#0088FF", "C": "#FF4444"},
        title="Formatsiyalar META Reytingi",
        text="META Rating"
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color="white",
        title_font_color="#00FF88"
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  O'YIN REJIMLARI
# ═══════════════════════════════════════════════════════════════

elif page == "game_modes":
    st.markdown("""
    <div class='section-header'>🎮 O'yin Rejimlari</div>
    """, unsafe_allow_html=True)

    # Rejimlar kartalari
    mode_names = list(GAME_MODES.keys())
    cols_per_row = 2

    for i in range(0, len(mode_names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(mode_names):
                mode_name = mode_names[i + j]
                mode = GAME_MODES[mode_name]
                with col:
                    with st.expander(f"{mode['icon']} {mode_name}", expanded=(i + j < 2)):
                        st.markdown(f"""
                        <div style='padding: 10px;'>
                            <div style='color: #aaaaaa; font-size: 14px; margin-bottom: 12px; line-height: 1.6;'>
                                {mode["description"]}
                            </div>

                            <div style='margin: 8px 0;'>
                                <span style='color: #FFD700; font-weight: bold;'>🏆 Mukofotlar:</span>
                                <span style='color: #ccc; font-size: 13px;'> {mode["rewards"]}</span>
                            </div>

                            <div style='margin: 8px 0;'>
                                <span style='color: #00B0FF; font-weight: bold;'>📅 Mavsumlar:</span>
                                <span style='color: #ccc; font-size: 13px;'> {mode["seasons"]}</span>
                            </div>

                            <div style='margin: 8px 0;'>
                                <span style='color: #FF8844; font-weight: bold;'>⚡ Qiyinchilik:</span>
                                <span style='color: #ccc; font-size: 13px;'> {mode["difficulty"]}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("**💡 Maslahatlar:**")
                        for tip in mode["tips"]:
                            st.markdown(f"""
                            <div style='background: rgba(0,176,80,0.1); border-left: 2px solid #00B050;
                                        padding: 6px 10px; margin: 4px 0; border-radius: 0 5px 5px 0;
                                        color: #cccccc; font-size: 13px;'>
                                {tip}
                            </div>
                            """, unsafe_allow_html=True)

    # O'yin rejimlari taqqoslash
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### ⚖️ Rejimlar Taqqoslash")

    diff_map = {"Oson": 1, "O'rta": 2, "Qiyin": 3, "Juda qiyin": 4}
    mode_compare = []
    for name, mode in GAME_MODES.items():
        mode_compare.append({
            "Rejim": name,
            "Icon": mode["icon"],
            "Qiyinchilik": diff_map.get(mode["difficulty"], 2),
            "Uslub": mode["difficulty"]
        })

    df_modes = pd.DataFrame(mode_compare)
    fig_modes = px.bar(
        df_modes,
        x="Rejim",
        y="Qiyinchilik",
        color="Uslub",
        title="O'yin Rejimlari Qiyinchiligi",
        color_discrete_map={
            "Oson": "#00B050", "O'rta": "#FFD700",
            "Qiyin": "#FF8844", "Juda qiyin": "#FF4444"
        },
        text="Uslub"
    )
    fig_modes.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color="white",
        title_font_color="#00FF88",
        yaxis=dict(tickvals=[1,2,3,4], ticktext=["Oson", "O'rta", "Qiyin", "Juda qiyin"])
    )
    st.plotly_chart(fig_modes, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  OVR KALKULYATORI
# ═══════════════════════════════════════════════════════════════

elif page == "ovr_calc":
    st.markdown("""
    <div class='section-header'>🧮 OVR Kalkulyatori</div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Jamoa OVR", "⬆️ Rank Up Hisoblash", "🆚 Taqqoslash"])

    with tab1:
        st.markdown("### 📊 Jamoa OVR Hisoblash")
        st.markdown("""
        <div class='glass-card'>
        11 ta asosiy o'yinchi va zaxira o'yinchilarning base OVR ni kiriting.
        Tizim avtomatik ravishda jamoaning umumiy OVR ni hisoblaydi.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**⚽ Asosiy 11 ta o'yinchi:**")
        main_ovrs = []
        main_cols = st.columns(4)
        for i in range(11):
            with main_cols[i % 4]:
                ovr_val = st.number_input(
                    f"O'yinchi {i+1}",
                    min_value=70, max_value=120, value=100,
                    key=f"main_player_{i}"
                )
                main_ovrs.append(ovr_val)

        st.markdown("**🔄 Zaxira o'yinchilar (ixtiyoriy):**")
        sub_ovrs = []
        sub_cols = st.columns(4)
        for i in range(7):
            with sub_cols[i % 4]:
                ovr_val = st.number_input(
                    f"Zaxira {i+1}",
                    min_value=70, max_value=120, value=95,
                    key=f"sub_player_{i}"
                )
                sub_ovrs.append(ovr_val)

        if st.button("🧮 OVR Hisoblash", key="calc_ovr"):
            team_ovr = calculate_team_ovr(main_ovrs)
            ovr_color = get_ovr_color(int(team_ovr))

            result_cols = st.columns(3)
            with result_cols[0]:
                st.markdown(f"""
                <div style='text-align: center; background: {ovr_color}22;
                            border: 3px solid {ovr_color}; border-radius: 20px; padding: 25px;'>
                    <div style='font-size: 60px; font-weight: bold; color: {ovr_color};'>{team_ovr:.0f}</div>
                    <div style='color: #aaa; font-size: 16px;'>Jamoaning OVR si</div>
                    <div style='color: {ovr_color}; font-size: 14px;'>{get_ovr_label(int(team_ovr))}</div>
                </div>
                """, unsafe_allow_html=True)

            with result_cols[1]:
                st.markdown(f"""
                <div style='background: rgba(0,176,80,0.1); border: 1px solid #00B050;
                            border-radius: 15px; padding: 20px;'>
                    <div style='color: #00FF88; font-weight: bold; margin-bottom: 10px;'>📊 Statistika</div>
                    <div style='color: #ccc; font-size: 13px;'>
                        Eng yuqori: <b style='color: #FFD700;'>{max(main_ovrs)}</b><br>
                        Eng past: <b style='color: #FF4444;'>{min(main_ovrs)}</b><br>
                        O'rtacha: <b style='color: #00FF88;'>{np.mean(main_ovrs):.1f}</b><br>
                        Farq: <b style='color: #00B0FF;'>{max(main_ovrs) - min(main_ovrs)}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with result_cols[2]:
                next_ovr = int(team_ovr) + 1
                needed = next_ovr * 11 - sum(sorted(main_ovrs, reverse=True)[:11])
                st.markdown(f"""
                <div style='background: rgba(255,165,0,0.1); border: 1px solid #FFA500;
                            border-radius: 15px; padding: 20px;'>
                    <div style='color: #FFD700; font-weight: bold; margin-bottom: 10px;'>⬆️ Keyingi OVR</div>
                    <div style='color: #ccc; font-size: 13px;'>
                        Maqsad: <b style='color: #FFD700;'>{next_ovr} OVR</b><br>
                        Kerakli: <b style='color: #00FF88;'>+{max(0, needed):.0f} OVR</b><br>
                        Strategiya: <b style='color: #00B0FF;'>Eng past kartani yaxshilang</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # OVR taqsimot grafigi
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(
                x=[f"O'yinchi {i+1}" for i in range(11)],
                y=main_ovrs,
                marker=dict(
                    color=main_ovrs,
                    colorscale=[[0, "#FF4444"], [0.5, "#FFD700"], [1, "#00B050"]],
                    colorbar=dict(title="OVR")
                )
            ))
            fig_dist.update_layout(
                title="O'yinchilar OVR Taqsimoti",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0.3)",
                font_color="white",
                title_font_color="#00FF88"
            )
            st.plotly_chart(fig_dist, use_container_width=True)

    with tab2:
        st.markdown("### ⬆️ Rank Up Hisoblagich")

        rank_col1, rank_col2 = st.columns(2)
        with rank_col1:
            base_ovr = st.number_input("Bazaviy OVR:", min_value=80, max_value=110, value=100)
        with rank_col2:
            current_ranks = st.number_input("Joriy Rank darajalari:", min_value=0, max_value=50, value=0)

        current_total = base_ovr + current_ranks

        rank_info = []
        for ranks in range(0, 21):
            total = base_ovr + ranks
            rank_info.append({"Rank": ranks, "Total OVR": total, "Qo'shilgan": f"+{ranks}"})

        df_ranks = pd.DataFrame(rank_info)

        st.markdown(f"""
        <div style='background: rgba(0,176,80,0.15); border: 2px solid #00B050;
                    border-radius: 15px; padding: 20px; text-align: center;'>
            <div style='color: #aaa;'>Joriy OVR</div>
            <div style='font-size: 50px; font-weight: bold; color: {get_ovr_color(current_total)};'>
                {current_total}
            </div>
            <div style='color: #aaa;'>Base: {base_ovr} + Rank: {current_ranks} = {current_total}</div>
        </div>
        """, unsafe_allow_html=True)

        fig_rank = px.line(
            df_ranks, x="Rank", y="Total OVR",
            title=f"Rank Up OVR Progressi (Base: {base_ovr})",
            markers=True,
            color_discrete_sequence=["#00B050"]
        )
        fig_rank.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.3)",
            font_color="white",
            title_font_color="#00FF88"
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    with tab3:
        st.markdown("### 🆚 O'yinchilar Taqqoslash")

        comp_col1, comp_col2 = st.columns(2)
        player_names_list = [p["name"] for p in PLAYERS_DATA]

        with comp_col1:
            player1_name = st.selectbox("O'yinchi 1:", player_names_list, key="comp_p1")
        with comp_col2:
            player2_name = st.selectbox("O'yinchi 2:", player_names_list, index=1, key="comp_p2")

        p1 = next((p for p in PLAYERS_DATA if p["name"] == player1_name), None)
        p2 = next((p for p in PLAYERS_DATA if p["name"] == player2_name), None)

        if p1 and p2:
            stats_to_compare = ["pace", "shooting", "passing", "dribbling", "defending", "physical"]
            stat_names = ["Tezlik", "Udarish", "Pas", "Dribbling", "Himoya", "Jismoniy"]

            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatterpolar(
                r=[p1[s] for s in stats_to_compare],
                theta=stat_names, fill='toself',
                name=p1["name"],
                fillcolor='rgba(0,176,80,0.2)',
                line=dict(color='#00B050', width=2)
            ))
            fig_comp.add_trace(go.Scatterpolar(
                r=[p2[s] for s in stats_to_compare],
                theta=stat_names, fill='toself',
                name=p2["name"],
                fillcolor='rgba(255,68,68,0.2)',
                line=dict(color='#FF4444', width=2)
            ))
            fig_comp.update_layout(
                polar=dict(radialaxis=dict(range=[0, 100], color="#666")),
                showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title="Statistika Taqqoslash",
                title_font_color="#00FF88"
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            # Parallel taqqoslash
            comp_table_cols = st.columns(3)
            with comp_table_cols[0]:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='color: #00FF88; font-size: 18px; font-weight: bold;'>{p1["name"]}</div>
                    <div style='font-size: 40px; font-weight: bold; color: {get_ovr_color(p1["ovr"])};'>{p1["ovr"]}</div>
                    <div style='color: #aaa;'>{p1["position"]} | {p1["team"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with comp_table_cols[1]:
                for stat, name in zip(stats_to_compare, stat_names):
                    v1, v2 = p1[stat], p2[stat]
                    winner = "green" if v1 > v2 else "red" if v1 < v2 else "gray"
                    st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; align-items: center;
                                padding: 4px; margin: 3px 0; border-radius: 5px;
                                background: rgba(255,255,255,0.05);'>
                        <span style='color: {"#00FF88" if v1 > v2 else "#FF4444" if v1 < v2 else "#aaa"};
                                     font-weight: bold;'>{v1}</span>
                        <span style='color: #666; font-size: 11px;'>{name}</span>
                        <span style='color: {"#FF4444" if v1 > v2 else "#00FF88" if v1 < v2 else "#aaa"};
                                     font-weight: bold;'>{v2}</span>
                    </div>
                    """, unsafe_allow_html=True)

            with comp_table_cols[2]:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='color: #FF4444; font-size: 18px; font-weight: bold;'>{p2["name"]}</div>
                    <div style='font-size: 40px; font-weight: bold; color: {get_ovr_color(p2["ovr"])};'>{p2["ovr"]}</div>
                    <div style='color: #aaa;'>{p2["position"]} | {p2["team"]}</div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  STATISTIKA VA TAHLIL
# ═══════════════════════════════════════════════════════════════

elif page == "stats":
    st.markdown("""
    <div class='section-header'>📊 Statistika va Tahlil</div>
    """, unsafe_allow_html=True)

    # O'yin statistikasi kiritish
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📝 O'yin Natijangizni Kiriting")

        games_played = st.number_input("O'ynalgan o'yinlar:", 0, 1000, 50)
        wins = st.number_input("G'alabalar:", 0, 1000, 30)
        draws = st.number_input("Durranglar:", 0, 1000, 8)
        goals_scored = st.number_input("Urilgan gollar:", 0, 5000, 120)
        goals_conceded = st.number_input("O'tkazilgan gollar:", 0, 5000, 60)
        current_division = st.selectbox("Joriy Division:", [
            "Bronze III", "Bronze II", "Bronze I",
            "Silver III", "Silver II", "Silver I",
            "Gold III", "Gold II", "Gold I",
            "Platinum III", "Platinum II", "Platinum I",
            "Elite III", "Elite II", "Elite I",
            "FC Champion"
        ], index=9)

        if st.button("📊 Tahlil qilish"):
            losses = games_played - wins - draws
            win_rate = (wins / games_played * 100) if games_played > 0 else 0
            goal_avg = (goals_scored / games_played) if games_played > 0 else 0
            goal_diff = goals_scored - goals_conceded

            # Natijalar
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("🏆 G'alaba foizi", f"{win_rate:.1f}%")
                st.metric("⚽ O'rtacha gol", f"{goal_avg:.1f}")
            with metrics_col2:
                st.metric("📈 Gol farqi", f"+{goal_diff}" if goal_diff >= 0 else str(goal_diff))
                st.metric("❌ Mag'lubiyat", losses)

    with col2:
        if games_played > 0:
            losses = games_played - wins - draws
            st.markdown("### 📈 Natijalar Grafigi")

            fig_results = go.Figure(data=[go.Pie(
                labels=["G'alabalar", "Durranglar", "Mag'lubiyatlar"],
                values=[wins, draws, losses],
                hole=0.4,
                marker=dict(colors=["#00B050", "#FFD700", "#FF4444"])
            )])
            fig_results.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title="Natijalar Taqsimoti",
                title_font_color="#00FF88"
            )
            st.plotly_chart(fig_results, use_container_width=True)

            # Progress bar
            st.markdown("### 📊 Samaradorlik Ko'rsatkichlari")

            indicators = [
                ("G'alaba foizi", wins/games_played*100 if games_played > 0 else 0, "#00B050"),
                ("Hujum samarasi", min(100, goals_scored/games_played*10) if games_played > 0 else 0, "#FF4444"),
                ("Himoya samarasi", max(0, 100 - goals_conceded/games_played*10) if games_played > 0 else 0, "#0088FF"),
            ]

            for name, value, color in indicators:
                st.markdown(f"""
                <div style='margin: 10px 0;'>
                    <div style='display: flex; justify-content: space-between; color: #aaa; font-size: 13px;'>
                        <span>{name}</span>
                        <span style='color: {color}; font-weight: bold;'>{value:.0f}%</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 15px; overflow: hidden;'>
                        <div style='width: {value}%; height: 100%;
                                    background: linear-gradient(90deg, {color}, {color}88);
                                    border-radius: 10px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Top o'yinchilar statistikasi
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🌟 Top O'yinchilar Tahlili")

    stat_choice = st.selectbox("Statistika turi:", ["OVR", "pace", "shooting", "passing", "dribbling", "defending"])
    top_n = st.slider("Ko'rsatish soni:", 5, 30, 15)

    top_players = sorted(PLAYERS_DATA, key=lambda x: x[stat_choice], reverse=True)[:top_n]

    df_top = pd.DataFrame(top_players)[["name", "position", "ovr", stat_choice, "team"]]
    df_top.columns = ["Ism", "Pozitsiya", "OVR", stat_choice.title(), "Jamoa"]

    fig_top = px.bar(
        df_top,
        x="Ism",
        y=stat_choice.title(),
        color="Pozitsiya",
        title=f"Top {top_n} O'yinchi - {stat_choice.title()} bo'yicha",
        text=stat_choice.title()
    )
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color="white",
        title_font_color="#00FF88",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_top, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  HODISALAR TAQVIMI
# ═══════════════════════════════════════════════════════════════

elif page == "events":
    st.markdown("""
    <div class='section-header'>📅 Hodisalar Taqvimi</div>
    """, unsafe_allow_html=True)

    # Filtr
    status_filter = st.radio("Status:", ["Hammasi", "Active", "Coming Soon", "Seasonal", "Past"], horizontal=True)

    filtered_events = EVENTS
    if status_filter != "Hammasi":
        filtered_events = [e for e in EVENTS if e["status"] == status_filter]

    # Hodisalar ko'rinishi
    for event in filtered_events:
        status_colors = {
            "Active": "#00B050",
            "Coming Soon": "#FFD700",
            "Seasonal": "#0088FF",
            "Past": "#666666"
        }
        status_color = status_colors.get(event["status"], "#888")
        status_bg = f"{status_color}22"

        st.markdown(f"""
        <div style='background: rgba(20,30,50,0.8); border: 1px solid {status_color}44;
                    border-left: 4px solid {status_color}; border-radius: 12px;
                    padding: 18px; margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div style='flex: 1;'>
                    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                        <span style='font-size: 24px;'>{event["icon"]}</span>
                        <span style='font-size: 18px; font-weight: bold; color: white;'>{event["name"]}</span>
                        <span style='background: {status_bg}; color: {status_color};
                                     border: 1px solid {status_color}44; padding: 2px 10px;
                                     border-radius: 15px; font-size: 12px; font-weight: bold;'>
                            {event["status"]}
                        </span>
                    </div>
                    <div style='color: #aaaaaa; font-size: 13px; margin-bottom: 8px; line-height: 1.5;'>
                        {event["description"]}
                    </div>
                    <div style='display: flex; gap: 20px; flex-wrap: wrap;'>
                        <span style='color: #888; font-size: 12px;'>
                            🎯 <b style='color: #aaa;'>Tur:</b> {event["type"]}
                        </span>
                        <span style='color: #888; font-size: 12px;'>
                            📅 <b style='color: #aaa;'>Tugash:</b> {event["end_date"]}
                        </span>
                    </div>
                </div>
                <div style='min-width: 200px; margin-left: 20px;'>
                    <div style='color: #FFD700; font-size: 12px; font-weight: bold; margin-bottom: 5px;'>
                        🏆 Mukofotlar:
                    </div>
                    <div style='color: #ccc; font-size: 12px;'>{event["rewards"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Taqvim vizualizatsiyasi
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📆 Haftalik Jadval")

    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    weekly_events = {
        "Dushanba": ["Daily Training reset", "VS Attack match"],
        "Seshanba": ["Division Rivals", "Daily Quests"],
        "Chorshanba": ["Team of the Week yangilanadi", "VS Attack"],
        "Payshanba": ["League tournament", "Daily Training"],
        "Juma": ["Division Rivals", "Event coins yig'ish"],
        "Shanba": ["League vs League", "VS Attack", "Head to Head"],
        "Yakshanba": ["Weekly reset", "Mukofotlar olish", "Yangi mavsumga tayyorlik"],
    }

    day_cols = st.columns(7)
    for i, (day, col) in enumerate(zip(days, day_cols)):
        with col:
            is_today = i == datetime.now().weekday()
            bg_color = "rgba(0,176,80,0.3)" if is_today else "rgba(255,255,255,0.05)"
            border_color = "#00B050" if is_today else "rgba(255,255,255,0.1)"

            events_html = "".join([f'<div style="font-size: 10px; color: #ccc; margin: 2px 0; padding: 3px 5px; background: rgba(0,0,0,0.3); border-radius: 4px;">{e}</div>' for e in weekly_events.get(day, [])])

            st.markdown(f"""
            <div style='background: {bg_color}; border: 1px solid {border_color};
                        border-radius: 10px; padding: 10px; min-height: 150px;'>
                <div style='color: {"#00FF88" if is_today else "#aaa"}; font-size: 12px;
                            font-weight: bold; margin-bottom: 8px; text-align: center;'>
                    {day[:3]}{"🟢" if is_today else ""}
                </div>
                {events_html}
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  MASLAHATLAR
# ═══════════════════════════════════════════════════════════════

elif page == "tips":
    st.markdown("""
    <div class='section-header'>💡 Maslahatlar va Hiylalar</div>
    """, unsafe_allow_html=True)

    level_tab1, level_tab2, level_tab3 = st.tabs([
        "🌱 Yangi boshlovchi", "⚽ O'rta daraja", "🔥 Ilg'or"
    ])

    for tab, level_name in zip([level_tab1, level_tab2, level_tab3],
                                 ["Yangi boshlovchilar", "O'rta daraja", "Ilg'or darajadagi"]):
        with tab:
            tips = TIPS_AND_TRICKS[level_name]
            for i, tip in enumerate(tips, 1):
                st.markdown(f"""
                <div style='background: rgba(0,176,80,0.1); border: 1px solid rgba(0,176,80,0.3);
                            border-radius: 10px; padding: 15px; margin: 8px 0;
                            display: flex; align-items: flex-start; gap: 12px;'>
                    <div style='background: #00B050; color: black; font-weight: bold; font-size: 14px;
                                min-width: 28px; height: 28px; border-radius: 50%;
                                display: flex; align-items: center; justify-content: center;'>{i}</div>
                    <div style='color: #cccccc; font-size: 14px; line-height: 1.5;'>{tip}</div>
                </div>
                """, unsafe_allow_html=True)

    # Qo'shimcha strategik maslahatlar
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🎯 Strategik Maslahatlar")

    strategy_tabs = st.tabs(["⚔️ Hujum", "🛡️ Himoya", "💰 Resurslar", "🏆 Division Rises"])

    with strategy_tabs[0]:
        st.markdown("""
        <div class='glass-card'>
        <h4 style='color: #FF4444;'>⚔️ Hujum Strategiyalari</h4>

        <div style='color: #ccc; line-height: 2;'>
        🔹 <b style='color: #00FF88;'>Tezkor qanotdan hujum:</b> Tez wingerlarga ega bo'ling va kross bering<br>
        🔹 <b style='color: #00FF88;'>Skill moves:</b> Penalty boxga kirishdan oldin bir skill moves ishlating<br>
        🔹 <b style='color: #00FF88;'>Through pass:</b> Himoya chizig'i orqasiga tushiruvchi pas muhim<br>
        🔹 <b style='color: #00FF88;'>Far post cross:</b> Far post'ga kross berish katta imkoniyat yaratadi<br>
        🔹 <b style='color: #00FF88;'>Low driven shot:</b> 1-on-1 da low driven shot eng xavfli<br>
        🔹 <b style='color: #00FF88;'>Set pieces:</b> Corner va free kick'larni yaxshi bajarish uchun mashq qiling<br>
        🔹 <b style='color: #00FF88;'>Finesse shot:</b> Penalty box ichida finesse shot ishlating<br>
        🔹 <b style='color: #00FF88;'>Counter attack:</b> Himoyada top olganingizdan so'ng tezkor kontr-hujum
        </div>
        </div>
        """, unsafe_allow_html=True)

    with strategy_tabs[1]:
        st.markdown("""
        <div class='glass-card'>
        <h4 style='color: #0088FF;'>🛡️ Himoya Strategiyalari</h4>

        <div style='color: #ccc; line-height: 2;'>
        🔹 <b style='color: #00FF88;'>Pressure applying:</b> High press taktikasi bilan raqibni chalg'iting<br>
        🔹 <b style='color: #00FF88;'>CDM o'rnini bilish:</b> CDM midfield markazda turishi kerak<br>
        🔹 <b style='color: #00FF88;'>Cover space:</b> Raqib wingerlarga yo'l bermang<br>
        🔹 <b style='color: #00FF88;'>CB xususiyatlari:</b> "Dives Into Tackles" trait ga ega CBlar tanlang<br>
        🔹 <b style='color: #00FF88;'>Jismoniy himoya:</b> Yuqori physicality ga ega himoyachilar<br>
        🔹 <b style='color: #00FF88;'>Penalty box nazorati:</b> Corner va free kick'da CB ni forward qo'ying<br>
        🔹 <b style='color: #00FF88;'>GK tanlov:</b> Reflexes va Positioning yuqori GK kerak<br>
        🔹 <b style='color: #00FF88;'>Line nazorat:</b> Offsayd tuzoqdan foydalaning
        </div>
        </div>
        """, unsafe_allow_html=True)

    with strategy_tabs[2]:
        st.markdown("""
        <div class='glass-card'>
        <h4 style='color: #FFD700;'>💰 Resurslarni Boshqarish</h4>

        <div style='color: #ccc; line-height: 2;'>
        🔹 <b style='color: #00FF88;'>Diamonds tejash:</b> Sale va event paytida diamonds sarflang<br>
        🔹 <b style='color: #00FF88;'>Coins boshqarish:</b> Transferga investitsiya qiling, pack'ga emas<br>
        🔹 <b style='color: #00FF88;'>Daily login:</b> Har kuni kirish bonuslarini to'plang<br>
        🔹 <b style='color: #00FF88;'>Quest bajarish:</b> Daily va Weekly questlar eng yaxshi resurs manbai<br>
        🔹 <b style='color: #00FF88;'>League bonuslar:</b> Faol ligada bo'lish qo'shimcha bonuslar beradi<br>
        🔹 <b style='color: #00FF88;'>Event prioriteti:</b> Limited time event'larga maksimal e'tibor bering<br>
        🔹 <b style='color: #00FF88;'>Skill boost tejash:</b> Muhim kartalar uchun skill boostlarni tejalang<br>
        🔹 <b style='color: #00FF88;'>Pack strategiyasi:</b> Guaranteed rare pack'larni oldindan to'plang
        </div>
        </div>
        """, unsafe_allow_html=True)

    with strategy_tabs[3]:
        st.markdown("""
        <div class='glass-card'>
        <h4 style='color: #9400D3;'>🏆 Division Rivals'da yuqorilash</h4>

        <div style='color: #ccc; line-height: 2;'>
        🔹 <b style='color: #00FF88;'>Muddatli o'ynash:</b> Haftasiga kamida 5-7 o'yin o'ynang<br>
        🔹 <b style='color: #00FF88;'>Streak ni saqlab qolish:</b> Win streak mukofotlarni oshiradi<br>
        🔹 <b style='color: #00FF88;'>Streak yo'qolganida:</b> 2-3 mag'lubiyat ketma-ket kelsa tanaffus oling<br>
        🔹 <b style='color: #00FF88;'>OVR moslashuv:</b> Division ga mos OVR ga ega bo'ling<br>
        🔹 <b style='color: #00FF88;'>Formation switch:</b> Har hafta META formatsiyani tekshiring<br>
        🔹 <b style='color: #00FF88;'>Yulduz tizimi:</b> Yangi star ranking tizimida promotion osonroq<br>
        🔹 <b style='color: #00FF88;'>Matchmaking:</b> Yaxshi matchmaking uchun to'g'ri vaqtda o'ynang<br>
        🔹 <b style='color: #00FF88;'>Haftalik mukofot:</b> Har hafta division mukofotini oling
        </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TRANSFER MARKETI
# ═══════════════════════════════════════════════════════════════

elif page == "transfer":
    st.markdown("""
    <div class='section-header'>💰 Transfer Marketi Simulyatori</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card'>
    <b style='color: #FFD700;'>ℹ️ Transfer Marketi haqida:</b><br>
    <span style='color: #aaa;'>FC Mobile da o'yinchilarni coins bilan sotib olish va sotish mumkin.
    Bu yerda o'yinchi narxlarini simulyatsiya qilishingiz mumkin.</span>
    </div>
    """, unsafe_allow_html=True)

    # Filtr
    transfer_col1, transfer_col2 = st.columns([3, 1])
    with transfer_col1:
        transfer_search = st.text_input("🔍 O'yinchi qidirish:", placeholder="Ism kiriting...")
    with transfer_col2:
        max_price = st.number_input("💰 Max narx (M):", min_value=1, max_value=20, value=10)

    # Filterlangan natijalar
    transfer_players = [p for p in PLAYERS_DATA
                       if (transfer_search.lower() in p["name"].lower() if transfer_search else True)
                       and p["price"] <= max_price * 1_000_000]
    transfer_players = sorted(transfer_players, key=lambda x: x["price"], reverse=True)

    st.markdown(f"**{len(transfer_players)} ta o'yinchi topildi**")

    # Transfer jadval
    if transfer_players:
        transfer_data = []
        for p in transfer_players:
            price_trend = random.choice(["📈 Oshmoqda", "📉 Tushmoqda", "➡️ Barqaror"])
            trend_colors = {"📈 Oshmoqda": "#00FF88", "📉 Tushmoqda": "#FF4444", "➡️ Barqaror": "#FFD700"}

            transfer_data.append({
                "O'yinchi": p["name"],
                "Pozitsiya": p["position"],
                "OVR": p["ovr"],
                "Liga": p["league"],
                "Narx": format_price(p["price"]),
                "Trenda": price_trend,
                "Tur": p["type"]
            })

        df_transfer = pd.DataFrame(transfer_data)
        st.dataframe(
            df_transfer,
            use_container_width=True,
            height=500,
            column_config={
                "OVR": st.column_config.ProgressColumn(
                    "OVR",
                    min_value=90,
                    max_value=110,
                    format="%d"
                )
            }
        )

    # Narx tahlili
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Narx Tahlili")

    price_col1, price_col2 = st.columns(2)

    with price_col1:
        # Narx vs OVR scatter
        df_scatter = pd.DataFrame(PLAYERS_DATA)
        fig_scatter = px.scatter(
            df_scatter,
            x="ovr",
            y="price",
            color="type",
            hover_name="name",
            title="OVR vs Narx",
            labels={"ovr": "OVR", "price": "Narx (Coins)"},
            color_discrete_map={"ICON": "#FFD700", "HERO": "#9400D3", "GOLD": "#00B050"}
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.3)",
            font_color="white",
            title_font_color="#00FF88"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with price_col2:
        # Karta turi bo'yicha o'rtacha narx
        type_avg_price = {}
        for p in PLAYERS_DATA:
            if p["type"] not in type_avg_price:
                type_avg_price[p["type"]] = []
            type_avg_price[p["type"]].append(p["price"])

        avg_prices = {k: np.mean(v) for k, v in type_avg_price.items()}

        fig_avg = px.bar(
            x=list(avg_prices.keys()),
            y=[v/1_000_000 for v in avg_prices.values()],
            title="Karta Turi bo'yicha O'rtacha Narx (M Coins)",
            color=list(avg_prices.keys()),
            color_discrete_map={"ICON": "#FFD700", "HERO": "#9400D3", "GOLD": "#00B050"},
            labels={"x": "Karta Turi", "y": "Narx (Millions)"}
        )
        fig_avg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.3)",
            font_color="white",
            title_font_color="#00FF88"
        )
        st.plotly_chart(fig_avg, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  O'YIN SIMULYATORI
# ═══════════════════════════════════════════════════════════════

elif page == "simulator":
    st.markdown("""
    <div class='section-header'>⚽ O'yin Simulyatori</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card'>
    Ikki jamoa o'rtasida simulyatsiya o'yini o'ynang. OVR ga asoslangan natijalar.
    </div>
    """, unsafe_allow_html=True)

    sim_col1, sim_col2, sim_col3 = st.columns([2, 1, 2])

    with sim_col1:
        st.markdown("### 🔵 Sizning Jamoangiz")
        your_team_name = st.text_input("Jamoa nomi:", "FC Mening Jamoam")
        your_ovr = st.slider("Jamoa OVR:", 80, 120, 105, key="your_ovr")
        your_formation = st.selectbox("Formatsiya:", list(FORMATIONS.keys()), key="your_form")

        # Jamoa statistikasi
        st.markdown(f"""
        <div style='background: rgba(0,136,255,0.1); border: 1px solid #0088FF;
                    border-radius: 10px; padding: 15px; margin: 10px 0;'>
            <div style='font-size: 36px; font-weight: bold; color: #0088FF; text-align: center;'>{your_ovr}</div>
            <div style='color: #aaa; text-align: center;'>OVR</div>
            <div style='color: #ccc; font-size: 12px; margin-top: 5px;'>Formatsiya: {your_formation}</div>
        </div>
        """, unsafe_allow_html=True)

    with sim_col2:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center;
                    justify-content: center; height: 200px; font-size: 48px;'>
            ⚔️<br>
            <div style='font-size: 24px; color: #FFD700; font-weight: bold;'>VS</div>
        </div>
        """, unsafe_allow_html=True)

    with sim_col3:
        st.markdown("### 🔴 Raqib Jamoa")
        opp_teams = [p["team"] for p in PLAYERS_DATA]
        opp_teams = list(set(opp_teams))
        opp_team_name = st.selectbox("Raqib jamoa:", sorted(opp_teams))
        opp_ovr = st.slider("Raqib OVR:", 80, 120, 103, key="opp_ovr")
        opp_formation = st.selectbox("Raqib formatsiya:", list(FORMATIONS.keys()), key="opp_form")

        ovr_diff = your_ovr - opp_ovr
        win_prob = min(90, max(10, 50 + ovr_diff * 2.5))

        st.markdown(f"""
        <div style='background: rgba(255,68,68,0.1); border: 1px solid #FF4444;
                    border-radius: 10px; padding: 15px; margin: 10px 0;'>
            <div style='font-size: 36px; font-weight: bold; color: #FF4444; text-align: center;'>{opp_ovr}</div>
            <div style='color: #aaa; text-align: center;'>OVR</div>
            <div style='color: #ccc; font-size: 12px; margin-top: 5px;'>Formatsiya: {opp_formation}</div>
        </div>
        """, unsafe_allow_html=True)

    # G'alaba ehtimolligi
    st.markdown(f"""
    <div style='background: rgba(255,215,0,0.1); border: 1px solid #FFD700;
                border-radius: 12px; padding: 15px; text-align: center; margin: 10px 0;'>
        <div style='color: #aaa;'>G'alaba Ehtimolligi</div>
        <div style='font-size: 32px; font-weight: bold; color: {"#00FF88" if win_prob >= 50 else "#FF4444"};'>
            {win_prob:.0f}%
        </div>
        <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 15px; overflow: hidden; margin: 10px 0;'>
            <div style='width: {win_prob}%; height: 100%;
                        background: linear-gradient(90deg, {"#00B050" if win_prob >= 50 else "#FF4444"}, transparent);'></div>
        </div>
        <div style='color: #888; font-size: 13px;'>OVR farqi: {ovr_diff:+d}</div>
    </div>
    """, unsafe_allow_html=True)

    # O'yin boshlash
    if st.button("▶️ O'YINNI BOSHLASH", key="start_game"):
        with st.spinner("O'yin o'ynalmoqda... ⚽"):
            import time
            time.sleep(1.5)

        outcome, gf, ga = simulate_match(your_ovr, opp_ovr)

        outcome_colors = {"G'ALABA": "#00FF88", "DURRANG": "#FFD700", "MAG'LUBIYAT": "#FF4444"}
        outcome_icons = {"G'ALABA": "🏆", "DURRANG": "🤝", "MAG'LUBIYAT": "😢"}
        oc = outcome_colors.get(outcome, "#888")
        oi = outcome_icons.get(outcome, "⚽")

        st.markdown(f"""
        <div style='background: {oc}22; border: 3px solid {oc};
                    border-radius: 20px; padding: 30px; text-align: center; margin: 20px 0;'>
            <div style='font-size: 48px;'>{oi}</div>
            <div style='font-size: 32px; font-weight: bold; color: {oc}; margin: 10px 0;'>{outcome}</div>
            <div style='font-size: 56px; font-weight: bold; color: white; margin: 10px 0;'>
                {gf} — {ga}
            </div>
            <div style='color: #aaa; font-size: 14px;'>
                {your_team_name} vs {opp_team_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # O'yin statistikasi
        possession = random.randint(40, 65) if outcome == "G'ALABA" else random.randint(35, 55)
        shots = gf * random.randint(3, 6) + random.randint(2, 5)
        shots_on = gf + random.randint(1, 4)
        corners = random.randint(3, 12)
        fouls = random.randint(8, 18)

        stat_c1, stat_c2, stat_c3 = st.columns(3)
        with stat_c1:
            st.metric("Egalik", f"{possession}% — {100-possession}%")
            st.metric("Urinishlar", f"{shots} — {random.randint(5,12)}")
        with stat_c2:
            st.metric("Darvozaga urinish", f"{shots_on} — {random.randint(2,7)}")
            st.metric("Burchak zarbalar", f"{corners} — {random.randint(2,8)}")
        with stat_c3:
            st.metric("Xatolar", f"{fouls} — {random.randint(8,20)}")
            st.metric("Sariq kartochka", f"{random.randint(0,3)} — {random.randint(0,4)}")

        # Golchilar
        if gf > 0:
            attackers = [p["name"] for p in PLAYERS_DATA if p["position"] in ["ST", "LW", "RW", "CAM"]]
            scorers = random.sample(attackers, min(gf, len(attackers)))
            goals_html = ""
            for i, scorer in enumerate(scorers):
                minute = random.randint(1, 90)
                goals_html += f'<div style="color: #ccc; font-size: 13px; margin: 3px 0;">⚽ {scorer} <span style="color: #888;">({minute}\')</span></div>'

            st.markdown(f"""
            <div style='background: rgba(0,176,80,0.1); border-radius: 10px; padding: 15px; margin: 10px 0;'>
                <div style='color: #00FF88; font-weight: bold; margin-bottom: 8px;'>⚽ Gol urganlar:</div>
                {goals_html}
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  LIGALAR VA JAMOALAR
# ═══════════════════════════════════════════════════════════════

elif page == "leagues":
    st.markdown("""
    <div class='section-header'>🏆 Ligalar va Jamoalar</div>
    """, unsafe_allow_html=True)

    # Ligalar overview
    leagues_cols = st.columns(3)

    for i, (league_name, league_data) in enumerate(LEAGUES.items()):
        with leagues_cols[i % 3]:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                        border-radius: 12px; padding: 20px; margin: 5px 0; text-align: center;
                        border-top: 3px solid {league_data["color"]};'>
                <div style='font-size: 18px; font-weight: bold; color: white;'>{league_name}</div>
                <div style='color: #888; font-size: 12px; margin: 5px 0;'>🌍 {league_data["country"]}</div>
                <div style='color: #aaa; font-size: 12px;'>👥 {league_data["teams"]} Jamoa</div>
                <div style='color: #FFD700; font-size: 12px; margin-top: 5px;'>🏆 {league_data["top_team"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Top jamoalar va o'yinchilar
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🏟️ Jamoalar va Ularning O'yinchilari")

    selected_team = st.selectbox(
        "Jamoa tanlang:",
        sorted(list(set([p["team"] for p in PLAYERS_DATA])))
    )

    team_players = [p for p in PLAYERS_DATA if p["team"] == selected_team]
    team_players = sorted(team_players, key=lambda x: x["ovr"], reverse=True)

    if team_players:
        team_avg_ovr = np.mean([p["ovr"] for p in team_players])
        team_league = team_players[0]["league"]

        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            st.metric("👥 O'yinchilar soni", len(team_players))
        with t_col2:
            st.metric("📊 O'rtacha OVR", f"{team_avg_ovr:.0f}")
        with t_col3:
            st.metric("🏆 Liga", team_league)

        # Jamoa o'yinchilar
        t_cols = st.columns(min(4, len(team_players)))
        for i, (player, col) in enumerate(zip(team_players[:8], t_cols * 2)):
            with col:
                ovr_color = get_ovr_color(player["ovr"])
                st.markdown(f"""
                <div style='background: {ovr_color}11; border: 1px solid {ovr_color}33;
                            border-radius: 10px; padding: 12px; text-align: center; margin: 3px 0;'>
                    <div style='font-size: 22px; font-weight: bold; color: {ovr_color};'>{player["ovr"]}</div>
                    <div style='font-size: 13px; color: white; font-weight: bold;'>{player["name"]}</div>
                    <div style='font-size: 11px; color: #888;'>{player["position"]}</div>
                    <div style='font-size: 11px; color: {ovr_color}88; margin-top: 3px;'>{player["type"]}</div>
                </div>
                """, unsafe_allow_html=True)

        # Jamoa statistika grafigi
        if len(team_players) >= 3:
            avg_stats = {
                "Tezlik": np.mean([p["pace"] for p in team_players]),
                "Udarish": np.mean([p["shooting"] for p in team_players]),
                "Pas": np.mean([p["passing"] for p in team_players]),
                "Dribbling": np.mean([p["dribbling"] for p in team_players]),
                "Himoya": np.mean([p["defending"] for p in team_players]),
                "Jismoniy": np.mean([p["physical"] for p in team_players]),
            }

            fig_team = go.Figure()
            fig_team.add_trace(go.Scatterpolar(
                r=list(avg_stats.values()),
                theta=list(avg_stats.keys()),
                fill='toself',
                fillcolor='rgba(0,176,80,0.2)',
                line=dict(color='#00B050', width=2),
                name=selected_team
            ))
            fig_team.update_layout(
                polar=dict(radialaxis=dict(range=[0, 100], color="#666")),
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title=f"{selected_team} - O'rtacha Statistika",
                title_font_color="#00FF88"
            )
            st.plotly_chart(fig_team, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SOZLAMALAR
# ═══════════════════════════════════════════════════════════════

elif page == "settings":
    st.markdown("""
    <div class='section-header'>🔧 Sozlamalar</div>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns(2)

    with set_col1:
        st.markdown("### 👤 Profil Sozlamalari")
        username = st.text_input("🎮 FC Mobile username:", placeholder="Username kiriting")
        favorite_team = st.selectbox("❤️ Sevimli jamoa:", ["— Tanlang —"] + sorted(list(set([p["team"] for p in PLAYERS_DATA]))))
        favorite_formation = st.selectbox("📐 Sevimli formatsiya:", list(FORMATIONS.keys()))
        player_level = st.selectbox("📈 O'yin darajasi:", ["Yangi boshlovchi", "O'rta", "Ilg'or", "Pro"])
        preferred_mode = st.selectbox("🎮 Sevimli rejim:", list(GAME_MODES.keys()))

        if st.button("💾 Profilni saqlash"):
            st.success(f"✅ {username} profili saqlandi!")
            st.markdown(f"""
            <div class='glass-card'>
                <div style='color: #00FF88; font-weight: bold;'>Profil ma'lumotlari:</div>
                <div style='color: #aaa; font-size: 13px;'>
                    👤 Username: {username or "Kiritilmagan"}<br>
                    ❤️ Jamoa: {favorite_team}<br>
                    📐 Formatsiya: {favorite_formation}<br>
                    📈 Daraja: {player_level}<br>
                    🎮 Rejim: {preferred_mode}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with set_col2:
        st.markdown("### ⚙️ Ilova Sozlamalari")

        show_animations = st.toggle("✨ Animatsiyalar", value=True)
        dark_mode = st.toggle("🌙 Qorong'u rejim", value=True)
        show_prices = st.toggle("💰 Narxlarni ko'rsatish", value=True)
        auto_refresh = st.toggle("🔄 Avtomatik yangilash", value=False)
        sound_effects = st.toggle("🔊 Tovush effektlari", value=False)

        st.markdown("---")
        st.markdown("### 📊 Ilova Statistikasi")
        st.markdown(f"""
        <div class='glass-card'>
            <div style='color: #aaa; font-size: 13px; line-height: 2;'>
                📅 Sana: <b style='color: #00FF88;'>{datetime.now().strftime('%Y-%m-%d')}</b><br>
                ⏰ Vaqt: <b style='color: #00FF88;'>{datetime.now().strftime('%H:%M:%S')}</b><br>
                📦 Versiya: <b style='color: #FFD700;'>FC Mobile 26 Companion v2.6</b><br>
                👥 O'yinchilar bazasi: <b style='color: #00B050;'>{len(PLAYERS_DATA)} ta</b><br>
                📐 Formatsiyalar: <b style='color: #00B050;'>{len(FORMATIONS)} ta</b><br>
                🎮 O'yin rejimlari: <b style='color: #00B050;'>{len(GAME_MODES)} ta</b><br>
                📅 Hodisalar: <b style='color: #00B050;'>{len(EVENTS)} ta</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Haqida
    st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
    st.markdown("### ℹ️ Ilova Haqida")

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0,176,80,0.1), rgba(0,48,135,0.1));
                border: 1px solid rgba(0,176,80,0.3); border-radius: 15px; padding: 25px; text-align: center;'>
        <div style='font-size: 50px; margin-bottom: 10px;'>⚽</div>
        <div style='font-size: 22px; font-weight: bold; color: #00FF88;'>FC Mobile 26 Companion App</div>
        <div style='color: #aaa; margin: 10px 0;'>EA Sports FC Mobile 26 o'yini uchun to'liq hamroh dastur</div>
        <div style='color: #666; font-size: 12px;'>
            Python + Streamlit bilan yaratilgan<br>
            Ma'lumotlar: EA Sports rasmiy sahifasidan<br>
            Versiya 2.6.0 | 2025-2026
        </div>
        <div style='margin-top: 15px;'>
            <span style='background: rgba(0,176,80,0.2); color: #00B050; padding: 4px 12px; border-radius: 15px; margin: 3px; font-size: 12px;'>Python</span>
            <span style='background: rgba(255,75,75,0.2); color: #FF4B4B; padding: 4px 12px; border-radius: 15px; margin: 3px; font-size: 12px;'>Streamlit</span>
            <span style='background: rgba(99,110,250,0.2); color: #636EFA; padding: 4px 12px; border-radius: 15px; margin: 3px; font-size: 12px;'>Plotly</span>
            <span style='background: rgba(255,215,0,0.2); color: #FFD700; padding: 4px 12px; border-radius: 15px; margin: 3px; font-size: 12px;'>Pandas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div class='footer'>
    <div style='height: 1px; background: linear-gradient(90deg, transparent, #00B050, transparent);
                margin-bottom: 15px;'></div>
    <div style='color: #444; font-size: 13px;'>
        ⚽ EA Sports FC Mobile 26 Companion App | Python + Streamlit bilan yaratilgan
        <br>
        Bu ilova rasmiy EA Sports mahsuloti emas. Fan tomonidan yaratilgan.
    </div>
</div>
""", unsafe_allow_html=True)
