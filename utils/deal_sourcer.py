"""
Deal Sourcer - Searches and filters investment deals
Matches criteria with deal database
"""
import logging
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DealSourcer:
    """
    Searches and filters investment opportunities by criteria
    INDEPENDENT: Does NOT use web_scraper
    """
    
    def __init__(self):
        self.deal_database = self._initialize_deals()
    
    def _initialize_deals(self) -> List[Dict]:
        """Initialize mock deal database (in production, would connect to real DB)"""
        deals = [
            # Fintech - Seed
            {"name": "PayNow", "industry": "Fintech", "stage": "Seed", "revenue": 0.2, "growth": 250, "geography": "North America", "team_score": 4.5, "traction": "100K users"},
            {"name": "FinFlow", "industry": "Fintech", "stage": "Seed", "revenue": 0.3, "growth": 180, "geography": "Europe", "team_score": 4.2, "traction": "50K users"},
            {"name": "BlockPay", "industry": "Fintech", "stage": "Seed", "revenue": 0.15, "growth": 300, "geography": "North America", "team_score": 4.8, "traction": "Ex-Goldman founders"},
            
            # Fintech - Series A
            {"name": "TransferWise Clone", "industry": "Fintech", "stage": "Series A", "revenue": 2.5, "growth": 120, "geography": "Europe", "team_score": 4.6, "traction": "500K users"},
            {"name": "CryptoVault", "industry": "Fintech", "stage": "Series A", "revenue": 1.8, "growth": 95, "geography": "Global", "team_score": 4.3, "traction": "$50M AUM"},
            {"name": "LendTech", "industry": "Fintech", "stage": "Series A", "revenue": 3.2, "growth": 150, "geography": "MENA", "team_score": 4.4, "traction": "$200M deployed"},
            
            # Fintech - Series B
            {"name": "NeoBank Pro", "industry": "Fintech", "stage": "Series B", "revenue": 8.5, "growth": 75, "geography": "Global", "team_score": 4.7, "traction": "5M users"},
            {"name": "PaymentOS", "industry": "Fintech", "stage": "Series B", "revenue": 6.2, "growth": 85, "geography": "North America", "team_score": 4.5, "traction": "$2B TPV"},
            
            # ClimateTech - Seed
            {"name": "SolarIO", "industry": "ClimateTech", "stage": "Seed", "revenue": 0.1, "growth": 400, "geography": "MENA", "team_score": 4.4, "traction": "10 MW deployed"},
            {"name": "CarbonTrack", "industry": "ClimateTech", "stage": "Seed", "revenue": 0.25, "growth": 220, "geography": "Europe", "team_score": 4.6, "traction": "100 companies tracked"},
            {"name": "GreenChain", "industry": "ClimateTech", "stage": "Seed", "revenue": 0.18, "growth": 280, "geography": "Asia Pacific", "team_score": 4.3, "traction": "MIT backed"},
            
            # ClimateTech - Series A
            {"name": "RenewHub", "industry": "ClimateTech", "stage": "Series A", "revenue": 1.5, "growth": 140, "geography": "Global", "team_score": 4.5, "traction": "50 MW managed"},
            {"name": "EnergyOptim", "industry": "ClimateTech", "stage": "Series A", "revenue": 2.8, "growth": 160, "geography": "Europe", "team_score": 4.7, "traction": "30% savings average"},
            
            # Enterprise SaaS - Seed
            {"name": "DataFlow", "industry": "Enterprise SaaS", "stage": "Seed", "revenue": 0.3, "growth": 200, "geography": "North America", "team_score": 4.4, "traction": "50 enterprise customers"},
            {"name": "WorkOS", "industry": "Enterprise SaaS", "stage": "Seed", "revenue": 0.22, "growth": 180, "geography": "Europe", "team_score": 4.5, "traction": "Stripe integration"},
            
            # Enterprise SaaS - Series A
            {"name": "CloudSync", "industry": "Enterprise SaaS", "stage": "Series A", "revenue": 4.5, "growth": 130, "geography": "Global", "team_score": 4.6, "traction": "Fortune 500 customer"},
            {"name": "SecureVault", "industry": "Enterprise SaaS", "stage": "Series A", "revenue": 3.2, "growth": 110, "geography": "North America", "team_score": 4.4, "traction": "SOC2 certified"},
            
            # HealthTech - Seed
            {"name": "TelemedicNow", "industry": "HealthTech", "stage": "Seed", "revenue": 0.15, "growth": 350, "geography": "MENA", "team_score": 4.6, "traction": "Doctor network growing"},
            {"name": "LabConnect", "industry": "HealthTech", "stage": "Seed", "revenue": 0.28, "growth": 260, "geography": "Asia Pacific", "team_score": 4.5, "traction": "200 labs connected"},
            
            # EdTech - Series A
            {"name": "SkillUp", "industry": "EdTech", "stage": "Series A", "revenue": 2.1, "growth": 125, "geography": "Global", "team_score": 4.5, "traction": "1M learners"},
            {"name": "CodeBootcamp", "industry": "EdTech", "stage": "Series A", "revenue": 1.8, "growth": 140, "geography": "North America", "team_score": 4.4, "traction": "85% job placement"},
        ]
        
        return deals
    
    def search_deals(self, industry_list: List[str], stage_list: List[str], 
                     revenue_min: float, revenue_max: float, geography_list: List[str],
                     screening_factors: List[str] = None) -> Dict:
        """
        Search deals matching criteria
        
        Args:
            industry_list: Industries to include
            stage_list: Funding stages to include
            revenue_min: Minimum revenue (millions)
            revenue_max: Maximum revenue (millions)
            geography_list: Geographic regions
            screening_factors: Criteria to prioritize
        
        Returns:
            Dictionary with matched deals and analysis
        """
        
        if screening_factors is None:
            screening_factors = []
        
        # Filter deals by criteria
        matched_deals = []
        
        for deal in self.deal_database:
            # Check industry
            if deal['industry'] not in industry_list:
                continue
            
            # Check stage
            if deal['stage'] not in stage_list:
                continue
            
            # Check revenue range
            if deal['revenue'] < revenue_min or deal['revenue'] > revenue_max:
                continue
            
            # Check geography (flexible - Global matches any)
            geo_match = False
            if "Global" in geography_list or deal['geography'] in geography_list or deal['geography'] == "Global":
                geo_match = True
            
            if not geo_match:
                continue
            
            # Calculate score based on screening factors
            score = self._calculate_deal_score(deal, screening_factors)
            deal_with_score = {**deal, 'investment_score': score}
            matched_deals.append(deal_with_score)
        
        # Sort by score
        matched_deals.sort(key=lambda x: x['investment_score'], reverse=True)
        
        logger.info(f"Found {len(matched_deals)} deals matching criteria")
        
        return {
            'total_matches': len(matched_deals),
            'deals': matched_deals,
            'search_criteria': {
                'industries': industry_list,
                'stages': stage_list,
                'revenue_range': f"${revenue_min}M-${revenue_max}M",
                'geographies': geography_list,
                'screening_factors': screening_factors
            }
        }
    
    def _calculate_deal_score(self, deal: Dict, screening_factors: List[str]) -> float:
        """Calculate investment score based on criteria"""
        
        score = 0
        max_score = len(screening_factors) if screening_factors else 1
        
        if not screening_factors:
            return deal.get('team_score', 3.0)
        
        # Score based on screening factors
        factor_scores = {
            'Unit Economics (LTV/CAC)': deal.get('growth', 0) / 100,  # Normalize growth
            'Growth Rate (YoY)': deal.get('growth', 0) / 200,
            'Market Traction': (deal.get('team_score', 3.0) / 5.0) * 100,
            'Team Quality': deal.get('team_score', 3.0),
            'IP/Technology': deal.get('team_score', 3.0) - 0.5 if deal.get('team_score', 3.0) > 4.2 else 3.0,
            'Strategic Fit with QDB': 5.0 if 'ClimateTech' in deal.get('industry', '') or 'Fintech' in deal.get('industry', '') else 3.5,
            'Exit Potential': (deal.get('revenue', 0) * 2) if deal.get('stage') in ['Series A', 'Series B'] else deal.get('revenue', 0),
            'ESG Alignment': 5.0 if 'ClimateTech' in deal.get('industry', '') else 3.0,
        }
        
        for factor in screening_factors:
            score += factor_scores.get(factor, 3.0)
        
        return (score / max_score) if max_score > 0 else score
    
    def get_deal_details(self, deal_name: str) -> Dict:
        """Get detailed information about a specific deal"""
        
        for deal in self.deal_database:
            if deal['name'] == deal_name:
                return {
                    **deal,
                    'analysis': f"""
                    ## {deal['name']} - Investment Summary
                    
                    **Company**: {deal['name']}  
                    **Industry**: {deal['industry']}  
                    **Stage**: {deal['stage']}  
                    **Current Revenue**: ${deal['revenue']}M  
                    **Growth Rate**: {deal['growth']}% YoY  
                    **Geographic Focus**: {deal['geography']}  
                    **Team Quality Score**: {deal['team_score']}/5.0  
                    **Market Traction**: {deal['traction']}  
                    
                    ### Investment Highlights
                    - Strong growth trajectory ({deal['growth']}% YoY)
                    - Experienced founding team (Score: {deal['team_score']}/5.0)
                    - Clear market traction: {deal['traction']}
                    - Strategic fit for portfolio diversification
                    
                    ### Funding Recommendation
                    **Recommendation**: STRONG INTEREST (Tier 1 Priority)  
                    **Suggested Check Size**: ${max(0.5, deal['revenue'] * 1.5)}M - ${max(1.0, deal['revenue'] * 3.0)}M  
                    **Expected ROI (5-year)**: 3-8x  
                    **Investment Timeline**: 60-90 days
                    """
                }
        
        return {}
    
    def get_market_summary(self, industry_list: List[str]) -> Dict:
        """Get market summary for selected industries"""
        
        industry_data = {}
        
        for industry in industry_list:
            industry_deals = [d for d in self.deal_database if d['industry'] == industry]
            
            if industry_deals:
                avg_growth = sum(d['growth'] for d in industry_deals) / len(industry_deals)
                avg_team = sum(d['team_score'] for d in industry_deals) / len(industry_deals)
                total_revenue = sum(d['revenue'] for d in industry_deals)
                
                industry_data[industry] = {
                    'deal_count': len(industry_deals),
                    'avg_growth_rate': avg_growth,
                    'avg_team_score': avg_team,
                    'total_revenue': total_revenue,
                    'top_deal': max(industry_deals, key=lambda x: x['growth'])['name']
                }
        
        return industry_data
