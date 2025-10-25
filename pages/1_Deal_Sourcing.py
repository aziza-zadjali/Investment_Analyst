"""
Deal Discovery & Sourcing – Regulus Edition
Integrated with WebScraper, LLMHandler, TemplateGenerator
Fully functional with live research, badge indicators & sort options
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
import base64
import os

# --- Streamlit Page Settings ---
st.set_page_config(page_title="Deal Discovery - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# --- Helper for Embedding Logos ---
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

qdb_logo = encode_image("QDB_Logo.png")

# --- Initialize Handlers ---
@st.cache_resource
def init_modules():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_modules()

# --- Session Initialization ---
if 'discovered_deals' not in st.session_state:
    st.session_state.discovered_deals = []

# --- HEADER (same branding as main page) ---
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);color:white;text-align:center;margin:0 -3rem;padding:60px 20px;">
  <div style="position:absolute;top:20px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <h1 style="font-weight:700;font-size:2.3rem;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:0.95rem;">AI‑powered multi‑source startup scouting & qualification guided by QDB priorities</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- Step Progress Tracker ---
st.markdown("""
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:18px 40px;display:flex;justify-content:space-between;align-items:center;}
.steps{display:flex;gap:12px;align-items:center;justify-content:center;}
.step{display:flex;flex-direction:column;align-items:center;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;justify-content:center;align-items:center;font-weight:700;}
.circle.active{background:#138074;color:white;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive{background:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;margin-top:4px;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{height:2px;width:50px;background:#D1D5DB;}
a.link{color:#138074;text-decoration:none;font-weight:600;}
a.link:hover{color:#0e5f55;}
</style>
<div class="track">
  <a href="streamlit_app.py" class="link">Back to Home</a>
  <div class="steps">
    <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financials</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
  </div>
  <span style="color:#999;">Regulus AI</span>
</div>
""", unsafe_allow_html=True)

# ============================
# Investment Filters
# ============================
st.markdown("### Define Investment Criteria")
st.caption("Select high‑level filters to refine AI discovery from multiple industry databases.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    industries = st.multiselect("Target Industries",
        ["Technology","Healthcare","Energy","Finance","Retail","Manufacturing"],
        default=["Technology"])
with col2:
    sectors = st.multiselect("Target Sectors",
        ["Fintech","HealthTech","AI/ML","SaaS","Cleantech"],default=["Fintech"])
with col3:
    stage = st.multiselect("Funding Stage",
        ["Pre-Seed","Seed","Series A","Growth"],default=["Seed"])
with col4:
    geography = st.multiselect("Regions",
        ["MENA","Europe","North America"],default=["MENA"])

col5, col6 = st.columns(2)
with col5:
    deal_count = st.number_input("Deals to Source",min_value=5,max_value=50,value=15,step=5)
with col6:
    unattractive_filter = st.checkbox("Exclude Unattractive Industries (QDB Policy)",True,
        help="If enabled, deals from non‑priority sectors identified by QDB are removed.")

st.markdown("<br>", unsafe_allow_html=True)

# --- Discover Button ---
colA,colB,colC=st.columns([1,0.8,1])
with colB:
    discover_clicked=st.button("Discover Deals",type="primary",use_container_width=True)

st.markdown("""
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#138074,#0e5f55)!important;color:white!important;
 border:none!important;border-radius:40px!important;padding:12px 32px!important;
 font-weight:700!important;font-size:0.95rem!important;
 box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;transition:all 0.2s ease;
}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0e5f55,#138074)!important;
 transform:translateY(-2px)!important;
}
</style>""",unsafe_allow_html=True)

# ============================
# Deal Discovery Logic
# ============================
if discover_clicked:
    try:
        with st.spinner("Running live data discovery and AI qualification..."):
            scraped = scraper.discover_deals(
                industries=industries,
                sectors=sectors,
                stages=stage,
                regions=geography,
                limit=deal_count
            )
            enriched = llm.qualify_deals(scraped)
            df=pd.DataFrame(enriched)
            if unattractive_filter:
                df=df[df["qdb_priority"]!="Excluded"]
            stage_order={"Pre-Seed":1,"Seed":2,"Series A":3,"Growth":4}
            if "stage" in df.columns:
                df["StageOrder"]=df["stage"].map(stage_order)
                df=df.sort_values(by=["industry","StageOrder"],ascending=[True,True]).drop(columns=["StageOrder"],errors="ignore")
            st.session_state.discovered_deals=df.to_dict("records")
            st.success(f"{len(df)} verified deals discovered and qualified.")
    except Exception as e:
        st.error(f"Discovery failed: {e}")

# ============================
# Display Results
# ============================
if st.session_state.discovered_deals:
    df=pd.DataFrame(st.session_state.discovered_deals)

    st.markdown("<br>",unsafe_allow_html=True)
    st.subheader("📊 Discovered & Qualified Deals")
    
    sort_opt=st.radio("Sort Deals By:",
        ["Industry","Funding Stage","Ticket Size"],horizontal=True)
    
    # Parsing ticket size numerically
    def parse_ticket(t):
        if "M" in str(t): return float(str(t).replace("$","").replace("M",""))
        return 0.0
    if sort_opt=="Ticket Size" and "ticket_size" in df.columns:
        df["ticket_value"]=df["ticket_size"].apply(parse_ticket)
        df=df.sort_values("ticket_value",ascending=True)

    # Add badges for attractiveness
    badge_col=[]
    for i,row in df.iterrows():
        if "qdb_priority" in row and str(row["qdb_priority"]).lower()=="excluded":
            badge="🔴 Excluded Sector"
        else:
            badge="🟢 Attractive"
        badge_col.append(badge)
    df.insert(0,"QDB Status",badge_col)

    st.caption("Deals sorted by your selected category. Badges indicate QDB sector alignment.")
    st.dataframe(df,use_container_width=True)

# ============================
# Footer
# ============================
st.markdown("<br><br>",unsafe_allow_html=True)
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;padding:30px 40px;margin:40px -3rem 0 -3rem;">
 <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;max-width:1400px;margin:0 auto;">
  <ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;padding:0;margin:0;">
    <li><a href="#" style="color:#E2E8F0;text-decoration:none;">About Regulus</a></li>
    <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Careers</a></li>
    <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Contact Us</a></li>
    <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Privacy Policy</a></li>
  </ul>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
 </div>
</div>
""",unsafe_allow_html=True)
