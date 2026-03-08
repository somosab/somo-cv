import streamlit as st
import random
import time
import json
import math
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EA FC Mobile Ultimate",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  GLOBAL CSS  ─────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;600;700;800;900&display=swap');

/* ── Root Variables ── */
:root {
  --gold:    #FFD700;
  --gold2:   #FFA500;
  --icon:    #C084FC;
  --elite:   #38BDF8;
  --green:   #4ADE80;
  --red:     #F87171;
  --dark:    #06090F;
  --dark2:   #0D1117;
  --dark3:   #161B22;
  --dark4:   #1C2333;
  --border:  #21262D;
  --text:    #E6EDF3;
  --muted:   #7D8590;
}

/* ── Base ── */
.stApp { background: var(--dark) !important; color: var(--text); font-family:'Rajdhani',sans-serif; }
.main .block-container { padding:1rem 1.5rem; max-width:1400px; }

/* ── Scrollbar ── */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:#0D1117}
::-webkit-scrollbar-thumb{background:#30363D;border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:#484F58}

/* ── Header ── */
.fc-header{
  background:linear-gradient(135deg,#0D1B2A 0%,#1A2540 40%,#0D2818 100%);
  border:1px solid rgba(255,215,0,.25);
  border-radius:16px;
  padding:24px 32px;
  margin-bottom:20px;
  position:relative;
  overflow:hidden;
}
.fc-header::before{
  content:'';
  position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 80% at 80% 50%,rgba(74,222,128,.06),transparent),
             radial-gradient(ellipse 40% 60% at 20% 50%,rgba(255,215,0,.05),transparent);
  pointer-events:none;
}
.fc-header-title{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(1.8rem,3vw,3rem);
  letter-spacing:4px;
  background:linear-gradient(90deg,#FFD700,#FFA500,#4ADE80);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin:0;line-height:1;
}
.fc-header-sub{color:var(--muted);font-size:.85rem;margin-top:4px;letter-spacing:2px;text-transform:uppercase}

/* ── Currency Bar ── */
.curr-bar{
  display:flex;gap:12px;flex-wrap:wrap;
  background:var(--dark3);border:1px solid var(--border);
  border-radius:12px;padding:14px 20px;margin-bottom:16px;
}
.curr-item{
  display:flex;align-items:center;gap:10px;
  background:var(--dark2);border:1px solid var(--border);
  border-radius:10px;padding:8px 16px;flex:1;min-width:120px;
}
.curr-icon{font-size:1.4em}
.curr-val{font-family:'Orbitron',sans-serif;font-size:1em;color:var(--gold);font-weight:700}
.curr-lbl{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  background:var(--dark3);border-radius:10px;gap:4px;border:1px solid var(--border);padding:4px;
}
.stTabs [data-baseweb="tab"]{
  background:transparent;color:var(--muted);border-radius:7px;
  font-family:'Rajdhani',sans-serif;font-weight:600;font-size:.9rem;
  letter-spacing:1px;padding:8px 16px;transition:all .2s;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#1A6B3C,#2D9E5F) !important;
  color:#fff !important;
}

/* ── Buttons ── */
div.stButton>button{
  background:linear-gradient(135deg,#1A6B3C,#2D9E5F);
  color:#fff;border:none;border-radius:10px;
  font-family:'Rajdhani',sans-serif;font-weight:700;
  font-size:.9rem;letter-spacing:1.5px;text-transform:uppercase;
  padding:10px 20px;width:100%;
  box-shadow:0 4px 15px rgba(45,158,95,.35);
  transition:all .2s;
}
div.stButton>button:hover{
  background:linear-gradient(135deg,#2D9E5F,#4ADE80);
  transform:translateY(-2px);
  box-shadow:0 6px 20px rgba(74,222,128,.5);
}
div.stButton>button:active{transform:translateY(0)}

/* ── Section Header ── */
.sec-head{
  font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
  letter-spacing:3px;color:var(--gold);
  border-bottom:2px solid #1A6B3C;
  padding-bottom:8px;margin:20px 0 14px;
}

/* ═══ PLAYER CARD STYLES ═══ */
.card-wrap{display:flex;flex-direction:column;align-items:center;gap:8px}

.pcard{
  width:140px;height:195px;border-radius:12px;
  position:relative;overflow:hidden;cursor:pointer;
  transition:transform .3s,box-shadow .3s;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:12px 8px;text-align:center;
}
.pcard:hover{transform:translateY(-6px) scale(1.03)}

.pcard-base{
  background:linear-gradient(160deg,#5c4004,#3d2800,#1a0f00);
  border:2px solid #FFD700;
  box-shadow:0 0 20px rgba(255,215,0,.4),inset 0 1px 0 rgba(255,215,0,.2);
}
.pcard-elite{
  background:linear-gradient(160deg,#0f3460,#1a4a8a,#0a1f40);
  border:2px solid #38BDF8;
  box-shadow:0 0 25px rgba(56,189,248,.45),inset 0 1px 0 rgba(56,189,248,.2);
}
.pcard-icon{
  background:linear-gradient(160deg,#3b1f6b,#5b2d9e,#1a0a35);
  border:2px solid #C084FC;
  box-shadow:0 0 30px rgba(192,132,252,.55),inset 0 1px 0 rgba(192,132,252,.2);
  animation:iconPulse 3s ease-in-out infinite;
}
.pcard-ultimate{
  background:linear-gradient(160deg,#4a0e0e,#8b1a1a,#1a0505);
  border:2px solid #F87171;
  box-shadow:0 0 35px rgba(248,113,113,.6),inset 0 1px 0 rgba(248,113,113,.2);
  animation:ultimatePulse 2s ease-in-out infinite;
}
.pcard-tots{
  background:linear-gradient(160deg,#0f4a20,#1a8040,#072510);
  border:2px solid #4ADE80;
  box-shadow:0 0 25px rgba(74,222,128,.45);
}
.pcard-ucl{
  background:linear-gradient(160deg,#0a1f4a,#1a3a8a,#050f25);
  border:2px solid #60A5FA;
  box-shadow:0 0 25px rgba(96,165,250,.45);
}

@keyframes iconPulse{
  0%,100%{box-shadow:0 0 30px rgba(192,132,252,.55)}
  50%{box-shadow:0 0 50px rgba(192,132,252,.9),0 0 80px rgba(192,132,252,.3)}
}
@keyframes ultimatePulse{
  0%,100%{box-shadow:0 0 35px rgba(248,113,113,.6)}
  50%{box-shadow:0 0 60px rgba(248,113,113,1),0 0 100px rgba(248,113,113,.4)}
}

.pcard-type{font-size:.6rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:2px}
.pcard-ovr{font-family:'Bebas Neue',sans-serif;font-size:3rem;line-height:1;margin:2px 0}
.pcard-name{font-weight:700;font-size:.75rem;line-height:1.2;margin:4px 0 2px}
.pcard-pos{font-size:.6rem;letter-spacing:2px;color:rgba(255,255,255,.6);background:rgba(0,0,0,.3);padding:1px 6px;border-radius:3px}
.pcard-club{font-size:.65rem;margin-top:4px;opacity:.8}
.pcard-nation{font-size:1.1rem;margin-top:2px}

/* Card shine effect */
.pcard::after{
  content:'';position:absolute;
  top:-50%;left:-60%;width:50%;height:200%;
  background:linear-gradient(105deg,transparent,rgba(255,255,255,.08),transparent);
  transform:rotate(25deg);transition:left .5s;
}
.pcard:hover::after{left:120%}

/* ═══ PACK CARDS ═══ */
.pack-card{
  border-radius:16px;padding:20px 14px;text-align:center;
  cursor:pointer;transition:all .3s;min-height:230px;
  display:flex;flex-direction:column;align-items:center;justify-content:space-between;
  position:relative;overflow:hidden;
}
.pack-card::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.06),transparent 70%);
}
.pack-gold{background:linear-gradient(145deg,#1a1000,#2a1d00);border:2px solid #FFD700;box-shadow:0 4px 20px rgba(255,215,0,.3)}
.pack-elite{background:linear-gradient(145deg,#00101a,#001a2a);border:2px solid #38BDF8;box-shadow:0 4px 20px rgba(56,189,248,.3)}
.pack-icon{background:linear-gradient(145deg,#150a25,#250f45);border:2px solid #C084FC;box-shadow:0 4px 25px rgba(192,132,252,.4);animation:iconPulse 3s infinite}
.pack-ultimate{background:linear-gradient(145deg,#1a0505,#2a0a0a);border:2px solid #F87171;box-shadow:0 4px 25px rgba(248,113,113,.4);animation:ultimatePulse 2s infinite}
.pack-ucl{background:linear-gradient(145deg,#000d1a,#001530);border:2px solid #60A5FA;box-shadow:0 4px 20px rgba(96,165,250,.3)}
.pack-tots{background:linear-gradient(145deg,#001a0a,#002a10);border:2px solid #4ADE80;box-shadow:0 4px 20px rgba(74,222,128,.3)}

.pack-card:hover{transform:translateY(-6px) scale(1.02)}
.pack-icon-emoji{font-size:2.8rem;margin:4px 0}
.pack-title{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:2px;margin:4px 0}
.pack-desc{font-size:.7rem;color:var(--muted);margin:2px 0 8px}
.pack-badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:800;letter-spacing:1px}
.badge-free{background:rgba(74,222,128,.15);color:#4ADE80;border:1px solid #4ADE80}
.badge-icon{background:rgba(192,132,252,.15);color:#C084FC;border:1px solid #C084FC}
.badge-elite{background:rgba(56,189,248,.15);color:#38BDF8;border:1px solid #38BDF8}
.badge-ult{background:rgba(248,113,113,.15);color:#F87171;border:1px solid #F87171}
.pack-count{font-size:.75rem;color:#4ADE80;font-weight:600}

/* ═══ PACK OPENING ANIMATION ═══ */
.pack-opening-overlay{
  position:fixed;inset:0;z-index:9999;
  background:rgba(0,0,0,.92);backdrop-filter:blur(10px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  animation:fadeIn .3s ease;
}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

.pack-anim-container{
  position:relative;width:300px;height:380px;
  display:flex;align-items:center;justify-content:center;
}

.pack-anim-glow{
  position:absolute;inset:-40px;border-radius:50%;
  background:radial-gradient(circle,var(--glow-color,.6) 0%,transparent 70%);
  animation:glowPulse 1s ease-in-out infinite;
}
@keyframes glowPulse{
  0%,100%{transform:scale(1);opacity:.6}
  50%{transform:scale(1.2);opacity:1}
}

.pack-anim-box{
  width:200px;height:280px;border-radius:16px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  position:relative;z-index:2;
  animation:packFloat 2s ease-in-out infinite;
}
@keyframes packFloat{
  0%,100%{transform:translateY(0) rotate(-2deg)}
  50%{transform:translateY(-15px) rotate(2deg)}
}

.pack-anim-particles{
  position:absolute;inset:-100px;pointer-events:none;
}

.particle{
  position:absolute;width:6px;height:6px;border-radius:50%;
  animation:particleFly linear infinite;
}
@keyframes particleFly{
  0%{transform:translate(0,0) scale(1);opacity:1}
  100%{transform:translate(var(--tx),var(--ty)) scale(0);opacity:0}
}

/* Result cards animation */
.result-card-wrap{
  opacity:0;transform:translateY(30px) scale(.8);
  animation:cardReveal .5s ease forwards;
}
@keyframes cardReveal{
  to{opacity:1;transform:translateY(0) scale(1)}
}

.result-icon-reveal{
  opacity:0;transform:scale(.5) rotate(-10deg);
  animation:iconReveal .6s cubic-bezier(.34,1.56,.64,1) forwards;
}
@keyframes iconReveal{
  to{opacity:1;transform:scale(1) rotate(0)}
}

/* ═══ RANK UP ANIMATION ═══ */
.rankup-overlay{
  position:fixed;inset:0;z-index:10000;
  background:radial-gradient(ellipse at center,rgba(255,215,0,.15),rgba(0,0,0,.95));
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  animation:rankupFadeIn .4s ease;
}
@keyframes rankupFadeIn{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}

.rankup-text{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(3rem,8vw,6rem);
  background:linear-gradient(90deg,#FFD700,#FFA500,#FFD700);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:rankupShine 1.5s linear infinite,rankupBounce .6s cubic-bezier(.34,1.56,.64,1);
  letter-spacing:8px;
  text-shadow:none;
  filter:drop-shadow(0 0 30px rgba(255,215,0,.8));
}
@keyframes rankupShine{
  0%{background-position:0%}100%{background-position:200%}
}
@keyframes rankupBounce{
  0%{transform:scale(.3) translateY(50px)}
  60%{transform:scale(1.15) translateY(-10px)}
  100%{transform:scale(1) translateY(0)}
}

.rankup-sub{
  font-family:'Orbitron',sans-serif;font-size:1rem;
  color:#FFD700;letter-spacing:4px;text-transform:uppercase;
  margin-top:10px;animation:fadeInUp .6s .3s both;
}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

.rankup-ovr-change{
  display:flex;align-items:center;gap:20px;margin-top:20px;
  animation:fadeInUp .6s .6s both;
}
.rankup-old-ovr{font-family:'Bebas Neue',sans-serif;font-size:3rem;color:var(--muted);text-decoration:line-through}
.rankup-arrow{font-size:2rem;color:#FFD700;animation:arrowPulse 1s ease infinite}
@keyframes arrowPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.3)}}
.rankup-new-ovr{font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#FFD700;
  filter:drop-shadow(0 0 20px rgba(255,215,0,.8))}

.rankup-stars{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.rstar{
  position:absolute;font-size:1.5rem;
  animation:starFloat 3s ease-in-out infinite;
}
@keyframes starFloat{
  0%{transform:translateY(100vh) rotate(0);opacity:1}
  100%{transform:translateY(-20px) rotate(720deg);opacity:0}
}

/* ═══ UPGRADE BOX ═══ */
.upg-box{
  background:linear-gradient(145deg,var(--dark3),var(--dark2));
  border:1.5px solid var(--border);border-radius:14px;padding:18px;margin-bottom:12px;
  transition:border-color .2s,box-shadow .2s;
}
.upg-box:hover{border-color:rgba(74,222,128,.4);box-shadow:0 4px 20px rgba(74,222,128,.1)}

.upg-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.upg-name{font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:2px;color:#fff}
.upg-lvl-badge{
  font-family:'Orbitron',sans-serif;font-size:.75rem;font-weight:700;
  padding:3px 10px;border-radius:20px;
}

.upg-progress{background:var(--dark);border-radius:6px;height:8px;overflow:hidden;margin:8px 0}
.upg-progress-fill{height:100%;border-radius:6px;transition:width .5s ease}

.upg-current-bonus{
  background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2);
  border-radius:8px;padding:6px 10px;font-size:.8rem;color:#4ADE80;margin-top:6px;
}
.upg-next-bonus{
  background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);
  border-radius:8px;padding:6px 10px;font-size:.8rem;color:#38BDF8;margin-top:4px;
}

/* ═══ SQUAD FIELD ═══ */
.field-wrap{
  background:linear-gradient(180deg,#0a2015 0%,#0d3020 40%,#0a2015 100%);
  border:2px solid rgba(74,222,128,.3);border-radius:16px;
  padding:20px;position:relative;overflow:hidden;
}
.field-wrap::before{
  content:'';position:absolute;inset:0;
  background:
    repeating-linear-gradient(90deg,transparent,transparent 49.5%,rgba(255,255,255,.03) 49.5%,rgba(255,255,255,.03) 50.5%,transparent 50.5%,transparent 100%),
    repeating-linear-gradient(0deg,transparent,transparent 16.5%,rgba(255,255,255,.02) 16.5%,rgba(255,255,255,.02) 17%,transparent 17%,transparent 100%);
  pointer-events:none;
}
.field-line{border-top:1px solid rgba(255,255,255,.08);margin:4px 0}

.squad-slot{
  background:rgba(0,0,0,.4);border:1.5px dashed rgba(255,255,255,.15);
  border-radius:10px;padding:8px 4px;text-align:center;
  min-height:85px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  transition:all .2s;cursor:pointer;
}
.squad-slot:hover{border-color:rgba(74,222,128,.4);background:rgba(74,222,128,.05)}
.squad-slot-filled{border-style:solid}
.squad-slot-ovr{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;line-height:1}
.squad-slot-name{font-size:.6rem;font-weight:700;margin:2px 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:75px}
.squad-slot-pos{font-size:.5rem;letter-spacing:1px;background:rgba(0,0,0,.4);padding:1px 4px;border-radius:3px;color:var(--muted)}

/* ═══ STAT BARS ═══ */
.stat-row{display:flex;align-items:center;gap:10px;margin:4px 0}
.stat-lbl{width:32px;font-size:.7rem;color:var(--muted);text-align:right;font-weight:600}
.stat-bar-bg{flex:1;height:7px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden}
.stat-bar-fill{height:100%;border-radius:4px;transition:width .6s ease}
.stat-val{width:24px;font-size:.75rem;font-weight:700;color:#fff}

/* ═══ ACHIEVEMENT CARD ═══ */
.ach-card{
  background:var(--dark3);border:1px solid var(--border);
  border-radius:12px;padding:14px;margin-bottom:8px;
  display:flex;align-items:center;gap:14px;transition:all .2s;
}
.ach-card.unlocked{border-color:rgba(255,215,0,.4);background:linear-gradient(135deg,rgba(255,215,0,.06),var(--dark3))}
.ach-card.locked{opacity:.45;filter:grayscale(.5)}
.ach-icon{font-size:2rem;min-width:40px;text-align:center}
.ach-name{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:1px;color:#fff}
.ach-desc{font-size:.75rem;color:var(--muted);margin-top:1px}
.ach-reward{font-size:.7rem;color:var(--gold);margin-top:3px;font-weight:600}
.ach-status{margin-left:auto;font-size:.75rem;font-weight:700;white-space:nowrap;padding:3px 10px;border-radius:20px}
.status-done{background:rgba(74,222,128,.15);color:#4ADE80}
.status-lock{background:rgba(255,255,255,.06);color:var(--muted)}

/* ═══ NOTIFICATION ═══ */
.notif{
  background:linear-gradient(135deg,rgba(74,222,128,.1),rgba(74,222,128,.05));
  border:1px solid rgba(74,222,128,.25);border-radius:8px;
  padding:8px 14px;margin:3px 0;font-size:.8rem;color:#a8f5c8;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"]{background:var(--dark2) !important;border-right:1px solid var(--border)}
[data-testid="stSidebar"] *{color:var(--text) !important}
[data-testid="stSidebar"] .stSelectbox>div>div{background:var(--dark3) !important;border-color:var(--border) !important}

/* ═══ INPUTS ═══ */
.stTextInput>div>div>input{background:var(--dark3) !important;border-color:var(--border) !important;color:var(--text) !important;border-radius:8px !important}
.stSelectbox>div>div{background:var(--dark3) !important;border-color:var(--border) !important;color:var(--text) !important}
label{color:var(--muted) !important;font-size:.8rem !important}

/* ═══ METRIC ═══ */
[data-testid="stMetric"]{background:var(--dark3);border:1px solid var(--border);border-radius:10px;padding:12px 16px}
[data-testid="stMetricValue"]{font-family:'Orbitron',sans-serif !important;color:var(--gold) !important;font-size:1.2rem !important}
[data-testid="stMetricLabel"]{color:var(--muted) !important;font-size:.7rem !important;letter-spacing:1px}

/* ═══ MISC ═══ */
hr{border-color:var(--border) !important;margin:16px 0}
.stSpinner>div{border-color:var(--green) transparent transparent !important}

/* ═══ PACK VIDEO ANIM (CSS only) ═══ */
.video-pack-container{
  display:flex;flex-direction:column;align-items:center;
  gap:16px;padding:30px;
}
.video-pack-box{
  width:200px;height:280px;border-radius:20px;
  display:flex;align-items:center;justify-content:center;
  font-size:5rem;position:relative;
  animation:videoPack 1.5s cubic-bezier(.34,1.56,.64,1) both;
  box-shadow:0 0 60px var(--vglow,rgba(255,215,0,.5));
}
@keyframes videoPack{
  0%{transform:scale(0) rotate(-20deg);opacity:0}
  60%{transform:scale(1.1) rotate(3deg)}
  100%{transform:scale(1) rotate(0);opacity:1}
}

.opening-flash{
  position:fixed;inset:0;z-index:10001;
  background:white;animation:flashOut .4s ease forwards;
  pointer-events:none;
}
@keyframes flashOut{
  0%{opacity:.9}100%{opacity:0;display:none}
}

.card-flip{
  perspective:1000px;width:140px;height:195px;
}
.card-flip-inner{
  position:relative;width:100%;height:100%;
  transform-style:preserve-3d;
  animation:flipCard .8s ease forwards;
  animation-delay:var(--delay,.1s);
}
@keyframes flipCard{
  0%{transform:rotateY(-180deg) scale(.5);opacity:0}
  60%{transform:rotateY(10deg) scale(1.05)}
  100%{transform:rotateY(0) scale(1);opacity:1}
}
.card-flip-front{
  position:absolute;inset:0;backface-visibility:hidden;
}
.card-back{
  position:absolute;inset:0;backface-visibility:hidden;
  transform:rotateY(180deg);
  background:linear-gradient(145deg,#1a2540,#0d1b35);
  border:2px solid var(--border);border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  font-size:2rem;
}

/* ═══ RANK UP PROGRESS BAR ═══ */
.rankup-progress{
  width:100%;background:var(--dark);border-radius:10px;height:20px;
  overflow:hidden;margin:10px 0;border:1px solid var(--border);
}
.rankup-progress-fill{
  height:100%;border-radius:10px;
  background:linear-gradient(90deg,#FFD700,#FFA500);
  transition:width 1s ease;
  box-shadow:0 0 10px rgba(255,215,0,.5);
  position:relative;overflow:hidden;
}
.rankup-progress-fill::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);
  animation:progressShine 1.5s linear infinite;
}
@keyframes progressShine{
  0%{transform:translateX(-100%)}100%{transform:translateX(100%)}
}

/* ═══ LEAGUE CARD ═══ */
.league-card{
  background:var(--dark3);border:1px solid var(--border);
  border-radius:12px;padding:16px;text-align:center;transition:all .2s;
}
.league-card:hover{border-color:rgba(255,215,0,.3);transform:translateY(-3px)}
.league-icon{font-size:2.5rem;margin-bottom:8px}
.league-name{font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px}
.league-rank{font-family:'Orbitron',sans-serif;font-size:1.5rem;color:var(--gold);font-weight:700}

/* ═══ SHIMMER LOADING ═══ */
.shimmer{
  background:linear-gradient(90deg,var(--dark3) 25%,rgba(255,255,255,.05) 37%,var(--dark3) 63%);
  background-size:400px 100%;
  animation:shimmer 1.4s ease infinite;
}
@keyframes shimmer{
  0%{background-position:-400px 0}100%{background-position:400px 0}
}

/* ═══ FIRE / SPECIAL EFFECTS ═══ */
.fire-text{
  font-family:'Bebas Neue',sans-serif;font-size:1.2rem;
  background:linear-gradient(180deg,#FFD700,#FF6B00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 0 8px rgba(255,165,0,.7));
}

.glow-green{filter:drop-shadow(0 0 10px rgba(74,222,128,.7))}
.glow-gold{filter:drop-shadow(0 0 10px rgba(255,215,0,.7))}
.glow-purple{filter:drop-shadow(0 0 10px rgba(192,132,252,.7))}

/* ═══ TABLE OVERRIDE ═══ */
.stDataFrame{background:var(--dark3) !important}
thead th{background:var(--dark2) !important;color:var(--muted) !important;font-family:'Rajdhani' !important;font-weight:600 !important;font-size:.8rem !important;letter-spacing:1px !important}
tbody td{background:var(--dark3) !important;color:var(--text) !important;border-color:var(--border) !important;font-size:.85rem !important}

/* ═══ INFO BOX ═══ */
.info-box{
  background:linear-gradient(135deg,rgba(56,189,248,.08),rgba(56,189,248,.03));
  border:1px solid rgba(56,189,248,.2);border-radius:10px;
  padding:12px 18px;margin:10px 0;color:#7DD3FC;font-size:.85rem;
}
.warn-box{
  background:linear-gradient(135deg,rgba(251,191,36,.08),rgba(251,191,36,.03));
  border:1px solid rgba(251,191,36,.2);border-radius:10px;
  padding:12px 18px;margin:10px 0;color:#FCD34D;font-size:.85rem;
}
.success-box{
  background:linear-gradient(135deg,rgba(74,222,128,.1),rgba(74,222,128,.04));
  border:1px solid rgba(74,222,128,.25);border-radius:10px;
  padding:12px 18px;margin:10px 0;color:#86EFAC;font-size:.85rem;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  DATA DEFINITIONS
# ═══════════════════════════════════════════════════════════════

# ── Single Player Definition ──
PLAYER = {
    "name": "ULTIMATE STRIKER",
    "full_name": "Ultimate Striker",
    "pos": "ST",
    "nation": "🌍",
    "nation_name": "World",
    "club": "FC Ultimate",
    "base_ovr": 117,
    "max_ovr": 122,
    "type": "ULTIMATE",
    "emoji": "🌠",
    "bio": "Dunyodagi eng zo'r futbolchi. Cheksiz imkoniyatlar bilan jihozlangan.",

    # Base stats (at OVR 117)
    "base_stats": {
        "PAC": 96, "SHO": 97, "PAS": 94,
        "DRI": 98, "DEF": 72, "PHY": 95,
        "Tezlik": 96, "Tezlashtirish": 95,
        "Uzoq Zarbalar": 97, "Penalties": 99, "Finishing": 98,
        "Qisqa Uzatmalar": 95, "Uzoq Uzatmalar": 93, "Ko'rishlik": 97,
        "Top Nazorat": 99, "Dribbling": 98, "Chapaqaylik": 89,
        "Jang": 72, "Qayta Olish": 68, "Muddao Hissi": 89,
        "Sakrash": 94, "Muvozanat": 93, "Kuch": 96, "Tajovuz": 92,
    },
    # Weak foot & skill moves
    "weak_foot": 5,
    "skill_moves": 5,
    "preferred_foot": "Right",
    "work_rate": "High / Medium",
    "height": "185 cm",
    "weight": "82 kg",
    "age": 26,
}

# ── Rank System ──
RANKS = [
    {"ovr": 117, "name": "BASE",           "icon": "⚪", "color": "#9CA3AF"},
    {"ovr": 118, "name": "SILVER STAR",    "icon": "⭐", "color": "#C0C0C0",
     "xp_req": 1000,  "bonus": "+1 PAC, +1 SHO",         "stat_boost": {"PAC":1,"SHO":1}},
    {"ovr": 119, "name": "GOLD STAR",      "icon": "🌟", "color": "#FFD700",
     "xp_req": 2500,  "bonus": "+2 DRI, +1 PHY",          "stat_boost": {"DRI":2,"PHY":1}},
    {"ovr": 120, "name": "ELITE",          "icon": "💎", "color": "#38BDF8",
     "xp_req": 5000,  "bonus": "+2 SHO, +2 PAS, +1 PAC",  "stat_boost": {"SHO":2,"PAS":2,"PAC":1}},
    {"ovr": 121, "name": "LEGEND",         "icon": "👑", "color": "#C084FC",
     "xp_req": 10000, "bonus": "+3 DRI, +2 SHO, +2 PHY",  "stat_boost": {"DRI":3,"SHO":2,"PHY":2}},
    {"ovr": 122, "name": "ULTIMATE ICON",  "icon": "🌠", "color": "#F87171",
     "xp_req": 20000, "bonus": "+5 tüm stats - MAX POWER!", "stat_boost": {"PAC":2,"SHO":3,"PAS":2,"DRI":3,"DEF":1,"PHY":2}},
]

# ── Packs ──
PACKS = [
    {
        "id": "starter_gold",
        "name": "Starter Gold Pack",
        "icon": "📦",
        "style": "pack-gold",
        "badge": "BEPUL", "badge_cls": "badge-free",
        "desc": "3 ta oltin o'yinchi + bonus items",
        "count": 3,
        "xp_reward": 150,
        "coins_reward": 5000,
        "items": ["xp_potion_sm", "coin_boost"],
        "color_var": "rgba(255,215,0,.3)",
    },
    {
        "id": "premium_gold",
        "name": "Premium Gold Pack",
        "icon": "🌟",
        "style": "pack-gold",
        "badge": "BEPUL", "badge_cls": "badge-free",
        "desc": "5 ta premium o'yinchi",
        "count": 5,
        "xp_reward": 350,
        "coins_reward": 12000,
        "items": ["xp_potion_md", "stat_card"],
        "color_var": "rgba(255,215,0,.4)",
    },
    {
        "id": "elite_pack",
        "name": "Elite Player Pack",
        "icon": "⚡",
        "style": "pack-elite",
        "badge": "ELITE", "badge_cls": "badge-elite",
        "desc": "Elite XP + Stat boost cards",
        "count": 5,
        "xp_reward": 800,
        "coins_reward": 25000,
        "items": ["xp_potion_lg", "stat_card", "stat_card"],
        "color_var": "rgba(56,189,248,.4)",
    },
    {
        "id": "rank_pack",
        "name": "Rank Boost Pack",
        "icon": "📈",
        "style": "pack-elite",
        "badge": "RANK UP", "badge_cls": "badge-elite",
        "desc": "Katta XP + Rank up yordam",
        "count": 5,
        "xp_reward": 1500,
        "coins_reward": 40000,
        "items": ["xp_potion_xl", "stat_card", "rank_token"],
        "color_var": "rgba(56,189,248,.5)",
    },
    {
        "id": "ucl_pack",
        "name": "Champions Pack",
        "icon": "⭐",
        "style": "pack-ucl",
        "badge": "UCL", "badge_cls": "badge-elite",
        "desc": "Champions League maxsus paketi",
        "count": 6,
        "xp_reward": 2000,
        "coins_reward": 60000,
        "items": ["xp_potion_xl", "stat_card", "stat_card", "rank_token"],
        "color_var": "rgba(96,165,250,.5)",
    },
    {
        "id": "icon_pack",
        "name": "Icon Power Pack",
        "icon": "👑",
        "style": "pack-icon",
        "badge": "ICON", "badge_cls": "badge-icon",
        "desc": "ICON XP + Mega stat boost!",
        "count": 7,
        "xp_reward": 4000,
        "coins_reward": 100000,
        "items": ["xp_potion_mega", "stat_card", "stat_card", "stat_card", "rank_token"],
        "color_var": "rgba(192,132,252,.5)",
    },
    {
        "id": "tots_pack",
        "name": "TOTS Mega Pack",
        "icon": "🏆",
        "style": "pack-tots",
        "badge": "TOTS", "badge_cls": "badge-free",
        "desc": "Team of the Season - max rewards!",
        "count": 8,
        "xp_reward": 5000,
        "coins_reward": 120000,
        "items": ["xp_potion_mega", "xp_potion_xl", "stat_card", "stat_card", "rank_token", "rank_token"],
        "color_var": "rgba(74,222,128,.5)",
    },
    {
        "id": "ultimate_pack",
        "name": "ULTIMATE PACK",
        "icon": "🌠",
        "style": "pack-ultimate",
        "badge": "ULTIMATE", "badge_cls": "badge-ult",
        "desc": "MAKSIMAL MUKOFOTLAR! Eng zo'r pack!",
        "count": 10,
        "xp_reward": 10000,
        "coins_reward": 250000,
        "items": ["xp_potion_mega", "xp_potion_mega", "stat_card", "stat_card", "stat_card", "rank_token", "rank_token", "rank_token"],
        "color_var": "rgba(248,113,113,.6)",
    },
]

# ── Items ──
ITEM_DEFS = {
    "xp_potion_sm":   {"name": "XP Potion S",    "icon": "🧪", "xp": 200,  "color": "#4ADE80"},
    "xp_potion_md":   {"name": "XP Potion M",    "icon": "⚗️",  "xp": 500,  "color": "#38BDF8"},
    "xp_potion_lg":   {"name": "XP Potion L",    "icon": "💊",  "xp": 1000, "color": "#60A5FA"},
    "xp_potion_xl":   {"name": "XP Potion XL",   "icon": "💉",  "xp": 2000, "color": "#818CF8"},
    "xp_potion_mega": {"name": "XP Mega Potion",  "icon": "🔮",  "xp": 5000, "color": "#C084FC"},
    "stat_card":      {"name": "Stat Boost Card", "icon": "📊",  "xp": 0,   "color": "#FFD700"},
    "rank_token":     {"name": "Rank Token",      "icon": "🏅",  "xp": 0,   "color": "#F87171"},
    "coin_boost":     {"name": "Coin Boost",      "icon": "💰",  "xp": 0,   "color": "#FCD34D"},
}

# ── Club Upgrades ──
CLUB_UPGRADES = {
    "Stadium": {
        "icon": "🏟️",
        "desc": "Katta stadion = ko'proq daromad",
        "max_lv": 5,
        "levels": [
            {"name": "Mini Arena",       "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "City Ground",      "bonus": "+10% Coins",     "color": "#3B82F6"},
            {"name": "National Arena",   "bonus": "+22% Coins",     "color": "#22C55E"},
            {"name": "Grand Stadium",    "bonus": "+38% Coins",     "color": "#EAB308"},
            {"name": "Elite Colosseum",  "bonus": "+55% Coins",     "color": "#F97316"},
            {"name": "LEGENDARY DOME",   "bonus": "+80% + 5000XP",  "color": "#C084FC"},
        ]
    },
    "Training Ground": {
        "icon": "🏋️",
        "desc": "Tezroq XP va stat o'sish",
        "max_lv": 5,
        "levels": [
            {"name": "Basic Field",      "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "Youth Academy",    "bonus": "+12% XP",        "color": "#3B82F6"},
            {"name": "Pro Center",       "bonus": "+25% XP",        "color": "#22C55E"},
            {"name": "Elite Hub",        "bonus": "+40% XP",        "color": "#EAB308"},
            {"name": "World Class",      "bonus": "+60% XP",        "color": "#F97316"},
            {"name": "CHAMPIONS LAB",    "bonus": "+90% XP + Stats","color": "#C084FC"},
        ]
    },
    "Scout Network": {
        "icon": "🔭",
        "desc": "Yaxshiroq pack sifati",
        "max_lv": 5,
        "levels": [
            {"name": "Local Scout",      "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "Regional Net",     "bonus": "+10% Pack",      "color": "#3B82F6"},
            {"name": "Continental",      "bonus": "+22% Pack",      "color": "#22C55E"},
            {"name": "Global Network",   "bonus": "+38% Pack",      "color": "#EAB308"},
            {"name": "Elite Scouts",     "bonus": "+55% Pack",      "color": "#F97316"},
            {"name": "LEGENDARY INTEL",  "bonus": "+80% Pack+Token","color": "#C084FC"},
        ]
    },
    "Medical Center": {
        "icon": "🏥",
        "desc": "O'yinchi tezroq tiklanadi",
        "max_lv": 5,
        "levels": [
            {"name": "First Aid",        "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "Clinic",           "bonus": "-20% Injury",    "color": "#3B82F6"},
            {"name": "Medical Hub",      "bonus": "-40% Injury",    "color": "#22C55E"},
            {"name": "Sports Hospital",  "bonus": "-60% Injury",    "color": "#EAB308"},
            {"name": "Recovery Lab",     "bonus": "-80% Injury",    "color": "#F97316"},
            {"name": "BIO-TECH CENTER",  "bonus": "No Injuries!",   "color": "#C084FC"},
        ]
    },
    "Fan Zone": {
        "icon": "👥",
        "desc": "Ko'proq muxlis bonuslari",
        "max_lv": 5,
        "levels": [
            {"name": "Small Section",    "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "Fan Corner",       "bonus": "+15% Tokens",    "color": "#3B82F6"},
            {"name": "Ultra Zone",       "bonus": "+30% Tokens",    "color": "#22C55E"},
            {"name": "Supporter Club",   "bonus": "+50% Tokens",    "color": "#EAB308"},
            {"name": "Global Fans",      "bonus": "+70% Tokens",    "color": "#F97316"},
            {"name": "LEGEND FANBASE",   "bonus": "+100% Tokens",   "color": "#C084FC"},
        ]
    },
    "Tech Lab": {
        "icon": "💻",
        "desc": "Taktik va analitik bonuslar",
        "max_lv": 5,
        "levels": [
            {"name": "Data Room",        "bonus": "Boshlang'ich",   "color": "#64748B"},
            {"name": "Analysis Hub",     "bonus": "+10% Tactic",    "color": "#3B82F6"},
            {"name": "AI Coaching",      "bonus": "+22% Tactic",    "color": "#22C55E"},
            {"name": "VR Training",      "bonus": "+38% Tactic",    "color": "#EAB308"},
            {"name": "Neural Engine",    "bonus": "+58% Tactic",    "color": "#F97316"},
            {"name": "QUANTUM LAB",      "bonus": "+85% ALL",       "color": "#C084FC"},
        ]
    },
}

# ── Achievements ──
ACHIEVEMENTS = [
    {"id":"first_open",  "name":"Birinchi Pack",        "desc":"Birinchi packni oching",              "icon":"📦","reward":"500 XP",   "xp":500},
    {"id":"open10",      "name":"Pack Enthusiast",       "desc":"10 ta pack oching",                   "icon":"⚡","reward":"1000 XP",  "xp":1000},
    {"id":"open50",      "name":"Pack Veteran",          "desc":"50 ta pack oching",                   "icon":"🏆","reward":"3000 XP",  "xp":3000},
    {"id":"open100",     "name":"Pack Legend",           "desc":"100 ta pack oching",                  "icon":"👑","reward":"10000 XP", "xp":10000},
    {"id":"rank118",     "name":"First Upgrade",         "desc":"O'yinchini 118 OVR ga olib chiqing",  "icon":"⭐","reward":"2000 XP",  "xp":2000},
    {"id":"rank119",     "name":"Rising Star",           "desc":"O'yinchini 119 OVR ga olib chiqing",  "icon":"🌟","reward":"4000 XP",  "xp":4000},
    {"id":"rank120",     "name":"Elite Player",          "desc":"O'yinchini 120 OVR ga olib chiqing",  "icon":"💎","reward":"8000 XP",  "xp":8000},
    {"id":"rank121",     "name":"Legend",                "desc":"O'yinchini 121 OVR ga olib chiqing",  "icon":"👑","reward":"15000 XP", "xp":15000},
    {"id":"rank122",     "name":"ULTIMATE ICON",         "desc":"O'yinchini 122 OVR MAX ga olib chiqing","icon":"🌠","reward":"50000 XP","xp":50000},
    {"id":"upg_one",     "name":"Builder",               "desc":"Bitta klub binosi yaxshilash",         "icon":"🏗️","reward":"500 XP",  "xp":500},
    {"id":"upg_all_max", "name":"FC Mogul",              "desc":"Barcha binolarni MAX darajaga olib chiqing","icon":"🏰","reward":"20000 XP","xp":20000},
    {"id":"items100",    "name":"Item Hoarder",          "desc":"100 ta item yig'ing",                  "icon":"🎒","reward":"2000 XP",  "xp":2000},
    {"id":"coins1m",     "name":"Millionaire",           "desc":"1,000,000 coin yig'ing",               "icon":"💰","reward":"5000 XP",  "xp":5000},
    {"id":"ultimate_pk", "name":"Ultimate Opener",       "desc":"Ultimate Pack oching",                 "icon":"🌠","reward":"10000 XP","xp":10000},
    {"id":"all_ach",     "name":"COMPLETIONIST",         "desc":"Barcha achievementlarni oching",        "icon":"🎖️","reward":"100000 XP","xp":100000},
]

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
def init():
    defaults = {
        # Currency
        "coins":     999_999_999,
        "gems":      9_999_999,
        "tokens":    99_999,
        "fan_tokens":999_999,

        # Player state
        "player_ovr":  117,
        "player_rank": 0,       # index into RANKS
        "player_xp":   0,
        "player_stats": dict(PLAYER["base_stats"]),
        "stat_boost_total": {k: 0 for k in PLAYER["base_stats"]},

        # Club
        "club_name": "FC Ultimate",
        "club_badge": "🌠",
        "club_levels": {k: 0 for k in CLUB_UPGRADES},
        "club_reputation": 5000,

        # Inventory
        "inventory": [],
        "total_items_collected": 0,

        # Pack stats
        "packs_opened": 0,
        "coins_collected": 0,
        "xp_collected": 0,
        "pack_history": [],  # list of {pack_id, ts, xp, coins, items}

        # Achievements
        "achievements": [],

        # Notifications
        "notifications": [],

        # UI State
        "show_pack_anim":   False,
        "anim_pack_id":     None,
        "anim_result":      None,
        "show_rankup_anim": False,
        "rankup_old_ovr":   117,
        "rankup_new_ovr":   118,
        "pending_rankup":   False,

        # Formation / squad (cosmetic only, 1 player)
        "formation": "4-3-3",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def add_notif(msg: str, icon: str = "✅"):
    st.session_state.notifications.insert(0, f"{icon} {msg}")
    if len(st.session_state.notifications) > 15:
        st.session_state.notifications = st.session_state.notifications[:15]

def get_xp_for_next_rank() -> int:
    rank_idx = st.session_state.player_rank
    if rank_idx >= len(RANKS) - 1:
        return 0
    return RANKS[rank_idx + 1]["xp_req"]

def get_xp_progress_pct() -> float:
    needed = get_xp_for_next_rank()
    if needed == 0:
        return 100.0
    return min(100.0, (st.session_state.player_xp / needed) * 100)

def can_rank_up() -> bool:
    rank_idx = st.session_state.player_rank
    if rank_idx >= len(RANKS) - 1:
        return False
    needed = RANKS[rank_idx + 1]["xp_req"]
    return st.session_state.player_xp >= needed

def do_rank_up():
    old_rank = st.session_state.player_rank
    old_ovr  = st.session_state.player_ovr
    new_rank = old_rank + 1
    new_rank_data = RANKS[new_rank]

    # Apply stat boosts
    for stat, boost in new_rank_data.get("stat_boost", {}).items():
        long_key = {"PAC":"Tezlik","SHO":"Finishing","PAS":"Qisqa Uzatmalar","DRI":"Dribbling","DEF":"Jang","PHY":"Kuch"}.get(stat, stat)
        short_map = {"PAC":"PAC","SHO":"SHO","PAS":"PAS","DRI":"DRI","DEF":"DEF","PHY":"PHY"}
        if stat in short_map:
            st.session_state.player_stats[stat] = min(99, st.session_state.player_stats.get(stat, 80) + boost)
        if long_key in st.session_state.player_stats:
            st.session_state.player_stats[long_key] = min(99, st.session_state.player_stats[long_key] + boost)

    st.session_state.player_rank  = new_rank
    st.session_state.player_ovr   = new_rank_data["ovr"]
    st.session_state.player_xp   -= new_rank_data["xp_req"]
    if st.session_state.player_xp < 0:
        st.session_state.player_xp = 0

    # Trigger anim
    st.session_state.show_rankup_anim = True
    st.session_state.rankup_old_ovr   = old_ovr
    st.session_state.rankup_new_ovr   = new_rank_data["ovr"]

    add_notif(f"RANK UP! OVR {old_ovr} → {new_rank_data['ovr']} — {new_rank_data['name']}!", "🏆")

    # Check achievements
    ach_map = {118:"rank118",119:"rank119",120:"rank120",121:"rank121",122:"rank122"}
    if new_rank_data["ovr"] in ach_map:
        grant_achievement(ach_map[new_rank_data["ovr"]])

def grant_achievement(ach_id: str):
    if ach_id in st.session_state.achievements:
        return
    ach = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
    if not ach:
        return
    st.session_state.achievements.append(ach_id)
    xp_gain = ach["xp"]
    st.session_state.player_xp += xp_gain
    st.session_state.xp_collected += xp_gain
    add_notif(f"ACHIEVEMENT: {ach['name']} — +{xp_gain:,} XP", "🏅")

    # completionist
    if len(st.session_state.achievements) >= len(ACHIEVEMENTS) - 1:
        grant_achievement("all_ach")

def do_open_pack(pack_id: str):
    pack = next(p for p in PACKS if p["id"] == pack_id)

    # XP gain (with training ground bonus)
    tg_lv = st.session_state.club_levels.get("Training Ground", 0)
    xp_mult = [1.0, 1.12, 1.25, 1.40, 1.60, 1.90][tg_lv]
    base_xp = pack["xp_reward"]
    total_xp = int(base_xp * xp_mult)

    # Coins gain (with stadium bonus)
    st_lv = st.session_state.club_levels.get("Stadium", 0)
    coin_mult = [1.0, 1.10, 1.22, 1.38, 1.55, 1.80][st_lv]
    total_coins = int(pack["coins_reward"] * coin_mult)

    # Scout bonus: extra items
    sc_lv = st.session_state.club_levels.get("Scout Network", 0)
    extra_items = []
    if sc_lv >= 3 and random.random() < .3:
        extra_items.append("xp_potion_md")
    if sc_lv >= 5 and random.random() < .2:
        extra_items.append("rank_token")

    items = pack["items"] + extra_items

    # Apply
    st.session_state.player_xp    += total_xp
    st.session_state.xp_collected += total_xp
    st.session_state.coins         += total_coins
    st.session_state.coins_collected += total_coins
    st.session_state.packs_opened  += 1
    st.session_state.total_items_collected += len(items)

    # Add items to inventory
    for item_id in items:
        if item_id in ITEM_DEFS:
            st.session_state.inventory.append({
                "id": item_id,
                "ts": datetime.now().strftime("%H:%M"),
            })

    # Record history
    st.session_state.pack_history.append({
        "pack_id": pack_id,
        "pack_name": pack["name"],
        "ts": datetime.now().strftime("%H:%M:%S"),
        "xp": total_xp,
        "coins": total_coins,
        "items": items,
    })

    # Check achievements
    grant_achievement("first_open")
    n = st.session_state.packs_opened
    if n >= 10:   grant_achievement("open10")
    if n >= 50:   grant_achievement("open50")
    if n >= 100:  grant_achievement("open100")
    if pack_id == "ultimate_pack": grant_achievement("ultimate_pk")
    if st.session_state.total_items_collected >= 100: grant_achievement("items100")
    if st.session_state.coins_collected >= 1_000_000: grant_achievement("coins1m")

    return {"xp": total_xp, "coins": total_coins, "items": items}

def use_item(item_id: str, slot_idx: int):
    item_def = ITEM_DEFS.get(item_id)
    if not item_def:
        return
    if item_def["xp"] > 0:
        # XP potion
        xp = item_def["xp"]
        tg_lv = st.session_state.club_levels.get("Training Ground", 0)
        xp_mult = [1.0, 1.12, 1.25, 1.40, 1.60, 1.90][tg_lv]
        total_xp = int(xp * xp_mult)
        st.session_state.player_xp += total_xp
        st.session_state.xp_collected += total_xp
        add_notif(f"{item_def['name']} ishlatildi! +{total_xp:,} XP", "🧪")
    elif item_id == "stat_card":
        # Random stat boost
        stat_keys = list(PLAYER["base_stats"].keys())
        stat = random.choice(stat_keys[:6])  # only primary 6
        boost = random.randint(1, 2)
        st.session_state.player_stats[stat] = min(99, st.session_state.player_stats.get(stat, 80) + boost)
        add_notif(f"Stat Card! +{boost} {stat}", "📊")
    elif item_id == "rank_token":
        # Gives 500 XP
        bonus = 500
        st.session_state.player_xp += bonus
        st.session_state.xp_collected += bonus
        add_notif(f"Rank Token! +{bonus} XP", "🏅")
    elif item_id == "coin_boost":
        bonus = 50000
        st.session_state.coins += bonus
        st.session_state.coins_collected += bonus
        add_notif(f"Coin Boost! +{bonus:,} Coins", "💰")

    # Remove from inventory
    st.session_state.inventory.pop(slot_idx)

def get_stat_color(val: int) -> str:
    if val >= 95: return "#4ADE80"
    if val >= 85: return "#A3E635"
    if val >= 75: return "#FACC15"
    if val >= 65: return "#FB923C"
    return "#F87171"

def get_ovr_color(ovr: int) -> str:
    if ovr >= 122: return "#F87171"
    if ovr >= 121: return "#C084FC"
    if ovr >= 120: return "#38BDF8"
    if ovr >= 119: return "#FFD700"
    if ovr >= 118: return "#C0C0C0"
    return "#9CA3AF"

def render_player_mini_card(ovr: int, rank_idx: int) -> str:
    rank = RANKS[rank_idx]
    ovr_color = get_ovr_color(ovr)
    bg_map = {
        0: "linear-gradient(160deg,#1a1a1a,#2a2a2a)",
        1: "linear-gradient(160deg,#1a1a2a,#2a2a4a)",
        2: "linear-gradient(160deg,#2a1a00,#4a3000)",
        3: "linear-gradient(160deg,#001a2a,#003050)",
        4: "linear-gradient(160deg,#150a25,#250f45)",
        5: "linear-gradient(160deg,#1a0505,#2a0a0a)",
    }
    bg = bg_map.get(rank_idx, bg_map[0])
    glow_color = rank["color"]
    card_type = ["BASE","SILVER","GOLD","ELITE","LEGEND","ULTIMATE"][rank_idx]

    return f"""
    <div style="
        background:{bg};
        border:2px solid {glow_color};
        box-shadow: 0 0 25px {glow_color}55, 0 0 60px {glow_color}22;
        border-radius:16px;
        padding:20px 16px;
        text-align:center;
        width:180px;
        {'animation:ultimatePulse 2s infinite' if rank_idx==5 else ('animation:iconPulse 3s infinite' if rank_idx==4 else '')};
        position:relative;overflow:hidden;
        margin:0 auto;
    ">
        <div style="font-size:.65rem;font-weight:800;letter-spacing:2px;color:{glow_color};margin-bottom:2px;">{card_type}</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:4.5rem;line-height:1;color:{glow_color};
            filter:drop-shadow(0 0 12px {glow_color}88);margin:4px 0;">{ovr}</div>
        <div style="font-size:.8rem;font-weight:700;color:#fff;margin:4px 0;">ULTIMATE STRIKER</div>
        <div style="font-size:.65rem;letter-spacing:2px;color:rgba(255,255,255,.5);background:rgba(0,0,0,.3);padding:2px 8px;border-radius:4px;display:inline-block;">ST</div>
        <div style="font-size:.7rem;color:{glow_color};margin-top:6px;">{rank['icon']} {rank['name']}</div>
        <div style="font-size:.7rem;color:rgba(255,255,255,.6);margin-top:2px;">🌍 • {PLAYER['club']}</div>
    </div>
    """

# ═══════════════════════════════════════════════════════════════
#  PACK OPENING ANIMATION (CSS-driven)
# ═══════════════════════════════════════════════════════════════
def render_pack_animation(pack, result):
    pack_styles = {
        "pack-gold":    ("linear-gradient(145deg,#3d2800,#5c4004)", "#FFD700", "rgba(255,215,0,.6)"),
        "pack-elite":   ("linear-gradient(145deg,#001a2a,#003050)", "#38BDF8", "rgba(56,189,248,.6)"),
        "pack-icon":    ("linear-gradient(145deg,#150a25,#250f45)", "#C084FC", "rgba(192,132,252,.6)"),
        "pack-ultimate":("linear-gradient(145deg,#1a0505,#2a0a0a)", "#F87171", "rgba(248,113,113,.6)"),
        "pack-ucl":     ("linear-gradient(145deg,#000d1a,#001530)", "#60A5FA", "rgba(96,165,250,.6)"),
        "pack-tots":    ("linear-gradient(145deg,#001a0a,#002a10)", "#4ADE80", "rgba(74,222,128,.6)"),
    }
    bg, accent, glow = pack_styles.get(pack["style"], pack_styles["pack-gold"])

    # Generate particle HTML
    particles_html = ""
    for i in range(20):
        tx = random.randint(-150, 150)
        ty = random.randint(-200, 50)
        delay = random.random() * 2
        dur = 1 + random.random() * 2
        size = random.randint(4, 10)
        colors = [accent, "#FFD700", "#FFF", "#4ADE80"]
        color = random.choice(colors)
        particles_html += f"""
        <div class="particle" style="
            left:{random.randint(20,80)}%;top:{random.randint(20,80)}%;
            width:{size}px;height:{size}px;background:{color};
            --tx:{tx}px;--ty:{ty}px;
            animation-delay:{delay:.2f}s;animation-duration:{dur:.1f}s;
        "></div>"""

    # Build items grid
    items_html = ""
    for i, item_id in enumerate(result["items"]):
        item = ITEM_DEFS.get(item_id, {"name": item_id, "icon": "❓", "color": "#888"})
        delay = 0.2 + i * 0.1
        items_html += f"""
        <div style="
            background:rgba(0,0,0,.5);border:1px solid {item['color']}44;
            border-radius:10px;padding:10px 14px;text-align:center;
            animation:cardReveal .5s {delay:.1f}s both;
            opacity:0;
        ">
            <div style="font-size:1.8rem;">{item['icon']}</div>
            <div style="font-size:.7rem;color:{item['color']};font-weight:700;margin-top:4px;">{item['name']}</div>
        </div>"""

    html = f"""
    <div style="
        background:rgba(0,0,0,.95);
        border:1px solid {accent}44;border-radius:20px;
        padding:32px 24px;text-align:center;max-width:600px;margin:0 auto;
        position:relative;overflow:hidden;
    ">
        <!-- Background glow -->
        <div style="
            position:absolute;top:-100px;left:50%;transform:translateX(-50%);
            width:400px;height:400px;border-radius:50%;
            background:radial-gradient(circle,{glow} 0%,transparent 70%);
            pointer-events:none;
            animation:glowPulse 1.5s ease-in-out infinite;
        "></div>

        <!-- Particles -->
        <div style="position:absolute;inset:0;pointer-events:none;overflow:hidden;">
            {particles_html}
        </div>

        <!-- Pack Box -->
        <div style="position:relative;z-index:2;">
            <div style="
                display:inline-flex;align-items:center;justify-content:center;
                width:160px;height:220px;border-radius:16px;
                background:{bg};
                border:3px solid {accent};
                box-shadow:0 0 40px {glow},0 0 80px {glow.replace('.6','.2')};
                font-size:5rem;
                animation:videoPack 1s cubic-bezier(.34,1.56,.64,1) both;
                margin:0 auto 20px;
            ">
                {pack['icon']}
            </div>

            <!-- Pack Name -->
            <div style="
                font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                letter-spacing:3px;color:{accent};
                animation:fadeInUp .5s .8s both;opacity:0;
            ">{pack['name']}</div>

            <!-- XP and Coins -->
            <div style="
                display:flex;justify-content:center;gap:20px;margin:14px 0;
                animation:fadeInUp .5s 1s both;opacity:0;
            ">
                <div style="background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);border-radius:10px;padding:8px 20px;">
                    <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#4ADE80;font-weight:700;">+{result['xp']:,}</div>
                    <div style="font-size:.65rem;color:#6EE7B7;letter-spacing:1px;">XP</div>
                </div>
                <div style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);border-radius:10px;padding:8px 20px;">
                    <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#FFD700;font-weight:700;">+{result['coins']:,}</div>
                    <div style="font-size:.65rem;color:#FCD34D;letter-spacing:1px;">COINS</div>
                </div>
            </div>

            <!-- Items -->
            <div style="font-size:.7rem;color:rgba(255,255,255,.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;
                animation:fadeInUp .5s 1.1s both;opacity:0;">
                ITEMS RECEIVED
            </div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(90px,1fr));gap:8px;
                animation:fadeInUp .5s 1.2s both;opacity:0;">
                {items_html}
            </div>
        </div>
    </div>
    """
    return html

# ═══════════════════════════════════════════════════════════════
#  RANK UP ANIMATION
# ═══════════════════════════════════════════════════════════════
def render_rankup_animation(old_ovr: int, new_ovr: int):
    rank_idx = st.session_state.player_rank
    rank = RANKS[rank_idx]
    color = rank["color"]

    stars_html = ""
    for i in range(25):
        left  = random.randint(0, 100)
        delay = random.random() * 3
        dur   = 2 + random.random() * 3
        stars_html += f"""
        <div class="rstar" style="left:{left}%;bottom:-50px;
            animation-delay:{delay:.2f}s;animation-duration:{dur:.1f}s;">
            {'⭐' if random.random() > 0.5 else '✨'}
        </div>"""

    stat_html = ""
    for stat, boost in rank.get("stat_boost", {}).items():
        stat_html += f"""
        <span style="
            background:rgba(255,255,255,.08);border:1px solid {color}44;
            border-radius:6px;padding:3px 10px;font-size:.75rem;
            color:{color};font-weight:700;
        ">+{boost} {stat}</span> """

    return f"""
    <div style="
        background:radial-gradient(ellipse at center,rgba(0,0,0,.98) 60%,rgba(30,20,5,.98));
        border:1px solid {color}44;border-radius:20px;
        padding:40px 30px;text-align:center;max-width:520px;margin:0 auto;
        position:relative;overflow:hidden;
    ">
        <!-- Stars -->
        <div class="rankup-stars" style="position:absolute;inset:0;overflow:hidden;">{stars_html}</div>

        <!-- Glow bg -->
        <div style="
            position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
            width:300px;height:300px;border-radius:50%;
            background:radial-gradient(circle,{color}20 0%,transparent 70%);
            pointer-events:none;
        "></div>

        <div style="position:relative;z-index:2;">
            <!-- RANK UP text -->
            <div class="rankup-text" style="
                background:linear-gradient(90deg,{color},{color}88,{color});
                background-size:200%;
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                font-family:'Bebas Neue',sans-serif;font-size:4.5rem;
                letter-spacing:8px;line-height:1;
                animation:rankupBounce .6s cubic-bezier(.34,1.56,.64,1);
                filter:drop-shadow(0 0 30px {color}88);
            ">RANK UP!</div>

            <!-- Rank name -->
            <div style="
                font-family:'Orbitron',sans-serif;font-size:.9rem;
                color:{color};letter-spacing:4px;text-transform:uppercase;
                margin:8px 0;animation:fadeInUp .6s .3s both;opacity:0;
            ">{rank['icon']} {rank['name']} {rank['icon']}</div>

            <!-- OVR Change -->
            <div style="
                display:flex;align-items:center;justify-content:center;gap:16px;
                margin:20px 0;animation:fadeInUp .6s .6s both;opacity:0;
            ">
                <div style="
                    font-family:'Bebas Neue',sans-serif;font-size:3rem;
                    color:rgba(255,255,255,.3);text-decoration:line-through;
                ">{old_ovr}</div>
                <div style="font-size:2rem;color:{color};animation:arrowPulse 1s ease infinite;">➜</div>
                <div style="
                    font-family:'Bebas Neue',sans-serif;font-size:4.5rem;
                    color:{color};
                    filter:drop-shadow(0 0 20px {color}88);
                    line-height:1;
                ">{new_ovr}</div>
            </div>

            <!-- Bonus text -->
            <div style="
                background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
                border-radius:10px;padding:10px 16px;margin:10px 0;
                animation:fadeInUp .6s .9s both;opacity:0;
            ">
                <div style="font-size:.7rem;color:rgba(255,255,255,.4);letter-spacing:2px;margin-bottom:6px;">STAT BOOST</div>
                <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:6px;">{stat_html}</div>
            </div>

            <!-- Bonus description -->
            <div style="
                font-size:.8rem;color:rgba(255,255,255,.5);margin-top:10px;
                animation:fadeInUp .6s 1.1s both;opacity:0;
            ">{rank.get('bonus','')}</div>
        </div>
    </div>
    """

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    rank_idx = st.session_state.player_rank
    rank = RANKS[rank_idx]
    rank_color = rank["color"]
    ovr_val = st.session_state.player_ovr

    # Club badge
    st.markdown(f"""
    <div style="
        background:linear-gradient(145deg,#0D1117,#1C2333);
        border:1px solid {rank_color}44;border-radius:14px;
        padding:16px;text-align:center;margin-bottom:12px;
    ">
        <div style="font-size:2.5rem;">{st.session_state.club_badge}</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
            color:#FFD700;letter-spacing:2px;">{st.session_state.club_name}</div>
        <div style="font-size:.75rem;color:rgba(255,255,255,.4);margin-top:2px;">
            ⭐ {st.session_state.club_reputation:,} Reputation
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Player OVR mini
    st.markdown(f"""
    <div style="
        background:linear-gradient(145deg,#0a0510,#150a25);
        border:1.5px solid {rank_color};border-radius:12px;
        padding:12px;text-align:center;margin-bottom:12px;
        box-shadow:0 0 20px {rank_color}44;
    ">
        <div style="font-size:.65rem;letter-spacing:2px;color:{rank_color};font-weight:700;">{rank['icon']} {rank['name']}</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:3.5rem;color:{rank_color};
            filter:drop-shadow(0 0 12px {rank_color}88);line-height:1;margin:4px 0;">
            {ovr_val}
        </div>
        <div style="font-size:.75rem;color:rgba(255,255,255,.6);">ULTIMATE STRIKER · ST</div>
    </div>
    """, unsafe_allow_html=True)

    # XP progress
    needed = get_xp_for_next_rank()
    xp_pct = get_xp_progress_pct()
    xp_cur = st.session_state.player_xp

    if rank_idx < len(RANKS) - 1:
        next_r = RANKS[rank_idx + 1]
        st.markdown(f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:.7rem;color:rgba(255,255,255,.4);">XP Progress</span>
                <span style="font-size:.7rem;color:{next_r['color']};">→ {next_r['name']}</span>
            </div>
            <div style="background:#06090F;border-radius:8px;height:12px;border:1px solid #21262D;overflow:hidden;">
                <div style="
                    width:{xp_pct:.1f}%;height:100%;
                    background:linear-gradient(90deg,{rank_color},{next_r['color']});
                    border-radius:8px;transition:width .5s;
                    box-shadow:0 0 8px {rank_color}88;
                    position:relative;overflow:hidden;
                ">
                    <div style="position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);animation:progressShine 1.5s infinite;"></div>
                </div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:3px;">
                <span style="font-size:.65rem;color:{rank_color};">{xp_cur:,} XP</span>
                <span style="font-size:.65rem;color:rgba(255,255,255,.3);">{needed:,} needed</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if can_rank_up():
            st.markdown("""
            <div style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.4);border-radius:8px;padding:8px;text-align:center;margin-bottom:8px;animation:glowPulse 1.5s infinite;">
                <span style="color:#FFD700;font-weight:700;font-size:.8rem;">🏆 RANK UP TAYYOR!</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.4);border-radius:8px;padding:8px;text-align:center;margin-bottom:8px;">
            <span style="color:#F87171;font-weight:700;font-size:.8rem;">🌠 MAX DARAJAGA ERISHDINGIZ!</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Club settings
    st.markdown("**⚙️ Klub Sozlamalari**")
    new_name = st.text_input("Klub nomi:", value=st.session_state.club_name, key="club_name_input")
    if new_name != st.session_state.club_name:
        st.session_state.club_name = new_name

    badge_opts = ["🌠","⚽","🦁","🦅","🐉","⚡","🔥","💫","🌟","👑","🏆","⚔️","🛡️","🌈","💎","🌊","🔱","♦️"]
    sel_badge = st.selectbox("Badge:", badge_opts,
        index=badge_opts.index(st.session_state.club_badge) if st.session_state.club_badge in badge_opts else 0)
    st.session_state.club_badge = sel_badge

    st.markdown("---")

    # Quick stats
    st.markdown("**📊 Quick Stats**")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Packs", st.session_state.packs_opened)
        st.metric("Items", st.session_state.total_items_collected)
    with c2:
        st.metric("XP", f"{st.session_state.xp_collected:,}")
        st.metric("Ach", len(st.session_state.achievements))

    st.markdown("---")

    # Notifications
    st.markdown("**🔔 Xabarlar**")
    if st.session_state.notifications:
        for n in st.session_state.notifications[:6]:
            st.markdown(f"<div class='notif'>{n}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#7D8590;font-size:.8rem;'>Hali xabar yo'q</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="fc-header">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
            <div class="fc-header-title">⚽ EA FC MOBILE ULTIMATE</div>
            <div class="fc-header-sub">Pack Ochish • Rank Up 117→122 • Klub Rivojlantirish</div>
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:rgba(255,215,0,.08);border:1px solid rgba(255,215,0,.2);border-radius:10px;padding:8px 16px;text-align:center;">
                <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#FFD700;font-weight:700;">∞</div>
                <div style="font-size:.65rem;color:rgba(255,255,255,.4);letter-spacing:1px;">COINS</div>
            </div>
            <div style="background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.2);border-radius:10px;padding:8px 16px;text-align:center;">
                <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#38BDF8;font-weight:700;">∞</div>
                <div style="font-size:.65rem;color:rgba(255,255,255,.4);letter-spacing:1px;">GEMS</div>
            </div>
            <div style="background:rgba(192,132,252,.08);border:1px solid rgba(192,132,252,.2);border-radius:10px;padding:8px 16px;text-align:center;">
                <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#C084FC;font-weight:700;">{st.session_state.packs_opened}</div>
                <div style="font-size:.65rem;color:rgba(255,255,255,.4);letter-spacing:1px;">PACKS</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  RANK UP ANIMATION (shown at top when active)
# ═══════════════════════════════════════════════════════════════
if st.session_state.show_rankup_anim:
    st.markdown(render_rankup_animation(
        st.session_state.rankup_old_ovr,
        st.session_state.rankup_new_ovr
    ), unsafe_allow_html=True)

    col_close = st.columns([2,1,2])[1]
    with col_close:
        if st.button("✖ Yopish", key="close_rankup"):
            st.session_state.show_rankup_anim = False
            st.rerun()
    st.markdown("---")

# ═══════════════════════════════════════════════════════════════
#  PACK ANIMATION RESULT (shown at top when active)
# ═══════════════════════════════════════════════════════════════
if st.session_state.show_pack_anim and st.session_state.anim_result:
    pack_obj = next((p for p in PACKS if p["id"] == st.session_state.anim_pack_id), PACKS[0])
    st.markdown(render_pack_animation(pack_obj, st.session_state.anim_result), unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("✖ Yopish", key="close_pack_anim"):
            st.session_state.show_pack_anim = False
            st.session_state.anim_result = None
            # Check if rank up possible
            if can_rank_up():
                st.session_state.pending_rankup = True
            st.rerun()

    st.markdown("---")

# ═══════════════════════════════════════════════════════════════
#  RANK UP PROMPT
# ═══════════════════════════════════════════════════════════════
if can_rank_up() and not st.session_state.show_pack_anim and not st.session_state.show_rankup_anim:
    rank_idx = st.session_state.player_rank
    next_rank = RANKS[rank_idx + 1]
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,rgba(255,215,0,.12),rgba(255,165,0,.06));
        border:2px solid rgba(255,215,0,.5);border-radius:14px;
        padding:16px 24px;margin-bottom:16px;
        animation:glowPulse 1.5s ease-in-out infinite;
        display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;
    ">
        <div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#FFD700;letter-spacing:3px;">
                🏆 RANK UP TAYYOR!
            </div>
            <div style="color:rgba(255,215,0,.7);font-size:.85rem;margin-top:2px;">
                {st.session_state.player_ovr} OVR → {next_rank['ovr']} OVR · {next_rank['icon']} {next_rank['name']}
            </div>
            <div style="color:rgba(255,255,255,.5);font-size:.8rem;margin-top:2px;">
                Bonus: {next_rank.get('bonus','')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    rcol1, rcol2, rcol3 = st.columns([1, 1, 1])
    with rcol2:
        if st.button("🚀 RANK UP!", key="do_rankup_btn"):
            do_rank_up()
            st.rerun()

# ═══════════════════════════════════════════════════════════════
#  MAIN TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📦 PACK OCHISH",
    "⚡ O'YINCHI & RANK UP",
    "🏟️ KLUB",
    "🎒 INVENTAR",
    "📊 STATISTIKA",
    "🏅 YUTUQLAR",
])

# ═══════════════════════════════════════════════════════════════
#  TAB 1 — PACK OCHISH
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">📦 PACK DO\'KONI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
        💡 <strong>Barcha packlar BEPUL!</strong> Har bir pack XP, Coins va maxsus itemlar beradi.
        XP to'plang va o'yinchingizni 117 dan 122 OVR ga rank up qiling!
    </div>
    """, unsafe_allow_html=True)

    # Pack grid - 4 columns
    for row_start in range(0, len(PACKS), 4):
        row_packs = PACKS[row_start:row_start + 4]
        cols = st.columns(4)

        for i, pack in enumerate(row_packs):
            with cols[i]:
                # Pack card HTML
                style_map = {
                    "pack-gold":    "#FFD700",
                    "pack-elite":   "#38BDF8",
                    "pack-icon":    "#C084FC",
                    "pack-ultimate":"#F87171",
                    "pack-ucl":     "#60A5FA",
                    "pack-tots":    "#4ADE80",
                }
                accent_c = style_map.get(pack["style"], "#FFD700")

                tg_lv = st.session_state.club_levels.get("Training Ground", 0)
                xp_mult = [1.0,1.12,1.25,1.40,1.60,1.90][tg_lv]
                actual_xp = int(pack["xp_reward"] * xp_mult)

                st.markdown(f"""
                <div class="pack-card {pack['style']}">
                    <div>
                        <span class="pack-badge {pack['badge_cls']}">{pack['badge']}</span>
                        <div class="pack-icon-emoji">{pack['icon']}</div>
                        <div class="pack-title" style="color:{accent_c};">{pack['name']}</div>
                        <div class="pack-desc">{pack['desc']}</div>
                    </div>
                    <div>
                        <div style="font-size:.7rem;color:#4ADE80;font-weight:700;margin:4px 0;">
                            +{actual_xp:,} XP · +{pack['coins_reward']:,} 🪙
                        </div>
                        <div class="pack-count">{pack['count']} ITEM</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"▶ OCHISH", key=f"open_{pack['id']}"):
                    result = do_open_pack(pack["id"])
                    st.session_state.show_pack_anim = True
                    st.session_state.anim_pack_id = pack["id"]
                    st.session_state.anim_result = result
                    st.rerun()

    # ── Pack History ──
    if st.session_state.pack_history:
        st.markdown("---")
        st.markdown('<div class="sec-head">📜 PACK TARIXI</div>', unsafe_allow_html=True)

        # Summary
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("📦 Jami Pack", st.session_state.packs_opened)
        with sc2:
            st.metric("⚡ Jami XP", f"{st.session_state.xp_collected:,}")
        with sc3:
            st.metric("💰 Jami Coins", f"{st.session_state.coins_collected:,}")
        with sc4:
            st.metric("🎒 Jami Items", st.session_state.total_items_collected)

        # Last 10 packs table
        st.markdown("#### Son 10 ta Pack")
        for rec in reversed(st.session_state.pack_history[-10:]):
            p = next((x for x in PACKS if x["id"] == rec["pack_id"]), None)
            if not p:
                continue
            style_colors = {
                "pack-gold":"#FFD700","pack-elite":"#38BDF8","pack-icon":"#C084FC",
                "pack-ultimate":"#F87171","pack-ucl":"#60A5FA","pack-tots":"#4ADE80",
            }
            c = style_colors.get(p["style"], "#888")
            items_str = " ".join([ITEM_DEFS.get(it, {}).get("icon", "❓") for it in rec["items"]])
            st.markdown(f"""
            <div style="
                background:var(--dark3);border:1px solid {c}22;border-radius:10px;
                padding:10px 16px;margin:4px 0;
                display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;
            ">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:1.2rem;">{p['icon']}</span>
                    <div>
                        <div style="font-size:.85rem;font-weight:600;color:{c};">{rec['pack_name']}</div>
                        <div style="font-size:.7rem;color:rgba(255,255,255,.4);">{rec['ts']}</div>
                    </div>
                </div>
                <div style="display:flex;gap:16px;align-items:center;">
                    <span style="font-size:.8rem;color:#4ADE80;">+{rec['xp']:,} XP</span>
                    <span style="font-size:.8rem;color:#FFD700;">+{rec['coins']:,} 🪙</span>
                    <span style="font-size:1rem;">{items_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TAB 2 — O'YINCHI & RANK UP
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">⚡ O\'YINCHI PROFILI</div>', unsafe_allow_html=True)

    c_left, c_mid, c_right = st.columns([1, 1.2, 1])

    with c_mid:
        # Big player card
        st.markdown(render_player_mini_card(
            st.session_state.player_ovr,
            st.session_state.player_rank
        ), unsafe_allow_html=True)

        # Player info
        rank = RANKS[st.session_state.player_rank]
        st.markdown(f"""
        <div style="
            background:var(--dark3);border:1px solid var(--border);
            border-radius:12px;padding:16px;margin-top:12px;text-align:center;
        ">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:left;">
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Pozitsiya</span><div style="font-weight:700;">{PLAYER['pos']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Millat</span><div style="font-weight:700;">{PLAYER['nation_name']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Yosh</span><div style="font-weight:700;">{PLAYER['age']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Boy</span><div style="font-weight:700;">{PLAYER['height']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Oyoq</span><div style="font-weight:700;">{PLAYER['preferred_foot']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Work Rate</span><div style="font-weight:700;font-size:.8rem;">{PLAYER['work_rate']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Skill Moves</span><div style="font-weight:700;">{'⭐'*PLAYER['skill_moves']}</div></div>
                <div><span style="color:rgba(255,255,255,.4);font-size:.7rem;">Weak Foot</span><div style="font-weight:700;">{'⭐'*PLAYER['weak_foot']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_left:
        st.markdown("#### 📊 Asosiy Statlar")
        main_stats = [
            ("PAC", st.session_state.player_stats.get("PAC", 96)),
            ("SHO", st.session_state.player_stats.get("SHO", 97)),
            ("PAS", st.session_state.player_stats.get("PAS", 94)),
            ("DRI", st.session_state.player_stats.get("DRI", 98)),
            ("DEF", st.session_state.player_stats.get("DEF", 72)),
            ("PHY", st.session_state.player_stats.get("PHY", 95)),
        ]
        for sname, sval in main_stats:
            color = get_stat_color(sval)
            st.markdown(f"""
            <div class="stat-row">
                <span class="stat-lbl" style="color:{color};">{sname}</span>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill" style="width:{sval}%;background:{color};"></div>
                </div>
                <span class="stat-val" style="color:{color};">{sval}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🏅 Rank Tarixi")
        for i, r in enumerate(RANKS):
            done = i <= st.session_state.player_rank
            current = i == st.session_state.player_rank
            bg = f"background:rgba({','.join(str(int(r['color'].lstrip('#')[j:j+2],16)) for j in (0,2,4))},.1)" if done else "background:var(--dark3)"
            border = f"border:1.5px solid {r['color']}" if current else f"border:1px solid {'rgba(255,255,255,.1)' if done else 'var(--border)'}"
            st.markdown(f"""
            <div style="
                {bg};{border};border-radius:8px;
                padding:8px 12px;margin:3px 0;
                display:flex;align-items:center;gap:10px;
                {'filter:grayscale(.7)' if not done else ''}
            ">
                <span style="font-size:1.2rem;">{r['icon']}</span>
                <div style="flex:1;">
                    <div style="font-weight:700;font-size:.85rem;color:{'#fff' if done else '#7D8590'};">{r['name']}</div>
                    <div style="font-size:.65rem;color:rgba(255,255,255,.4);">OVR {r['ovr']}</div>
                </div>
                <div style="font-size:.8rem;color:{r['color']};font-weight:700;">{'✅' if done else ('🔒' if not done else '')}</div>
            </div>
            """, unsafe_allow_html=True)

    with c_right:
        st.markdown("#### ⭐ To'liq Statlar")
        detail_stats = [
            ("Tezlik", st.session_state.player_stats.get("Tezlik", 96)),
            ("Tezlashtirish", st.session_state.player_stats.get("Tezlashtirish", 95)),
            ("Uzoq Zarbalar", st.session_state.player_stats.get("Uzoq Zarbalar", 97)),
            ("Penalties", st.session_state.player_stats.get("Penalties", 99)),
            ("Finishing", st.session_state.player_stats.get("Finishing", 98)),
            ("Q. Uzatmalar", st.session_state.player_stats.get("Qisqa Uzatmalar", 95)),
            ("U. Uzatmalar", st.session_state.player_stats.get("Uzoq Uzatmalar", 93)),
            ("Ko'rishlik", st.session_state.player_stats.get("Ko'rishlik", 97)),
            ("Top Nazorat", st.session_state.player_stats.get("Top Nazorat", 99)),
            ("Dribbling", st.session_state.player_stats.get("Dribbling", 98)),
            ("Chapaqaylik", st.session_state.player_stats.get("Chapaqaylik", 89)),
            ("Sakrash", st.session_state.player_stats.get("Sakrash", 94)),
            ("Muvozanat", st.session_state.player_stats.get("Muvozanat", 93)),
            ("Kuch", st.session_state.player_stats.get("Kuch", 96)),
            ("Tajovuz", st.session_state.player_stats.get("Tajovuz", 92)),
        ]
        for sname, sval in detail_stats:
            color = get_stat_color(sval)
            bar_w = min(100, sval)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                <span style="width:95px;font-size:.7rem;color:rgba(255,255,255,.5);text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{sname}</span>
                <div style="flex:1;background:rgba(255,255,255,.04);border-radius:3px;height:6px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{color};border-radius:3px;"></div>
                </div>
                <span style="width:22px;font-size:.75rem;font-weight:700;color:{color};">{sval}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Rank Up Section ──
    st.markdown("---")
    st.markdown('<div class="sec-head">🚀 RANK UP TIZIMI</div>', unsafe_allow_html=True)

    rank_cols = st.columns(len(RANKS))
    for i, r in enumerate(RANKS):
        with rank_cols[i]:
            done = i <= st.session_state.player_rank
            current = i == st.session_state.player_rank
            color = r["color"]
            bg = "linear-gradient(145deg,rgba(30,20,5,.9),rgba(20,10,0,.9))" if done else "var(--dark3)"
            brd = f"border:2px solid {color}" if current else f"border:1px solid {color}44" if done else "border:1px solid var(--border)"

            if i == 0:
                xp_txt = "—"
                bonus_txt = "Boshlang'ich daraja"
            else:
                xp_txt = f"{r['xp_req']:,} XP"
                bonus_txt = r.get("bonus", "")

            st.markdown(f"""
            <div style="
                {bg};{brd};border-radius:12px;padding:14px 10px;text-align:center;
                {'box-shadow:0 0 20px '+ color + '44' if current else ''}
                {'filter:grayscale(.6)' if not done else ''}
                transition:all .2s;
            ">
                <div style="font-size:1.8rem;margin-bottom:4px;">{r['icon']}</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:{color};line-height:1;">{r['ovr']}</div>
                <div style="font-size:.7rem;color:{color};font-weight:700;letter-spacing:1px;margin:4px 0;">{r['name']}</div>
                <div style="font-size:.65rem;color:rgba(255,255,255,.4);margin-bottom:6px;">{xp_txt}</div>
                <div style="font-size:.65rem;color:rgba(255,255,255,.6);line-height:1.4;">{bonus_txt}</div>
                {'<div style="color:#4ADE80;font-size:.7rem;margin-top:6px;font-weight:700;">✅ OLINGAN</div>' if done and not current else ''}
                {'<div style="color:'+color+';font-size:.7rem;margin-top:6px;font-weight:700;animation:glowPulse 1.5s infinite;">▶ JORIY</div>' if current else ''}
                {'<div style="color:rgba(255,255,255,.3);font-size:.7rem;margin-top:6px;">🔒 Qulfli</div>' if not done else ''}
            </div>
            """, unsafe_allow_html=True)

    # Rank up buttons
    st.markdown("---")
    ru_c1, ru_c2, ru_c3 = st.columns([1, 2, 1])
    with ru_c2:
        rank_idx = st.session_state.player_rank
        xp_needed = get_xp_for_next_rank()
        xp_have   = st.session_state.player_xp
        xp_pct2   = get_xp_progress_pct()

        if rank_idx < len(RANKS) - 1:
            next_r = RANKS[rank_idx + 1]
            st.markdown(f"""
            <div style="
                background:linear-gradient(145deg,var(--dark3),var(--dark2));
                border:1.5px solid {next_r['color']}44;border-radius:14px;
                padding:20px;text-align:center;
            ">
                <div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:2px;margin-bottom:4px;">KEYINGI RANK</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:{next_r['color']};">
                    {next_r['icon']} {next_r['name']} — OVR {next_r['ovr']}
                </div>
                <div style="font-size:.8rem;color:rgba(255,255,255,.5);margin:8px 0;">{next_r.get('bonus','')}</div>

                <div style="background:var(--dark);border-radius:8px;height:14px;border:1px solid var(--border);overflow:hidden;margin:10px 0;">
                    <div style="width:{xp_pct2:.1f}%;height:100%;
                        background:linear-gradient(90deg,{RANKS[rank_idx]['color']},{next_r['color']});
                        border-radius:8px;transition:width .5s;
                        box-shadow:0 0 8px {next_r['color']}88;
                        position:relative;overflow:hidden;">
                        <div style="position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);animation:progressShine 1.5s infinite;"></div>
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:.75rem;color:rgba(255,255,255,.4);margin-bottom:12px;">
                    <span style="color:{next_r['color']};">{xp_have:,} XP</span>
                    <span>{xp_needed:,} kerak</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if can_rank_up():
                if st.button(f"🚀 RANK UP! ({st.session_state.player_ovr} → {next_r['ovr']})", key="rankup_main"):
                    do_rank_up()
                    st.rerun()
            else:
                remaining = xp_needed - xp_have
                st.markdown(f"""
                <div class="info-box">
                    📊 Rank up uchun yana <strong>{remaining:,} XP</strong> kerak.
                    Pack oching yoki inventory itemlarini ishlating!
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background:linear-gradient(145deg,rgba(248,113,113,.15),rgba(248,113,113,.05));
                border:2px solid #F87171;border-radius:14px;padding:24px;text-align:center;
            ">
                <div style="font-size:3rem;margin-bottom:8px;">🌠</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#F87171;letter-spacing:3px;">ULTIMATE ICON!</div>
                <div style="color:rgba(255,255,255,.6);margin-top:8px;">Siz eng yuqori darajaga erishdingiz — OVR 122!</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TAB 3 — KLUB
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">🏟️ KLUB RIVOJLANTIRISH</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
        💡 Barcha yaxshilanishlar <strong>BEPUL</strong>! Har bir bino maxsus bonuslar beradi.
        Training Ground XP ni oshiradi, Stadium ko'proq Coin beradi, Scout yaxshiroq itemlar beradi.
    </div>
    """, unsafe_allow_html=True)

    # Club overview
    total_upg = sum(st.session_state.club_levels.values())
    max_upg   = len(CLUB_UPGRADES) * 5
    upg_pct   = (total_upg / max_upg * 100) if max_upg > 0 else 0

    st.markdown(f"""
    <div style="
        background:linear-gradient(145deg,var(--dark3),var(--dark2));
        border:1.5px solid rgba(192,132,252,.3);border-radius:14px;
        padding:20px;margin-bottom:16px;
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:2px;color:#C084FC;">
                    🏰 KLUB UMUMIY RIVOJLANISH
                </div>
                <div style="font-size:.8rem;color:rgba(255,255,255,.4);margin-top:2px;">
                    ⭐ {st.session_state.club_reputation:,} Reputation
                </div>
            </div>
            <div style="font-family:'Orbitron',sans-serif;font-size:1.5rem;color:#FFD700;font-weight:700;">
                {total_upg}/{max_upg}
            </div>
        </div>
        <div style="background:var(--dark);border-radius:8px;height:12px;border:1px solid var(--border);overflow:hidden;">
            <div style="width:{upg_pct:.1f}%;height:100%;
                background:linear-gradient(90deg,#7C3AED,#C084FC);
                border-radius:8px;transition:width .5s;
                box-shadow:0 0 10px rgba(192,132,252,.5);
                position:relative;overflow:hidden;">
                <div style="position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);animation:progressShine 1.5s infinite;"></div>
            </div>
        </div>
        <div style="font-size:.75rem;color:rgba(255,255,255,.3);margin-top:4px;">{upg_pct:.1f}% to'liq</div>
    </div>
    """, unsafe_allow_html=True)

    # All upgrades
    upg_cols = st.columns(2)
    for idx, (upg_name, upg_data) in enumerate(CLUB_UPGRADES.items()):
        with upg_cols[idx % 2]:
            current_lv = st.session_state.club_levels[upg_name]
            max_lv     = upg_data["max_lv"]
            lv_data    = upg_data["levels"][current_lv]
            lv_color   = lv_data["color"]
            lv_pct     = (current_lv / max_lv * 100)

            # Next level
            next_lv_data = upg_data["levels"][current_lv + 1] if current_lv < max_lv else None

            st.markdown(f"""
            <div class="upg-box" style="border-color:{lv_color}22;">
                <div class="upg-header">
                    <div>
                        <div style="font-size:1.6rem;margin-bottom:4px;">{upg_data['icon']}</div>
                        <div class="upg-name">{upg_name}</div>
                        <div style="font-size:.75rem;color:rgba(255,255,255,.4);">{upg_data['desc']}</div>
                    </div>
                    <div class="upg-lvl-badge" style="
                        background:rgba({','.join(str(int(lv_color.lstrip('#')[j:j+2],16)) for j in (0,2,4))},.1);
                        color:{lv_color};
                        border:1px solid {lv_color}44;
                    ">LVL {current_lv}/{max_lv}</div>
                </div>

                <div class="upg-progress">
                    <div class="upg-progress-fill" style="width:{lv_pct:.0f}%;background:linear-gradient(90deg,{lv_color},{lv_color}88);"></div>
                </div>

                <div class="upg-current-bonus">
                    ✅ Joriy: <strong>{lv_data['name']}</strong> — {lv_data['bonus']}
                </div>
                {f'<div class="upg-next-bonus">➡ Keyingi: <strong>{next_lv_data["name"]}</strong> — {next_lv_data["bonus"]}</div>' if next_lv_data else ''}
            </div>
            """, unsafe_allow_html=True)

            if current_lv < max_lv:
                if st.button(f"⬆ Yaxshilash ({upg_name})", key=f"upg_{upg_name}"):
                    st.session_state.club_levels[upg_name] += 1
                    bonus_rep = 300 * st.session_state.club_levels[upg_name]
                    st.session_state.club_reputation += bonus_rep
                    new_lv = st.session_state.club_levels[upg_name]
                    new_info = CLUB_UPGRADES[upg_name]["levels"][new_lv]
                    add_notif(f"{upg_name} LVL {new_lv}! {new_info['bonus']} bonus!", "🏗️")
                    grant_achievement("upg_one")
                    # Check all max
                    if all(v >= 5 for v in st.session_state.club_levels.values()):
                        grant_achievement("upg_all_max")
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="
                    background:rgba({','.join(str(int(lv_color.lstrip('#')[j:j+2],16)) for j in (0,2,4))},.1);
                    border:1px solid {lv_color}44;border-radius:8px;
                    padding:8px;text-align:center;
                    font-family:'Bebas Neue',sans-serif;font-size:.9rem;
                    letter-spacing:1px;color:{lv_color};
                ">🏆 MAX DARAJA!</div>
                """, unsafe_allow_html=True)

    # Active bonuses summary
    st.markdown("---")
    st.markdown('<div class="sec-head">🎁 FAOL BONUSLAR</div>', unsafe_allow_html=True)

    active_bonuses = []
    for upg_name, upg_data in CLUB_UPGRADES.items():
        lv = st.session_state.club_levels[upg_name]
        if lv > 0:
            lv_d = upg_data["levels"][lv]
            active_bonuses.append({
                "icon": upg_data["icon"],
                "name": upg_name,
                "lv_name": lv_d["name"],
                "bonus": lv_d["bonus"],
                "color": lv_d["color"],
            })

    if active_bonuses:
        ab_cols = st.columns(3)
        for i, ab in enumerate(active_bonuses):
            with ab_cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background:linear-gradient(145deg,rgba({','.join(str(int(ab['color'].lstrip('#')[j:j+2],16)) for j in (0,2,4))},.08),var(--dark3));
                    border:1px solid {ab['color']}33;border-radius:10px;
                    padding:12px;margin-bottom:8px;
                ">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                        <span style="font-size:1.3rem;">{ab['icon']}</span>
                        <span style="font-weight:700;font-size:.85rem;">{ab['name']}</span>
                    </div>
                    <div style="font-size:.75rem;color:rgba(255,255,255,.4);">{ab['lv_name']}</div>
                    <div style="font-size:.85rem;color:{ab['color']};font-weight:700;margin-top:3px;">{ab['bonus']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            Hali hech qanday bonus yo'q. Yuqoridagi binolarni yaxshilang!
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TAB 4 — INVENTAR
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">🎒 INVENTAR</div>', unsafe_allow_html=True)

    inv = st.session_state.inventory

    if not inv:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,.3);">
            <div style="font-size:3rem;margin-bottom:12px;">📭</div>
            <div style="font-size:1.1rem;">Inventar bo'sh.</div>
            <div style="font-size:.85rem;margin-top:6px;">Pack oching va itemlar to'plang!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary by type
        item_counts = {}
        for it in inv:
            item_counts[it["id"]] = item_counts.get(it["id"], 0) + 1

        summ_cols = st.columns(min(len(item_counts), 4))
        for i, (iid, count) in enumerate(item_counts.items()):
            idef = ITEM_DEFS.get(iid, {"name": iid, "icon": "❓", "color": "#888"})
            with summ_cols[i % min(len(item_counts), 4)]:
                st.markdown(f"""
                <div style="
                    background:rgba({','.join(str(int(idef['color'].lstrip('#')[j:j+2],16)) for j in (0,2,4)) if len(idef['color'])==7 else '100,100,100'},.08);
                    border:1px solid {idef['color']}44;border-radius:10px;
                    padding:12px;text-align:center;margin-bottom:8px;
                ">
                    <div style="font-size:2rem;">{idef['icon']}</div>
                    <div style="font-size:.8rem;font-weight:700;color:{idef['color']};margin-top:4px;">{idef['name']}</div>
                    <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#fff;font-weight:700;">×{count}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"#### 📋 Barcha Itemlar ({len(inv)} ta)")

        # Group and display
        inv_display_cols = st.columns(4)
        for slot_idx, item in enumerate(inv):
            idef = ITEM_DEFS.get(item["id"], {"name": item["id"], "icon": "❓", "color": "#888", "xp": 0})
            with inv_display_cols[slot_idx % 4]:
                st.markdown(f"""
                <div style="
                    background:var(--dark3);border:1px solid {idef['color']}33;
                    border-radius:10px;padding:12px;text-align:center;margin-bottom:6px;
                    transition:border-color .2s;
                ">
                    <div style="font-size:2rem;">{idef['icon']}</div>
                    <div style="font-size:.8rem;font-weight:700;color:{idef['color']};margin:4px 0;">{idef['name']}</div>
                    <div style="font-size:.65rem;color:rgba(255,255,255,.4);">{item['ts']}</div>
                    {f'<div style="font-size:.7rem;color:#4ADE80;margin-top:2px;">+{idef["xp"]:,} XP</div>' if idef.get("xp",0) > 0 else ''}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"▶ Ishlatish", key=f"use_{slot_idx}"):
                    use_item(item["id"], slot_idx)
                    # Check if rank up possible after using
                    if can_rank_up():
                        st.session_state.pending_rankup = True
                    st.rerun()

# ═══════════════════════════════════════════════════════════════
#  TAB 5 — STATISTIKA
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-head">📊 TO\'LIQ STATISTIKA</div>', unsafe_allow_html=True)

    # Main metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("📦 Packs",  st.session_state.packs_opened)
    with m2: st.metric("⚡ XP",     f"{st.session_state.xp_collected:,}")
    with m3: st.metric("💰 Coins",  f"{st.session_state.coins_collected:,}")
    with m4: st.metric("🏅 Ach",    len(st.session_state.achievements))

    m5, m6, m7, m8 = st.columns(4)
    with m5: st.metric("🎒 Items",  st.session_state.total_items_collected)
    with m6: st.metric("⚽ OVR",    st.session_state.player_ovr)
    with m7: st.metric("🏟️ Upgrades", sum(st.session_state.club_levels.values()))
    with m8: st.metric("⭐ Rep",    f"{st.session_state.club_reputation:,}")

    st.markdown("---")

    c_stat1, c_stat2 = st.columns(2)

    with c_stat1:
        st.markdown("#### 🎯 O'yinchi Statlar Comparasyon")

        stat_compare = [
            ("PAC", PLAYER["base_stats"]["PAC"], st.session_state.player_stats.get("PAC", 96)),
            ("SHO", PLAYER["base_stats"]["SHO"], st.session_state.player_stats.get("SHO", 97)),
            ("PAS", PLAYER["base_stats"]["PAS"], st.session_state.player_stats.get("PAS", 94)),
            ("DRI", PLAYER["base_stats"]["DRI"], st.session_state.player_stats.get("DRI", 98)),
            ("DEF", PLAYER["base_stats"]["DEF"], st.session_state.player_stats.get("DEF", 72)),
            ("PHY", PLAYER["base_stats"]["PHY"], st.session_state.player_stats.get("PHY", 95)),
        ]

        for sn, base, current in stat_compare:
            boost = current - base
            boost_str = f"+{boost}" if boost > 0 else str(boost)
            color = get_stat_color(current)
            st.markdown(f"""
            <div style="margin:8px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="font-size:.8rem;font-weight:700;">{sn}</span>
                    <div>
                        <span style="font-size:.75rem;color:rgba(255,255,255,.4);">{base} → </span>
                        <span style="font-size:.85rem;font-weight:700;color:{color};">{current}</span>
                        {'<span style="font-size:.7rem;color:#4ADE80;margin-left:4px;">'+boost_str+'</span>' if boost > 0 else ''}
                    </div>
                </div>
                <div style="display:flex;gap:4px;height:8px;">
                    <div style="flex:{base};background:#3B82F666;border-radius:3px 0 0 3px;"></div>
                    <div style="flex:{current-base if current>base else 0};background:#4ADE80;border-radius:0 3px 3px 0;"></div>
                    <div style="flex:{100-current};background:rgba(255,255,255,.04);border-radius:0 3px 3px 0;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c_stat2:
        st.markdown("#### 🏟️ Klub Rivojlanish Grafigi")

        for upg_name, upg_data in CLUB_UPGRADES.items():
            lv = st.session_state.club_levels[upg_name]
            lv_d = upg_data["levels"][lv]
            pct = (lv / upg_data["max_lv"] * 100)
            color = lv_d["color"]

            st.markdown(f"""
            <div style="margin:6px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="font-size:.8rem;">{upg_data['icon']} {upg_name}</span>
                    <span style="font-size:.75rem;color:{color};font-weight:700;">LVL {lv}/{upg_data['max_lv']}</span>
                </div>
                <div style="background:rgba(255,255,255,.04);border-radius:5px;height:10px;overflow:hidden;">
                    <div style="width:{pct:.0f}%;height:100%;background:{color};border-radius:5px;
                        box-shadow:0 0 6px {color}88;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Pack breakdown
    if st.session_state.pack_history:
        st.markdown("#### 📦 Pack Turi bo'yicha")
        pack_type_counts = {}
        pack_type_xp = {}
        for rec in st.session_state.pack_history:
            pid = rec["pack_id"]
            pack_type_counts[pid] = pack_type_counts.get(pid, 0) + 1
            pack_type_xp[pid] = pack_type_xp.get(pid, 0) + rec["xp"]

        pt_cols = st.columns(min(len(pack_type_counts), 4))
        for i, (pid, cnt) in enumerate(sorted(pack_type_counts.items(), key=lambda x: -x[1])):
            p = next((x for x in PACKS if x["id"] == pid), None)
            if not p: continue
            style_colors2 = {
                "pack-gold":"#FFD700","pack-elite":"#38BDF8","pack-icon":"#C084FC",
                "pack-ultimate":"#F87171","pack-ucl":"#60A5FA","pack-tots":"#4ADE80",
            }
            c2 = style_colors2.get(p["style"], "#888")
            with pt_cols[i % min(len(pack_type_counts), 4)]:
                st.markdown(f"""
                <div style="
                    background:rgba({','.join(str(int(c2.lstrip('#')[j:j+2],16)) for j in (0,2,4))},.06);
                    border:1px solid {c2}33;border-radius:10px;padding:12px;text-align:center;
                ">
                    <div style="font-size:1.8rem;">{p['icon']}</div>
                    <div style="font-size:.75rem;color:{c2};font-weight:700;">{p['name']}</div>
                    <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#fff;font-weight:700;">×{cnt}</div>
                    <div style="font-size:.7rem;color:#4ADE80;margin-top:2px;">+{pack_type_xp[pid]:,} XP</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            Statistika ko'rish uchun pack oching!
        </div>
        """, unsafe_allow_html=True)

    # XP to max breakdown
    st.markdown("---")
    st.markdown("#### 🚀 Max Darajaga Masofa")

    current_rank_idx = st.session_state.player_rank
    current_xp = st.session_state.player_xp

    remaining_total = 0
    for i in range(current_rank_idx + 1, len(RANKS)):
        remaining_total += RANKS[i]["xp_req"]
    remaining_total -= current_xp

    if current_rank_idx < len(RANKS) - 1:
        st.markdown(f"""
        <div style="
            background:linear-gradient(145deg,var(--dark3),var(--dark2));
            border:1.5px solid rgba(248,113,113,.3);border-radius:14px;padding:20px;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div>
                    <div style="font-size:.8rem;color:rgba(255,255,255,.4);">OVR 122 (ULTIMATE ICON) ga</div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#F87171;">
                        Yana {max(0,remaining_total):,} XP kerak
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:.75rem;color:rgba(255,255,255,.4);">Joriy rank</div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#FFD700;">
                        {RANKS[current_rank_idx]['name']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Step by step remaining
        for i in range(current_rank_idx + 1, len(RANKS)):
            r = RANKS[i]
            xp_req = r["xp_req"]
            done_fraction = min(1.0, current_xp / xp_req) if i == current_rank_idx + 1 else 0
            pct = done_fraction * 100
            st.markdown(f"""
            <div style="margin:6px 0;display:flex;align-items:center;gap:12px;">
                <span style="font-size:1rem;">{r['icon']}</span>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
                        <span style="font-size:.75rem;color:{r['color']};">{r['name']}</span>
                        <span style="font-size:.7rem;color:rgba(255,255,255,.4);">{xp_req:,} XP</span>
                    </div>
                    <div style="background:rgba(255,255,255,.05);border-radius:4px;height:8px;overflow:hidden;">
                        <div style="width:{pct:.0f}%;height:100%;background:{r['color']};border-radius:4px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background:linear-gradient(145deg,rgba(248,113,113,.1),rgba(248,113,113,.05));
            border:2px solid #F87171;border-radius:14px;padding:20px;text-align:center;
        ">
            <div style="font-size:2rem;">🌠</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#F87171;margin-top:8px;">
                ULTIMATE ICON — OVR 122 OLINGAN!
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TAB 6 — YUTUQLAR
# ═══════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="sec-head">🏅 YUTUQLAR</div>', unsafe_allow_html=True)

    unlocked_count = len(st.session_state.achievements)
    total_ach = len(ACHIEVEMENTS)
    ach_pct = (unlocked_count / total_ach * 100) if total_ach > 0 else 0

    # Progress overview
    st.markdown(f"""
    <div style="
        background:linear-gradient(145deg,var(--dark3),var(--dark2));
        border:1.5px solid rgba(255,215,0,.3);border-radius:14px;
        padding:20px;margin-bottom:16px;
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#FFD700;letter-spacing:2px;">
                    🏆 YUTUQLAR PROGRESSI
                </div>
                <div style="font-size:.8rem;color:rgba(255,255,255,.4);margin-top:2px;">
                    Jami: {unlocked_count}/{total_ach} bajarilgan
                </div>
            </div>
            <div style="font-family:'Orbitron',sans-serif;font-size:1.8rem;color:#FFD700;font-weight:700;">
                {ach_pct:.0f}%
            </div>
        </div>
        <div style="background:var(--dark);border-radius:8px;height:14px;border:1px solid var(--border);overflow:hidden;">
            <div style="width:{ach_pct:.1f}%;height:100%;
                background:linear-gradient(90deg,#FFD700,#FFA500);
                border-radius:8px;transition:width .5s;
                box-shadow:0 0 10px rgba(255,215,0,.4);
                position:relative;overflow:hidden;">
                <div style="position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);animation:progressShine 1.5s infinite;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter tabs
    show_filter = st.radio("Filtr:", ["Barchasi", "Bajarilgan", "Qulfli"], horizontal=True, key="ach_filter")

    filtered_achs = ACHIEVEMENTS
    if show_filter == "Bajarilgan":
        filtered_achs = [a for a in ACHIEVEMENTS if a["id"] in st.session_state.achievements]
    elif show_filter == "Qulfli":
        filtered_achs = [a for a in ACHIEVEMENTS if a["id"] not in st.session_state.achievements]

    ach_cols2 = st.columns(2)
    for i, ach in enumerate(filtered_achs):
        unlocked = ach["id"] in st.session_state.achievements
        with ach_cols2[i % 2]:
            st.markdown(f"""
            <div class="ach-card {'unlocked' if unlocked else 'locked'}">
                <div class="ach-icon">{ach['icon']}</div>
                <div style="flex:1;">
                    <div class="ach-name">{ach['name']}</div>
                    <div class="ach-desc">{ach['desc']}</div>
                    <div class="ach-reward">🎁 {ach['reward']}</div>
                </div>
                <div class="ach-status {'status-done' if unlocked else 'status-lock'}">
                    {'✅ BAJARILDI' if unlocked else '🔒 Qulfli'}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick complete buttons (cheats)
    st.markdown("---")
    st.markdown('<div class="sec-head">⚡ TEZKOR BUYRUQLAR</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
        ⚠️ Bu yerda tezkor XP qo'shish va boshqa buyruqlar bor.
    </div>
    """, unsafe_allow_html=True)

    btn_cols = st.columns(4)
    with btn_cols[0]:
        if st.button("⚡ +1000 XP", key="add_xp_1k"):
            st.session_state.player_xp += 1000
            st.session_state.xp_collected += 1000
            add_notif("+1,000 XP qo'shildi!", "⚡")
            st.rerun()
    with btn_cols[1]:
        if st.button("🔥 +5000 XP", key="add_xp_5k"):
            st.session_state.player_xp += 5000
            st.session_state.xp_collected += 5000
            add_notif("+5,000 XP qo'shildi!", "🔥")
            st.rerun()
    with btn_cols[2]:
        if st.button("💎 +10000 XP", key="add_xp_10k"):
            st.session_state.player_xp += 10000
            st.session_state.xp_collected += 10000
            add_notif("+10,000 XP qo'shildi!", "💎")
            st.rerun()
    with btn_cols[3]:
        if st.button("🌠 MAX XP", key="add_xp_max"):
            # Enough for all ranks
            st.session_state.player_xp += 100000
            st.session_state.xp_collected += 100000
            add_notif("+100,000 XP! Barcha ranklar tayyor!", "🌠")
            st.rerun()

    btn_cols2 = st.columns(4)
    with btn_cols2[0]:
        if st.button("💰 +100K Coins", key="add_coins"):
            st.session_state.coins += 100000
            st.session_state.coins_collected += 100000
            add_notif("+100,000 Coins!", "💰")
            st.rerun()
    with btn_cols2[1]:
        if st.button("🔮 Mega Potion", key="give_mega_pot"):
            st.session_state.inventory.append({"id": "xp_potion_mega", "ts": datetime.now().strftime("%H:%M")})
            st.session_state.total_items_collected += 1
            add_notif("XP Mega Potion inventarga qo'shildi!", "🔮")
            st.rerun()
    with btn_cols2[2]:
        if st.button("🏅 Rank Token x3", key="give_rank_tokens"):
            for _ in range(3):
                st.session_state.inventory.append({"id": "rank_token", "ts": datetime.now().strftime("%H:%M")})
            st.session_state.total_items_collected += 3
            add_notif("3 ta Rank Token qo'shildi!", "🏅")
            st.rerun()
    with btn_cols2[3]:
        if st.button("🏗️ Klub MAX", key="max_all_upg"):
            for k in st.session_state.club_levels:
                st.session_state.club_levels[k] = 5
            st.session_state.club_reputation += 50000
            add_notif("Barcha klub binolari MAX darajaga olib chiqildi!", "🏰")
            grant_achievement("upg_one")
            grant_achievement("upg_all_max")
            st.rerun()

    # Tips
    st.markdown("---")
    st.markdown('<div class="sec-head">💡 O\'YIN MASLAHATLARI</div>', unsafe_allow_html=True)

    tips = [
        ("📦", "Pack Ochish",      "Ultimate Pack eng ko'p XP beradi (10,000 XP). Rank up uchun tez-tez oching."),
        ("🚀", "Rank Up",          "XP yig'ing va 117 OVR dan 122 OVR ga qadar 5 ta rank bosqichini o'ting."),
        ("🏟️", "Training Ground",  "Training Ground MAX darajasida XP ×1.9 ko'payadi — eng muhim bino!"),
        ("🎒", "Inventar",         "XP Potionlarni ishlating — Mega Potion bir marta +5000 XP beradi."),
        ("⚡", "Tezkor XP",        "Yutuqlar tabida MAX XP tugmasini bosing va darhol rank up qiling!"),
        ("🌠", "Ultimate Icon",    "OVR 122 ga erishgandan so'ng barcha statlar maksimal darajada bo'ladi."),
        ("📊", "Stat Cards",       "Inventardagi Stat Card lar tasodifiy stat ni +1 yoki +2 oshiradi."),
        ("🏅", "Achievementlar",   "Barcha achievementlarni yig'ib COMPLETIONIST unvonini oling!"),
    ]

    tip_cols2 = st.columns(4)
    for i, (icon, title, desc) in enumerate(tips):
        with tip_cols2[i % 4]:
            st.markdown(f"""
            <div style="
                background:var(--dark3);border:1px solid var(--border);
                border-radius:10px;padding:12px;margin-bottom:8px;
                transition:border-color .2s;
            " onmouseenter="this.style.borderColor='rgba(74,222,128,.3)'"
              onmouseleave="this.style.borderColor='var(--border)'">
                <div style="font-size:1.4rem;margin-bottom:6px;">{icon}</div>
                <div style="font-weight:700;color:#FFD700;font-size:.85rem;margin-bottom:4px;">{title}</div>
                <div style="font-size:.75rem;color:rgba(255,255,255,.5);line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    text-align:center;padding:24px;
    color:rgba(255,255,255,.2);font-size:.75rem;
    border-top:1px solid var(--border);margin-top:30px;
">
    <div style="margin-bottom:4px;">
        ⚽ EA FC Mobile Ultimate Simulator
    </div>
    <div>
        Barcha packlar bepul · Cheksiz pul · OVR 117 → 122 · Claude AI tomonidan yaratilgan
    </div>
</div>
""", unsafe_allow_html=True)
