"""
Web scraping utilities for deal sourcing and market data
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import streamlit as st
from config.constants import REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT

class WebScraper:
    """Handle web scraping for various data sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """Scrape content from a URL"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract text
                text = soup.get_text(separator='\n', strip=True)
                
                # Extract links
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                
                return {
                    'url': url,
                    'text': text,
                    'links': links,
                    'success': True
                }
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    st.warning(f"Failed to scrape {url}: {str(e)}")
                    return {'url': url, 'success': False, 'error': str(e)}
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {'url': url, 'success': False}
    
    def scrape_startup_data(self, platform: str = "crunchbase") -> List[Dict]:
        """Scrape startup data from various platforms"""
        # Note: This is a simplified example. Real implementation would need
        # proper API access or more sophisticated scraping
        
        startups = []
        
        if platform == "demo":
            # Demo data for testing
            startups = [
                {
                    'name': 'TechVenture AI',
                    'industry': 'Artificial Intelligence',
                    'stage': 'Series A',
                    'funding': '$5M',
                    'location': 'San Francisco',
                    'description': 'AI-powered analytics platform'
                },
                {
                    'name': 'GreenEnergy Solutions',
                    'industry': 'CleanTech',
                    'stage': 'Seed',
                    'funding': '$2M',
                    'location': 'Austin',
                    'description': 'Renewable energy management'
                },
                {
                    'name': 'HealthTech Innovations',
                    'industry': 'HealthTech',
                    'stage': 'Series B',
                    'funding': '$15M',
                    'location': 'Boston',
                    'description': 'Digital health platform'
                }
            ]
        
        return startups
    
    def search_market_data(self, query: str) -> Dict[str, Any]:
        """Search for market data and news"""
        # Simplified implementation
        return {
            'query': query,
            'results': [
                {
                    'title': f'Market Analysis: {query}',
                    'source': 'Market Research Report',
                    'summary': f'Latest trends and insights for {query}'
                }
            ]
        }
    
    def get_company_info(self, company_name: str) -> Dict[str, Any]:
        """Retrieve company information"""
        # This would typically use APIs like Crunchbase, LinkedIn, etc.
        return {
            'name': company_name,
            'founded': 'N/A',
            'employees': 'N/A',
            'funding': 'N/A',
            'description': f'Information for {company_name}'
        }
