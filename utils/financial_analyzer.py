"""
Financial analysis and modeling utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import streamlit as st
from config.constants import PROJECTION_YEARS, DEFAULT_DISCOUNT_RATE, GROWTH_RATES

class FinancialAnalyzer:
    """Perform financial analysis and modeling"""
    
    def __init__(self):
        self.projection_years = PROJECTION_YEARS
        self.discount_rate = DEFAULT_DISCOUNT_RATE
    
    def create_projection_model(self, base_data: Dict[str, float], 
                                growth_scenario: str = 'moderate') -> pd.DataFrame:
        """Create financial projection model"""
        
        growth_rate = GROWTH_RATES.get(growth_scenario, 0.15)
        
        # Initialize dataframe
        years = list(range(1, self.projection_years + 1))
        projections = pd.DataFrame({'Year': years})
        
        # Revenue projections
        base_revenue = base_data.get('revenue', 1000000)
        projections['Revenue'] = [base_revenue * ((1 + growth_rate) ** year) for year in years]
        
        # Cost projections (assuming 60% of revenue)
        projections['COGS'] = projections['Revenue'] * 0.60
        
        # Gross Profit
        projections['Gross_Profit'] = projections['Revenue'] - projections['COGS']
        
        # Operating Expenses (assuming 25% of revenue)
        projections['OpEx'] = projections['Revenue'] * 0.25
        
        # EBITDA
        projections['EBITDA'] = projections['Gross_Profit'] - projections['OpEx']
        
        # EBITDA Margin
        projections['EBITDA_Margin'] = (projections['EBITDA'] / projections['Revenue']) * 100
        
        return projections
    
    def calculate_dcf_valuation(self, cash_flows: List[float], 
                                terminal_growth_rate: float = 0.03) -> Dict[str, float]:
        """Calculate DCF valuation"""
        
        # Discount cash flows
        pv_cash_flows = []
        for i, cf in enumerate(cash_flows):
            pv = cf / ((1 + self.discount_rate) ** (i + 1))
            pv_cash_flows.append(pv)
        
        # Terminal value
        terminal_cf = cash_flows[-1] * (1 + terminal_growth_rate)
        terminal_value = terminal_cf / (self.discount_rate - terminal_growth_rate)
        pv_terminal_value = terminal_value / ((1 + self.discount_rate) ** len(cash_flows))
        
        # Enterprise value
        enterprise_value = sum(pv_cash_flows) + pv_terminal_value
        
        return {
            'enterprise_value': enterprise_value,
            'pv_cash_flows': sum(pv_cash_flows),
            'pv_terminal_value': pv_terminal_value,
            'terminal_value': terminal_value
        }
    
    def run_scenario_analysis(self, base_data: Dict[str, float]) -> Dict[str, pd.DataFrame]:
        """Run multiple scenario analyses"""
        
        scenarios = {}
        
        for scenario_name, growth_rate in GROWTH_RATES.items():
            projections = self.create_projection_model(base_data, scenario_name)
            scenarios[scenario_name] = projections
        
        return scenarios
    
    def calculate_financial_ratios(self, financial_data: Dict[str, float]) -> Dict[str, float]:
        """Calculate key financial ratios"""
        
        ratios = {}
        
        # Profitability ratios
        if 'revenue' in financial_data and 'net_income' in financial_data:
            ratios['net_margin'] = (financial_data['net_income'] / financial_data['revenue']) * 100
        
        if 'revenue' in financial_data and 'gross_profit' in financial_data:
            ratios['gross_margin'] = (financial_data['gross_profit'] / financial_data['revenue']) * 100
        
        # Liquidity ratios
        if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
            ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
        
        # Leverage ratios
        if 'total_debt' in financial_data and 'equity' in financial_data:
            ratios['debt_to_equity'] = financial_data['total_debt'] / financial_data['equity']
        
        # Return ratios
        if 'net_income' in financial_data and 'equity' in financial_data:
            ratios['roe'] = (financial_data['net_income'] / financial_data['equity']) * 100
        
        if 'net_income' in financial_data and 'total_assets' in financial_data:
            ratios['roa'] = (financial_data['net_income'] / financial_data['total_assets']) * 100
        
        return ratios
    
    def perform_sensitivity_analysis(self, base_value: float, 
                                    variables: Dict[str, List[float]]) -> pd.DataFrame:
        """Perform sensitivity analysis on key variables"""
        
        results = []
        
        for var_name, var_values in variables.items():
            for var_value in var_values:
                # Calculate impact
                impact = base_value * (1 + var_value)
                change_pct = var_value * 100
                
                results.append({
                    'Variable': var_name,
                    'Change_%': change_pct,
                    'New_Value': impact,
                    'Absolute_Change': impact - base_value
                })
        
        return pd.DataFrame(results)
