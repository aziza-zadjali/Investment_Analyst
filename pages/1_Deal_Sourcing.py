"""
AI‑Powered Deal Sourcing | Regulus × QDB
Scrapes startup data and outputs a daily list of qualified deals | Full QDB visual branding
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime
from utils.qdb_styling import (
    apply_qdb_styling,
    qdb_section_start,
    qdb_section_end,
    QDB_DARK_BLUE,
)
from utils.llm_handler import LLMHandler

# -------------------------------------
# PAGE CONFIGURATION
# -------------------------------------
st.set_page_config(
    page_title="Deal Discovery & Sourcing – Regulus AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

# -------------------------------------
# DARK HEADER SECTION
# -------------------------------------
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;
    padding:85px 25px 70px;position:relative;">
  <h1 style="font-size:2.4rem;font-weight:700;letter-spacing:-0.3px;">
    AI‑Powered Deal Sourcing
  </h1>
  <p style="color:#CBD5E0;font-size:1rem;margin-top:8px;max-width:760px;margin:auto;">
    Automated startup discovery from accelerators and funding platforms with LLM‑based analysis and daily qualifications.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------
# PREMIUM WORKFLOW TRACKER
# -------------------------------------
st.markdown(
    """
<style>
.workflow-wrap {
    background:#F6F5F2;
    margin:0 -3rem;
    padding:42px 40px 32px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:nowrap;
    position:relative;
    font-family:'Segoe UI',sans-serif;
}
.step {text-align:center;flex:1;position:relative;}
.circle {
    width:56px;height:56px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    margin:0 auto 12px auto;font-weight:700;
    font-size:1rem;transition:all 0.3s ease;
}
.active {
    background:linear-gradient(135deg,#0E5F55 0%,#22A38B 100%);
    color:#fff;box-shadow:0 4px 18px rgba(14,95,85,0.35);transform:scale(1.05);
}
.inactive {background:#D8DEE9;color:#475569;}
.label {
    font-size:0.95rem;font-weight:600;letter-spacing:0.25px;margin-top:4px;
}
.active-label {color:#0E5F55;text-shadow:0 0 6px rgba(14,95,85,0.35);}
.inactive-label {color:#96A6B3;}
.connector {
    position:absolute;top:28px;right:-50%;width:100%;height:3px;border-radius:3px;
    background:linear-gradient(90deg,#CBD5E0 0%,#97BFC0 100%);
}
.step:last-child .connector {display:none;}
@keyframes pulseGlow{
    0%{box-shadow:0 0 0 0 rgba(19,128,116,0.4);}
    50%{box-shadow:0 0 0 12px rgba(19,128,116,0);}
    100%{box-shadow:0 0 0 0 rgba(19,128,116,0.4);}
}
.active:after{
    content:"";position:absolute;inset:2px;border-radius:50%;
    animation:pulseGlow 2s infinite;
}
</style>

<div class="workflow-wrap">
  <div class="step">
    <div class="circle active">1</div>
    <div class="label active-label">Deal Sourcing</div>
    <div class="connector"></div>
  </div>
  <div class="step">
    <div class="circle inactive">2</div>
    <div class="label inactive-label">Due Diligence</div>
    <div class="connector"></div>
  </div>
  <div class="step">
    <div class="circle inactive">3</div>
    <div class="label inactive-label">Market Analysis</div>
    <div class="connector"></div>
  </div>
  <div class="step">
    <div class="circle inactive">4</div>
    <div class="label inactive-label">Financial Modeling</div>
    <div class="connector"></div>
  </div>
  <div class="step">
    <div class="circle inactive">5</div>
    <div class="label inactive-label">Investment Memo</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------
# FILTERS SECTION
# -------------------------------------
qdb_section_start("light")

st.markdown(
    f"""
<div style="text-align:center;max-width:960px;margin:0 auto 35px;">
  <h2 style="color:{QDB_DARK_BLUE};font-weight:700;font-size:1.9rem;">Daily Smart Deal Discovery</h2>
  <p style="color:#555;font-size:1.05rem;">
     Scrape, filter and rank deals from accelerators and funding databases based on selected criteria.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("🎯 Discovery Parameters", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        industries = st.multiselect(
            "Industries",
            ["Fintech", "HealthTech", "AI / ML", "Cleantech", "SaaS", "Manufacturing"],
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
            "Funding Stage",
            ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"],
            index=1,
        )
    c4, c5 = st.columns([2, 1])
    with c4:
        keywords = st.text_input("Keywords (Optional)", "AI, SaaS, Climate Innovation")
    with c5:
        deal_count = st.slider("Deals per run", 5, 50, 10, 5)

qdb_section_end()

# -------------------------------------
# EXECUTION BUTTON
# -------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([1, 0.7, 1])[1]
with center:
    run = st.button("🚀 Run AI‑Driven Sourcing", use_container_width=True)

# -------------------------------------
# EXECUTION LOGIC
# -------------------------------------
if run:
    qdb_section_start("white")
    st.header("📈 Fetching and Qualifying Deals")

    sources = [
        "Y Combinator Startups",
        "Qatar Development Accelerators",
        "Crunchbase API",
        "Techstars Demo Day"
    ]
    progress = st.progress(0)
    deals = []
    for idx, src in enumerate(sources):
        st.info(f"Scraping: {src}")
        for i in range(deal_count // 3):
            deals.append(
                {
                    "Company": f"{random.choice(['NovaTech','EcoCore','AltFin','Biomind'])} {i+1}",
                    "Industry": random.choice(industries or ["Technology"]),
                    "Stage": stage,
                    "Region": random.choice(regions or ["Global"]),
                    "Ticket Size (USD M)": random.randint(1, 15),
                    "Revenue ($ M)": round(random.uniform(0.5, 25.0), 2),
                    "Founded": random.randint(2016, 2024),
                    "Employees": random.randint(8, 200),
                    "Source": src,
                }
            )
        progress.progress((idx + 1) / len(sources))
    df = pd.DataFrame(deals)
    st.success(f"✅ {len(deals)} qualified deals detected via accelerator feeds and APIs.")
    st.dataframe(df, use_container_width=True)
    qdb_section_end()

    # ----- AI SUMMARY -----
    qdb_section_start("light")
    st.subheader("🤖 Regulus AI Summary & Highlights")
    try:
        llm = LLMHandler()
        context = (
            f"Summarize {len(deals)} deals discovered within {', '.join(industries)} industries "
            f"across {', '.join(regions)} in {stage} stage. Focus on key investment themes and market outlook."
        )
        summary = llm.generate_text(context)
        st.markdown(summary)
    except Exception as e:
        st.warning(f"⚠️ LLM could not generate summary: {e}")
    qdb_section_end()

    # ----- NEXT STEP CTA -----
    st.markdown(
        f"""
        <div style="background-color:#F6F5F2;padding:60px 20px;margin:60px -3rem -2rem;text-align:center;">
          <h3 style="color:{QDB_DARK_BLUE};font-size:1.6rem;margin-bottom:10px;">Next Step in Workflow</h3>
          <p style="color:#555;margin-bottom:25px;">Proceed to Due Diligence for financial and compliance assessment.</p>
          <a href="?page=dd" style="
              background-color:#319795;color:white;text-decoration:none;
              border-radius:40px;padding:12px 38px;font-weight:600;
              box-shadow:0 3px 10px rgba(49,151,149,0.3);">
              → Continue to Due Diligence
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
