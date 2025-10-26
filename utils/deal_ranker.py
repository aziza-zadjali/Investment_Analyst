"""
Deal Ranker - Advanced scoring and ranking
METHODOLOGIES: 
- Financial metrics scoring
- Market attractiveness
- Team assessment
- Risk scoring
"""
from typing import Dict, List

class DealRanker:
    """Score and rank deals based on multiple factors"""
    
    def __init__(self):
        self.weights = {
            'financial_health': 0.25,
            'market_opportunity': 0.25,
            'team_quality': 0.20,
            'growth_trajectory': 0.20,
            'risk_profile': 0.10
        }
    
    def score_deal(self, deal: Dict) -> float:
        """Calculate composite score (0-10)"""
        
        scores = {
            'financial': self._score_financial(deal),
            'market': self._score_market(deal),
            'team': self._score_team(deal),
            'growth': self._score_growth(deal),
            'risk': self._score_risk(deal)
        }
        
        composite = (
            scores['financial'] * self.weights['financial_health'] +
            scores['market'] * self.weights['market_opportunity'] +
            scores['team'] * self.weights['team_quality'] +
            scores['growth'] * self.weights['growth_trajectory'] +
            scores['risk'] * self.weights['risk_profile']
        )
        
        deal['scores'] = scores
        deal['composite_score'] = round(composite, 1)
        
        return composite
    
    def _score_financial(self, deal: Dict) -> float:
        """Score financial metrics"""
        score = 5.0
        
        # Revenue scoring
        if 'revenue' in deal:
            if '$' in deal['revenue']:
                score += 2
        
        # Funding scoring
        if 'total_raised' in deal:
            score += 2
        
        return min(score, 10)
    
    def _score_market(self, deal: Dict) -> float:
        """Score market opportunity"""
        score = 5.0
        
        attractive_industries = ["AI/ML", "ClimaTech", "FinTech", "Biotech"]
        if deal.get('industry') in attractive_industries:
            score += 3
        
        return min(score, 10)
    
    def _score_team(self, deal: Dict) -> float:
        """Score team quality"""
        score = 5.0
        
        if 'founders' in deal and len(deal['founders']) > 0:
            score += 2
        
        if 'investors' in deal:
            reputable = ["Sequoia", "Accel", "A16Z", "Benchmark"]
            if any(inv in str(deal['investors']) for inv in reputable):
                score += 2
        
        return min(score, 10)
    
    def _score_growth(self, deal: Dict) -> float:
        """Score growth trajectory"""
        score = 5.0
        
        if 'growth' in deal:
            growth_str = deal['growth'].lower()
            if '120%' in growth_str or '200%' in growth_str:
                score += 3
            elif '80%' in growth_str or '100%' in growth_str:
                score += 2
            elif '50%' in growth_str:
                score += 1
        
        return min(score, 10)
    
    def _score_risk(self, deal: Dict) -> float:
        """Score risk profile"""
        score = 7.0
        
        if deal.get('stage') == 'Seed':
            score -= 2
        elif deal.get('stage') == 'Series C':
            score += 1
        
        return min(max(score, 0), 10)
    
    def rank_deals(self, deals: List[Dict]) -> List[Dict]:
        """Rank all deals"""
        for deal in deals:
            self.score_deal(deal)
        
        # Sort by composite score
        ranked = sorted(deals, key=lambda x: x.get('composite_score', 0), reverse=True)
        
        # Add rank
        for idx, deal in enumerate(ranked, 1):
            deal['rank'] = idx
        
        return ranked
    
    def get_recommendation(self, score: float) -> str:
        """Get investment recommendation"""
        if score >= 8.5:
            return "STRONG BUY"
        elif score >= 7.5:
            return "BUY"
        elif score >= 6.5:
            return "HOLD"
        else:
            return "PASS"
