import streamlit as st
import random
import json
import time
from datetime import datetime

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="EA FC Mobile Simulator",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS - FC MOBILE STYLE
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a2540 50%, #0d1b35 100%);
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1a6b3c 0%, #2d9e5f 50%, #1a6b3c 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #4ade80;
        box-shadow: 0 0 30px rgba(74, 222, 128, 0.4);
    }
    
    .main-header h1 {
        font-family: 'Oswald', sans-serif;
        font-size: 3em;
        color: #FFD700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        margin: 0;
        letter-spacing: 3px;
    }
    
    .main-header p {
        color: #a8f5c8;
        font-size: 1.1em;
        margin: 5px 0 0;
    }
    
    .currency-bar {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #FFD700;
        border-radius: 12px;
        padding: 15px 20px;
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    
    .currency-item {
        text-align: center;
        flex: 1;
    }
    
    .currency-value {
        font-family: 'Oswald', sans-serif;
        font-size: 1.8em;
        color: #FFD700;
        font-weight: 700;
    }
    
    .currency-label {
        color: #94a3b8;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .player-card {
        background: linear-gradient(145deg, #1e3a5f, #0f2040);
        border: 2px solid #3b82f6;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        margin: 5px;
    }
    
    .player-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
        border-color: #60a5fa;
    }
    
    .player-card.gold {
        background: linear-gradient(145deg, #5c4004, #3d2800);
        border-color: #FFD700;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
    }
    
    .player-card.gold:hover {
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.7);
    }
    
    .player-card.silver {
        background: linear-gradient(145deg, #374151, #1f2937);
        border-color: #9ca3af;
        box-shadow: 0 4px 15px rgba(156, 163, 175, 0.3);
    }
    
    .player-card.legend {
        background: linear-gradient(145deg, #7c3aed, #4c1d95);
        border-color: #c084fc;
        box-shadow: 0 4px 25px rgba(192, 132, 252, 0.5);
        animation: legendGlow 2s ease-in-out infinite;
    }
    
    @keyframes legendGlow {
        0%, 100% { box-shadow: 0 4px 25px rgba(192, 132, 252, 0.5); }
        50% { box-shadow: 0 8px 40px rgba(192, 132, 252, 0.9); }
    }
    
    .player-ovr {
        font-family: 'Oswald', sans-serif;
        font-size: 2.5em;
        font-weight: 700;
        line-height: 1;
    }
    
    .player-name {
        font-weight: 700;
        font-size: 1em;
        color: white;
        margin: 5px 0;
    }
    
    .player-pos {
        font-size: 0.8em;
        color: #94a3b8;
        letter-spacing: 2px;
    }
    
    .player-club {
        font-size: 0.75em;
        color: #60a5fa;
        margin-top: 3px;
    }
    
    .pack-card {
        background: linear-gradient(145deg, #1a2540, #0d1b35);
        border: 2px solid;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
    
    .pack-gold {
        border-color: #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    
    .pack-legend {
        border-color: #c084fc;
        box-shadow: 0 0 25px rgba(192, 132, 252, 0.5);
        background: linear-gradient(145deg, #3b1f6b, #1e0f3a);
    }
    
    .pack-special {
        border-color: #ef4444;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
        background: linear-gradient(145deg, #3f1515, #1f0a0a);
    }
    
    .pack-ucl {
        border-color: #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        background: linear-gradient(145deg, #1a3a6b, #0d1f3a);
    }
    
    .pack-title {
        font-family: 'Oswald', sans-serif;
        font-size: 1.4em;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 10px;
    }
    
    .pack-icon {
        font-size: 3em;
    }
    
    .pack-price {
        font-size: 0.9em;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .section-header {
        font-family: 'Oswald', sans-serif;
        font-size: 1.8em;
        color: #FFD700;
        border-bottom: 2px solid #2d9e5f;
        padding-bottom: 10px;
        margin: 20px 0 15px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .upgrade-box {
        background: linear-gradient(135deg, #0f2d1a, #1a4a2a);
        border: 2px solid #2d9e5f;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .stat-bar-container {
        display: flex;
        align-items: center;
        margin: 5px 0;
        gap: 10px;
    }
    
    .stat-label {
        width: 80px;
        font-size: 0.8em;
        color: #94a3b8;
        text-align: right;
    }
    
    .stat-bar {
        flex: 1;
        height: 8px;
        background: #1e293b;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .stat-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .stat-value {
        width: 30px;
        font-size: 0.85em;
        font-weight: 700;
        color: white;
    }
    
    .notification {
        background: linear-gradient(135deg, #1a4a2a, #2d6b40);
        border: 1px solid #4ade80;
        border-radius: 10px;
        padding: 12px 20px;
        margin: 5px 0;
        color: #a8f5c8;
        font-size: 0.9em;
    }
    
    .squad-position {
        background: linear-gradient(145deg, #1e3a5f, #0f2040);
        border: 2px solid #3b82f6;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .badge-item {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #3b82f6;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75em;
        color: #60a5fa;
        margin: 2px;
    }
    
    .progress-bar {
        background: #1e293b;
        border-radius: 10px;
        height: 15px;
        overflow: hidden;
        margin: 5px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #2d9e5f, #4ade80);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b3c, #2d9e5f);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'Oswald', sans-serif;
        font-size: 1em;
        letter-spacing: 1px;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(45, 158, 95, 0.4);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2d9e5f, #4ade80);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 222, 128, 0.6);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    .stSelectbox label, .stSlider label, .stRadio label {
        color: #94a3b8 !important;
        font-family: 'Roboto', sans-serif !important;
    }
    
    .stSelectbox > div > div {
        background: #1e293b !important;
        border-color: #3b82f6 !important;
        color: white !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0a0e1a, #1a2540);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e1a, #1a2540) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .tab-content {
        padding: 10px 0;
    }
    
    .club-upgrade-section {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 2px solid #7c3aed;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .achievement-card {
        background: linear-gradient(145deg, #1a2540, #0d1b35);
        border: 1px solid #FFD700;
        border-radius: 10px;
        padding: 12px;
        margin: 5px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .shimmer {
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .pack-opening-card {
        background: linear-gradient(145deg, #0d1b35, #1a2540);
        border: 3px solid;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin: 8px;
        transition: all 0.3s ease;
    }
    
    hr {
        border-color: #1e3a5f !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #0a0e1a;
        border-radius: 10px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a2540;
        color: #94a3b8;
        border-radius: 8px;
        font-family: 'Oswald', sans-serif;
        letter-spacing: 1px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a6b3c, #2d9e5f) !important;
        color: white !important;
    }
    
    .stMetric {
        background: #1a2540;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #3b82f6;
    }
    
    .stMetric label {
        color: #94a3b8 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-family: 'Oswald', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# CONSTANTS & DATA
# =============================================

LEAGUES = {
    "Premier League": ["Manchester City", "Liverpool", "Chelsea", "Arsenal", "Manchester United", 
                       "Tottenham Hotspur", "Newcastle United", "Aston Villa"],
    "La Liga": ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Real Betis", "Villarreal"],
    "Bundesliga": ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen", "Wolfsburg"],
    "Serie A": ["Juventus", "Inter Milan", "AC Milan", "Napoli", "Roma", "Lazio"],
    "Ligue 1": ["PSG", "Marseille", "Lyon", "Monaco", "Lille"],
    "UCL": ["Real Madrid", "Manchester City", "Bayern Munich", "PSG", "Liverpool"]
}

ALL_PLAYERS = {
    # Legends (105-112 OVR)
    "Ronaldinho": {"ovr": 110, "pos": "CAM", "club": "Barcelona", "nation": "🇧🇷", "type": "ICON", "pace": 92, "shoot": 95, "pass": 97, "dribble": 99, "defend": 45, "physical": 80},
    "Zinedine Zidane": {"ovr": 109, "pos": "CM", "club": "Real Madrid", "nation": "🇫🇷", "type": "ICON", "pace": 82, "shoot": 88, "pass": 98, "dribble": 99, "defend": 72, "physical": 79},
    "David Beckham": {"ovr": 106, "pos": "RM", "club": "Manchester United", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "ICON", "pace": 87, "shoot": 92, "pass": 97, "dribble": 88, "defend": 58, "physical": 73},
    "Zlatan Ibrahimovic": {"ovr": 107, "pos": "ST", "club": "AC Milan", "nation": "🇸🇪", "type": "ICON", "pace": 82, "shoot": 96, "pass": 83, "dribble": 92, "defend": 35, "physical": 95},
    "Roy Keane": {"ovr": 105, "pos": "CDM", "club": "Manchester United", "nation": "🇮🇪", "type": "ICON", "pace": 79, "shoot": 79, "pass": 85, "dribble": 82, "defend": 93, "physical": 91},
    "Iker Casillas": {"ovr": 105, "pos": "GK", "club": "Real Madrid", "nation": "🇪🇸", "type": "ICON", "pace": 60, "shoot": 30, "pass": 75, "dribble": 30, "defend": 98, "physical": 82},
    "Roberto Carlos": {"ovr": 106, "pos": "LB", "club": "Real Madrid", "nation": "🇧🇷", "type": "ICON", "pace": 95, "shoot": 85, "pass": 80, "dribble": 84, "defend": 88, "physical": 90},
    "Kaka": {"ovr": 107, "pos": "CAM", "club": "AC Milan", "nation": "🇧🇷", "type": "ICON", "pace": 88, "shoot": 91, "pass": 94, "dribble": 95, "defend": 42, "physical": 82},
    
    # Elite (99-104 OVR)
    "Jude Bellingham": {"ovr": 103, "pos": "CM", "club": "Real Madrid", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "LIVE", "pace": 88, "shoot": 88, "pass": 90, "dribble": 92, "defend": 85, "physical": 87},
    "Erling Haaland": {"ovr": 102, "pos": "ST", "club": "Manchester City", "nation": "🇳🇴", "type": "LIVE", "pace": 96, "shoot": 98, "pass": 75, "dribble": 85, "defend": 45, "physical": 93},
    "Vinicius Jr": {"ovr": 101, "pos": "LW", "club": "Real Madrid", "nation": "🇧🇷", "type": "LIVE", "pace": 99, "shoot": 88, "pass": 82, "dribble": 97, "defend": 30, "physical": 74},
    "Kylian Mbappe": {"ovr": 101, "pos": "ST", "club": "Real Madrid", "nation": "🇫🇷", "type": "LIVE", "pace": 99, "shoot": 95, "pass": 84, "dribble": 95, "defend": 38, "physical": 80},
    "Mohamed Salah": {"ovr": 100, "pos": "RW", "club": "Liverpool", "nation": "🇪🇬", "type": "LIVE", "pace": 97, "shoot": 93, "pass": 83, "dribble": 93, "defend": 45, "physical": 79},
    "Kevin De Bruyne": {"ovr": 99, "pos": "CM", "club": "Manchester City", "nation": "🇧🇪", "type": "LIVE", "pace": 80, "shoot": 88, "pass": 99, "dribble": 91, "defend": 64, "physical": 78},
    "Rodri": {"ovr": 99, "pos": "CDM", "club": "Manchester City", "nation": "🇪🇸", "type": "LIVE", "pace": 75, "shoot": 80, "pass": 93, "dribble": 85, "defend": 95, "physical": 88},
    "Virgil van Dijk": {"ovr": 100, "pos": "CB", "club": "Liverpool", "nation": "🇳🇱", "type": "LIVE", "pace": 82, "shoot": 68, "pass": 78, "dribble": 72, "defend": 98, "physical": 97},
    "Thibaut Courtois": {"ovr": 99, "pos": "GK", "club": "Real Madrid", "nation": "🇧🇪", "type": "LIVE", "pace": 55, "shoot": 25, "pass": 72, "dribble": 25, "defend": 98, "physical": 90},
    "Lamine Yamal": {"ovr": 99, "pos": "RW", "club": "Barcelona", "nation": "🇪🇸", "type": "LIVE", "pace": 95, "shoot": 85, "pass": 88, "dribble": 96, "defend": 35, "physical": 68},
    "Cole Palmer": {"ovr": 98, "pos": "CAM", "club": "Chelsea", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "LIVE", "pace": 85, "shoot": 92, "pass": 90, "dribble": 93, "defend": 55, "physical": 72},
    "Jamal Musiala": {"ovr": 98, "pos": "CAM", "club": "Bayern Munich", "nation": "🇩🇪", "type": "LIVE", "pace": 89, "shoot": 87, "pass": 87, "dribble": 94, "defend": 55, "physical": 74},
    "Son Heung-Min": {"ovr": 97, "pos": "LW", "club": "Tottenham", "nation": "🇰🇷", "type": "LIVE", "pace": 94, "shoot": 91, "pass": 83, "dribble": 90, "defend": 48, "physical": 75},
    "Phil Foden": {"ovr": 97, "pos": "LW", "club": "Manchester City", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "LIVE", "pace": 88, "shoot": 88, "pass": 88, "dribble": 93, "defend": 55, "physical": 72},
    "Rafael Leao": {"ovr": 97, "pos": "LW", "club": "AC Milan", "nation": "🇵🇹", "type": "TOTS", "pace": 98, "shoot": 85, "pass": 80, "dribble": 94, "defend": 25, "physical": 78},
    "Harry Kane": {"ovr": 97, "pos": "ST", "club": "Bayern Munich", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "LIVE", "pace": 82, "shoot": 97, "pass": 87, "dribble": 85, "defend": 45, "physical": 85},
    
    # Gold (93-96 OVR)
    "Marcus Rashford": {"ovr": 95, "pos": "LW", "club": "Manchester United", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "GOLD", "pace": 95, "shoot": 85, "pass": 77, "dribble": 88, "defend": 35, "physical": 80},
    "Bruno Fernandes": {"ovr": 94, "pos": "CAM", "club": "Manchester United", "nation": "🇵🇹", "type": "GOLD", "pace": 78, "shoot": 87, "pass": 92, "dribble": 85, "defend": 62, "physical": 70},
    "Pedri": {"ovr": 94, "pos": "CM", "club": "Barcelona", "nation": "🇪🇸", "type": "GOLD", "pace": 82, "shoot": 80, "pass": 93, "dribble": 93, "defend": 70, "physical": 62},
    "Leroy Sane": {"ovr": 93, "pos": "RW", "club": "Bayern Munich", "nation": "🇩🇪", "type": "GOLD", "pace": 97, "shoot": 82, "pass": 79, "dribble": 90, "defend": 30, "physical": 72},
    "Antoine Griezmann": {"ovr": 93, "pos": "ST", "club": "Atletico Madrid", "nation": "🇫🇷", "type": "GOLD", "pace": 85, "shoot": 90, "pass": 82, "dribble": 87, "defend": 55, "physical": 76},
    "Bernardo Silva": {"ovr": 93, "pos": "CM", "club": "Manchester City", "nation": "🇵🇹", "type": "GOLD", "pace": 83, "shoot": 82, "pass": 90, "dribble": 91, "defend": 65, "physical": 72},
    "Trent Alexander-Arnold": {"ovr": 94, "pos": "RB", "club": "Liverpool", "nation": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "type": "GOLD", "pace": 88, "shoot": 80, "pass": 95, "dribble": 82, "defend": 82, "physical": 76},
    "Ruben Dias": {"ovr": 93, "pos": "CB", "club": "Manchester City", "nation": "🇵🇹", "type": "GOLD", "pace": 78, "shoot": 55, "pass": 72, "dribble": 65, "defend": 96, "physical": 90},
}

CLUB_UPGRADES = {
    "Stadium": {
        "icon": "🏟️",
        "description": "Katta stadion = ko'proq daromad va muxlis",
        "levels": [
            {"name": "Mini Arena", "capacity": 10000, "bonus": "+5% Coins/game", "cost": 0},
            {"name": "Local Ground", "capacity": 25000, "bonus": "+10% Coins/game", "cost": 50000},
            {"name": "City Stadium", "capacity": 45000, "bonus": "+18% Coins/game", "cost": 150000},
            {"name": "National Stadium", "capacity": 75000, "bonus": "+28% Coins/game", "cost": 400000},
            {"name": "Elite Arena", "capacity": 100000, "bonus": "+40% Coins/game", "cost": 900000},
            {"name": "Mega Stadium", "capacity": 150000, "bonus": "+55% Coins/game", "cost": 2000000},
        ]
    },
    "Training Ground": {
        "icon": "🏋️",
        "description": "Yaxshi trening = tezroq o'sish",
        "levels": [
            {"name": "Basic Field", "capacity": 0, "bonus": "+5% XP", "cost": 0},
            {"name": "Youth Academy", "capacity": 0, "bonus": "+12% XP", "cost": 60000},
            {"name": "Pro Training", "capacity": 0, "bonus": "+22% XP", "cost": 180000},
            {"name": "Elite Center", "capacity": 0, "bonus": "+35% XP", "cost": 450000},
            {"name": "World Class", "capacity": 0, "bonus": "+50% XP", "cost": 1000000},
            {"name": "Champions Lab", "capacity": 0, "bonus": "+70% XP", "cost": 2500000},
        ]
    },
    "Medical Center": {
        "icon": "🏥",
        "description": "O'yinchilar tezroq tiklanadi",
        "levels": [
            {"name": "First Aid", "capacity": 0, "bonus": "-5% Injury risk", "cost": 0},
            {"name": "Clinic", "capacity": 0, "bonus": "-15% Injury risk", "cost": 40000},
            {"name": "Medical Hub", "capacity": 0, "bonus": "-30% Injury risk", "cost": 120000},
            {"name": "Sports Hospital", "capacity": 0, "bonus": "-50% Injury risk", "cost": 350000},
            {"name": "Recovery Center", "capacity": 0, "bonus": "-70% Injury risk", "cost": 800000},
            {"name": "Bio-Tech Lab", "capacity": 0, "bonus": "-90% Injury risk", "cost": 2000000},
        ]
    },
    "Scout Network": {
        "icon": "🔭",
        "description": "Yaxshi scouts = nadir o'yinchilar topish",
        "levels": [
            {"name": "Local Scout", "capacity": 0, "bonus": "+5% Pack quality", "cost": 0},
            {"name": "Regional Scout", "capacity": 0, "bonus": "+12% Pack quality", "cost": 70000},
            {"name": "National Scout", "capacity": 0, "bonus": "+22% Pack quality", "cost": 200000},
            {"name": "Continental Scout", "capacity": 0, "bonus": "+35% Pack quality", "cost": 500000},
            {"name": "Global Network", "capacity": 0, "bonus": "+52% Pack quality", "cost": 1100000},
            {"name": "Elite Scout Hub", "capacity": 0, "bonus": "+70% Pack quality", "cost": 2800000},
        ]
    },
    "Fan Zone": {
        "icon": "👥",
        "description": "Ko'proq muxlis = ko'proq bonus",
        "levels": [
            {"name": "Small Section", "capacity": 0, "bonus": "+5% Fan tokens", "cost": 0},
            {"name": "Fan Corner", "capacity": 0, "bonus": "+15% Fan tokens", "cost": 45000},
            {"name": "Supporter Club", "capacity": 0, "bonus": "+28% Fan tokens", "cost": 130000},
            {"name": "Ultra Zone", "capacity": 0, "bonus": "+45% Fan tokens", "cost": 380000},
            {"name": "Global Fanbase", "capacity": 0, "bonus": "+65% Fan tokens", "cost": 900000},
            {"name": "Legendary Fans", "capacity": 0, "bonus": "+90% Fan tokens", "cost": 2200000},
        ]
    },
    "Tech Lab": {
        "icon": "💻",
        "description": "Yangi texnologiyalar - taktik bonuslar",
        "levels": [
            {"name": "Basic Analysis", "capacity": 0, "bonus": "+3% Tactical bonus", "cost": 0},
            {"name": "Data Center", "capacity": 0, "bonus": "+10% Tactical bonus", "cost": 80000},
            {"name": "AI Coaching", "capacity": 0, "bonus": "+20% Tactical bonus", "cost": 220000},
            {"name": "VR Training", "capacity": 0, "bonus": "+35% Tactical bonus", "cost": 600000},
            {"name": "Neural Engine", "capacity": 0, "bonus": "+55% Tactical bonus", "cost": 1300000},
            {"name": "Quantum Lab", "capacity": 0, "bonus": "+80% Tactical bonus", "cost": 3000000},
        ]
    },
}

PACKS = {
    "Standard Gold Pack": {
        "icon": "📦",
        "color": "gold",
        "description": "3 ta oltin yulduzli o'yinchi",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 3,
        "min_ovr": 93,
        "max_ovr": 96,
        "legend_chance": 0,
        "elite_chance": 0,
        "type": "gold",
        "badge": "BEPUL"
    },
    "Premium Gold Pack": {
        "icon": "🌟",
        "color": "gold",
        "description": "5 ta yuqori sifatli oltin o'yinchi",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 5,
        "min_ovr": 93,
        "max_ovr": 97,
        "legend_chance": 0,
        "elite_chance": 15,
        "type": "gold",
        "badge": "BEPUL"
    },
    "Elite Player Pack": {
        "icon": "⚡",
        "color": "ucl",
        "description": "Elite o'yinchi - 97+ OVR kafolatlangan!",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 5,
        "min_ovr": 97,
        "max_ovr": 103,
        "legend_chance": 0,
        "elite_chance": 100,
        "type": "elite",
        "badge": "BEPUL"
    },
    "Icon Pack": {
        "icon": "👑",
        "color": "legend",
        "description": "ICON o'yinchi kafolatlangan! Ronaldinho? Zidane?",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 5,
        "min_ovr": 105,
        "max_ovr": 112,
        "legend_chance": 100,
        "elite_chance": 100,
        "type": "icon",
        "badge": "ICON"
    },
    "TOTW Pack": {
        "icon": "🏆",
        "color": "special",
        "description": "Team of the Week - eng zo'r o'yinchilar!",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 5,
        "min_ovr": 95,
        "max_ovr": 104,
        "legend_chance": 5,
        "elite_chance": 60,
        "type": "totw",
        "badge": "TOTW"
    },
    "UCL Pack": {
        "icon": "⭐",
        "color": "ucl",
        "description": "UEFA Champions League maxsus paketi",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 5,
        "min_ovr": 95,
        "max_ovr": 104,
        "legend_chance": 8,
        "elite_chance": 70,
        "type": "ucl",
        "badge": "UCL"
    },
    "MEGA Pack x10": {
        "icon": "💎",
        "color": "legend",
        "description": "10 ta o'yinchi - eng yaxshi ehtimollar!",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 10,
        "min_ovr": 97,
        "max_ovr": 112,
        "legend_chance": 20,
        "elite_chance": 100,
        "type": "mega",
        "badge": "x10 MEGA"
    },
    "Ultimate Icon Pack": {
        "icon": "🌠",
        "color": "legend",
        "description": "2 ta ICON kafolatlangan! Ultra rare!",
        "price_coins": 0,
        "price_gems": 0,
        "player_count": 8,
        "min_ovr": 107,
        "max_ovr": 112,
        "legend_chance": 100,
        "elite_chance": 100,
        "type": "ultimate",
        "badge": "2x ICON"
    },
}

FORMATIONS = ["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1", "3-4-3", "5-4-1", "4-3-2-1"]

POSITIONS = {
    "4-3-3": ["GK", "RB", "CB", "CB", "LB", "CM", "CDM", "CM", "RW", "ST", "LW"],
    "4-4-2": ["GK", "RB", "CB", "CB", "LB", "RM", "CM", "CM", "LM", "ST", "ST"],
    "4-2-3-1": ["GK", "RB", "CB", "CB", "LB", "CDM", "CDM", "CAM", "CAM", "CAM", "ST"],
    "3-5-2": ["GK", "CB", "CB", "CB", "RM", "CM", "CDM", "CM", "LM", "ST", "ST"],
    "5-3-2": ["GK", "RB", "CB", "CB", "CB", "LB", "CM", "CM", "CM", "ST", "ST"],
}

# =============================================
# SESSION STATE INITIALIZATION
# =============================================
def init_state():
    defaults = {
        "coins": 999_999_999,
        "gems": 999_999,
        "tokens": 99999,
        "fan_tokens": 500000,
        "squad": {},
        "inventory": [],
        "club_levels": {name: 0 for name in CLUB_UPGRADES.keys()},
        "club_name": "FC Ultimate",
        "club_badge": "⚽",
        "formation": "4-3-3",
        "history": [],
        "total_packs": 0,
        "total_players": 0,
        "achievements": [],
        "team_ovr": 0,
        "notifications": [],
        "pack_history": [],
        "club_reputation": 1000,
        "season_wins": 0,
        "league_rank": 1,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# =============================================
# HELPER FUNCTIONS
# =============================================
def get_player_color_class(ovr, ptype="GOLD"):
    if ptype == "ICON": return "legend"
    if ovr >= 99: return "gold"
    if ovr >= 93: return "silver"
    return "silver"

def get_stat_color(val):
    if val >= 90: return "#4ade80"
    if val >= 75: return "#facc15"
    if val >= 60: return "#fb923c"
    return "#ef4444"

def calc_team_ovr():
    if not st.session_state.squad:
        return 0
    ovrs = [p["ovr"] for p in st.session_state.squad.values() if p]
    return round(sum(ovrs) / len(ovrs)) if ovrs else 0

def add_notification(msg, ntype="✅"):
    st.session_state.notifications.insert(0, f"{ntype} {msg}")
    if len(st.session_state.notifications) > 10:
        st.session_state.notifications = st.session_state.notifications[:10]

def open_pack(pack_name):
    pack = PACKS[pack_name]
    players_list = list(ALL_PLAYERS.items())
    result = []
    
    for _ in range(pack["player_count"]):
        roll = random.random() * 100
        if roll < pack["legend_chance"]:
            candidates = [(n, p) for n, p in players_list if p["type"] == "ICON"]
        elif roll < pack["legend_chance"] + pack["elite_chance"]:
            candidates = [(n, p) for n, p in players_list if p["ovr"] >= pack["min_ovr"] and p["ovr"] <= pack["max_ovr"] and p["type"] != "ICON"]
        else:
            candidates = [(n, p) for n, p in players_list if p["ovr"] >= 93 and p["ovr"] <= 96]
        
        if not candidates:
            candidates = random.choices(players_list, k=1)
        
        name, player = random.choice(candidates)
        result.append((name, player.copy()))
    
    st.session_state.total_packs += 1
    st.session_state.total_players += len(result)
    st.session_state.pack_history.extend(result)
    add_notification(f"{pack_name} ochildi! {len(result)} ta o'yinchi olindi", "📦")
    
    # Check achievements
    check_achievements()
    return result

def auto_equip_player(name, player):
    formation = st.session_state.formation
    positions = POSITIONS.get(formation, POSITIONS["4-3-3"])
    player_pos = player["pos"]
    
    pos_map = {
        "GK": ["GK"],
        "RB": ["RB", "CB"],
        "LB": ["LB", "CB"],
        "CB": ["CB"],
        "CDM": ["CDM", "CM"],
        "CM": ["CM", "CAM", "CDM"],
        "CAM": ["CAM", "CM"],
        "RM": ["RM", "RW", "CM"],
        "LM": ["LM", "LW", "CM"],
        "RW": ["RW", "RM", "ST"],
        "LW": ["LW", "LM", "ST"],
        "ST": ["ST", "LW", "RW"],
    }
    
    suitable_positions = pos_map.get(player_pos, [player_pos])
    
    for i, pos in enumerate(positions):
        slot_key = f"slot_{i}"
        if slot_key not in st.session_state.squad and pos in suitable_positions:
            st.session_state.squad[slot_key] = {"name": name, **player, "slot_pos": pos}
            return True
        elif slot_key in st.session_state.squad:
            existing = st.session_state.squad[slot_key]
            if player["ovr"] > existing["ovr"] and pos in suitable_positions:
                st.session_state.squad[slot_key] = {"name": name, **player, "slot_pos": pos}
                return True
    return False

def check_achievements():
    new_achievements = []
    total = st.session_state.total_packs
    if total >= 1 and "first_pack" not in st.session_state.achievements:
        st.session_state.achievements.append("first_pack")
        new_achievements.append("🎉 Birinchi pack ochildi!")
    if total >= 10 and "pack_veteran" not in st.session_state.achievements:
        st.session_state.achievements.append("pack_veteran")
        new_achievements.append("⚡ Pack Veteran - 10 ta pack")
    if total >= 50 and "pack_master" not in st.session_state.achievements:
        st.session_state.achievements.append("pack_master")
        new_achievements.append("🏆 Pack Master - 50 ta pack")
    if total >= 100 and "pack_legend" not in st.session_state.achievements:
        st.session_state.achievements.append("pack_legend")
        new_achievements.append("👑 Pack Legend - 100 ta pack!")
    
    icons = [p for _, p in st.session_state.pack_history if p.get("type") == "ICON"]
    if len(icons) >= 1 and "first_icon" not in st.session_state.achievements:
        st.session_state.achievements.append("first_icon")
        new_achievements.append("🌟 Birinchi ICON topildi!")
    if len(icons) >= 5 and "icon_collector" not in st.session_state.achievements:
        st.session_state.achievements.append("icon_collector")
        new_achievements.append("💎 Icon Collector - 5 ta ICON!")
    
    for a in new_achievements:
        add_notification(a, "🏅")

# =============================================
# RENDER FUNCTIONS
# =============================================
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>⚽ EA FC MOBILE SIMULATOR</h1>
        <p>Cheksiz Pul • Bepul Packlar • To'liq Tajriba</p>
    </div>
    """, unsafe_allow_html=True)

def render_currency_bar():
    ovr = calc_team_ovr()
    st.markdown(f"""
    <div class="currency-bar">
        <div class="currency-item">
            <div class="currency-value">🪙 ∞</div>
            <div class="currency-label">COINS</div>
        </div>
        <div class="currency-item">
            <div class="currency-value">💎 ∞</div>
            <div class="currency-label">GEMS</div>
        </div>
        <div class="currency-item">
            <div class="currency-value">🎫 ∞</div>
            <div class="currency-label">TOKENS</div>
        </div>
        <div class="currency-item">
            <div class="currency-value">👥 ∞</div>
            <div class="currency-label">FAN TOKENS</div>
        </div>
        <div class="currency-item">
            <div class="currency-value">📦 {st.session_state.total_packs}</div>
            <div class="currency-label">TOTAL PACKS</div>
        </div>
        <div class="currency-item">
            <div class="currency-value">⚽ {ovr if ovr > 0 else "—"}</div>
            <div class="currency-label">TEAM OVR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_player_card_html(name, player, size="normal"):
    color_class = get_player_color_class(player["ovr"], player.get("type", "GOLD"))
    type_colors = {
        "ICON": "#c084fc",
        "LIVE": "#4ade80",
        "TOTS": "#f97316",
        "TOTW": "#facc15",
        "GOLD": "#FFD700",
        "UCL": "#60a5fa",
    }
    ovr_color = type_colors.get(player.get("type", "GOLD"), "#FFD700")
    
    border_color = {
        "legend": "#c084fc",
        "gold": "#FFD700",
        "silver": "#9ca3af",
    }.get(color_class, "#3b82f6")
    
    bg_gradient = {
        "legend": "linear-gradient(145deg, #3b1f6b, #1e0f3a)",
        "gold": "linear-gradient(145deg, #5c4004, #3d2800)",
        "silver": "linear-gradient(145deg, #374151, #1f2937)",
    }.get(color_class, "linear-gradient(145deg, #1e3a5f, #0f2040)")
    
    return f"""
    <div style="
        background: {bg_gradient};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
        box-shadow: 0 4px 15px {border_color}44;
        margin: 4px;
        min-width: 100px;
    ">
        <div style="font-size: 0.7em; color: {ovr_color}; font-weight: 700; letter-spacing: 1px;">{player.get('type', 'GOLD')}</div>
        <div style="font-size: 2.2em; font-weight: 900; color: {ovr_color}; font-family: 'Oswald', sans-serif; line-height: 1.1;">{player['ovr']}</div>
        <div style="font-size: 0.75em; font-weight: 600; color: white; margin: 3px 0;">{name}</div>
        <div style="font-size: 0.65em; color: #94a3b8; letter-spacing: 2px;">{player['pos']}</div>
        <div style="font-size: 0.65em; color: #60a5fa; margin-top: 2px;">{player['club']}</div>
        <div style="font-size: 0.9em; margin-top: 3px;">{player['nation']}</div>
    </div>
    """

def render_player_stats(name, player):
    stats = [
        ("PAC", player.get("pace", 80)),
        ("SHO", player.get("shoot", 80)),
        ("PAS", player.get("pass", 80)),
        ("DRI", player.get("dribble", 80)),
        ("DEF", player.get("defend", 80)),
        ("PHY", player.get("physical", 80)),
    ]
    
    bars_html = ""
    for stat_name, val in stats:
        color = get_stat_color(val)
        bars_html += f"""
        <div style="display: flex; align-items: center; gap: 8px; margin: 3px 0;">
            <span style="width: 35px; font-size: 0.75em; color: #94a3b8; text-align: right;">{stat_name}</span>
            <div style="flex: 1; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden;">
                <div style="width: {val}%; height: 100%; background: {color}; border-radius: 4px;"></div>
            </div>
            <span style="width: 25px; font-size: 0.8em; font-weight: 700; color: white;">{val}</span>
        </div>
        """
    
    color_class = get_player_color_class(player["ovr"], player.get("type", "GOLD"))
    type_colors = {
        "ICON": "#c084fc",
        "LIVE": "#4ade80",
        "TOTS": "#f97316",
        "TOTW": "#facc15",
        "GOLD": "#FFD700",
    }
    ovr_color = type_colors.get(player.get("type", "GOLD"), "#FFD700")
    
    return f"""
    <div style="background: linear-gradient(145deg, #1a2540, #0d1b35); border: 2px solid {ovr_color}44; border-radius: 12px; padding: 15px; margin: 5px 0;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <div style="background: {ovr_color}22; border: 2px solid {ovr_color}; border-radius: 8px; padding: 5px 10px; text-align: center;">
                <div style="font-size: 1.8em; font-weight: 900; color: {ovr_color}; font-family: 'Oswald', sans-serif; line-height: 1;">{player['ovr']}</div>
                <div style="font-size: 0.65em; color: {ovr_color}; letter-spacing: 1px;">{player['pos']}</div>
            </div>
            <div>
                <div style="font-weight: 700; color: white; font-size: 1em;">{name}</div>
                <div style="font-size: 0.8em; color: #60a5fa;">{player['club']}</div>
                <div style="font-size: 0.8em; color: #94a3b8;">{player['nation']} {player.get('type','GOLD')}</div>
            </div>
        </div>
        {bars_html}
    </div>
    """

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: linear-gradient(145deg, #1a2540, #0d1b35); border-radius: 12px; border: 1px solid #2d9e5f; margin-bottom: 15px;">
        <div style="font-size: 2.5em;">{st.session_state.club_badge}</div>
        <div style="font-family: 'Oswald', sans-serif; font-size: 1.3em; color: #FFD700; font-weight: 700; letter-spacing: 2px;">{st.session_state.club_name}</div>
        <div style="font-size: 0.8em; color: #94a3b8;">⭐ {st.session_state.club_reputation:,} Reputation</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Klub Sozlamalari")
    new_name = st.text_input("Klub nomi:", value=st.session_state.club_name, key="club_name_input")
    if new_name != st.session_state.club_name:
        st.session_state.club_name = new_name
    
    badge_options = ["⚽", "🦁", "🦅", "🐉", "⚡", "🔥", "💫", "🌟", "👑", "🏆", "⚔️", "🛡️"]
    selected_badge = st.selectbox("Klub badge:", badge_options, 
                                  index=badge_options.index(st.session_state.club_badge) if st.session_state.club_badge in badge_options else 0)
    st.session_state.club_badge = selected_badge
    
    formation = st.selectbox("Formatsiya:", FORMATIONS, 
                              index=FORMATIONS.index(st.session_state.formation) if st.session_state.formation in FORMATIONS else 0)
    st.session_state.formation = formation
    
    st.markdown("---")
    st.markdown("### 📊 Statistika")
    team_ovr = calc_team_ovr()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Team OVR", team_ovr if team_ovr > 0 else "—")
        st.metric("Packs", st.session_state.total_packs)
    with col2:
        st.metric("Players", st.session_state.total_players)
        st.metric("Achievements", len(st.session_state.achievements))
    
    st.markdown("---")
    st.markdown("### 🔔 So'nggi Xabarlar")
    for notif in st.session_state.notifications[:5]:
        st.markdown(f"<div style='font-size: 0.8em; color: #a8f5c8; padding: 3px 0;'>{notif}</div>", 
                   unsafe_allow_html=True)
    
    if not st.session_state.notifications:
        st.markdown("<div style='font-size: 0.8em; color: #64748b;'>Hali xabar yo'q...</div>", 
                   unsafe_allow_html=True)

# =============================================
# MAIN CONTENT
# =============================================
render_header()
render_currency_bar()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 PACK OCHISH", 
    "🏟️ KLUB RIVOJLANTIRISH", 
    "👥 TARKIB VA SQUAD",
    "📊 STATISTIKA",
    "🏅 YUTUQLAR"
])

# =============================================
# TAB 1: PACK OPENING
# =============================================
with tab1:
    st.markdown('<div class="section-header">📦 PACK DO\'KONI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f2d1a, #1a4a2a); border: 1px solid #4ade80; border-radius: 10px; padding: 12px 20px; margin-bottom: 15px; color: #a8f5c8; font-size: 0.9em;">
        💡 <strong>Barcha packlar BEPUL!</strong> Cheksiz pul va gemlar bilan xohlagan packni oching. ICON, LIVE, TOTW va ko'plab o'yinchilarni yig'ing!
    </div>
    """, unsafe_allow_html=True)
    
    # Pack grid
    pack_cols = st.columns(4)
    pack_names = list(PACKS.keys())
    
    for i, pack_name in enumerate(pack_names):
        pack = PACKS[pack_name]
        with pack_cols[i % 4]:
            color_styles = {
                "gold": ("border: 2px solid #FFD700; box-shadow: 0 0 20px rgba(255,215,0,0.4);", "#FFD700"),
                "legend": ("border: 2px solid #c084fc; box-shadow: 0 0 25px rgba(192,132,252,0.5); background: linear-gradient(145deg, #3b1f6b, #1e0f3a);", "#c084fc"),
                "special": ("border: 2px solid #ef4444; box-shadow: 0 0 20px rgba(239,68,68,0.4); background: linear-gradient(145deg, #3f1515, #1f0a0a);", "#ef4444"),
                "ucl": ("border: 2px solid #3b82f6; box-shadow: 0 0 20px rgba(59,130,246,0.5); background: linear-gradient(145deg, #1a3a6b, #0d1f3a);", "#3b82f6"),
            }
            style, accent_color = color_styles.get(pack["color"], color_styles["gold"])
            
            badge_styles = {
                "BEPUL": ("background: #1a4a2a; color: #4ade80; border: 1px solid #4ade80;"),
                "ICON": ("background: #4c1d95; color: #c084fc; border: 1px solid #c084fc;"),
                "TOTW": ("background: #713f12; color: #facc15; border: 1px solid #facc15;"),
                "UCL": ("background: #1e3a5f; color: #60a5fa; border: 1px solid #60a5fa;"),
                "2x ICON": ("background: #4c1d95; color: #c084fc; border: 1px solid #c084fc;"),
                "x10 MEGA": ("background: #4c1d95; color: #c084fc; border: 1px solid #c084fc;"),
            }
            badge_style = badge_styles.get(pack["badge"], "background: #1a4a2a; color: #4ade80;")
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #1a2540, #0d1b35);
                {style}
                border-radius: 16px;
                padding: 18px 12px;
                text-align: center;
                margin-bottom: 8px;
                min-height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
            ">
                <span style="{badge_style} border-radius: 20px; padding: 2px 10px; font-size: 0.7em; font-weight: 700; letter-spacing: 1px;">{pack['badge']}</span>
                <div style="font-size: 2.5em; margin: 8px 0;">{pack['icon']}</div>
                <div style="font-family: 'Oswald', sans-serif; font-size: 1em; color: {accent_color}; font-weight: 700; letter-spacing: 1px;">{pack_name}</div>
                <div style="font-size: 0.7em; color: #94a3b8; margin: 5px 0;">{pack['description']}</div>
                <div style="font-size: 0.75em; color: #4ade80; font-weight: 600;">💰 BEPUL | {pack['player_count']} O'YINCHI</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"OCHISH ▶", key=f"open_pack_{i}"):
                with st.spinner("Pack ochilmoqda..."):
                    time.sleep(0.3)
                    players = open_pack(pack_name)
                    st.session_state["last_opened_players"] = players
                    st.session_state["last_opened_pack"] = pack_name
                    for name, player in players:
                        auto_equip_player(name, player)
                st.rerun()
    
    # Show last opened pack results
    if "last_opened_players" in st.session_state and st.session_state["last_opened_players"]:
        st.markdown("---")
        st.markdown(f'<div class="section-header">🎁 {st.session_state.get("last_opened_pack", "PACK")} NATIJALARI</div>', unsafe_allow_html=True)
        
        result_players = st.session_state["last_opened_players"]
        
        # Check for icons/elite
        icons = [(n, p) for n, p in result_players if p.get("type") == "ICON"]
        elites = [(n, p) for n, p in result_players if p["ovr"] >= 99 and p.get("type") != "ICON"]
        
        if icons:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #4c1d95, #2d1169); border: 2px solid #c084fc; border-radius: 12px; margin-bottom: 10px; animation: legendGlow 2s infinite;">
                <div style="font-size: 2em;">👑</div>
                <div style="font-family: 'Oswald', sans-serif; font-size: 1.5em; color: #c084fc; font-weight: 700;">ICON O'YINCHI TOPILDI!!!</div>
            </div>
            """, unsafe_allow_html=True)
        elif elites:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, #1a3a6b, #0d1f3a); border: 2px solid #60a5fa; border-radius: 12px; margin-bottom: 10px;">
                <div style="font-family: 'Oswald', sans-serif; font-size: 1.2em; color: #60a5fa; font-weight: 700;">⚡ ELITE O'YINCHI!</div>
            </div>
            """, unsafe_allow_html=True)
        
        result_cols = st.columns(min(len(result_players), 5))
        for i, (name, player) in enumerate(result_players):
            with result_cols[i % min(len(result_players), 5)]:
                st.markdown(render_player_card_html(name, player), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header">📋 O\'YINCHILAR TAFSILOTI</div>', unsafe_allow_html=True)
        
        detail_cols = st.columns(min(len(result_players), 3))
        for i, (name, player) in enumerate(result_players):
            with detail_cols[i % min(len(result_players), 3)]:
                st.markdown(render_player_stats(name, player), unsafe_allow_html=True)
    
    # Pack statistics
    st.markdown("---")
    st.markdown('<div class="section-header">📦 PACK TARIXI</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        icons_count = len([p for _, p in st.session_state.pack_history if p.get("type") == "ICON"])
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #3b1f6b, #1e0f3a); border: 1px solid #c084fc; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: 700; color: #c084fc; font-family: 'Oswald', sans-serif;">👑 {icons_count}</div>
            <div style="font-size: 0.8em; color: #94a3b8;">ICON</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        elite_count = len([p for _, p in st.session_state.pack_history if p["ovr"] >= 99 and p.get("type") != "ICON"])
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1e3a5f, #0d1f3a); border: 1px solid #60a5fa; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: 700; color: #60a5fa; font-family: 'Oswald', sans-serif;">⚡ {elite_count}</div>
            <div style="font-size: 0.8em; color: #94a3b8;">ELITE (99+)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        gold_count = len([p for _, p in st.session_state.pack_history if 93 <= p["ovr"] <= 98])
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #5c4004, #3d2800); border: 1px solid #FFD700; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: 700; color: #FFD700; font-family: 'Oswald', sans-serif;">🌟 {gold_count}</div>
            <div style="font-size: 0.8em; color: #94a3b8;">GOLD (93-98)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        total = st.session_state.total_packs
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a2540, #0d1b35); border: 1px solid #4ade80; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: 700; color: #4ade80; font-family: 'Oswald', sans-serif;">📦 {total}</div>
            <div style="font-size: 0.8em; color: #94a3b8;">JAMI PACK</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Last 10 players
    if st.session_state.pack_history:
        st.markdown("#### 🕐 So'nggi Topilgan O'yinchilar")
        last_players = list(reversed(st.session_state.pack_history[-20:]))
        
        hist_cols = st.columns(5)
        for i, (name, player) in enumerate(last_players[:10]):
            with hist_cols[i % 5]:
                st.markdown(render_player_card_html(name, player, size="small"), unsafe_allow_html=True)

# =============================================
# TAB 2: CLUB UPGRADE
# =============================================
with tab2:
    st.markdown('<div class="section-header">🏟️ KLUB RIVOJLANTIRISH</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f2d1a, #1a4a2a); border: 1px solid #4ade80; border-radius: 10px; padding: 12px 20px; margin-bottom: 15px; color: #a8f5c8; font-size: 0.9em;">
        💡 <strong>Barcha yaxshilanishlar BEPUL!</strong> Cheksiz coin bilan klubingizni rivojlantiring va bonuslar oling!
    </div>
    """, unsafe_allow_html=True)
    
    # Overall club progress
    total_levels = sum(st.session_state.club_levels.values())
    max_levels = len(CLUB_UPGRADES) * 5  # max level is 5 (0-5)
    progress_pct = (total_levels / max_levels) * 100 if max_levels > 0 else 0
    
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1a2540, #0d1b35); border: 2px solid #7c3aed; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-family: 'Oswald', sans-serif; font-size: 1.3em; color: #c084fc; font-weight: 700;">🏆 KLUB DARAJASI</div>
            <div style="font-size: 1.5em; font-weight: 700; color: #FFD700; font-family: 'Oswald', sans-serif;">{total_levels}/{max_levels}</div>
        </div>
        <div style="background: #1e293b; border-radius: 10px; height: 15px; overflow: hidden;">
            <div style="width: {progress_pct:.1f}%; height: 100%; background: linear-gradient(90deg, #7c3aed, #c084fc); border-radius: 10px; transition: width 0.5s ease;"></div>
        </div>
        <div style="font-size: 0.8em; color: #94a3b8; margin-top: 8px;">Klub reputatsiyasi: ⭐ {st.session_state.club_reputation:,}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Upgrade cards
    upgrade_cols = st.columns(2)
    
    for idx, (upgrade_name, upgrade_data) in enumerate(CLUB_UPGRADES.items()):
        with upgrade_cols[idx % 2]:
            current_level = st.session_state.club_levels[upgrade_name]
            max_level = len(upgrade_data["levels"]) - 1
            current_info = upgrade_data["levels"][current_level]
            next_info = upgrade_data["levels"][current_level + 1] if current_level < max_level else None
            
            level_pct = (current_level / max_level) * 100
            
            level_color = ["#64748b", "#3b82f6", "#22c55e", "#eab308", "#f97316", "#c084fc"][current_level]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #1a2540, #0d1b35);
                border: 2px solid {level_color};
                border-radius: 15px;
                padding: 18px;
                margin-bottom: 12px;
                box-shadow: 0 4px 15px {level_color}33;
            ">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                    <div>
                        <div style="font-size: 1.8em;">{upgrade_data['icon']}</div>
                        <div style="font-family: 'Oswald', sans-serif; font-size: 1.1em; color: white; font-weight: 700; letter-spacing: 1px;">{upgrade_name}</div>
                        <div style="font-size: 0.75em; color: #94a3b8;">{upgrade_data['description']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-family: 'Oswald', sans-serif; font-size: 1.5em; color: {level_color}; font-weight: 700;">LVL {current_level}</div>
                        <div style="font-size: 0.75em; color: #64748b;">/{max_level}</div>
                    </div>
                </div>
                
                <div style="background: #1e293b; border-radius: 8px; height: 8px; overflow: hidden; margin-bottom: 10px;">
                    <div style="width: {level_pct:.1f}%; height: 100%; background: linear-gradient(90deg, {level_color}, {'#4ade80' if level_pct < 100 else level_color}); border-radius: 8px;"></div>
                </div>
                
                <div style="background: #0d1b35; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px;">
                    <div style="font-size: 0.8em; color: #94a3b8;">Joriy daraja:</div>
                    <div style="font-size: 0.9em; color: #4ade80; font-weight: 600;">{current_info['name']} → {current_info['bonus']}</div>
                </div>
                
                {f'''
                <div style="background: #0d1b35; border-radius: 8px; padding: 8px 12px; border: 1px solid {level_color}44;">
                    <div style="font-size: 0.75em; color: #94a3b8;">Keyingi daraja:</div>
                    <div style="font-size: 0.85em; color: {level_color}; font-weight: 600;">{next_info['name']} → {next_info['bonus']}</div>
                    <div style="font-size: 0.75em; color: #4ade80; margin-top: 3px;">💰 BEPUL (∞ Coins)</div>
                </div>
                ''' if next_info else '<div style="text-align: center; color: #FFD700; font-family: Oswald; font-size: 0.9em; padding: 5px;">🏆 MAKSIMAL DARAJA!</div>'}
            </div>
            """, unsafe_allow_html=True)
            
            if current_level < max_level:
                if st.button(f"⬆️ Yaxshilash", key=f"upgrade_{upgrade_name}"):
                    st.session_state.club_levels[upgrade_name] += 1
                    st.session_state.club_reputation += 500 * (st.session_state.club_levels[upgrade_name])
                    add_notification(f"{upgrade_name} LVL {st.session_state.club_levels[upgrade_name]} ga ko'tarildi! {upgrade_data['levels'][st.session_state.club_levels[upgrade_name]]['bonus']}", "🏟️")
                    check_achievements()
                    st.rerun()
            else:
                st.markdown("""
                <div style="text-align: center; padding: 8px; background: linear-gradient(135deg, #713f12, #92400e); border-radius: 8px; color: #FFD700; font-family: 'Oswald'; font-size: 0.9em; font-weight: 700; letter-spacing: 1px;">
                    🏆 MAX LEVEL!
                </div>
                """, unsafe_allow_html=True)
    
    # Bonuses summary
    st.markdown("---")
    st.markdown('<div class="section-header">🎁 FAOL BONUSLAR</div>', unsafe_allow_html=True)
    
    bonus_cols = st.columns(3)
    all_bonuses = []
    for upgrade_name, upgrade_data in CLUB_UPGRADES.items():
        current_level = st.session_state.club_levels[upgrade_name]
        current_info = upgrade_data["levels"][current_level]
        if current_level > 0:
            all_bonuses.append((upgrade_data["icon"], upgrade_name, current_info["name"], current_info["bonus"]))
    
    if all_bonuses:
        for i, (icon, name, level_name, bonus) in enumerate(all_bonuses):
            with bonus_cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #0f2d1a, #1a4a2a); border: 1px solid #4ade80; border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                    <div style="font-size: 1.2em;">{icon} <span style="font-size: 0.8em; color: white; font-weight: 600;">{name}</span></div>
                    <div style="font-size: 0.75em; color: #94a3b8;">{level_name}</div>
                    <div style="font-size: 0.85em; color: #4ade80; font-weight: 700; margin-top: 3px;">{bonus}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #64748b; font-size: 0.9em; text-align: center; padding: 20px;'>Hali hech qanday yaxshilanish yo'q. Yuqoridagi tugmalarni bosing!</div>", unsafe_allow_html=True)

# =============================================
# TAB 3: SQUAD
# =============================================
with tab3:
    st.markdown('<div class="section-header">👥 TARKIB VA SQUAD</div>', unsafe_allow_html=True)
    
    team_ovr = calc_team_ovr()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        ovr_color = "#4ade80" if team_ovr >= 99 else "#facc15" if team_ovr >= 95 else "#60a5fa"
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(145deg, #1a2540, #0d1b35); border: 2px solid {ovr_color}; border-radius: 15px; margin-bottom: 15px;">
            <div style="font-family: 'Oswald', sans-serif; font-size: 3em; color: {ovr_color}; font-weight: 700;">{team_ovr if team_ovr > 0 else '—'}</div>
            <div style="color: #94a3b8; font-size: 0.9em; letter-spacing: 2px;">TEAM OVR</div>
            <div style="color: {ovr_color}; font-size: 0.8em; margin-top: 5px;">{st.session_state.formation} Formatsiya</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Squad display
    formation = st.session_state.formation
    positions = POSITIONS.get(formation, POSITIONS["4-3-3"])
    
    st.markdown(f"#### ⚽ {st.session_state.formation} - Asosiy Tarkib")
    
    # Group by lines
    squad_rows = {
        "GK": [],
        "DEF": [],
        "MID": [],
        "ATT": [],
    }
    
    def get_line(pos):
        if pos in ["GK"]: return "GK"
        if pos in ["RB", "LB", "CB"]: return "DEF"
        if pos in ["CDM", "CM", "CAM", "RM", "LM"]: return "MID"
        return "ATT"
    
    position_slots = []
    for i, pos in enumerate(positions):
        slot_key = f"slot_{i}"
        player_data = st.session_state.squad.get(slot_key, None)
        position_slots.append((i, pos, slot_key, player_data))
    
    # Group by line for visual layout
    lines = {"ATT": [], "MID": [], "DEF": [], "GK": []}
    for i, pos, slot_key, player_data in position_slots:
        line = get_line(pos)
        lines[line].append((i, pos, slot_key, player_data))
    
    for line_name in ["ATT", "MID", "DEF", "GK"]:
        slots_in_line = lines[line_name]
        if not slots_in_line:
            continue
        
        line_cols = st.columns(len(slots_in_line))
        for col_idx, (i, pos, slot_key, player_data) in enumerate(slots_in_line):
            with line_cols[col_idx]:
                if player_data:
                    type_colors = {
                        "ICON": "#c084fc", "LIVE": "#4ade80", "TOTS": "#f97316",
                        "TOTW": "#facc15", "GOLD": "#FFD700", "UCL": "#60a5fa",
                    }
                    p_color = type_colors.get(player_data.get("type", "GOLD"), "#FFD700")
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(145deg, #1a2540, #0d1b35);
                        border: 2px solid {p_color};
                        border-radius: 10px;
                        padding: 10px 5px;
                        text-align: center;
                        box-shadow: 0 2px 10px {p_color}44;
                        margin: 3px;
                    ">
                        <div style="font-size: 0.6em; color: {p_color}; font-weight: 700;">{player_data.get('type','GOLD')}</div>
                        <div style="font-size: 1.6em; font-weight: 900; color: {p_color}; font-family: 'Oswald', sans-serif;">{player_data['ovr']}</div>
                        <div style="font-size: 0.65em; font-weight: 600; color: white; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{player_data['name']}</div>
                        <div style="font-size: 0.55em; color: #60a5fa; background: #0d1b35; border-radius: 3px; padding: 1px 4px; margin-top: 2px; display: inline-block;">{pos}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        background: #0a0e1a;
                        border: 2px dashed #2d3748;
                        border-radius: 10px;
                        padding: 10px 5px;
                        text-align: center;
                        min-height: 80px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        margin: 3px;
                    ">
                        <div style="font-size: 1.2em; color: #2d3748;">➕</div>
                        <div style="font-size: 0.65em; color: #4a5568; letter-spacing: 1px;">{pos}</div>
                        <div style="font-size: 0.6em; color: #2d3748;">Bo'sh</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Inventory - all collected players
    st.markdown("---")
    st.markdown('<div class="section-header">🎒 O\'YINCHILAR INVENTORI</div>', unsafe_allow_html=True)
    
    if st.session_state.pack_history:
        # Filter options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            filter_pos = st.selectbox("Pozitsiya bo'yicha:", ["Barchasi", "GK", "CB", "RB", "LB", "CDM", "CM", "CAM", "RM", "LM", "RW", "LW", "ST"])
        with filter_col2:
            filter_type = st.selectbox("Tur bo'yicha:", ["Barchasi", "ICON", "LIVE", "GOLD", "TOTS", "TOTW"])
        with filter_col3:
            sort_by = st.selectbox("Tartib:", ["OVR (Yuqori)", "OVR (Past)", "Nom", "Pozitsiya"])
        
        # Get unique players (latest occurrence)
        seen = {}
        for name, player in st.session_state.pack_history:
            seen[name] = player
        
        all_inv_players = list(seen.items())
        
        # Apply filters
        if filter_pos != "Barchasi":
            all_inv_players = [(n, p) for n, p in all_inv_players if p["pos"] == filter_pos]
        if filter_type != "Barchasi":
            all_inv_players = [(n, p) for n, p in all_inv_players if p.get("type", "GOLD") == filter_type]
        
        # Sort
        if sort_by == "OVR (Yuqori)":
            all_inv_players.sort(key=lambda x: x[1]["ovr"], reverse=True)
        elif sort_by == "OVR (Past)":
            all_inv_players.sort(key=lambda x: x[1]["ovr"])
        elif sort_by == "Nom":
            all_inv_players.sort(key=lambda x: x[0])
        elif sort_by == "Pozitsiya":
            all_inv_players.sort(key=lambda x: x[1]["pos"])
        
        st.markdown(f"<div style='color: #94a3b8; font-size: 0.85em; margin-bottom: 10px;'>{len(all_inv_players)} ta o'yinchi topildi</div>", unsafe_allow_html=True)
        
        if all_inv_players:
            inv_cols = st.columns(5)
            for i, (name, player) in enumerate(all_inv_players):
                with inv_cols[i % 5]:
                    st.markdown(render_player_card_html(name, player), unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #64748b; text-align: center; padding: 20px;'>Filtrga mos o'yinchi topilmadi</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #64748b;">
            <div style="font-size: 3em; margin-bottom: 10px;">📦</div>
            <div style="font-size: 1.1em;">Hali hech qanday pack ochilmadi.</div>
            <div style="font-size: 0.9em; margin-top: 5px;">PACK OCHISH tabiga o'ting va birinchi packni oching!</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# TAB 4: STATISTICS
# =============================================
with tab4:
    st.markdown('<div class="section-header">📊 TO\'LIQ STATISTIKA</div>', unsafe_allow_html=True)
    
    # Main stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Jami Pack", st.session_state.total_packs)
    with col2:
        st.metric("👥 Jami O'yinchi", st.session_state.total_players)
    with col3:
        icons_total = len([p for _, p in st.session_state.pack_history if p.get("type") == "ICON"])
        st.metric("👑 ICON", icons_total)
    with col4:
        elite_total = len([p for _, p in st.session_state.pack_history if p["ovr"] >= 99])
        st.metric("⚡ Elite (99+)", elite_total)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("🏟️ Club Upgrades", sum(st.session_state.club_levels.values()))
    with col6:
        st.metric("⭐ Reputation", f"{st.session_state.club_reputation:,}")
    with col7:
        team_ovr = calc_team_ovr()
        st.metric("📈 Team OVR", team_ovr if team_ovr > 0 else "—")
    with col8:
        st.metric("🏅 Achievements", len(st.session_state.achievements))
    
    st.markdown("---")
    
    # OVR distribution
    if st.session_state.pack_history:
        st.markdown("#### 📊 OVR Taqsimoti")
        
        ovr_ranges = {
            "105-112 (ICON)": 0,
            "99-104 (Elite)": 0,
            "95-98 (Super Gold)": 0,
            "93-94 (Gold)": 0,
        }
        
        for _, player in st.session_state.pack_history:
            ovr = player["ovr"]
            if ovr >= 105:
                ovr_ranges["105-112 (ICON)"] += 1
            elif ovr >= 99:
                ovr_ranges["99-104 (Elite)"] += 1
            elif ovr >= 95:
                ovr_ranges["95-98 (Super Gold)"] += 1
            else:
                ovr_ranges["93-94 (Gold)"] += 1
        
        total_counted = sum(ovr_ranges.values())
        
        range_colors = {
            "105-112 (ICON)": "#c084fc",
            "99-104 (Elite)": "#60a5fa",
            "95-98 (Super Gold)": "#facc15",
            "93-94 (Gold)": "#FFD700",
        }
        
        for range_name, count in ovr_ranges.items():
            pct = (count / total_counted * 100) if total_counted > 0 else 0
            color = range_colors[range_name]
            st.markdown(f"""
            <div style="margin: 8px 0; display: flex; align-items: center; gap: 12px;">
                <div style="width: 180px; font-size: 0.85em; color: {color}; text-align: right; font-weight: 600;">{range_name}</div>
                <div style="flex: 1; background: #1e293b; border-radius: 6px; height: 22px; overflow: hidden;">
                    <div style="width: {pct:.1f}%; height: 100%; background: {color}; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px;">
                        <span style="font-size: 0.75em; color: #000; font-weight: 700;">{count}</span>
                    </div>
                </div>
                <div style="width: 50px; font-size: 0.85em; color: #94a3b8;">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Best players
        st.markdown("#### 🏆 Eng Yaxshi O'yinchilar (Top 5)")
        
        if st.session_state.pack_history:
            seen = {}
            for name, player in st.session_state.pack_history:
                if name not in seen or player["ovr"] > seen[name]["ovr"]:
                    seen[name] = player
            
            top5 = sorted(seen.items(), key=lambda x: x[1]["ovr"], reverse=True)[:5]
            
            for rank, (name, player) in enumerate(top5, 1):
                rank_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#60a5fa", "#94a3b8"]
                rank_color = rank_colors[rank - 1]
                type_colors = {"ICON": "#c084fc", "LIVE": "#4ade80", "GOLD": "#FFD700"}
                p_color = type_colors.get(player.get("type", "GOLD"), "#FFD700")
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, #1a2540, #0d1b35);
                    border: 1px solid {rank_color};
                    border-radius: 10px;
                    padding: 12px 20px;
                    margin: 5px 0;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                ">
                    <div style="font-size: 1.5em; font-weight: 900; color: {rank_color}; width: 30px; font-family: 'Oswald', sans-serif;">#{rank}</div>
                    <div style="background: {p_color}22; border: 1px solid {p_color}; border-radius: 8px; padding: 5px 10px; text-align: center; min-width: 55px;">
                        <div style="font-size: 1.3em; font-weight: 900; color: {p_color}; font-family: 'Oswald', sans-serif; line-height: 1;">{player['ovr']}</div>
                        <div style="font-size: 0.6em; color: {p_color};">{player['pos']}</div>
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: white;">{name}</div>
                        <div style="font-size: 0.8em; color: #60a5fa;">{player['club']} • {player['nation']}</div>
                    </div>
                    <div style="background: {p_color}22; padding: 3px 10px; border-radius: 20px; font-size: 0.75em; color: {p_color}; font-weight: 700;">{player.get('type','GOLD')}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; color: #64748b; padding: 40px;'>Statistika ko'rish uchun pack oching!</div>", unsafe_allow_html=True)
    
    # Club upgrade progress
    st.markdown("---")
    st.markdown("#### 🏟️ Klub Rivojlanish Holati")
    
    upg_cols = st.columns(3)
    for idx, (name, data) in enumerate(CLUB_UPGRADES.items()):
        with upg_cols[idx % 3]:
            level = st.session_state.club_levels[name]
            max_lv = len(data["levels"]) - 1
            pct = (level / max_lv) * 100
            colors = ["#64748b", "#3b82f6", "#22c55e", "#eab308", "#f97316", "#c084fc"]
            color = colors[level]
            
            st.markdown(f"""
            <div style="background: #1a2540; border: 1px solid {color}; border-radius: 10px; padding: 12px; margin: 5px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span>{data['icon']} <span style="color: white; font-size: 0.85em; font-weight: 600;">{name}</span></span>
                    <span style="color: {color}; font-family: 'Oswald'; font-weight: 700;">LVL {level}/{max_lv}</span>
                </div>
                <div style="background: #0d1b35; border-radius: 5px; height: 8px; overflow: hidden;">
                    <div style="width: {pct:.0f}%; height: 100%; background: {color}; border-radius: 5px;"></div>
                </div>
                <div style="font-size: 0.7em; color: #4ade80; margin-top: 4px;">{data['levels'][level]['bonus']}</div>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# TAB 5: ACHIEVEMENTS
# =============================================
with tab5:
    st.markdown('<div class="section-header">🏅 YUTUQLAR VA ACHIEVEMENTS</div>', unsafe_allow_html=True)
    
    all_achievements = [
        {"id": "first_pack", "name": "Birinchi Qadam", "desc": "Birinchi packni oching", "icon": "📦", "reward": "50 Reputation"},
        {"id": "pack_veteran", "name": "Pack Veteran", "desc": "10 ta pack oching", "icon": "⚡", "reward": "200 Reputation"},
        {"id": "pack_master", "name": "Pack Master", "desc": "50 ta pack oching", "icon": "🏆", "reward": "1000 Reputation"},
        {"id": "pack_legend", "name": "Pack Legend", "desc": "100 ta pack oching", "icon": "👑", "reward": "5000 Reputation"},
        {"id": "first_icon", "name": "Legend Hunter", "desc": "Birinchi ICONni toping", "icon": "🌟", "reward": "2000 Reputation"},
        {"id": "icon_collector", "name": "Icon Collector", "desc": "5 ta ICON to'plang", "icon": "💎", "reward": "10000 Reputation"},
        {"id": "squad_full", "name": "Dream Team", "desc": "Barcha squad joylarini to'ldiring", "icon": "⚽", "reward": "3000 Reputation"},
        {"id": "max_upgrade", "name": "Club Builder", "desc": "Bitta yaxshilanishni MAX darajaga olib chiqing", "icon": "🏟️", "reward": "5000 Reputation"},
        {"id": "all_max", "name": "FC Mogul", "desc": "Barcha yaxshilanishlarni MAX darajaga olib chiqing", "icon": "🌠", "reward": "50000 Reputation"},
    ]
    
    # Check squad full
    formation = st.session_state.formation
    positions_count = len(POSITIONS.get(formation, POSITIONS["4-3-3"]))
    squad_filled = sum(1 for i in range(positions_count) if f"slot_{i}" in st.session_state.squad)
    
    if squad_filled >= positions_count and "squad_full" not in st.session_state.achievements:
        st.session_state.achievements.append("squad_full")
        add_notification("Dream Team - Barcha tarkib to'ldirildi!", "⚽")
    
    max_levels_check = [v >= 5 for v in st.session_state.club_levels.values()]
    if any(max_levels_check) and "max_upgrade" not in st.session_state.achievements:
        st.session_state.achievements.append("max_upgrade")
        add_notification("Club Builder - MAX darajaga erishildi!", "🏟️")
    
    if all(max_levels_check) and "all_max" not in st.session_state.achievements:
        st.session_state.achievements.append("all_max")
        add_notification("FC Mogul - Barcha MAX!", "🌠")
    
    # Progress overview
    unlocked = len(st.session_state.achievements)
    total_ach = len(all_achievements)
    ach_pct = (unlocked / total_ach * 100) if total_ach > 0 else 0
    
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1a2540, #0d1b35); border: 2px solid #FFD700; border-radius: 15px; padding: 20px; margin-bottom: 20px; text-align: center;">
        <div style="font-family: 'Oswald', sans-serif; font-size: 2em; color: #FFD700; font-weight: 700;">{unlocked}/{total_ach}</div>
        <div style="color: #94a3b8; margin-bottom: 10px;">Achievements ochilgan</div>
        <div style="background: #1e293b; border-radius: 10px; height: 15px; overflow: hidden;">
            <div style="width: {ach_pct:.1f}%; height: 100%; background: linear-gradient(90deg, #FFD700, #facc15); border-radius: 10px;"></div>
        </div>
        <div style="color: #94a3b8; font-size: 0.85em; margin-top: 5px;">{ach_pct:.1f}% bajarildi</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievement list
    ach_cols = st.columns(2)
    for idx, ach in enumerate(all_achievements):
        with ach_cols[idx % 2]:
            unlocked_this = ach["id"] in st.session_state.achievements
            
            bg_color = "linear-gradient(145deg, #1a4a2a, #0f2d1a)" if unlocked_this else "linear-gradient(145deg, #1a2540, #0d1b35)"
            border_color = "#4ade80" if unlocked_this else "#1e3a5f"
            opacity = "1" if unlocked_this else "0.5"
            status = "✅ BAJARILDI" if unlocked_this else "🔒 Qulfli"
            status_color = "#4ade80" if unlocked_this else "#64748b"
            
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                opacity: {opacity};
            ">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 2em; min-width: 40px; text-align: center;">{ach['icon']}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: white; font-family: 'Oswald', sans-serif; font-size: 1.05em;">{ach['name']}</div>
                        <div style="font-size: 0.8em; color: #94a3b8; margin-top: 2px;">{ach['desc']}</div>
                        <div style="font-size: 0.75em; color: #FFD700; margin-top: 3px;">🎁 {ach['reward']}</div>
                    </div>
                    <div style="font-size: 0.75em; color: {status_color}; font-weight: 700; white-space: nowrap;">{status}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips
    st.markdown("---")
    st.markdown('<div class="section-header">💡 O\'YIN MASLAHATLARI</div>', unsafe_allow_html=True)
    
    tips = [
        ("📦", "Pack ochish", "Icon Pack va Ultimate Icon Pack dan eng yaxshi o'yinchilar chiqadi!"),
        ("🏟️", "Klub rivojlantirish", "Barcha yaxshilanishlarni MAX darajaga olib chiqing - katta bonuslar olasiz!"),
        ("👥", "Squad tuzish", "SQUAD tabida formatsiyangizni tanlang va tarkibingizni ko'ring."),
        ("⚡", "Elite o'yinchilar", "99+ OVR o'yinchilar - Jude Bellingham, Haaland, Vinicius Jr va boshqalar!"),
        ("👑", "ICON o'yinchilar", "Ronaldinho, Zidane, Beckham - eng zo'r legendlar! ICON Pack oching!"),
        ("📊", "Statistika", "Statistika tabida o'yinchilaringizning OVR taqsimotini kuzating."),
    ]
    
    tip_cols = st.columns(3)
    for idx, (icon, title, desc) in enumerate(tips):
        with tip_cols[idx % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #1a2540, #0d1b35); border: 1px solid #2d3748; border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                <div style="font-size: 1.3em;">{icon}</div>
                <div style="font-weight: 700; color: #FFD700; font-size: 0.9em; margin: 3px 0;">{title}</div>
                <div style="font-size: 0.8em; color: #94a3b8;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; color: #4a5568; font-size: 0.8em; margin-top: 20px;">
    <div style="border-top: 1px solid #1e3a5f; padding-top: 15px;">
        ⚽ EA FC Mobile Simulator • Barcha packlar bepul • Cheksiz pul • Claude AI tomonidan yaratilgan
    </div>
</div>
""", unsafe_allow_html=True)
