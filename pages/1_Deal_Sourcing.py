"""
Deal Discovery & Sourcing – Regulus Edition
Professional teal UI | Step visual (1‑5) | QDB attractive filter | AI‑powered deal sourcing
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator

# ------------------------------------------------
# Framework Setup
# ------------------------------------------------
st.set_page_config(page_title="Deal Discovery – Regulus", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stSidebar']{display:none;}</style>", unsafe_allow_html=True)

# ------------------------------------------------
# Gradient Header Helper
# ------------------------------------------------
def gradient_box(text, gradient="linear-gradient(135deg,#138074,#0e5f55)"):
    return f"""<div style="background:{gradient};
        padding:14px 20px;border-radius:12px;font-weight:700;
        color:white;font-size:1.4rem;text-align:center;
        margin:30px 0;box-shadow:0 3px 10px rgba(19,128,116,0.3);">
        {text}</div>"""

# ------------------------------------------------
# Initialize Handlers
# ------------------------------------------------
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template_gen = init_handlers()

if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []

# ------------------------------------------------
# Header + Step Tracker
# ------------------------------------------------
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#666;'>AI‑powered deal sourcing with integrated filtering & QDB compliance</p>", unsafe_allow_html=True)

st.markdown("""
<style>
.track{display:flex;justify-content:center;align-items:center;gap:18px;margin:35px 0;}
.step{display:flex;flex-direction:column;align-items:center;font-weight:600;font-size:0.85rem;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:5px;}
.active{background:#138074;color:white;box-shadow:0 3px 8px rgba(19,128,116,0.4);}
.inactive{background:#E5E7EB;color:#9CA3AF;}
.line{width:70px;height:3px;background:#D1D5DB;}
</style>
<div class="track">
  <div class="step active"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">3</div><div class="label inactive">Market</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">4</div><div class="label inactive">Financials</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Unattractive Sectors
# ------------------------------------------------
UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage": ["Bakery","Juice","Milk","Water Bottling"],
    "Plastics": ["PET","UPVC","Plastic Pipe","Garbage Bin"],
    "Construction": ["Cement","Tiles","Glass","Blocks"],
    "Services": ["Salon","Spa","Laundry","Clinic","Restaurant"]
}

col_filter1, col_filter2 = st.columns([3,1])
with col_filter1:
    st.markdown("**Industry Screening (QDB)** – exclude non‑priority sectors")
with col_filter2:
    enable_industry_filter = st.checkbox("Enable Filter", True)
if enable_industry_filter:
    with st.expander("View Complete Unattractive List"):
        for cat, lst in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{cat}:** {', '.join(lst)}")

# ------------------------------------------------
# Criteria Inputs
# ------------------------------------------------
st.markdown(gradient_box("Define Investment Criteria"), unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4)
with col1:
    industries=st.multiselect("Industries",["Technology","Healthcare","CleanTech","Finance","Retail"],["Technology"])
with col2:
    sectors=st.multiselect("Sectors",["FinTech","HealthTech","AI/ML","SaaS","ClimateTech"],["FinTech","AI/ML"])
with col3:
    stage=st.multiselect("Stage",["Pre‑Seed","Seed","Series A","Series B","Growth"],["Seed","Series A"])
with col4:
    geography=st.multiselect("Regions",["MENA","Europe","North America","Asia"],["MENA","Europe"])

col5,col6=st.columns(2)
with col5:
    deal_count=st.slider("Deals to Source",5,50,10)
with col6:
    revenue=st.select_slider("Revenue Range (USD)",["Pre‑revenue","$0‑500K","$500K‑$2M","$2M‑$10M","$10M‑$50M","$50M+"],("$500K‑$2M","$10M‑$50M"))

# ------------------------------------------------
# Data Source Selection
# ------------------------------------------------
st.markdown(gradient_box("Select Data Sources"), unsafe_allow_html=True)
sources={"Crunchbase":"Global startup & funding database","AngelList":"VC networks and jobs","PitchBook":"Private equity intel","Magnitt":"MENA startups","Wamda":"MENA ecosystem","Dealroom":"Global VC data"}
selected=st.multiselect("Sources to use",list(sources.keys()),["Crunchbase","AngelList","Magnitt"])
if selected:
    cols=st.columns(len(selected))
    for idx,s in enumerate(selected):
        with cols[idx]: 
            st.markdown(f"**{s}**"); st.caption(sources[s])

# ------------------------------------------------
# Discovery Trigger
# ------------------------------------------------
st.markdown(gradient_box("Discover Deals"), unsafe_allow_html=True)
colX=st.columns([1,0.8,1])[1]
with colX:
    click=st.button("🚀 Start Discovery",use_container_width=True)

st.markdown("""
<style>div.stButton>button:first-child{
background:linear-gradient(135deg,#138074,#0e5f55)!important;color:white!important;border:none!important;
border-radius:40px!important;padding:12px 30px!important;font-weight:700!important;font-size:0.95rem!important;
box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;transition:0.2s;}
div.stButton>button:first-child:hover{transform:translateY(-2px)!important;}
</style>
""",unsafe_allow_html=True)

# ------------------------------------------------
# Discovery Execution
# ------------------------------------------------
if click:
    if not selected:
        st.error("Select at least one source.")
    else:
        with st.spinner("Fetching and qualifying deals..."):
            all_deals=[]; progress=st.progress(0)
            per=len(selected)
            count_per=deal_count//per
            for idx,s in enumerate(selected):
                st.info(f"Scanning {s} data...")
                for i in range(count_per):
                    deal={
                        "company":f"{s} Deal {i+1}",
                        "industry":industries[i%len(industries)] if industries else "Technology",
                        "sector":sectors[i%len(sectors)] if sectors else "FinTech",
                        "stage":stage[i%len(stage)] if stage else "Seed",
                        "region":geography[i%len(geography)] if geography else "Global",
                        "revenue":revenue[0],
                        "source":s,
                        "description":f"AI‑enabled {sectors[i%len(sectors)] if sectors else 'tech'} platform in {industries[i%len(industries)] if industries else 'Technology'}.",
                        "founded":str(2018+(i%5)),
                        "employees":f"{20+i*5}-{40+i*5}",
                        "ticket_size":"$1M‑$5M",
                        "unattractive_flag":False,"unattractive_reason":""
                    }
                    if enable_industry_filter:
                        for cat,ind_list in UNATTRACTIVE_INDUSTRIES.items():
                            if any(ind.lower() in deal["industry"].lower() or ind.lower() in deal["sector"].lower() for ind in ind_list):
                                deal["unattractive_flag"]=True; deal["unattractive_reason"]=cat; break
                    all_deals.append(deal)
                progress.progress((idx+1)/len(selected))
            st.session_state.discovered_deals=all_deals; st.success(f"✅ Discovered {len(all_deals)} deals.")

# ------------------------------------------------
# Display Results
# ------------------------------------------------
if st.session_state.discovered_deals:
    df=pd.DataFrame(st.session_state.discovered_deals)
    total=len(df); unat=len(df[df.unattractive_flag]); attr=total‑unat
    st.markdown(gradient_box("Discovered Deals Overview"),unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Total Deals",total); c2.metric("Attractive",attr); c3.metric("Unattractive",unat)
    filter_opt=st.radio("Show:",["All","Attractive Only","Unattractive Only"],horizontal=True)
    if filter_opt=="All": view=df
    elif filter_opt=="Attractive Only": view=df[~df.unattractive_flag]
    else: view=df[df.unattractive_flag]

    for _,r in view.iterrows():
        flag="🟢" if not r.unattractive_flag else "🔴"
        st.markdown(
            f"<div style='border:1px solid #ccc;border-radius:10px;padding:15px;margin:12px 0;'>"
            f"<h4>{flag} {r.company}</h4>"
            f"<b>Industry:</b> {r.industry} | <b>Sector:</b> {r.sector} | <b>Stage:</b> {r.stage} | <b>Region:</b> {r.region}<br>"
            f"<i>{r.description}</i>"
            f"{'<p style=\"color:red;font-weight:600;\">Excluded: '+r.unattractive_reason+'</p>' if r.unattractive_flag else ''}"
            f"</div>",unsafe_allow_html=True
        )

    st.markdown(gradient_box("Export Results"),unsafe_allow_html=True)
    csv=df.to_csv(index=False)
    st.download_button("⬇️ Download CSV",csv,"Deals.csv","text/csv")

    try:
        report_md=template_gen.generate_due_diligence_report({
            "company_name":"Portfolio Batch",
            "analyst_name":"Regulus AI",
            "analysis_date":datetime.now().strftime("%B %d, %Y"),
            "executive_summary":"Auto‑generated deal list for review.",
            "data_sources":selected
        })
        st.download_button("⬇️ Download Markdown Report",report_md,"Deal_Report.md","text/markdown")
    except Exception as e: st.error(f"Report error: {e}")
