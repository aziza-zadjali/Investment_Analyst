"""
Investment Analyst AI – Regulus Edition
Grey Dashboard Toggle Button - FIXED
"""
import streamlit as st
import base64
import os
from datetime import datetime
from utils.qdb_styling import (
    apply_qdb_styling,
    QDB_PURPLE,
    QDB_DARK_BLUE,
    qdb_section_start,
    qdb_section_end,
)

# --- Page configuration
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== SESSION STATE FOR DASHBOARD TOGGLE =====
if 'dashboard_expanded' not in st.session_state:
    st.session_state.dashboard_expanded = True

# ===== HERO SECTION (FULL-WIDTH) =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 60px 20px 80px 20px;
    position: relative;
    overflow:visible;
    width: calc(100% + 6rem);">

  <!-- Left: QDB -->
  <div style="position:absolute; top:18px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:65px;">' if qdb_logo else '<b>QDB</b>'}
  </div>

  <!-- Right: Regulus -->
  <div style="position:absolute; top:18px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:65px;">' if regulus_logo else '<b>Regulus</b>'}
  </div>

  <div style="max-width:900px; margin:0 auto;">
    <h1 style="font-size:2.2rem; font-weight:800; margin-bottom:8px;">Investment Analyst AI – Regulus Edition</h1>
    <p style="color:#E2E8F0; font-size:1rem; margin-bottom:10px;">Supporting Qatar's Economic Vision with Data‑Driven Investment Insights</p>
    <p style="color:#CBD5E0; font-size:0.9rem; line-height:1.6; max-width:700px; margin:auto 0 24px;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
  </div>

  <!-- FULL-WIDTH Decorative Divider -->
  <svg viewBox="0 0 1920 140" xmlns="http://www.w3.org/2000/svg" style="position:absolute; bottom:-1px; left:0; width:calc(100% + 6rem); margin-left:0; height:100px; overflow:visible;">
    <path fill="#F6F5F2" d="M0,40 Q480,20 960,40 T1920,40 L1920,140 L0,140 Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== STYLE: TEAL NAV BUTTONS + GREY TOGGLE BUTTON =====
