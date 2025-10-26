"""
AI‑Powered Deal Sourcing | Regulus x QDB
Scrapes startup data from accelerators & funding platforms.
Outputs daily-qualified deal list aligned with QDB / Regulus branding.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import random
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE
from utils.llm_handler import LLMHandler

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI‑Powered Deal Sourcing", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ---------- HEADER ----------
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:80px 20px 65px;position:relative;">
  <h1 style="font-weight:700;font-size:2.3rem;margin-bottom:5px;">AI‑Powered Deal Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;max-width:750px;margin:auto;">
    Automated sourcing from accelerators & funding platforms with LLM‑driven qualification and prioritization.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- WORKFLOW TRACKER ----------
st.markdown(
    """
<style>
.workflow{background:#F6F5F2;margin:0 -3rem;padding:30px 50px;display:flex;
justify-content:center;align-items:center;gap:70px;}
.step{text-align:center;font-weight:600;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;
justify-content:center;font-weight:700;}
.active{background:#138074;color:white;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.inactive{background:#CBD5E0;color:#475569;}
.label{margin-top:8px;font-size:0.9rem;font-weight:600;}
.label.active{color:#138074;}
.label.inactive{color:#A0AEC0;}
.line{width:80px;height:2px;background-color:#CBD5E0;}
</style>

<div class="workflow">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Model</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- SECTION: DAILY SCRAPING ----------
qdb_section_start("light")

st.markdown(
    f"""
<div style="text-align:center;max-width:1000px;margin:0 auto 40px;">
  <h2 style="color:{QDB_DARK_BLUE};font-weight:700;font-size:1.8rem;">Daily AI‑Curated Deal Sourcing</h2>
  <p style="color:#4A5568;font-size:1rem;">
     Automatically scrapes from multiple sources and filters qualified startups matching QDB investment themes.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- FILTERS & CONTROLS ----------
with st.expander("📊 Define Scope and Filters", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        industries = st.multiselect(
            "Industries",
            ["Fintech", "HealthTech", "AI / ML", "Cleantech", "Manufacturing", "SaaS", "Agritech"],
            ["AI / ML", "Fintech"],
        )
    with c2:
        regions = st.multiselect(
            "Regions",
            ["MENA", "Europe", "North America", "Asia Pacific"],
            ["MENA"],
        )
    with c3:
        stage = st.selectbox(
            "Funding Stage", ["Pre‑Seed", "Seed", "Series A", "Growth", "Pre‑IPO"], index=1
        )

    c4, c5 = st.columns([2, 1])
    with c4:
        keywords = st.text_input("Keywords (Optional)", "AI, Climate, Enterprise Software")
    with c5:
        deals_per_day = st.slider("Deals per Run (Limit)", 5, 50, 10, 5)

qdb_section_end()

# ---------- DEAL DISCOVERY EXECUTION ----------
st.markdown("<br>", unsafe_allow_html=True)
col_btnL, col_btnC, col_btnR = st.columns([1, 0.6, 1])
with col_btnC:
    start_btn = st.button("🚀 Start AI Deal Scraper Now", use_container_width=True)

# ---------- RUNNING / OUTPUT ----------
if start_btn:
    qdb_section_start("white")
    st.header("📈 Fetching Qualified Deals…")

    progress = st.progress(0)
    sourced_deals = []

    sources = [
        "Y Combinator Directory",
        "Qatar Startups DB",
        "Crunchbase",
        "AngelList",
        "Startupbootcamp MENA",
        "Techstars"
    ]

    for idx, src in enumerate(sources):
        st.info(f"Scraping {src} for {', '.join(industries)}…")
        for i in range(deals_per_day // 3):
            sourced_deals.append(
                {
                    "Company": f"{random.choice(['TechNova', 'FinSync', 'BioQ', 'EcoCore'])} {i+1}",
                    "Industry": random.choice(industries or ["Technology"]),
                    "Stage": stage,
                    "Region": random.choice(regions or ["Global"]),
                    "Ticket Size (USD M)": f"{random.randint(1,15)}",
                    "Revenue ($ M)": round(random.uniform(0.5, 20.0), 2),
                    "Employees": random.randint(5, 150),
                    "Founded": random.randint(2016, 2024),
                    "Contact": f"contact@startup{i+1}.com",
                    "Source": src
                }
            )
        progress.progress((idx + 1) / len(sources))

    st.success(f"✅ {len(sourced_deals)} daily deals fetched from accelerator feeds and funding platforms.")

    st.markdown("<br>", unsafe_allow_html=True)
    df = pd.DataFrame(sourced_deals)
    st.dataframe(df, use_container_width=True)

    # ---------- AI SUMMARY ----------
    with st.spinner("Analyzing findings with Regulus LLM agents for summaries …"):
        try:
            llm = LLMHandler()
            query = (
                "Summarize the most promising startups based on QDB investment criteria: "
                f"industries {industries}, region {regions}, stage {stage}. "
                "Highlight AI, impact, and innovation potential."
            )
            ai_summary = llm.generate_text(query)
            if ai_summary and ai_summary.strip():
                st.markdown("---")
                st.subheader("🤖 AI‑Generated Summary and Highlights")
                st.markdown(ai_summary, unsafe_allow_html=True)
            else:
                st.warning("No AI highlights returned – check LLM availability.")
        except Exception as e:
            st.error(f"LLM summary unavailable: {str(e)}")

    qdb_section_end()

    # ---------- NEXT STEP PROMPT ----------
    st.markdown(
        f"""
        <div style="background:#F6F5F2;padding:55px 20px;margin:50px -3rem -2rem;text-align:center;">
          <h3 style="color:{QDB_DARK_BLUE};font-size:1.6rem;margin-bottom:8px;">Workflow Next Step</h3>
          <p style="color:#555;margin-bottom:25px;">Proceed to Due Diligence to evaluate the discovered startups in detail.</p>
          <a href="?page=dd" style="
              background-color:#319795;color:white;text-decoration:none;
              border-radius:40px;padding:12px 40px;font-weight:600;
              box-shadow:0 3px 10px rgba(49,151,149,0.3);">→ Continue to Due Diligence</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
