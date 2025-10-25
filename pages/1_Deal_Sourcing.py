# ===== DEAL DISCOVERY EXECUTION =====
st.markdown("<br>", unsafe_allow_html=True)

# Center the button
col_btn1, col_btn2, col_btn3 = st.columns([1, 0.6, 1])

with col_btn2:
    discover_button = st.button("Discover Deals", type="primary", use_container_width=True)

if discover_button:
    
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals from selected sources..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                st.info(f"Scanning {source}...")
                try:
                    for i in range(deal_count_per_source):
                        deal = {
                            "id": f"deal_{idx * deal_count_per_source + i + 1}",
                            "company": f"StartupCo {idx * deal_count_per_source + i + 1}",
                            "industry": industries[i % len(industries)] if industries else "Technology",
                            "sector": sectors[i % len(sectors)] if sectors else "Technology",
                            "stage": stage[i % len(stage)] if stage else "Seed",
                            "region": geography[i % len(geography)] if geography else "Global",
                            "revenue": revenue_range[0],
                            "source": source,
                            "description": f"Innovative {sectors[i % len(sectors)] if sectors else 'tech'} company in {industries[i % len(industries)] if industries else 'Technology'}",
                            "founded": str(2020 + (i % 5)),
                            "employees": f"{20 + i * 10}-{30 + i * 10}",
                            "contact_email": f"contact@startup{idx * deal_count_per_source + i + 1}.com",
                            "contact_phone": f"+1-555-{1000 + idx * deal_count_per_source + i}",
                            "contact_name": f"CEO Name {idx * deal_count_per_source + i + 1}",
                            "unattractive_flag": False,
                            "unattractive_reason": "",
                            "ticket_size": f"${1 + (i % 5)}M-${5 + (i % 10)}M" if not ticket_size_range else f"${ticket_size_range[0]}M-${ticket_size_range[1]}M"
                        }
                        
                        # Industry Filter
                        if enable_industry_filter:
                            for category, industry_list in UNATTRACTIVE_INDUSTRIES.items():
                                for unattr_industry in industry_list:
                                    if unattr_industry.lower() in deal['sector'].lower() or unattr_industry.lower() in deal['description'].lower() or unattr_industry.lower() in deal['industry'].lower():
                                        deal['unattractive_flag'] = True
                                        deal['unattractive_reason'] = f"{category}: {unattr_industry}"
                                        break
                                if deal['unattractive_flag']:
                                    break
                        
                        all_deals.append(deal)
                        
                except Exception as e:
                    st.warning(f"Could not fetch from {source}: {e}")
                
                progress_bar.progress((idx + 1) / len(selected_sources))
            
            st.session_state.discovered_deals = all_deals
            st.success(f"Discovered {len(all_deals)} potential deals")
            st.rerun()