st.markdown("""
<style>
.nav-container {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 26px 0 28px 0;
    text-align: center;
}

/* TEAL buttons for navigation */
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:45px!important;
    padding:13px 38px!important;
    font-weight:700!important;
    font-size:0.93rem!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
    width:210px!important;
    height:54px!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    text-align:center!important;
    white-space:nowrap!important;
    margin:auto!important;
    transition:all 0.25s ease!important;
}

.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 6px 18px rgba(22,160,133,0.4)!important;
}

.stButton>button:active{
    transform:translateY(0)!important;
    box-shadow:0 3px 10px rgba(22,160,133,0.25)!important;
}

/* GREY toggle button OVERRIDE */
button[kind="secondary"] {
    background: linear-gradient(135deg, #A9A9A9 0%, #8B8B8B 100%)!important;
    color: white!important;
    border: none!important;
    border-radius: 8px!important;
    padding: 11px 28px!important;
    font-weight: 600!important;
    font-size: 0.9rem!important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15)!important;
    transition: all 0.25s ease!important;
}

button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #8B8B8B 0%, #707070 100%)!important;
    transform: translateY(-1px)!important;
    box-shadow: 0 5px 14px rgba(0,0,0,0.2)!important;
}

div[data-testid="column"] {display:flex; justify-content:center;}

/* Smart Compact Metric Boxes - GREY */
.metric-pill {
    background: linear-gradient(135deg, #D3D3D3 0%, #C0C0C0 100%);
    color: #333;
    padding: 16px 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.25s ease;
}

.metric-pill:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.metric-number {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 4px 0;
    color: #1B2B4D;
}

.metric-label {
    font-size: 0.8rem;
    opacity: 0.85;
    font-weight: 600;
    color: #333;
}

/* Compact Activity Cards - GREY */
.activity-card {
    background: #F5F5F5;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    border-left: 4px solid #A9A9A9;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.activity-card:hover {
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    border-left-color: #808080;
    background: #EFEFEF;
}

/* Task Priority Badges */
.badge-red {
    background: #FEE2E2;
    color: #DC2626;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-yellow {
    background: #FEF3C7;
    color: #D97706;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-green {
    background: #DCFCE7;
    color: #16A085;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ===== NAVIGATION BAR =====
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_cols = st.columns(5)
buttons = [
    ("Deal Sourcing", "pages/1_Deal_Sourcing.py"),
    ("Due Diligence", "pages/2_Due_Diligence_Analysis.py"),
    ("Market Analysis", "pages/3_Market_Analysis.py"),
    ("Financial Modeling", "pages/4_Financial_Modeling.py"),
    ("Investment Memo", "pages/5_Investment_Memo.py")
]
for i, (label, path) in enumerate(buttons):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{i}"):
            st.switch_page(path)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DASHBOARD TOGGLE BUTTON (CENTERED & GREY) =====
st.markdown("""
<div style="
    display: flex;
    justify-content: center;
    padding: 12px 0;
    background-color: #F6F5F2;
    margin: 0 -3rem;
    width: calc(100% + 6rem);
">
""", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 0.3, 1])
with col_c:
    if st.button(
        f"{'▼ Hide' if st.session_state.dashboard_expanded else '▶ View'} Dashboard",
        key="toggle_dashboard",
        type="secondary",  # This makes it use the grey style!
        use_container_width=False
    ):
        st.session_state.dashboard_expanded = not st.session_state.dashboard_expanded
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ===== DASHBOARD CONTENT (CONDITIONAL) =====
if st.session_state.dashboard_expanded:
    st.markdown("<div style='padding: 0 3rem;'>", unsafe_allow_html=True)
    
    # KPI METRICS ROW (GREY) 
    metric_cols = st.columns([1, 1, 1, 1])

    with metric_cols[0]:
        st.markdown("""
        <div class="metric-pill">
            <div style="font-size:1.05rem; opacity:0.88;">⏳ Pending</div>
            <div class="metric-number">5</div>
            <div class="metric-label">Due Diligence</div>
        </div>
        """, unsafe_allow_html=True)

    with metric_cols[1]:
        st.markdown("""
        <div class="metric-pill">
            <div style="font-size:1.05rem; opacity:0.88;">📈 Active</div>
            <div class="metric-number">12</div>
            <div class="metric-label">In Pipeline</div>
        </div>
        """, unsafe_allow_html=True)

    with metric_cols[2]:
        st.markdown("""
        <div class="metric-pill">
            <div style="font-size:1.05rem; opacity:0.88;">✅ Complete</div>
            <div class="metric-number">28</div>
            <div class="metric-label">This Quarter</div>
        </div>
        """, unsafe_allow_html=True)

    with metric_cols[3]:
        st.markdown("""
        <div class="metric-pill">
            <div style="font-size:1.05rem; opacity:0.88;">⚡ Avg Time</div>
            <div class="metric-number">2h</div>
            <div class="metric-label">Per Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # DASHBOARD CONTENT ROWS (GREY CARDS)
    dash_col1, dash_col2, dash_col3 = st.columns([1, 1, 1])

    # === ACTION REQUIRED ===
    with dash_col1:
        st.markdown("""
        <div style="background:#F5F5F5; border-radius:10px; padding:16px; box-shadow:0 2px 12px rgba(0,0,0,0.08); border-top:3px solid #E74C3C;">
            <h4 style="color:#1B2B4D; margin:0 0 12px 0; font-size:1rem;">🔴 Action Required</h4>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">GreenTech</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Financial review</span>
                </div>
                <span class="badge-red">Today</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">CloudFlow AI</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Compliance check</span>
                </div>
                <span class="badge-red">Oct 28</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">SustainBox</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Market analysis</span>
                </div>
                <span class="badge-red">Oct 29</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # === IN PROGRESS ===
    with dash_col2:
        st.markdown("""
        <div style="background:#F5F5F5; border-radius:10px; padding:16px; box-shadow:0 2px 12px rgba(0,0,0,0.08); border-top:3px solid #F39C12;">
            <h4 style="color:#1B2B4D; margin:0 0 12px 0; font-size:1rem;">🟡 In Progress</h4>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">DataFlow</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Awaiting review</span>
                </div>
                <span class="badge-yellow">75%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">FinTech Innov</strong><br>
                    <span style="color:#666; font-size:0.8rem;">DD analysis</span>
                </div>
                <span class="badge-yellow">50%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">EcoEnergy</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Memo generation</span>
                </div>
                <span class="badge-yellow">90%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # === RECENT ACTIVITY ===
    with dash_col3:
        st.markdown("""
        <div style="background:#F5F5F5; border-radius:10px; padding:16px; box-shadow:0 2px 12px rgba(0,0,0,0.08); border-top:3px solid #16A085;">
            <h4 style="color:#1B2B4D; margin:0 0 12px 0; font-size:1rem;">📋 Recent Activity</h4>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">✅ DD Report</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Baladna Q.P.S.C</span>
                </div>
                <span style="color:#666; font-size:0.75rem;">Today</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">📊 Financial Model</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Emirates Tech</span>
                </div>
                <span style="color:#666; font-size:0.75rem;">Yesterday</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="activity-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <strong style="color:#1B2B4D; font-size:0.9rem;">📈 Market Analysis</strong><br>
                    <span style="color:#666; font-size:0.8rem;">Aquaculture</span>
                </div>
                <span style="color:#666; font-size:0.75rem;">Oct 23</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

else:
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ===== CHOOSE PATH SECTION =====
qdb_section_start("light")
st.markdown(f"""
<div style="text-align:center; max-width:900px; margin:0 auto 32px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:1.8rem; font-weight:800; margin-bottom:8px;">
    ➜ Start Your Analysis
  </h2>
  <p style="color:#666; font-size:1.05rem; margin:0; font-weight:500;">Choose a workflow to begin investment analysis</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns([0.4, 1.8, 1.8, 0.4])
with cols[1]:
    st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:28px 24px; height:280px;
                    box-shadow:0 4px 16px rgba(0,0,0,0.08); border-top:4px solid #16A085;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.2rem; font-weight:700; margin:0 0 8px 0;">🔍 Deal Sourcing</h3>
                <p style="color:#666; font-size:0.88rem; margin:8px 0 0 0; line-height:1.5;">
                    Discover opportunities with AI-powered market scanning
                </p>
            </div>
            <ul style="line-height:1.6; color:#555; font-size:0.88rem; margin:8px 0 0 0; padding-left:16px;">
                <li>Automated screening</li>
                <li>Pipeline management</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", key="btn_deal", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

with cols[2]:
    st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:28px 24px; height:280px;
                    box-shadow:0 4px 16px rgba(0,0,0,0.08); border-top:4px solid #16A085;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.2rem; font-weight:700; margin:0 0 8px 0;">⚖️ Due Diligence</h3>
                <p style="color:#666; font-size:0.88rem; margin:8px 0 0 0; line-height:1.5;">
                    Deep analysis: financials, legal, operations & risk
                </p>
            </div>
            <ul style="line-height:1.6; color:#555; font-size:0.88rem; margin:8px 0 0 0; padding-left:16px;">
                <li>Document analysis</li>
                <li>Report generation</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", key="btn_dd", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

qdb_section_end()

st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

# ===== FOOTER (FULL-WIDTH) =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:28px 40px;
    margin:40px -3rem 0 -3rem;
    font-size:0.92rem;
    width: calc(100% + 6rem);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">About</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Insights</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Contact</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Privacy</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.88rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.92;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
