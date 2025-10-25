"""
Investment Analyst AI - QDB Edition
Properly aligned and responsive header layout
"""

import streamlit as st
import base64
import os

# Streamlit configuration
st.set_page_config(
    page_title="Investment Analyst AI - QDB",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {visibility: hidden;}
.main > div {padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)


# Convert logo file to Base64 for consistent display
def image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        return f"data:image/png;base64,{encoded}"
    return None


qdb_logo = image_as_base64("QDB_Logo.png")
regulus_logo = image_as_base64("regulus_logo.png")

# --- HEADER LAYOUT FIX ---
st.markdown("""
<style>
.header-flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 40px auto;
  padding: 10px 20px;
}
.header-col {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.header-mid {
  flex: 2;
  text-align: center;
}
.header-mid h1 {
  margin-bottom: 5px;
  font-size: 2.6rem;
  font-weight: 700;
  color: #222;
}
.header-mid p {
  color: #777;
  font-size: 1.1rem;
  margin: 0;
}
.header-logo {
  max-height: 85px;
  object-fit: contain;
  margin: 0 auto;
}
@media (max-width: 900px) {
  .header-flex {
    flex-direction: column;
  }
  .header-mid h1 {font-size: 2.1rem;}
  .header-mid p {font-size: 1rem;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-flex'>", unsafe_allow_html=True)

# Left: QDB logo
st.markdown("<div class='header-col'>", unsafe_allow_html=True)
if qdb_logo:
    st.markdown(f"<img src='{qdb_logo}' class='header-logo'>", unsafe_allow_html=True)
else:
    st.markdown("<p><b>Qatar Development Bank</b></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Middle: Title
st.markdown("""
<div class='header-mid'>
  <h1>Investment Analyst AI</h1>
  <p>Intelligent Investment Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# Right: Regulus logo
st.markdown("<div class='header-col'>", unsafe_allow_html=True)
if regulus_logo:
    st.markdown(f"<img src='{regulus_logo}' class='header-logo'>", unsafe_allow_html=True)
else:
    st.markdown("<p><b>Regulus</b></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
# --- END HEADER ---


# Divider line
st.markdown("<div style='background:linear-gradient(90deg,#A6D8FF,#D5B8FF);height:4px;border-radius:2px;margin-bottom:35px;'></div>", unsafe_allow_html=True)


# --- MAIN CONTENT ---
st.markdown("""
<div style='text-align:center;margin-bottom:30px;'>
  <h2 style='color:#333;margin-bottom:10px;'>Choose Your Analysis Path</h2>
  <p style='color:#666;font-size:1.1rem;'>Select one option to begin your workflow</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# DEAL SOURCING PATH
with col1:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                border-radius:15px;padding:40px;color:white;height:400px;
                display:flex;flex-direction:column;
                box-shadow:0 6px 18px rgba(0,0,0,0.15);'>
        <h2 style='margin:0 0 15px 0;font-size:1.9rem;'>Deal Sourcing Path</h2>
        <p style='font-size:1.1rem;line-height:1.6;margin-bottom:20px;'>
            <b>Start here if you are:</b><br><br>
            • Looking for new investment opportunities<br>
            • Building your deal pipeline<br>
            • Discovering and filtering potential deals
        </p>
        <div style='margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,0.3);'>
            <b>Workflow:</b> Deal Discovery → Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", type="primary", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

# DUE DILIGENCE PATH
with col2:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);
                border-radius:15px;padding:40px;color:white;height:400px;
                display:flex;flex-direction:column;
                box-shadow:0 6px 18px rgba(0,0,0,0.15);'>
        <h2 style='margin:0 0 15px 0;font-size:1.9rem;'>Due Diligence Path</h2>
        <p style='font-size:1.1rem;line-height:1.6;margin-bottom:20px;'>
            <b>Start here if you have:</b><br><br>
            • Received investment proposals<br>
            • Uploaded company documents<br>
            • Need deep-dive review
        </p>
        <div style='margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,0.3);'>
            <b>Workflow:</b> Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", type="primary", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")


# --- QUICK ACCESS TOOLS ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("Direct Access to Specific Tools", expanded=False):
    col_tool1, col_tool2, col_tool3 = st.columns(3)
    with col_tool1:
        if st.button("Market Analysis", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
    with col_tool2:
        if st.button("Financial Modeling", use_container_width=True):
            st.switch_page("pages/4_Financial_Modeling.py")
    with col_tool3:
        if st.button("Investment Memo", use_container_width=True):
            st.switch_page("pages/5_Investment_Memo.py")


# --- FOOTER ---
st.markdown("<br><div style='background:linear-gradient(90deg,#A6D8FF,#D5B8FF);height:4px;border-radius:2px;margin-bottom:20px;'></div>", unsafe_allow_html=True)

colF1, colF2, colF3 = st.columns([1, 2, 1])
with colF1:
    st.markdown("<p style='text-align:left;color:#666;'>© 2025 Qatar Development Bank</p>", unsafe_allow_html=True)
with colF2:
    st.markdown("<p style='text-align:center;color:#999;font-size:0.9rem;'><b>Investment Analyst AI</b> | Version 1.0.0</p>", unsafe_allow_html=True)
with colF3:
    st.markdown("<p style='text-align:right;color:#666;'>Powered by Regulus</p>", unsafe_allow_html=True)
