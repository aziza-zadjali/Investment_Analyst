# ===== DEAL DISCOVERY EXECUTION =====
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center;'>
    """,
    unsafe_allow_html=True,
)

discover_clicked = st.button(
    "Discover Deals",
    type="primary",
    use_container_width=False
)

st.markdown(
    """
    </div>
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #138074 0%, #0e5f55 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 14px 40px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(19,128,116,0.3) !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
        margin: 0 auto !important;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #0e5f55 0%, #138074 100%) !important;
        box-shadow: 0 6px 18px rgba(14,95,85,0.4) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if discover_clicked:
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals..."):
            # Your discovery logic stays the same here
            pass
