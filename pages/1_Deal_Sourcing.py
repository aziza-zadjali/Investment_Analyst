"""
Deal Discovery & Sourcing | Regulus AI × QDB
Fixed version with final scraping status summary.
"""
import streamlit as st
import os, base64, pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY

st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")

# ==== HERO SECTION ====
st.markdown(
    f"""
<div style="
    background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
    color:white;
    position:relative;
    margin:0 -3rem; padding:100px 0 80px 0;
    min-height:390px; text-align:center; overflow:hidden;">
  <div style="position:absolute;left:50px;top:48px;">
    {'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
  </div>
  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.8rem;font-weight:800;letter-spacing:-0.5px;line-height:1.18; margin-bottom:16px;">
      Deal Discovery & Sourcing
    </h1>
    <p style="font-size:1.35rem;color:#E2E8F0; font-weight:500; margin-bottom:18px;">
      Supporting Qatar's Economic Vision with Data-Driven Startup Intelligence
    </p>
    <p style="color:#CBD5E0; font-size:1.07rem;line-height:1.6;max-width:760px;margin:0 auto 38px;">
      Daily AI-powered identification and curation of investment opportunities. <br>
      End-to-End Sourcing, Due Diligence, Market Analysis & Investment Memos.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== RETURN HOME BUTTON ====
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("Return Home", use_container_width=True, key="home_btn"):
        st.switch_page("streamlit_app.py")

st.markdown(
    """
<style>
button[key="home_btn"]{
 background:linear-gradient(135deg,#16A085 0%,#138074 80%,#0E5F55 100%)!important;
 color:white!important; border:none!important; border-radius:44px!important;
 padding:14px 44px!important; font-weight:700!important; font-size:1.08rem!important;
 box-shadow:0 8px 34px rgba(19,128,116,.20)!important;
 transition:all .19s!important; cursor:pointer!important;}
button[key="home_btn"]:hover{
 transform:translateY(-2px)!important;
 box-shadow:0 10px 40px rgba(19,128,116,.30)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ==== WORKFLOW TRACKER ====
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:-2px -3rem;padding:34px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== FILTERS SECTION ====
st.markdown(
    """
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Daily Deal Discovery Dashboard
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Apply custom filters to identify pre-qualified, relevant startups fast.
</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("Define Investment Criteria", expanded=True):
    c1, c2, c3 = st.columns(3)
    industries = c1.multiselect(
        "Industries",
        ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
        ["Technology","Healthcare"],
    )
    regions = c2.multiselect(
        "Regions",["MENA","Europe","North America","Asia Pacific"],["MENA"]
    )
    stage = c3.selectbox("Funding Stage",["Pre-Seed","Seed","Series A","Series B","Growth"],index=1)
    
    c4, c5 = st.columns([2,1])
    sectors = c4.multiselect("Sectors",["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    deal_count = c5.slider("Deals per run",5,50,15,5)

    # ==== TICKET SIZE FILTER ====
    st.markdown("---")
    t1, t2 = st.columns(2)
    with t1:
        min_investment = st.slider("Minimum Ticket Size (USD Millions)", 0, 50, 1, 1, key="min_ticket")
    with t2:
        max_investment = st.slider("Maximum Ticket Size (USD Millions)", 1, 100, 20, 1, key="max_ticket")

sources = st.multiselect(
    "Active Sources",
    ["Crunchbase","AngelList","Magnitt","Wamda","PitchBook"],
    ["Crunchbase","AngelList","Magnitt"],
)

# ==== ACTION BUTTON ====
st.markdown("<br>", unsafe_allow_html=True)
col1,col2,col3 = st.columns([1,0.8,1])
with col2:
    discover = st.button("Discover Live Deals", use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:40px!important;
 padding:14px 42px!important;font-weight:700!important;font-size:1rem!important;
 box-shadow:0 5px 18px rgba(19,128,116,0.35)!important;transition:all 0.3s ease!important;}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 8px 22px rgba(19,128,116,0.45)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ==== EXECUTION WITH DETAILED STATUS ====
if discover:
    try:
        scraper = WebScraper()
        llm = LLMHandler()
        
        progress_container = st.container()
        status_message = progress_container.info("Starting deal discovery process...")
        
        all_data = []
        source_stats = {}
        total_retrieved = 0
        
        for idx, src in enumerate(sources):
            status_message.info(f"Scraping {src}... (Step {idx+1} of {len(sources)})")
            try:
                src_data = scraper.search_startups(
                    src, industries, sectors, [stage], regions, 
                    limit=int(deal_count/len(sources))
                )
                src_count = len(src_data) if src_data else 0
                all_data.extend(src_data if src_data else [])
                source_stats[src] = src_count
                total_retrieved += src_count
            except Exception as e:
                source_stats[src] = 0
                st.warning(f"Error scraping {src}: {str(e)}")
                continue
        
        # Filter by ticket size
        filtered_data = []
        for deal in all_data:
            try:
                ticket = deal.get("funding_amount", 0)
                if isinstance(ticket, str):
                    ticket = float(ticket.replace("$", "").replace("M", "").strip())
                if min_investment <= ticket <= max_investment:
                    filtered_data.append(deal)
            except:
                filtered_data.append(deal)
        
        # Display results
        if not filtered_data:
            st.warning(f"No deals found in ticket size range ${min_investment}M - ${max_investment}M")
        else:
            df = pd.DataFrame(filtered_data)
            st.success(f"Success: {len(df)} deals found in your ticket size range.")
            st.dataframe(df, use_container_width=True)
            
            st.markdown("#### AI Summary")
            filter_summary = f"{len(df)} deals for {', '.join(industries)} in {', '.join(regions)}, ticket size: ${min_investment}M-${max_investment}M"
            try:
                ai_insight = llm.generate_text(f"Summarize: {filter_summary}")
                st.info(ai_insight)
            except Exception as e:
                st.warning(f"Could not generate AI summary: {str(e)}")
        
        # === FINAL SCRAPING STATUS SUMMARY ===
        st.markdown("---")
        st.markdown("#### Scraping Completion Summary")
        
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("Total Retrieved", f"{total_retrieved} deals")
        with summary_cols[1]:
            st.metric("Ticket Size Filtered", f"{len(filtered_data)} deals")
        with summary_cols[2]:
            st.metric("Scraping Status", "Completed")
        
        st.markdown("**Source Breakdown:**")
        for src, count in source_stats.items():
            st.write(f"- {src}: {count} deals")
        
        if total_retrieved == 0:
            st.info("No deals retrieved from selected sources. Try adjusting filters or expanding source selection.")
        elif len(filtered_data) == 0:
            st.info(f"Retrieved {total_retrieved} deals total, but none match your ticket size range (${min_investment}M-${max_investment}M). Try adjusting the range.")
        else:
            st.success(f"Scraping complete. {len(filtered_data)} of {total_retrieved} deals matched your criteria.")
    
    except Exception as e:
        st.error(f"Critical error during deal discovery: {str(e)}")

# ==== FOOTER ====
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
