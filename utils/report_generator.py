"""
Report and presentation generation utilities
"""

from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
import streamlit as st
from config.constants import MEMO_SECTIONS

class ReportGenerator:
    """Generate investment reports and memos"""
    
    def __init__(self):
        self.report_sections = MEMO_SECTIONS
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary section"""
        
        summary = f"""
## Executive Summary

**Company**: {data.get('company_name', 'N/A')}
**Investment Size**: ${data.get('investment_size', 'N/A')}
**Valuation**: ${data.get('valuation', 'N/A')}
**Investment Recommendation**: {data.get('recommendation', 'Under Review')}

### Key Highlights

{data.get('key_highlights', 'No highlights provided.')}

### Investment Thesis

{data.get('investment_thesis', 'Investment thesis to be developed.')}

---
"""
        return summary
    
    def generate_company_overview(self, data: Dict[str, Any]) -> str:
        """Generate company overview section"""
        
        overview = f"""
## Company Overview

**Founded**: {data.get('founded', 'N/A')}
**Location**: {data.get('location', 'N/A')}
**Industry**: {data.get('industry', 'N/A')}
**Stage**: {data.get('stage', 'N/A')}

### Business Model

{data.get('business_model', 'Business model description.')}

### Products/Services

{data.get('products_services', 'Product and service offerings.')}

### Team

{data.get('team_info', 'Team information.')}

---
"""
        return overview
    
    def generate_market_analysis(self, data: Dict[str, Any]) -> str:
        """Generate market analysis section"""
        
        analysis = f"""
## Market Analysis

### Market Size and Opportunity

**Total Addressable Market (TAM)**: ${data.get('tam', 'N/A')}
**Serviceable Addressable Market (SAM)**: ${data.get('sam', 'N/A')}
**Serviceable Obtainable Market (SOM)**: ${data.get('som', 'N/A')}

### Market Trends

{data.get('market_trends', 'Market trends analysis.')}

### Competitive Landscape

{data.get('competitive_landscape', 'Competitive analysis.')}

---
"""
        return analysis
    
    def generate_financial_analysis(self, data: Dict[str, Any]) -> str:
        """Generate financial analysis section"""
        
        analysis = f"""
## Financial Analysis

### Historical Performance

{data.get('historical_performance', 'Historical financial data.')}

### Projections

{data.get('projections', 'Financial projections.')}

### Key Metrics

{data.get('key_metrics', 'Key financial metrics and ratios.')}

### Valuation

{data.get('valuation_analysis', 'Valuation methodology and results.')}

---
"""
        return analysis
    
    def generate_risk_assessment(self, data: Dict[str, Any]) -> str:
        """Generate risk assessment section"""
        
        assessment = f"""
## Risk Assessment

### Business Risks

{data.get('business_risks', 'Business risk factors.')}

### Financial Risks

{data.get('financial_risks', 'Financial risk considerations.')}

### Market Risks

{data.get('market_risks', 'Market-related risks.')}

### Risk Mitigation

{data.get('risk_mitigation', 'Risk mitigation strategies.')}

---
"""
        return assessment
    
    def generate_investment_recommendation(self, data: Dict[str, Any]) -> str:
        """Generate investment recommendation section"""
        
        recommendation = f"""
## Investment Recommendation

### Overall Assessment

**Recommendation**: {data.get('recommendation', 'HOLD')}
**Confidence Level**: {data.get('confidence_level', 'Medium')}

### Rationale

{data.get('recommendation_rationale', 'Recommendation rationale.')}

### Terms and Conditions

{data.get('terms_conditions', 'Proposed terms and conditions.')}

### Next Steps

{data.get('next_steps', 'Recommended next steps.')}

---
"""
        return recommendation
    
    def generate_complete_memo(self, data: Dict[str, Any]) -> str:
        """Generate complete investment memo"""
        
        # Header
        memo = f"""
# Investment Memo: {data.get('company_name', 'Company Name')}

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Prepared By**: {data.get('analyst_name', 'Investment Team')}
**Deal Stage**: {data.get('stage', 'N/A')}

---

"""
        
        # Add all sections
        memo += self.generate_executive_summary(data)
        memo += self.generate_company_overview(data)
        memo += self.generate_market_analysis(data)
        memo += self.generate_financial_analysis(data)
        memo += self.generate_risk_assessment(data)
        memo += self.generate_investment_recommendation(data)
        
        # Footer
        memo += f"""
---

## Appendix

### Sources and References

{data.get('sources', 'Documents and sources used in this analysis.')}

### Disclaimers

This investment memo is prepared for informational purposes only and does not constitute 
investment advice. All information should be verified independently before making any 
investment decisions.

---

*End of Investment Memo*
"""
        
        return memo
    
    def export_to_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Convert data to DataFrame for Excel export"""
        
        df = pd.DataFrame([data])
        return df
