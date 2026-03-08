import streamlit as st
import random
import time
from datetime import datetime

# ══════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="EA FC Mobile Ultimate",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap');

:root {
  --gold:#FFD700; --gold2:#FFA500; --icon:#C084FC; --elite:#38BDF8;
  --green:#4ADE80; --red:#F87171; --dark:#06090F; --dark2:#0D1117;
  --dark3:#161B22; --border:#21262D; --text:#E6EDF3; --muted:#7D8590;
}

.stApp { background:var(--dark) !important; color:var(--text); font-family:'Rajdhani',sans-serif; }
.main .block-container { padding:1rem 1.5rem; max-width:1400px; }

::-webkit-scrollbar{width:6px} ::-webkit-scrollbar-track{background:#0D1117}
::-webkit-scrollbar-thumb{background:#30363D;border-radius:3px}

/* HEADER */
.fc-header {
  background:linear-gradient(135deg,#0D1B2A,#1A2540,#0D2818);
  border:1px solid rgba(255,215,0,.25); border-radius:16px;
  padding:22px 28px; margin-bottom:18px; position:relative; overflow:hidden;
}
.fc-header::before {
  content:''; position:absolute; inset:0;
  background:radial-gradient(ellipse 60% 80% at 80% 50%,rgba(74,222,128,.06),transparent);
  pointer-events:none;
}
.fc-title {
  font-family:'Bebas Neue',sans-serif; font-size:clamp(1.6rem,3vw,2.8rem);
  letter-spacing:4px;
  background:linear-gradient(90deg,#FFD700,#FFA500,#4ADE80);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  margin:0; line-height:1;
}
.fc-sub { color:var(--muted); font-size:.8rem; margin-top:4px; letter-spacing:2px; text-transform:uppercase; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  background:var(--dark3); border-radius:10px; gap:4px;
  border:1px solid var(--border); padding:4px;
}
.stTabs [data-baseweb="tab"] {
  background:transparent; color:var(--muted); border-radius:7px;
  font-family:'Rajdhani',sans-serif; font-weight:600; font-size:.88rem;
  letter-spacing:1px; padding:8px 14px; transition:all .2s;
}
.stTabs [aria-selected="true"] {
  background:linear-gradient(135deg,#1A6B3C,#2D9E5F) !important;
  color:#fff !important;
}

/* BUTTONS */
div.stButton>button {
  background:linear-gradient(135deg,#1A6B3C,#2D9E5F);
  color:#fff; border:none; border-radius:10px;
  font-family:'Rajdhani',sans-serif; font-weight:700;
  font-size:.88rem; letter-spacing:1.5px; text-transform:uppercase;
  padding:10px 18px; width:100%;
  box-shadow:0 4px 15px rgba(45,158,95,.35); transition:all .2s;
}
div.stButton>button:hover {
  background:linear-gradient(135deg,#2D9E5F,#4ADE80);
  transform:translateY(-2px); box-shadow:0 6px 20px rgba(74,222,128,.5);
}

/* SECTION HEADER */
.sec-head {
  font-family:'Bebas Neue',sans-serif; font-size:1.5rem; letter-spacing:3px;
  color:var(--gold); border-bottom:2px solid #1A6B3C;
  padding-bottom:8px; margin:18px 0 12px;
}

/* PACK CARD */
.pack-card {
  border-radius:14px; padding:18px 12px; text-align:center;
  min-height:220px; display:flex; flex-direction:column;
  align-items:center; justify-content:space-between;
  transition:transform .25s, box-shadow .25s;
}
.pack-card:hover { transform:translateY(-5px); }
.pack-gold    { background:linear-gradient(145deg,#1a1000,#2a1d00); border:2px solid #FFD700; box-shadow:0 4px 18px rgba(255,215,0,.28); }
.pack-elite   { background:linear-gradient(145deg,#00101a,#001a2a); border:2px solid #38BDF8; box-shadow:0 4px 18px rgba(56,189,248,.28); }
.pack-icon    { background:linear-gradient(145deg,#150a25,#250f45); border:2px solid #C084FC; box-shadow:0 4px 22px rgba(192,132,252,.38); }
.pack-ultimate{ background:linear-gradient(145deg,#1a0505,#2a0a0a); border:2px solid #F87171; box-shadow:0 4px 22px rgba(248,113,113,.38); }
.pack-ucl     { background:linear-gradient(145deg,#000d1a,#001530); border:2px solid #60A5FA; box-shadow:0 4px 18px rgba(96,165,250,.28); }
.pack-tots    { background:linear-gradient(145deg,#001a0a,#002a10); border:2px solid #4ADE80; box-shadow:0 4px 18px rgba(74,222,128,.28); }

.pack-emoji { font-size:2.6rem; margin:4px 0; }
.pack-title { font-family:'Bebas Neue',sans-serif; font-size:1rem; letter-spacing:2px; margin:4px 0; }
.pack-desc  { font-size:.68rem; color:var(--muted); margin:2px 0 6px; }
.pack-badge { display:inline-block; padding:2px 9px; border-radius:20px; font-size:.62rem; font-weight:800; letter-spacing:1px; }
.b-free   { background:rgba(74,222,128,.15);  color:#4ADE80; border:1px solid #4ADE80; }
.b-elite  { background:rgba(56,189,248,.15);  color:#38BDF8; border:1px solid #38BDF8; }
.b-icon   { background:rgba(192,132,252,.15); color:#C084FC; border:1px solid #C084FC; }
.b-ult    { background:rgba(248,113,113,.15); color:#F87171; border:1px solid #F87171; }

/* PLAYER CARD (big) */
.pcard-big {
  border-radius:16px; padding:24px 18px; text-align:center;
  width:185px; margin:0 auto; position:relative; overflow:hidden;
}
.pcard-base    { background:linear-gradient(160deg,#1a1a1a,#2a2a2a); border:2px solid #9CA3AF; box-shadow:0 0 18px rgba(156,163,175,.3); }
.pcard-silver  { background:linear-gradient(160deg,#1a1a2a,#2a2a4a); border:2px solid #C0C0C0; box-shadow:0 0 22px rgba(192,192,192,.4); }
.pcard-gold    { background:linear-gradient(160deg,#2a1a00,#4a3000); border:2px solid #FFD700; box-shadow:0 0 25px rgba(255,215,0,.5); }
.pcard-elite   { background:linear-gradient(160deg,#001a2a,#003050); border:2px solid #38BDF8; box-shadow:0 0 28px rgba(56,189,248,.55); }
.pcard-legend  { background:linear-gradient(160deg,#150a25,#250f45); border:2px solid #C084FC; box-shadow:0 0 32px rgba(192,132,252,.6); }
.pcard-ultimate{ background:linear-gradient(160deg,#1a0505,#2a0a0a); border:2px solid #F87171; box-shadow:0 0 36px rgba(248,113,113,.65); }
.pcard-ovr  { font-family:'Bebas Neue',sans-serif; font-size:4.5rem; line-height:1; }
.pcard-rank { font-size:.65rem; font-weight:800; letter-spacing:2px; margin-bottom:3px; }
.pcard-name { font-weight:700; font-size:.8rem; margin:5px 0 3px; color:#fff; }
.pcard-pos  { font-size:.6rem; letter-spacing:2px; color:rgba(255,255,255,.5); background:rgba(0,0,0,.35); padding:1px 7px; border-radius:4px; }

/* STAT BAR */
.srow { display:flex; align-items:center; gap:9px; margin:4px 0; }
.slbl { width:34px; font-size:.7rem; color:var(--muted); text-align:right; font-weight:700; }
.sbg  { flex:1; height:7px; background:rgba(255,255,255,.05); border-radius:4px; overflow:hidden; }
.sfill{ height:100%; border-radius:4px; transition:width .6s ease; }
.sval { width:24px; font-size:.75rem; font-weight:700; color:#fff; }

/* UPGRADE BOX */
.upg-box {
  background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid var(--border); border-radius:13px;
  padding:16px; margin-bottom:10px; transition:border-color .2s;
}
.upg-box:hover { border-color:rgba(74,222,128,.35); }

/* PROGRESS BAR */
.prog-wrap { background:var(--dark); border-radius:7px; height:10px; overflow:hidden; border:1px solid var(--border); margin:8px 0; }
.prog-fill  { height:100%; border-radius:7px; transition:width .5s; position:relative; overflow:hidden; }
.prog-fill::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);
  animation:shine 1.6s linear infinite;
}
@keyframes shine { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }

/* RANK CARD */
.rank-card {
  border-radius:11px; padding:13px 8px; text-align:center; transition:all .2s;
}

/* ACHIEVEMENT */
.ach-card {
  background:var(--dark3); border:1px solid var(--border);
  border-radius:11px; padding:13px; margin-bottom:7px;
  display:flex; align-items:center; gap:12px;
}
.ach-card.done { border-color:rgba(255,215,0,.35); background:linear-gradient(135deg,rgba(255,215,0,.05),var(--dark3)); }
.ach-icon { font-size:1.8rem; min-width:36px; text-align:center; }
.ach-title{ font-family:'Bebas Neue',sans-serif; font-size:1rem; letter-spacing:1px; color:#fff; }
.ach-desc { font-size:.72rem; color:var(--muted); margin-top:1px; }
.ach-rew  { font-size:.68rem; color:var(--gold); margin-top:2px; font-weight:600; }
.ach-done { margin-left:auto; font-size:.7rem; font-weight:700; padding:3px 9px; border-radius:20px; white-space:nowrap; }
.st-done  { background:rgba(74,222,128,.15); color:#4ADE80; }
.st-lock  { background:rgba(255,255,255,.05); color:var(--muted); }

/* NOTIF */
.notif { background:rgba(74,222,128,.08); border:1px solid rgba(74,222,128,.2); border-radius:7px; padding:7px 12px; margin:2px 0; font-size:.78rem; color:#86EFAC; }

/* BOXES */
.info-box  { background:rgba(56,189,248,.07);  border:1px solid rgba(56,189,248,.2);  border-radius:9px; padding:11px 16px; margin:8px 0; color:#7DD3FC; font-size:.83rem; }
.warn-box  { background:rgba(251,191,36,.07);  border:1px solid rgba(251,191,36,.2);  border-radius:9px; padding:11px 16px; margin:8px 0; color:#FCD34D; font-size:.83rem; }
.succ-box  { background:rgba(74,222,128,.08);  border:1px solid rgba(74,222,128,.22); border-radius:9px; padding:11px 16px; margin:8px 0; color:#86EFAC; font-size:.83rem; }

/* SIDEBAR */
[data-testid="stSidebar"]{ background:var(--dark2) !important; border-right:1px solid var(--border); }
[data-testid="stSidebar"] *{ color:var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox>div>div{ background:var(--dark3) !important; border-color:var(--border) !important; }

/* INPUTS */
.stTextInput>div>div>input{ background:var(--dark3) !important; border-color:var(--border) !important; color:var(--text) !important; border-radius:8px !important; }
.stSelectbox>div>div{ background:var(--dark3) !important; border-color:var(--border) !important; color:var(--text) !important; }
label{ color:var(--muted) !important; font-size:.78rem !important; }

/* METRICS */
[data-testid="stMetric"]{ background:var(--dark3); border:1px solid var(--border); border-radius:9px; padding:11px 14px; }
[data-testid="stMetricValue"]{ font-family:'Orbitron',sans-serif !important; color:var(--gold) !important; font-size:1.1rem !important; }
[data-testid="stMetricLabel"]{ color:var(--muted) !important; font-size:.68rem !important; letter-spacing:1px; }

/* PACK OPEN RESULT BOX */
.result-box {
  border-radius:16px; padding:24px; text-align:center;
  margin-bottom:16px; position:relative; overflow:hidden;
}
.result-title { font-family:'Bebas Neue',sans-serif; font-size:2.2rem; letter-spacing:4px; }
.result-xp    { font-family:'Orbitron',sans-serif; font-size:1.4rem; font-weight:700; color:#4ADE80; }
.result-coins { font-family:'Orbitron',sans-serif; font-size:1.4rem; font-weight:700; color:#FFD700; }

/* RANK UP BOX */
.rankup-box {
  background:linear-gradient(135deg,rgba(255,215,0,.1),rgba(0,0,0,.95));
  border:2px solid var(--gold); border-radius:18px;
  padding:32px; text-align:center; margin-bottom:18px;
}
.rankup-title {
  font-family:'Bebas Neue',sans-serif; font-size:3.5rem;
  letter-spacing:8px; color:var(--gold);
  text-shadow:0 0 30px rgba(255,215,0,.6);
  animation:ru-bounce .6s cubic-bezier(.34,1.56,.64,1);
}
.rankup-ovr {
  font-family:'Bebas Neue',sans-serif; font-size:4rem; line-height:1;
}
@keyframes ru-bounce {
  0%{transform:scale(.3) translateY(40px);opacity:0}
  60%{transform:scale(1.1) translateY(-8px)}
  100%{transform:scale(1) translateY(0);opacity:1}
}

/* ITEM CARD */
.item-card {
  background:var(--dark3); border:1px solid var(--border);
  border-radius:10px; padding:12px 8px; text-align:center; margin-bottom:6px;
}
.item-icon { font-size:1.9rem; }
.item-name { font-size:.75rem; font-weight:700; margin-top:4px; }
.item-sub  { font-size:.65rem; color:var(--muted); margin-top:1px; }

hr { border-color:var(--border) !important; margin:14px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════

PLAYER = {
    "name":  "ULTIMATE STRIKER",
    "pos":   "ST",
    "club":  "FC Ultimate",
    "nation":"🌍",
    "base_ovr": 117,
    "max_ovr":  122,
    "age": 26, "height": "185 cm", "weight": "82 kg",
    "weak_foot": 5, "skill_moves": 5,
    "preferred_foot": "O'ng",
    "work_rate": "Yuqori / O'rta",
}

BASE_STATS = {
    "PAC": 96, "SHO": 97, "PAS": 94,
    "DRI": 98, "DEF": 72, "PHY": 95,
}

DETAIL_STATS = {
    "Tezlik": 96, "Tezlashtirish": 95,
    "Finishing": 98, "Penalties": 99, "Uzoq Zarba": 97,
    "Q.Uzatma": 95, "U.Uzatma": 93, "Ko'rish": 97,
    "Top Nazorat": 99, "Dribbling": 98, "Chapaqaylik": 89,
    "Sakrash": 94, "Kuch": 96, "Muvozanat": 93, "Tajovuz": 92,
}

RANKS = [
    {"ovr": 117, "name": "BASE",         "icon": "⚪", "color": "#9CA3AF", "xp_req": 0,     "bonus": "Boshlang'ich daraja",                   "stat_boost": {}},
    {"ovr": 118, "name": "SILVER STAR",  "icon": "⭐", "color": "#C0C0C0", "xp_req": 1000,  "bonus": "+1 PAC, +1 SHO",                        "stat_boost": {"PAC":1,"SHO":1}},
    {"ovr": 119, "name": "GOLD STAR",    "icon": "🌟", "color": "#FFD700", "xp_req": 2500,  "bonus": "+2 DRI, +1 PHY",                         "stat_boost": {"DRI":2,"PHY":1}},
    {"ovr": 120, "name": "ELITE",        "icon": "💎", "color": "#38BDF8", "xp_req": 5000,  "bonus": "+2 SHO, +2 PAS, +1 PAC",                "stat_boost": {"SHO":2,"PAS":2,"PAC":1}},
    {"ovr": 121, "name": "LEGEND",       "icon": "👑", "color": "#C084FC", "xp_req": 10000, "bonus": "+3 DRI, +2 SHO, +2 PHY",                "stat_boost": {"DRI":3,"SHO":2,"PHY":2}},
    {"ovr": 122, "name": "ULTIMATE ICON","icon": "🌠", "color": "#F87171", "xp_req": 20000, "bonus": "+2 PAC, +3 SHO, +2 PAS, +3 DRI, +2 PHY","stat_boost": {"PAC":2,"SHO":3,"PAS":2,"DRI":3,"PHY":2}},
]

PACKS = [
    {"id":"starter",   "name":"Starter Gold",     "emoji":"📦","style":"pack-gold",    "badge":"BEPUL","bcls":"b-free",  "desc":"Boshlang'ich oltin pack",       "count":3,  "xp":150,   "coins":5000,   "items":["xp_sm","coin_boost"]},
    {"id":"premium",   "name":"Premium Gold",      "emoji":"🌟","style":"pack-gold",    "badge":"BEPUL","bcls":"b-free",  "desc":"5 ta premium item",             "count":5,  "xp":350,   "coins":12000,  "items":["xp_md","stat_card"]},
    {"id":"elite",     "name":"Elite Pack",         "emoji":"⚡","style":"pack-elite",   "badge":"ELITE","bcls":"b-elite", "desc":"Elite XP + Stat boost",         "count":5,  "xp":800,   "coins":25000,  "items":["xp_lg","stat_card","stat_card"]},
    {"id":"rank",      "name":"Rank Boost Pack",    "emoji":"📈","style":"pack-elite",   "badge":"RANK", "bcls":"b-elite", "desc":"Katta XP + Rank up yordam",     "count":5,  "xp":1500,  "coins":40000,  "items":["xp_xl","stat_card","rank_token"]},
    {"id":"ucl",       "name":"Champions Pack",     "emoji":"⭐","style":"pack-ucl",     "badge":"UCL",  "bcls":"b-elite", "desc":"UCL maxsus paketi",             "count":6,  "xp":2000,  "coins":60000,  "items":["xp_xl","stat_card","stat_card","rank_token"]},
    {"id":"icon",      "name":"Icon Power Pack",    "emoji":"👑","style":"pack-icon",    "badge":"ICON", "bcls":"b-icon",  "desc":"ICON XP + Mega boost!",         "count":7,  "xp":4000,  "coins":100000, "items":["xp_mega","stat_card","stat_card","rank_token"]},
    {"id":"tots",      "name":"TOTS Mega Pack",      "emoji":"🏆","style":"pack-tots",    "badge":"TOTS", "bcls":"b-free",  "desc":"Team of the Season — max!",     "count":8,  "xp":5000,  "coins":120000, "items":["xp_mega","xp_xl","stat_card","rank_token","rank_token"]},
    {"id":"ultimate",  "name":"ULTIMATE PACK",      "emoji":"🌠","style":"pack-ultimate","badge":"ULTRA","bcls":"b-ult",   "desc":"MAKSIMAL mukofotlar!",          "count":10, "xp":10000, "coins":250000, "items":["xp_mega","xp_mega","stat_card","stat_card","rank_token","rank_token","rank_token"]},
]

ITEMS = {
    "xp_sm":      {"name":"XP Potion S",    "emoji":"🧪","xp":200,  "color":"#4ADE80"},
    "xp_md":      {"name":"XP Potion M",    "emoji":"⚗️", "xp":500,  "color":"#38BDF8"},
    "xp_lg":      {"name":"XP Potion L",    "emoji":"💊", "xp":1000, "color":"#60A5FA"},
    "xp_xl":      {"name":"XP Potion XL",   "emoji":"💉", "xp":2000, "color":"#818CF8"},
    "xp_mega":    {"name":"XP Mega Potion", "emoji":"🔮","xp":5000, "color":"#C084FC"},
    "stat_card":  {"name":"Stat Boost Card","emoji":"📊","xp":0,    "color":"#FFD700"},
    "rank_token": {"name":"Rank Token",     "emoji":"🏅","xp":500,  "color":"#F87171"},
    "coin_boost": {"name":"Coin Boost",     "emoji":"💰","xp":0,    "color":"#FCD34D"},
}

CLUB_UPGRADES = {
    "Stadium":         {"icon":"🏟️","desc":"Ko'proq Coins",    "max_lv":5,
        "levels":[{"name":"Mini Arena","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"City Ground","bonus":"+10% Coins","color":"#3B82F6"},
                  {"name":"National Arena","bonus":"+22% Coins","color":"#22C55E"},
                  {"name":"Grand Stadium","bonus":"+38% Coins","color":"#EAB308"},
                  {"name":"Elite Colosseum","bonus":"+55% Coins","color":"#F97316"},
                  {"name":"LEGENDARY DOME","bonus":"+80% + 5000XP","color":"#C084FC"}]},
    "Training Ground": {"icon":"🏋️","desc":"Ko'proq XP",       "max_lv":5,
        "levels":[{"name":"Basic Field","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"Youth Academy","bonus":"+12% XP","color":"#3B82F6"},
                  {"name":"Pro Center","bonus":"+25% XP","color":"#22C55E"},
                  {"name":"Elite Hub","bonus":"+40% XP","color":"#EAB308"},
                  {"name":"World Class","bonus":"+60% XP","color":"#F97316"},
                  {"name":"CHAMPIONS LAB","bonus":"+90% XP","color":"#C084FC"}]},
    "Scout Network":   {"icon":"🔭","desc":"Yaxshi items",      "max_lv":5,
        "levels":[{"name":"Local Scout","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"Regional Net","bonus":"+10% Pack","color":"#3B82F6"},
                  {"name":"Continental","bonus":"+22% Pack","color":"#22C55E"},
                  {"name":"Global Net","bonus":"+38% Pack","color":"#EAB308"},
                  {"name":"Elite Scouts","bonus":"+55% Pack","color":"#F97316"},
                  {"name":"LEGENDARY INTEL","bonus":"+80%+Token","color":"#C084FC"}]},
    "Medical Center":  {"icon":"🏥","desc":"Jarohatsizlik",     "max_lv":5,
        "levels":[{"name":"First Aid","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"Clinic","bonus":"-20% Injury","color":"#3B82F6"},
                  {"name":"Medical Hub","bonus":"-40% Injury","color":"#22C55E"},
                  {"name":"Sports Hospital","bonus":"-60% Injury","color":"#EAB308"},
                  {"name":"Recovery Lab","bonus":"-80% Injury","color":"#F97316"},
                  {"name":"BIO-TECH CENTER","bonus":"No Injuries!","color":"#C084FC"}]},
    "Fan Zone":        {"icon":"👥","desc":"Fan bonuslari",     "max_lv":5,
        "levels":[{"name":"Small Section","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"Fan Corner","bonus":"+15% Tokens","color":"#3B82F6"},
                  {"name":"Ultra Zone","bonus":"+30% Tokens","color":"#22C55E"},
                  {"name":"Supporter Club","bonus":"+50% Tokens","color":"#EAB308"},
                  {"name":"Global Fans","bonus":"+70% Tokens","color":"#F97316"},
                  {"name":"LEGEND FANBASE","bonus":"+100% Tokens","color":"#C084FC"}]},
    "Tech Lab":        {"icon":"💻","desc":"Taktik bonuslar",   "max_lv":5,
        "levels":[{"name":"Data Room","bonus":"Boshlang'ich","color":"#64748B"},
                  {"name":"Analysis Hub","bonus":"+10% Tactic","color":"#3B82F6"},
                  {"name":"AI Coaching","bonus":"+22% Tactic","color":"#22C55E"},
                  {"name":"VR Training","bonus":"+38% Tactic","color":"#EAB308"},
                  {"name":"Neural Engine","bonus":"+58% Tactic","color":"#F97316"},
                  {"name":"QUANTUM LAB","bonus":"+85% ALL","color":"#C084FC"}]},
}

ACHIEVEMENTS = [
    {"id":"first_open", "name":"Birinchi Pack",     "desc":"Birinchi packni oching",             "icon":"📦","xp":500},
    {"id":"open10",     "name":"Pack Enthusiast",   "desc":"10 ta pack oching",                  "icon":"⚡","xp":1000},
    {"id":"open50",     "name":"Pack Veteran",      "desc":"50 ta pack oching",                  "icon":"🏆","xp":3000},
    {"id":"open100",    "name":"Pack Legend",       "desc":"100 ta pack oching",                 "icon":"👑","xp":10000},
    {"id":"rank118",    "name":"First Upgrade",     "desc":"O'yinchini 118 ga olib chiqing",     "icon":"⭐","xp":2000},
    {"id":"rank119",    "name":"Rising Star",       "desc":"O'yinchini 119 ga olib chiqing",     "icon":"🌟","xp":4000},
    {"id":"rank120",    "name":"Elite Player",      "desc":"O'yinchini 120 ga olib chiqing",     "icon":"💎","xp":8000},
    {"id":"rank121",    "name":"Legend",            "desc":"O'yinchini 121 ga olib chiqing",     "icon":"👑","xp":15000},
    {"id":"rank122",    "name":"ULTIMATE ICON",     "desc":"O'yinchini 122 OVR MAX ga olib chiqing","icon":"🌠","xp":50000},
    {"id":"upg_one",    "name":"Builder",           "desc":"Bitta klub binosi yaxshilash",        "icon":"🏗️","xp":500},
    {"id":"upg_max",    "name":"FC Mogul",          "desc":"Barcha binolarni MAX ga olib chiqing","icon":"🏰","xp":20000},
    {"id":"items50",    "name":"Item Hoarder",      "desc":"50 ta item yig'ing",                  "icon":"🎒","xp":2000},
    {"id":"coins500k",  "name":"Millionaire",       "desc":"500,000 coin yig'ing",               "icon":"💰","xp":5000},
    {"id":"ultimate_p", "name":"Ultimate Opener",  "desc":"Ultimate Pack oching",               "icon":"🌠","xp":10000},
]

# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
def init():
    defs = {
        "coins": 999_999_999, "gems": 9_999_999,
        "tokens": 99_999, "fan_tokens": 999_999,
        "player_ovr": 117, "player_rank": 0,
        "player_xp": 0, "player_xp_total": 0,
        "player_stats": dict(BASE_STATS),
        "player_detail": dict(DETAIL_STATS),
        "club_name": "FC Ultimate", "club_badge": "🌠",
        "club_levels": {k: 0 for k in CLUB_UPGRADES},
        "club_rep": 5000,
        "inventory": [],
        "total_items": 0,
        "packs_opened": 0,
        "coins_earned": 0,
        "xp_earned": 0,
        "pack_history": [],
        "achievements": [],
        "notifications": [],
        # Pack animation state
        "show_result": False,
        "last_pack_id": None,
        "last_result": None,
        # Rank up state
        "show_rankup": False,
        "ru_old": 117, "ru_new": 118,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════
def add_notif(msg, icon="✅"):
    st.session_state.notifications.insert(0, f"{icon} {msg}")
    st.session_state.notifications = st.session_state.notifications[:12]

def stat_color(v):
    if v >= 95: return "#4ADE80"
    if v >= 85: return "#A3E635"
    if v >= 75: return "#FACC15"
    if v >= 65: return "#FB923C"
    return "#F87171"

def ovr_color(o):
    if o >= 122: return "#F87171"
    if o >= 121: return "#C084FC"
    if o >= 120: return "#38BDF8"
    if o >= 119: return "#FFD700"
    if o >= 118: return "#C0C0C0"
    return "#9CA3AF"

def pcard_class(rank_idx):
    return ["pcard-base","pcard-silver","pcard-gold","pcard-elite","pcard-legend","pcard-ultimate"][rank_idx]

def xp_needed():
    ri = st.session_state.player_rank
    if ri >= len(RANKS)-1: return 0
    return RANKS[ri+1]["xp_req"]

def xp_pct():
    n = xp_needed()
    if n == 0: return 100.0
    return min(100.0, st.session_state.player_xp / n * 100)

def can_rankup():
    ri = st.session_state.player_rank
    if ri >= len(RANKS)-1: return False
    return st.session_state.player_xp >= RANKS[ri+1]["xp_req"]

def grant(ach_id):
    if ach_id in st.session_state.achievements: return
    ach = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
    if not ach: return
    st.session_state.achievements.append(ach_id)
    st.session_state.player_xp      += ach["xp"]
    st.session_state.player_xp_total += ach["xp"]
    st.session_state.xp_earned       += ach["xp"]
    add_notif(f"ACHIEVEMENT: {ach['name']} +{ach['xp']:,} XP", "🏅")

def do_rankup():
    ri = st.session_state.player_rank
    old_ovr = st.session_state.player_ovr
    nr = RANKS[ri + 1]
    for stat, boost in nr["stat_boost"].items():
        if stat in st.session_state.player_stats:
            st.session_state.player_stats[stat] = min(99, st.session_state.player_stats[stat] + boost)
    st.session_state.player_xp   -= nr["xp_req"]
    if st.session_state.player_xp < 0: st.session_state.player_xp = 0
    st.session_state.player_rank  = ri + 1
    st.session_state.player_ovr   = nr["ovr"]
    st.session_state.club_rep    += 1000 * (ri + 2)
    st.session_state.show_rankup  = True
    st.session_state.ru_old = old_ovr
    st.session_state.ru_new = nr["ovr"]
    add_notif(f"RANK UP! {old_ovr} → {nr['ovr']} — {nr['name']} {nr['icon']}", "🏆")
    ach_map = {118:"rank118",119:"rank119",120:"rank120",121:"rank121",122:"rank122"}
    if nr["ovr"] in ach_map: grant(ach_map[nr["ovr"]])

def do_open_pack(pack_id):
    pack = next(p for p in PACKS if p["id"] == pack_id)
    tg_lv = st.session_state.club_levels.get("Training Ground", 0)
    xp_mult = [1.0,1.12,1.25,1.40,1.60,1.90][tg_lv]
    st_lv = st.session_state.club_levels.get("Stadium", 0)
    co_mult = [1.0,1.10,1.22,1.38,1.55,1.80][st_lv]

    total_xp    = int(pack["xp"] * xp_mult)
    total_coins = int(pack["coins"] * co_mult)
    items = list(pack["items"])

    # Scout bonus
    sc_lv = st.session_state.club_levels.get("Scout Network", 0)
    if sc_lv >= 3 and random.random() < .3: items.append("xp_md")
    if sc_lv >= 5 and random.random() < .2: items.append("rank_token")

    st.session_state.player_xp      += total_xp
    st.session_state.player_xp_total += total_xp
    st.session_state.xp_earned       += total_xp
    st.session_state.coins           += total_coins
    st.session_state.coins_earned    += total_coins
    st.session_state.packs_opened    += 1
    st.session_state.total_items     += len(items)

    for it in items:
        if it in ITEMS:
            st.session_state.inventory.append({"id": it, "ts": datetime.now().strftime("%H:%M")})

    st.session_state.pack_history.append({
        "pack_id": pack_id, "pack_name": pack["name"],
        "pack_emoji": pack["emoji"],
        "ts": datetime.now().strftime("%H:%M:%S"),
        "xp": total_xp, "coins": total_coins, "items": items,
    })

    # Achievements
    grant("first_open")
    n = st.session_state.packs_opened
    if n >= 10:  grant("open10")
    if n >= 50:  grant("open50")
    if n >= 100: grant("open100")
    if pack_id == "ultimate": grant("ultimate_p")
    if st.session_state.total_items >= 50: grant("items50")
    if st.session_state.coins_earned >= 500000: grant("coins500k")

    return {"xp": total_xp, "coins": total_coins, "items": items}

def use_item(item_id, idx):
    idef = ITEMS.get(item_id)
    if not idef: return
    if idef["xp"] > 0:
        tg = st.session_state.club_levels.get("Training Ground", 0)
        mult = [1.0,1.12,1.25,1.40,1.60,1.90][tg]
        gained = int(idef["xp"] * mult)
        st.session_state.player_xp      += gained
        st.session_state.player_xp_total += gained
        st.session_state.xp_earned       += gained
        add_notif(f"{idef['name']} ishlatildi! +{gained:,} XP", idef["emoji"])
    elif item_id == "stat_card":
        stats = list(BASE_STATS.keys())
        s = random.choice(stats)
        b = random.randint(1, 2)
        st.session_state.player_stats[s] = min(99, st.session_state.player_stats[s] + b)
        add_notif(f"Stat Card! +{b} {s}", "📊")
    elif item_id == "coin_boost":
        st.session_state.coins       += 50000
        st.session_state.coins_earned += 50000
        add_notif("Coin Boost! +50,000 Coins", "💰")
    st.session_state.inventory.pop(idx)

# ══════════════════════════════════════════════
# RENDER HELPERS (safe HTML — no random loops)
# ══════════════════════════════════════════════
def render_player_card_html(ovr, rank_idx):
    rank   = RANKS[rank_idx]
    color  = rank["color"]
    cls    = pcard_class(rank_idx)
    types  = ["BASE","SILVER","GOLD","ELITE","LEGEND","ULTIMATE"]
    rtype  = types[rank_idx]
    return f"""
<div class="pcard-big {cls}" style="border-color:{color};box-shadow:0 0 30px {color}44;">
  <div class="pcard-rank" style="color:{color};">{rank['icon']} {rtype}</div>
  <div class="pcard-ovr"  style="color:{color};filter:drop-shadow(0 0 12px {color}88);">{ovr}</div>
  <div class="pcard-name">ULTIMATE STRIKER</div>
  <div class="pcard-pos">ST</div>
  <div style="font-size:.75rem;color:rgba(255,255,255,.5);margin-top:6px;">
    🌍 &nbsp; {PLAYER['club']}
  </div>
</div>"""

def render_stat_bar(label, value):
    c = stat_color(value)
    return f"""
<div class="srow">
  <span class="slbl" style="color:{c};">{label}</span>
  <div class="sbg"><div class="sfill" style="width:{value}%;background:{c};"></div></div>
  <span class="sval" style="color:{c};">{value}</span>
</div>"""

def render_xp_bar_html(current_xp, needed_xp, rank_idx):
    if needed_xp == 0:
        pct = 100
    else:
        pct = min(100, current_xp / needed_xp * 100)
    ri = rank_idx
    c1 = RANKS[ri]["color"]
    c2 = RANKS[min(ri+1, len(RANKS)-1)]["color"]
    return f"""
<div style="margin:8px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
    <span style="font-size:.72rem;color:{c1};">{current_xp:,} XP</span>
    <span style="font-size:.72rem;color:rgba(255,255,255,.35);">{needed_xp:,} kerak</span>
  </div>
  <div class="prog-wrap">
    <div class="prog-fill" style="width:{pct:.1f}%;background:linear-gradient(90deg,{c1},{c2});
      box-shadow:0 0 8px {c1}77;">
    </div>
  </div>
</div>"""

# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    ri    = st.session_state.player_rank
    rank  = RANKS[ri]
    color = rank["color"]
    ovr   = st.session_state.player_ovr

    # Club badge + name
    st.markdown(f"""
<div style="background:linear-gradient(145deg,#0D1117,#1C2333);
  border:1px solid {color}33;border-radius:13px;
  padding:14px;text-align:center;margin-bottom:10px;">
  <div style="font-size:2.2rem;">{st.session_state.club_badge}</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
    color:#FFD700;letter-spacing:2px;">{st.session_state.club_name}</div>
  <div style="font-size:.72rem;color:rgba(255,255,255,.35);margin-top:2px;">
    ⭐ {st.session_state.club_rep:,} Reputation
  </div>
</div>""", unsafe_allow_html=True)

    # Player OVR widget
    st.markdown(f"""
<div style="background:linear-gradient(145deg,#0a0510,#150a25);
  border:2px solid {color};border-radius:12px;
  padding:12px;text-align:center;margin-bottom:10px;
  box-shadow:0 0 18px {color}44;">
  <div style="font-size:.62rem;letter-spacing:2px;color:{color};font-weight:800;">
    {rank['icon']} {rank['name']}
  </div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:3.5rem;
    color:{color};filter:drop-shadow(0 0 10px {color}77);line-height:1;margin:4px 0;">
    {ovr}
  </div>
  <div style="font-size:.72rem;color:rgba(255,255,255,.55);">
    ULTIMATE STRIKER &bull; ST
  </div>
</div>""", unsafe_allow_html=True)

    # XP Progress
    needed_xp = xp_needed()
    cur_xp    = st.session_state.player_xp
    pct       = xp_pct()

    if ri < len(RANKS) - 1:
        nr = RANKS[ri + 1]
        st.markdown(f"""
<div style="margin-bottom:10px;">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:.7rem;color:rgba(255,255,255,.4);">XP Progress</span>
    <span style="font-size:.7rem;color:{nr['color']};">→ {nr['name']}</span>
  </div>
  <div class="prog-wrap">
    <div class="prog-fill" style="width:{pct:.1f}%;
      background:linear-gradient(90deg,{color},{nr['color']});
      box-shadow:0 0 8px {color}88;">
    </div>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:2px;">
    <span style="font-size:.65rem;color:{color};">{cur_xp:,} XP</span>
    <span style="font-size:.65rem;color:rgba(255,255,255,.3);">{needed_xp:,} kerak</span>
  </div>
</div>""", unsafe_allow_html=True)

        if can_rankup():
            st.markdown(f"""
<div style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.4);
  border-radius:8px;padding:8px;text-align:center;margin-bottom:8px;">
  <span style="color:#FFD700;font-weight:700;font-size:.8rem;">🏆 RANK UP TAYYOR!</span>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.4);
  border-radius:8px;padding:8px;text-align:center;margin-bottom:8px;">
  <span style="color:#F87171;font-weight:700;font-size:.8rem;">🌠 MAX OVR 122!</span>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**⚙️ Klub Sozlamalari**")
    new_name = st.text_input("Klub nomi:", value=st.session_state.club_name, key="club_name_in")
    if new_name != st.session_state.club_name:
        st.session_state.club_name = new_name

    badges = ["🌠","⚽","🦁","🦅","🐉","⚡","🔥","💫","🌟","👑","🏆","⚔️","🛡️","💎","🌈","🌊"]
    sel = st.selectbox("Badge:", badges,
        index=badges.index(st.session_state.club_badge) if st.session_state.club_badge in badges else 0)
    st.session_state.club_badge = sel

    st.markdown("---")
    st.markdown("**📊 Quick Stats**")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Packs", st.session_state.packs_opened)
        st.metric("Items",  st.session_state.total_items)
    with c2:
        st.metric("XP",    f"{st.session_state.xp_earned:,}")
        st.metric("Ach",   len(st.session_state.achievements))

    st.markdown("---")
    st.markdown("**🔔 Xabarlar**")
    if st.session_state.notifications:
        for n in st.session_state.notifications[:5]:
            st.markdown(f"<div class='notif'>{n}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#7D8590;font-size:.78rem;'>Hali xabar yo'q</span>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown(f"""
<div class="fc-header">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
    <div>
      <div class="fc-title">⚽ EA FC MOBILE ULTIMATE</div>
      <div class="fc-sub">Pack Ochish • Rank Up 117→122 • Klub Rivojlantirish • Cheksiz Pul</div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
      <div style="background:rgba(255,215,0,.07);border:1px solid rgba(255,215,0,.2);border-radius:9px;padding:7px 14px;text-align:center;">
        <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#FFD700;font-weight:700;">∞</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.35);letter-spacing:1px;">COINS</div>
      </div>
      <div style="background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.2);border-radius:9px;padding:7px 14px;text-align:center;">
        <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#38BDF8;font-weight:700;">∞</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.35);letter-spacing:1px;">GEMS</div>
      </div>
      <div style="background:rgba(192,132,252,.07);border:1px solid rgba(192,132,252,.2);border-radius:9px;padding:7px 14px;text-align:center;">
        <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#C084FC;font-weight:700;">{st.session_state.packs_opened}</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.35);letter-spacing:1px;">PACKS</div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# RANK UP BANNER (shown when triggered)
# ══════════════════════════════════════════════
if st.session_state.show_rankup:
    ri2   = st.session_state.player_rank
    rnk   = RANKS[ri2]
    color2 = rnk["color"]
    old_o = st.session_state.ru_old
    new_o = st.session_state.ru_new

    # Stars row
    stars = "⭐ " * min(ri2, 5)

    stat_chips = ""
    for stat, boost in rnk.get("stat_boost", {}).items():
        stat_chips += f'<span style="background:rgba(255,255,255,.08);border:1px solid {color2}44;border-radius:5px;padding:2px 9px;font-size:.72rem;color:{color2};font-weight:700;">+{boost} {stat}</span> '

    st.markdown(f"""
<div class="rankup-box" style="border-color:{color2};
  background:linear-gradient(135deg,rgba(0,0,0,.97),rgba(20,10,5,.97));
  box-shadow:0 0 40px {color2}33;">
  <div style="font-size:1.8rem;margin-bottom:6px;">{stars}</div>
  <div class="rankup-title" style="color:{color2};text-shadow:0 0 30px {color2}77;">
    RANK UP!
  </div>
  <div style="font-family:'Orbitron',sans-serif;font-size:.9rem;
    color:{color2};letter-spacing:4px;margin:8px 0;">
    {rnk['icon']} {rnk['name']}
  </div>
  <div style="display:flex;align-items:center;justify-content:center;gap:14px;margin:16px 0;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;
      color:rgba(255,255,255,.25);text-decoration:line-through;">{old_o}</div>
    <div style="font-size:1.8rem;color:{color2};">➜</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4.5rem;
      color:{color2};filter:drop-shadow(0 0 18px {color2}88);line-height:1;">{new_o}</div>
  </div>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin:8px 0;">
    {stat_chips}
  </div>
  <div style="font-size:.8rem;color:rgba(255,255,255,.45);margin-top:6px;">
    {rnk.get('bonus','')}
  </div>
</div>""", unsafe_allow_html=True)

    c_close = st.columns([1,1,1])[1]
    with c_close:
        if st.button("✖ Yopish", key="close_rankup_btn"):
            st.session_state.show_rankup = False
            st.rerun()
    st.markdown("---")

# ══════════════════════════════════════════════
# PACK RESULT BANNER
# ══════════════════════════════════════════════
if st.session_state.show_result and st.session_state.last_result:
    res  = st.session_state.last_result
    pid  = st.session_state.last_pack_id
    pack = next((p for p in PACKS if p["id"] == pid), PACKS[0])

    style_colors = {
        "pack-gold":"#FFD700","pack-elite":"#38BDF8","pack-icon":"#C084FC",
        "pack-ultimate":"#F87171","pack-ucl":"#60A5FA","pack-tots":"#4ADE80",
    }
    ac = style_colors.get(pack["style"], "#FFD700")

    # Items HTML — plain divs, no f-string loops generating HTML
    items_html_parts = []
    for it_id in res["items"]:
        idef = ITEMS.get(it_id, {"name": it_id, "emoji": "❓", "color": "#888", "xp": 0})
        xp_txt = f"+{idef['xp']:,} XP" if idef["xp"] > 0 else idef["name"]
        items_html_parts.append(
            f'<div style="background:rgba(0,0,0,.45);border:1px solid {idef["color"]}33;'
            f'border-radius:9px;padding:10px 12px;text-align:center;min-width:80px;">'
            f'<div style="font-size:1.8rem;">{idef["emoji"]}</div>'
            f'<div style="font-size:.68rem;color:{idef["color"]};font-weight:700;margin-top:4px;">{idef["name"]}</div>'
            f'<div style="font-size:.62rem;color:rgba(255,255,255,.4);">{xp_txt}</div>'
            f'</div>'
        )
    items_html = "".join(items_html_parts)

    st.markdown(f"""
<div style="background:linear-gradient(145deg,#06090F,#0D1117);
  border:2px solid {ac};border-radius:16px;padding:24px;
  text-align:center;margin-bottom:16px;
  box-shadow:0 0 30px {ac}33;">
  <div style="font-size:3.5rem;margin-bottom:6px;">{pack['emoji']}</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
    letter-spacing:3px;color:{ac};margin-bottom:14px;">
    {pack['name']} — OCHILDI!
  </div>
  <div style="display:flex;justify-content:center;gap:16px;margin-bottom:16px;flex-wrap:wrap;">
    <div style="background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);
      border-radius:10px;padding:10px 20px;">
      <div style="font-family:'Orbitron',sans-serif;font-size:1.3rem;
        color:#4ADE80;font-weight:700;">+{res['xp']:,}</div>
      <div style="font-size:.65rem;color:#6EE7B7;letter-spacing:1px;">XP</div>
    </div>
    <div style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);
      border-radius:10px;padding:10px 20px;">
      <div style="font-family:'Orbitron',sans-serif;font-size:1.3rem;
        color:#FFD700;font-weight:700;">+{res['coins']:,}</div>
      <div style="font-size:.65rem;color:#FCD34D;letter-spacing:1px;">COINS</div>
    </div>
  </div>
  <div style="font-size:.68rem;color:rgba(255,255,255,.35);letter-spacing:2px;
    text-transform:uppercase;margin-bottom:10px;">ITEMS OLINDI</div>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px;">
    {items_html}
  </div>
</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("✖ Yopish", key="close_result_btn"):
            st.session_state.show_result = False
            st.session_state.last_result = None
            st.rerun()
    st.markdown("---")

# ══════════════════════════════════════════════
# RANK UP PROMPT BAR
# ══════════════════════════════════════════════
if can_rankup() and not st.session_state.show_result and not st.session_state.show_rankup:
    ri3  = st.session_state.player_rank
    nr3  = RANKS[ri3 + 1]
    c_ru = st.columns([2,1,2])
    st.markdown(f"""
<div style="background:rgba(255,215,0,.08);border:2px solid rgba(255,215,0,.4);
  border-radius:12px;padding:12px 20px;margin-bottom:14px;
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
  <div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
      color:#FFD700;letter-spacing:2px;">🏆 RANK UP TAYYOR!</div>
    <div style="font-size:.8rem;color:rgba(255,215,0,.6);">
      OVR {st.session_state.player_ovr} → {nr3['ovr']} · {nr3['icon']} {nr3['name']}
    </div>
  </div>
</div>""", unsafe_allow_html=True)
    with c_ru[1]:
        if st.button(f"🚀 RANK UP!", key="ru_prompt_btn"):
            do_rankup()
            st.rerun()

# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📦 PACK OCHISH",
    "⚡ O'YINCHI & RANK UP",
    "🏟️ KLUB",
    "🎒 INVENTAR",
    "📊 STATISTIKA",
    "🏅 YUTUQLAR",
])

# ══════════════════════════════════════════════
# TAB 1 — PACK OCHISH
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">📦 PACK DO\'KONI</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="succ-box">
  💡 <strong>Barcha packlar BEPUL!</strong> XP, Coins va itemlar to'plang.
  O'yinchingizni 117 dan 122 OVR ga rank up qiling!
</div>""", unsafe_allow_html=True)

    # 4-column grid
    for row in range(0, len(PACKS), 4):
        row_packs = PACKS[row:row+4]
        cols = st.columns(4)
        for i, pack in enumerate(row_packs):
            with cols[i]:
                ac2 = {"pack-gold":"#FFD700","pack-elite":"#38BDF8","pack-icon":"#C084FC",
                       "pack-ultimate":"#F87171","pack-ucl":"#60A5FA","pack-tots":"#4ADE80"}.get(pack["style"],"#FFD700")
                tg = st.session_state.club_levels.get("Training Ground", 0)
                xp_show = int(pack["xp"] * [1.0,1.12,1.25,1.40,1.60,1.90][tg])

                st.markdown(f"""
<div class="pack-card {pack['style']}">
  <span class="pack-badge {pack['bcls']}">{pack['badge']}</span>
  <div class="pack-emoji">{pack['emoji']}</div>
  <div class="pack-title" style="color:{ac2};">{pack['name']}</div>
  <div class="pack-desc">{pack['desc']}</div>
  <div style="font-size:.7rem;color:#4ADE80;font-weight:600;">
    +{xp_show:,} XP &nbsp;&bull;&nbsp; +{pack['coins']:,} 🪙
  </div>
  <div style="font-size:.68rem;color:rgba(255,255,255,.35);">{pack['count']} item</div>
</div>""", unsafe_allow_html=True)

                if st.button(f"▶ OCHISH", key=f"open_{pack['id']}_{row}"):
                    result = do_open_pack(pack["id"])
                    st.session_state.show_result  = True
                    st.session_state.last_pack_id = pack["id"]
                    st.session_state.last_result  = result
                    if can_rankup():
                        pass  # Prompt will appear automatically
                    st.rerun()

    # Pack history
    if st.session_state.pack_history:
        st.markdown("---")
        st.markdown('<div class="sec-head">📜 PACK TARIXI</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("📦 Jami Pack",  st.session_state.packs_opened)
        with m2: st.metric("⚡ Jami XP",    f"{st.session_state.xp_earned:,}")
        with m3: st.metric("💰 Jami Coins", f"{st.session_state.coins_earned:,}")
        with m4: st.metric("🎒 Jami Items", st.session_state.total_items)

        st.markdown("#### Son 10 ta Pack")
        for rec in reversed(st.session_state.pack_history[-10:]):
            p2 = next((x for x in PACKS if x["id"] == rec["pack_id"]), None)
            if not p2: continue
            c3 = {"pack-gold":"#FFD700","pack-elite":"#38BDF8","pack-icon":"#C084FC",
                  "pack-ultimate":"#F87171","pack-ucl":"#60A5FA","pack-tots":"#4ADE80"}.get(p2["style"],"#888")
            item_emojis = " ".join(ITEMS.get(it, {}).get("emoji","❓") for it in rec["items"])
            st.markdown(f"""
<div style="background:var(--dark3);border:1px solid {c3}22;border-radius:9px;
  padding:9px 14px;margin:3px 0;
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
  <div style="display:flex;align-items:center;gap:9px;">
    <span style="font-size:1.2rem;">{p2['emoji']}</span>
    <div>
      <div style="font-size:.83rem;font-weight:600;color:{c3};">{rec['pack_name']}</div>
      <div style="font-size:.68rem;color:rgba(255,255,255,.35);">{rec['ts']}</div>
    </div>
  </div>
  <div style="display:flex;gap:14px;align-items:center;">
    <span style="font-size:.78rem;color:#4ADE80;">+{rec['xp']:,} XP</span>
    <span style="font-size:.78rem;color:#FFD700;">+{rec['coins']:,} 🪙</span>
    <span style="font-size:.95rem;">{item_emojis}</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — O'YINCHI & RANK UP
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">⚡ O\'YINCHI PROFILI</div>', unsafe_allow_html=True)

    cl, cm, cr = st.columns([1, 1.1, 1])

    with cm:
        st.markdown(render_player_card_html(
            st.session_state.player_ovr,
            st.session_state.player_rank
        ), unsafe_allow_html=True)

        ri_now = st.session_state.player_rank
        rnk_now = RANKS[ri_now]
        co_now  = rnk_now["color"]

        st.markdown(f"""
<div style="background:var(--dark3);border:1px solid var(--border);
  border-radius:11px;padding:14px;margin-top:12px;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
    <div><span style="font-size:.68rem;color:var(--muted);">Pozitsiya</span><div style="font-weight:700;">{PLAYER['pos']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Millat</span><div style="font-weight:700;">🌍 World</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Yosh</span><div style="font-weight:700;">{PLAYER['age']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Boy</span><div style="font-weight:700;">{PLAYER['height']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Oyoq</span><div style="font-weight:700;">{PLAYER['preferred_foot']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Skill</span><div style="font-weight:700;">{'⭐'*PLAYER['skill_moves']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Weak Foot</span><div style="font-weight:700;">{'⭐'*PLAYER['weak_foot']}</div></div>
    <div><span style="font-size:.68rem;color:var(--muted);">Work Rate</span><div style="font-size:.78rem;font-weight:700;">{PLAYER['work_rate']}</div></div>
  </div>
</div>""", unsafe_allow_html=True)

    with cl:
        st.markdown("#### 📊 Asosiy Statlar")
        stats_html = "".join(
            render_stat_bar(k, st.session_state.player_stats[k])
            for k in BASE_STATS
        )
        st.markdown(stats_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🏅 Rank Yo'li")
        for i, r in enumerate(RANKS):
            done    = i <= st.session_state.player_rank
            current = i == st.session_state.player_rank
            c_r     = r["color"]
            brd     = f"border:2px solid {c_r}" if current else \
                      f"border:1px solid {c_r}44" if done else \
                       "border:1px solid var(--border)"
            bg_r    = f"background:rgba(30,20,5,.6)" if done else "background:var(--dark3)"
            flt     = "" if done else "filter:grayscale(.65);"
            st.markdown(f"""
<div style="{bg_r};{brd};border-radius:8px;padding:8px 11px;margin:3px 0;
  display:flex;align-items:center;gap:9px;{flt}">
  <span style="font-size:1.1rem;">{r['icon']}</span>
  <div style="flex:1;">
    <div style="font-weight:700;font-size:.82rem;color:{'#fff' if done else 'var(--muted)'};">{r['name']}</div>
    <div style="font-size:.62rem;color:rgba(255,255,255,.35);">OVR {r['ovr']}</div>
  </div>
  <div style="font-size:.75rem;font-weight:700;color:{c_r};">
    {'✅' if done and not current else ('▶' if current else '🔒')}
  </div>
</div>""", unsafe_allow_html=True)

    with cr:
        st.markdown("#### ⭐ To'liq Statlar")
        for sname, sval in st.session_state.player_detail.items():
            c4 = stat_color(sval)
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:7px;margin:3px 0;">
  <span style="width:90px;font-size:.68rem;color:rgba(255,255,255,.45);
    text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{sname}</span>
  <div style="flex:1;background:rgba(255,255,255,.04);border-radius:3px;height:6px;overflow:hidden;">
    <div style="width:{min(100,sval)}%;height:100%;background:{c4};border-radius:3px;"></div>
  </div>
  <span style="width:22px;font-size:.73rem;font-weight:700;color:{c4};">{sval}</span>
</div>""", unsafe_allow_html=True)

    # ── RANK UP SECTION ──
    st.markdown("---")
    st.markdown('<div class="sec-head">🚀 RANK UP TIZIMI</div>', unsafe_allow_html=True)

    rank_cols = st.columns(len(RANKS))
    for i, r in enumerate(RANKS):
        with rank_cols[i]:
            done    = i <= st.session_state.player_rank
            current = i == st.session_state.player_rank
            c_r     = r["color"]
            brd     = f"2px solid {c_r}" if current else f"1px solid {c_r}44" if done else "1px solid var(--border)"
            bg_rk   = f"linear-gradient(145deg,rgba(30,20,5,.9),rgba(0,0,0,.9))" if done else "var(--dark3)"
            glt     = f"box-shadow:0 0 18px {c_r}44" if current else ""
            flt2    = "" if done else "opacity:.45;filter:grayscale(.6);"

            xp_t = "—" if i == 0 else f"{r['xp_req']:,} XP"
            st.markdown(f"""
<div class="rank-card" style="background:{bg_rk};border:{brd};{glt};{flt2}">
  <div style="font-size:1.5rem;">{r['icon']}</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;
    color:{c_r};line-height:1;filter:drop-shadow(0 0 6px {c_r}66);">{r['ovr']}</div>
  <div style="font-size:.65rem;color:{c_r};font-weight:700;letter-spacing:1px;margin:3px 0;">{r['name']}</div>
  <div style="font-size:.6rem;color:rgba(255,255,255,.35);">{xp_t}</div>
  <div style="font-size:.6rem;color:rgba(255,255,255,.55);margin-top:4px;line-height:1.3;">{r['bonus'][:30]}{'...' if len(r['bonus'])>30 else ''}</div>
  {'<div style="color:#4ADE80;font-size:.65rem;margin-top:5px;font-weight:700;">✅ OLINGAN</div>' if done and not current else ''}
  {'<div style="color:'+c_r+';font-size:.65rem;margin-top:5px;font-weight:700;">▶ JORIY</div>' if current else ''}
</div>""", unsafe_allow_html=True)

    # Rank up button zone
    st.markdown("---")
    ri4    = st.session_state.player_rank
    xp_hv  = st.session_state.player_xp
    xp_nd  = xp_needed()
    pct4   = xp_pct()

    r_c1, r_c2, r_c3 = st.columns([1,2,1])
    with r_c2:
        if ri4 < len(RANKS) - 1:
            nr4   = RANKS[ri4 + 1]
            c4_nr = nr4["color"]
            remaining = max(0, xp_nd - xp_hv)
            st.markdown(f"""
<div style="background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid {c4_nr}44;border-radius:13px;padding:18px;text-align:center;">
  <div style="font-size:.75rem;color:rgba(255,255,255,.35);letter-spacing:2px;margin-bottom:3px;">
    KEYINGI RANK
  </div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{c4_nr};">
    {nr4['icon']} {nr4['name']} — OVR {nr4['ovr']}
  </div>
  <div style="font-size:.78rem;color:rgba(255,255,255,.45);margin:6px 0;">
    {nr4['bonus']}
  </div>
  {render_xp_bar_html(xp_hv, xp_nd, ri4)}
</div>""", unsafe_allow_html=True)

            if can_rankup():
                if st.button(f"🚀 RANK UP! ({st.session_state.player_ovr} → {nr4['ovr']})", key="rankup_main_btn"):
                    do_rankup()
                    st.rerun()
            else:
                st.markdown(f"""
<div class="info-box">
  📊 Rank up uchun yana <strong>{remaining:,} XP</strong> kerak.
  Pack oching yoki Inventardagi itemlarni ishlating!
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:rgba(248,113,113,.1);border:2px solid #F87171;
  border-radius:13px;padding:24px;text-align:center;">
  <div style="font-size:2.5rem;">🌠</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
    color:#F87171;letter-spacing:3px;margin-top:8px;">ULTIMATE ICON!</div>
  <div style="color:rgba(255,255,255,.55);margin-top:6px;">
    Eng yuqori daraja — OVR 122!
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — KLUB
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">🏟️ KLUB RIVOJLANTIRISH</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="succ-box">
  💡 Barcha yaxshilanishlar <strong>BEPUL</strong>!
  Training Ground XP ni, Stadium Coinlarni, Scout Pack sifatini oshiradi.
</div>""", unsafe_allow_html=True)

    # Overview
    tot_lv = sum(st.session_state.club_levels.values())
    max_lv = len(CLUB_UPGRADES) * 5
    ov_pct = tot_lv / max_lv * 100 if max_lv else 0

    st.markdown(f"""
<div style="background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid rgba(192,132,252,.25);border-radius:13px;
  padding:18px;margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;
        letter-spacing:2px;color:#C084FC;">🏰 KLUB RIVOJLANISH</div>
      <div style="font-size:.75rem;color:rgba(255,255,255,.35);">
        ⭐ {st.session_state.club_rep:,} Reputation
      </div>
    </div>
    <div style="font-family:'Orbitron',sans-serif;font-size:1.5rem;
      color:#FFD700;font-weight:700;">{tot_lv}/{max_lv}</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-fill" style="width:{ov_pct:.1f}%;
      background:linear-gradient(90deg,#7C3AED,#C084FC);
      box-shadow:0 0 8px rgba(192,132,252,.5);">
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    upg_cols = st.columns(2)
    for idx, (upg_name, upg_data) in enumerate(CLUB_UPGRADES.items()):
        with upg_cols[idx % 2]:
            cur_lv = st.session_state.club_levels[upg_name]
            max_lv2 = upg_data["max_lv"]
            lv_d   = upg_data["levels"][cur_lv]
            lv_c   = lv_d["color"]
            lv_pct = cur_lv / max_lv2 * 100
            nxt    = upg_data["levels"][cur_lv + 1] if cur_lv < max_lv2 else None

            # hex→rgb for rgba usage
            try:
                hr = lv_c.lstrip("#")
                rgb = f"{int(hr[0:2],16)},{int(hr[2:4],16)},{int(hr[4:6],16)}"
            except Exception:
                rgb = "100,100,100"

            st.markdown(f"""
<div class="upg-box" style="border-color:{lv_c}22;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
    <div>
      <div style="font-size:1.5rem;">{upg_data['icon']}</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;
        letter-spacing:1.5px;color:#fff;">{upg_name}</div>
      <div style="font-size:.72rem;color:rgba(255,255,255,.38);">{upg_data['desc']}</div>
    </div>
    <div style="background:rgba({rgb},.1);color:{lv_c};
      border:1px solid {lv_c}44;border-radius:20px;
      font-family:'Orbitron',sans-serif;font-size:.7rem;font-weight:700;
      padding:3px 10px;">LVL {cur_lv}/{max_lv2}</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-fill" style="width:{lv_pct:.0f}%;background:{lv_c};
      box-shadow:0 0 6px {lv_c}77;"></div>
  </div>
  <div style="background:rgba(74,222,128,.07);border:1px solid rgba(74,222,128,.18);
    border-radius:7px;padding:6px 10px;font-size:.78rem;color:#4ADE80;margin-top:6px;">
    ✅ Joriy: <strong>{lv_d['name']}</strong> — {lv_d['bonus']}
  </div>
  {f'<div style="background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:7px;padding:6px 10px;font-size:.75rem;color:#38BDF8;margin-top:4px;">➡ Keyingi: <strong>{nxt["name"]}</strong> — {nxt["bonus"]}</div>' if nxt else ''}
</div>""", unsafe_allow_html=True)

            if cur_lv < max_lv2:
                if st.button(f"⬆ Yaxshilash", key=f"upg_{upg_name}"):
                    st.session_state.club_levels[upg_name] += 1
                    new_lv2 = st.session_state.club_levels[upg_name]
                    new_d   = CLUB_UPGRADES[upg_name]["levels"][new_lv2]
                    st.session_state.club_rep += 300 * new_lv2
                    add_notif(f"{upg_name} LVL {new_lv2}! {new_d['bonus']}", "🏗️")
                    grant("upg_one")
                    if all(v >= 5 for v in st.session_state.club_levels.values()):
                        grant("upg_max")
                    st.rerun()
            else:
                st.markdown(f"""
<div style="background:rgba({rgb},.1);border:1px solid {lv_c}44;
  border-radius:8px;padding:7px;text-align:center;
  font-family:'Bebas Neue',sans-serif;font-size:.88rem;
  letter-spacing:1px;color:{lv_c};">🏆 MAX DARAJA!</div>""", unsafe_allow_html=True)

    # Active bonuses
    st.markdown("---")
    st.markdown('<div class="sec-head">🎁 FAOL BONUSLAR</div>', unsafe_allow_html=True)
    ab_list = [(upg_data["icon"], upg_name,
                upg_data["levels"][st.session_state.club_levels[upg_name]]["name"],
                upg_data["levels"][st.session_state.club_levels[upg_name]]["bonus"],
                upg_data["levels"][st.session_state.club_levels[upg_name]]["color"])
               for upg_name, upg_data in CLUB_UPGRADES.items()
               if st.session_state.club_levels[upg_name] > 0]

    if ab_list:
        ab_cols = st.columns(3)
        for i, (icon, name, lv_name, bonus, c5) in enumerate(ab_list):
            try:
                hr2 = c5.lstrip("#")
                rgb2 = f"{int(hr2[0:2],16)},{int(hr2[2:4],16)},{int(hr2[4:6],16)}"
            except Exception:
                rgb2 = "100,100,100"
            with ab_cols[i % 3]:
                st.markdown(f"""
<div style="background:rgba({rgb2},.07);border:1px solid {c5}33;
  border-radius:9px;padding:11px;margin-bottom:7px;">
  <div style="font-size:1.2rem;">{icon} <span style="font-size:.82rem;font-weight:700;">{name}</span></div>
  <div style="font-size:.72rem;color:rgba(255,255,255,.38);">{lv_name}</div>
  <div style="font-size:.82rem;color:{c5};font-weight:700;margin-top:3px;">{bonus}</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Hali bonus yo\'q. Binolarni yaxshilang!</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — INVENTAR
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">🎒 INVENTAR</div>', unsafe_allow_html=True)
    inv = st.session_state.inventory

    if not inv:
        st.markdown("""
<div style="text-align:center;padding:50px 20px;color:rgba(255,255,255,.3);">
  <div style="font-size:3rem;">📭</div>
  <div style="font-size:1rem;margin-top:10px;">Inventar bo'sh. Pack oching!</div>
</div>""", unsafe_allow_html=True)
    else:
        # Summary
        counts = {}
        for it in inv: counts[it["id"]] = counts.get(it["id"], 0) + 1
        s_cols = st.columns(min(len(counts), 4))
        for i, (iid, cnt) in enumerate(counts.items()):
            idef = ITEMS.get(iid, {"name": iid, "emoji": "❓", "color": "#888"})
            try:
                hr3 = idef["color"].lstrip("#")
                rgb3 = f"{int(hr3[0:2],16)},{int(hr3[2:4],16)},{int(hr3[4:6],16)}"
            except Exception:
                rgb3 = "100,100,100"
            with s_cols[i % min(len(counts), 4)]:
                st.markdown(f"""
<div style="background:rgba({rgb3},.07);border:1px solid {idef['color']}33;
  border-radius:9px;padding:11px;text-align:center;margin-bottom:8px;">
  <div style="font-size:1.8rem;">{idef['emoji']}</div>
  <div style="font-size:.72rem;font-weight:700;color:{idef['color']};margin-top:3px;">{idef['name']}</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#fff;font-weight:700;">×{cnt}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"#### 📋 Barcha Itemlar ({len(inv)} ta)")

        i_cols = st.columns(4)
        for slot_idx, item in enumerate(inv):
            idef = ITEMS.get(item["id"], {"name": item["id"], "emoji": "❓", "color": "#888", "xp": 0})
            with i_cols[slot_idx % 4]:
                st.markdown(f"""
<div class="item-card" style="border-color:{idef['color']}33;">
  <div class="item-icon">{idef['emoji']}</div>
  <div class="item-name" style="color:{idef['color']};">{idef['name']}</div>
  <div class="item-sub">{item['ts']}</div>
  {f'<div style="font-size:.65rem;color:#4ADE80;margin-top:2px;">+{idef["xp"]:,} XP</div>' if idef.get("xp",0) > 0 else ''}
</div>""", unsafe_allow_html=True)
                if st.button("▶ Ishlatish", key=f"use_{slot_idx}"):
                    use_item(item["id"], slot_idx)
                    st.rerun()

# ══════════════════════════════════════════════
# TAB 5 — STATISTIKA
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-head">📊 TO\'LIQ STATISTIKA</div>', unsafe_allow_html=True)

    m1,m2,m3,m4 = st.columns(4)
    with m1: st.metric("📦 Packs",  st.session_state.packs_opened)
    with m2: st.metric("⚡ XP",     f"{st.session_state.xp_earned:,}")
    with m3: st.metric("💰 Coins",  f"{st.session_state.coins_earned:,}")
    with m4: st.metric("🏅 Ach",    len(st.session_state.achievements))

    m5,m6,m7,m8 = st.columns(4)
    with m5: st.metric("🎒 Items",   st.session_state.total_items)
    with m6: st.metric("⚽ OVR",    st.session_state.player_ovr)
    with m7: st.metric("🏟️ Upgrades",sum(st.session_state.club_levels.values()))
    with m8: st.metric("⭐ Rep",    f"{st.session_state.club_rep:,}")

    st.markdown("---")
    sc1, sc2 = st.columns(2)

    with sc1:
        st.markdown("#### 🎯 Stat O'sishi (Base vs Hozir)")
        for sname, base_val in BASE_STATS.items():
            cur_val = st.session_state.player_stats[sname]
            boost   = cur_val - base_val
            c6      = stat_color(cur_val)
            st.markdown(f"""
<div style="margin:7px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
    <span style="font-size:.78rem;font-weight:700;">{sname}</span>
    <div>
      <span style="font-size:.72rem;color:rgba(255,255,255,.35);">{base_val} → </span>
      <span style="font-size:.83rem;font-weight:700;color:{c6};">{cur_val}</span>
      {f'<span style="font-size:.68rem;color:#4ADE80;margin-left:4px;">+{boost}</span>' if boost>0 else ''}
    </div>
  </div>
  <div style="display:flex;height:8px;border-radius:4px;overflow:hidden;">
    <div style="flex:{base_val};background:#3B82F666;"></div>
    <div style="flex:{boost if boost>0 else 0};background:#4ADE80;"></div>
    <div style="flex:{100-cur_val};background:rgba(255,255,255,.03);"></div>
  </div>
</div>""", unsafe_allow_html=True)

    with sc2:
        st.markdown("#### 🏟️ Klub Rivojlanish")
        for upg_name2, upg_data2 in CLUB_UPGRADES.items():
            lv2 = st.session_state.club_levels[upg_name2]
            lv_d2 = upg_data2["levels"][lv2]
            pct2  = lv2 / upg_data2["max_lv"] * 100
            c7    = lv_d2["color"]
            st.markdown(f"""
<div style="margin:6px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
    <span style="font-size:.78rem;">{upg_data2['icon']} {upg_name2}</span>
    <span style="font-size:.72rem;color:{c7};font-weight:700;">LVL {lv2}/{upg_data2['max_lv']}</span>
  </div>
  <div style="background:rgba(255,255,255,.04);border-radius:5px;height:9px;overflow:hidden;">
    <div style="width:{pct2:.0f}%;height:100%;background:{c7};border-radius:5px;box-shadow:0 0 5px {c7}66;"></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🚀 Max Darajaga Masofa")

    ri5 = st.session_state.player_rank
    if ri5 < len(RANKS) - 1:
        xp_hv2 = st.session_state.player_xp
        remaining_total = sum(RANKS[i]["xp_req"] for i in range(ri5+1, len(RANKS))) - xp_hv2
        remaining_total = max(0, remaining_total)

        st.markdown(f"""
<div style="background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid rgba(248,113,113,.25);border-radius:13px;padding:18px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
    <div>
      <div style="font-size:.75rem;color:rgba(255,255,255,.35);">OVR 122'ga</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#F87171;">
        {remaining_total:,} XP kerak
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:.72rem;color:rgba(255,255,255,.35);">Joriy</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#FFD700;">
        {RANKS[ri5]['name']}
      </div>
    </div>
  </div>""", unsafe_allow_html=True)

        for i in range(ri5+1, len(RANKS)):
            r8  = RANKS[i]
            pct8 = min(100.0, st.session_state.player_xp / r8["xp_req"] * 100) if i == ri5+1 else 0
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
  <span style="font-size:.95rem;">{r8['icon']}</span>
  <div style="flex:1;">
    <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
      <span style="font-size:.72rem;color:{r8['color']};">{r8['name']}</span>
      <span style="font-size:.68rem;color:rgba(255,255,255,.35);">{r8['xp_req']:,} XP</span>
    </div>
    <div style="background:rgba(255,255,255,.04);border-radius:4px;height:7px;overflow:hidden;">
      <div style="width:{pct8:.0f}%;height:100%;background:{r8['color']};border-radius:4px;"></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="background:rgba(248,113,113,.08);border:2px solid #F87171;
  border-radius:12px;padding:20px;text-align:center;">
  <div style="font-size:2rem;">🌠</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#F87171;margin-top:6px;">
    OVR 122 — ULTIMATE ICON!
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 6 — YUTUQLAR
# ══════════════════════════════════════════════
with tab6:
    st.markdown('<div class="sec-head">🏅 YUTUQLAR</div>', unsafe_allow_html=True)

    u_cnt = len(st.session_state.achievements)
    t_cnt = len(ACHIEVEMENTS)
    a_pct = u_cnt / t_cnt * 100 if t_cnt else 0

    st.markdown(f"""
<div style="background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid rgba(255,215,0,.25);border-radius:13px;
  padding:18px;margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;
        color:#FFD700;letter-spacing:2px;">🏆 YUTUQLAR</div>
      <div style="font-size:.72rem;color:rgba(255,255,255,.35);">{u_cnt}/{t_cnt} bajarilgan</div>
    </div>
    <div style="font-family:'Orbitron',sans-serif;font-size:1.5rem;
      color:#FFD700;font-weight:700;">{a_pct:.0f}%</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-fill" style="width:{a_pct:.1f}%;
      background:linear-gradient(90deg,#FFD700,#FFA500);
      box-shadow:0 0 8px rgba(255,215,0,.4);">
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    flt = st.radio("Filtr:", ["Barchasi","Bajarilgan","Qulfli"], horizontal=True, key="ach_flt")
    show_achs = ACHIEVEMENTS
    if flt == "Bajarilgan": show_achs = [a for a in ACHIEVEMENTS if a["id"] in st.session_state.achievements]
    elif flt == "Qulfli":   show_achs = [a for a in ACHIEVEMENTS if a["id"] not in st.session_state.achievements]

    a_cols = st.columns(2)
    for i, ach in enumerate(show_achs):
        done = ach["id"] in st.session_state.achievements
        with a_cols[i % 2]:
            st.markdown(f"""
<div class="ach-card {'done' if done else ''}">
  <div class="ach-icon">{ach['icon']}</div>
  <div style="flex:1;">
    <div class="ach-title">{ach['name']}</div>
    <div class="ach-desc">{ach['desc']}</div>
    <div class="ach-rew">🎁 +{ach['xp']:,} XP</div>
  </div>
  <div class="ach-done {'st-done' if done else 'st-lock'}">
    {'✅ BAJARILDI' if done else '🔒 Qulfli'}
  </div>
</div>""", unsafe_allow_html=True)

    # Cheat panel
    st.markdown("---")
    st.markdown('<div class="sec-head">⚡ TEZKOR BUYRUQLAR</div>', unsafe_allow_html=True)
    st.markdown('<div class="warn-box">⚡ Tezkor XP va bonuslar qo\'shing!</div>', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("⚡ +1,000 XP", key="add1k"):
            st.session_state.player_xp += 1000; st.session_state.xp_earned += 1000
            add_notif("+1,000 XP!", "⚡"); st.rerun()
    with b2:
        if st.button("🔥 +5,000 XP", key="add5k"):
            st.session_state.player_xp += 5000; st.session_state.xp_earned += 5000
            add_notif("+5,000 XP!", "🔥"); st.rerun()
    with b3:
        if st.button("💎 +10,000 XP", key="add10k"):
            st.session_state.player_xp += 10000; st.session_state.xp_earned += 10000
            add_notif("+10,000 XP!", "💎"); st.rerun()
    with b4:
        if st.button("🌠 MAX XP (122)", key="addmax"):
            st.session_state.player_xp += 100000; st.session_state.xp_earned += 100000
            add_notif("+100,000 XP — barcha ranklar tayyor!", "🌠"); st.rerun()

    b5, b6, b7, b8 = st.columns(4)
    with b5:
        if st.button("💰 +100K Coins", key="addcoins"):
            st.session_state.coins += 100000; st.session_state.coins_earned += 100000
            add_notif("+100,000 Coins!", "💰"); st.rerun()
    with b6:
        if st.button("🔮 Mega Potion", key="givemega"):
            st.session_state.inventory.append({"id":"xp_mega","ts":datetime.now().strftime("%H:%M")})
            st.session_state.total_items += 1
            add_notif("XP Mega Potion qo'shildi!", "🔮"); st.rerun()
    with b7:
        if st.button("🏅 Rank Token ×3", key="givetokens"):
            for _ in range(3):
                st.session_state.inventory.append({"id":"rank_token","ts":datetime.now().strftime("%H:%M")})
            st.session_state.total_items += 3
            add_notif("3 ta Rank Token qo'shildi!", "🏅"); st.rerun()
    with b8:
        if st.button("🏗️ Klub MAX", key="clubmax"):
            for k in st.session_state.club_levels: st.session_state.club_levels[k] = 5
            st.session_state.club_rep += 50000
            grant("upg_one"); grant("upg_max")
            add_notif("Barcha klub binolari MAX!", "🏰"); st.rerun()

    # Tips
    st.markdown("---")
    st.markdown('<div class="sec-head">💡 MASLAHATLAR</div>', unsafe_allow_html=True)
    tips = [
        ("📦","Pack Ochish","Ultimate Pack eng ko'p XP beradi — 10,000 XP!"),
        ("🚀","Rank Up","117→118→119→120→121→122 — har birida stats oshadi."),
        ("🏋️","Training Ground","MAX darajada XP ×1.9! Eng muhim bino."),
        ("🔮","Mega Potion","Inventardagi Mega Potion = +5,000 XP bir marta."),
        ("⚡","Tezkor Buyruq","Yutuqlar tabida MAX XP tugmasi bor!"),
        ("📊","Stat Card","Tasodifiy asosiy statni +1 yoki +2 oshiradi."),
        ("🏅","Rank Token","Har biri +500 XP beradi — rank up uchun yaxshi!"),
        ("🌠","OVR 122","Ultimate Icon — hamma statlar maximum darajada!"),
    ]
    t_cols = st.columns(4)
    for i, (ic, ti, de) in enumerate(tips):
        with t_cols[i % 4]:
            st.markdown(f"""
<div style="background:var(--dark3);border:1px solid var(--border);
  border-radius:9px;padding:11px;margin-bottom:7px;">
  <div style="font-size:1.3rem;margin-bottom:5px;">{ic}</div>
  <div style="font-weight:700;color:#FFD700;font-size:.82rem;margin-bottom:3px;">{ti}</div>
  <div style="font-size:.72rem;color:rgba(255,255,255,.45);line-height:1.4;">{de}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:20px;
  color:rgba(255,255,255,.2);font-size:.72rem;
  border-top:1px solid var(--border);margin-top:24px;">
  ⚽ EA FC Mobile Ultimate Simulator &bull;
  Barcha packlar bepul &bull; Cheksiz pul &bull;
  OVR 117 → 122 &bull; Claude AI tomonidan yaratilgan
</div>""", unsafe_allow_html=True)
