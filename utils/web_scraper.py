"""
Unified Web Scraping & Data Extraction System
Handles: Deal sourcing, company IR data, market research, general scraping
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any, Optional, Set
import re
from datetime import datetime
import PyPDF2
from io import BytesIO
import time
import streamlit as st
from config.constants import REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT


class WebScraper:
    """Unified web scraping for all investment analysis needs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        # Keywords for intelligent content discovery
        self.ir_keywords = [
            'investor', 'corporate', 'financial', 'annual-report', 'quarterly',
            'governance', 'sustainability', 'esg', 'shareholders', 'sec-filings'
        ]
        
        self.report_categories = {
            'financial_statements': ['financial-statement', 'quarterly-result', 'interim-result', 'earnings'],
            'annual_reports': ['annual-report', 'yearly-report', 'report-publication'],
            'governance': ['corporate-governance', 'board-directors', 'governance-report'],
            'sustainability': ['sustainability', 'esg-report', 'csr-report', 'environmental'],
            'presentations': ['investor-presentation', 'earnings-presentation', 'company-presentation'],
            'fact_sheet': ['fact-sheet', 'company-profile', 'company-overview', 'key-figures'],
            'share_info': ['share-information', 'stock-price', 'share-price', 'share-graph']
        }
    
    # ========== GENERAL WEB SCRAPING ==========
    
    def scrape_url(self, url: str, extract_links: bool = True) -> Dict[str, Any]:
        """General purpose URL scraping with retry logic"""
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove unwanted elements
                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()
                
                # Extract text
                text = soup.get_text(separator='\n', strip=True)
                
                result = {
                    'url': url,
                    'text': text,
                    'success': True,
                    'status_code': response.status_code
                }
                
                # Optionally extract links
                if extract_links:
                    links = [a.get('href') for a in soup.find_all('a', href=True)]
                    result['links'] = links
                
                return result
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    return {
                        'url': url,
                        'success': False,
                        'error': str(e),
                        'status_code': None
                    }
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {'url': url, 'success': False}
    
    # ========== COMPANY-SPECIFIC EXTRACTION ==========
    
    def discover_investor_relations(self, company_url: str) -> Dict[str, List[str]]:
        """Intelligently discover all investor relations pages"""
        
        if not company_url.startswith('http'):
            company_url = 'https://' + company_url
        
        base_url = company_url.rstrip('/')
        discovered_urls = {category: [] for category in self.report_categories.keys()}
        discovered_urls['home'] = []
        
        try:
            response = self.session.get(company_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Skip external links
                if urlparse(full_url).netloc != urlparse(base_url).netloc:
                    continue
                
                href_lower = href.lower()
                link_text_lower = link.get_text().lower()
                
                # Categorize by keywords
                for category, keywords in self.report_categories.items():
                    if any(kw in href_lower or kw in link_text_lower for kw in keywords):
                        if full_url not in discovered_urls[category]:
                            discovered_urls[category].append(full_url)
                
                # Check for general IR links
                if any(kw in href_lower for kw in self.ir_keywords):
                    if full_url not in discovered_urls['home']:
                        discovered_urls['home'].append(full_url)
            
            # Deep crawl IR pages if nothing found
            if not any(urls for cat, urls in discovered_urls.items() if cat != 'home'):
                for ir_url in discovered_urls['home'][:3]:
                    self._crawl_ir_page(ir_url, base_url, discovered_urls)
            
        except Exception as e:
            st.warning(f"Error discovering IR pages: {e}")
        
        return discovered_urls
    
    def _crawl_ir_page(self, page_url: str, base_url: str, discovered_urls: Dict):
        """Deep crawl specific IR page"""
        
        try:
            response = self.session.get(page_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                full_url = urljoin(base_url, href)
                
                if urlparse(full_url).netloc != urlparse(base_url).netloc:
                    continue
                
                href_lower = href.lower()
                link_text_lower = link.get_text().lower()
                
                for category, keywords in self.report_categories.items():
                    if any(kw in href_lower or kw in link_text_lower for kw in keywords):
                        if full_url not in discovered_urls[category]:
                            discovered_urls[category].append(full_url)
        
        except Exception as e:
            print(f"Error crawling IR page: {e}")
    
    def extract_company_data(self, company_url: str, company_name: str) -> Dict[str, str]:
        """Extract comprehensive company data from website"""
        
        discovered = self.discover_investor_relations(company_url)
        extracted_data = {}
        
        for category, urls in discovered.items():
            if not urls or category == 'home':
                continue
            
            category_data = []
            for url in urls[:2]:  # Top 2 URLs per category
                try:
                    if url.lower().endswith('.pdf'):
                        data = self._extract_pdf_from_url(url)
                    else:
                        result = self.scrape_url(url, extract_links=False)
                        if result['success']:
                            data = result['text']
                            
                            # Also check for PDFs on the page
                            pdf_data = self._find_and_extract_pdfs(url, result.get('text', ''))
                            if pdf_data:
                                data += f"\n\n=== PDF Content ===\n{pdf_data}"
                        else:
                            data = ""
                    
                    if data and len(data) > 100:
                        category_data.append(data)
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error extracting {url}: {e}")
            
            if category_data:
                extracted_data[category] = '\n\n'.join(category_data)
        
        return extracted_data
    
    def _find_and_extract_pdfs(self, page_url: str, page_html: str) -> str:
        """Find and extract first PDF from page"""
        
        try:
            soup = BeautifulSoup(page_html, 'html.parser')
            pdf_links = [link['href'] for link in soup.find_all('a', href=True) 
                        if link['href'].lower().endswith('.pdf')]
            
            if pdf_links:
                pdf_url = urljoin(page_url, pdf_links[0])
                return self._extract_pdf_from_url(pdf_url)
        
        except Exception as e:
            print(f"Error finding PDFs: {e}")
        
        return ""
    
    def _extract_pdf_from_url(self, pdf_url: str, max_pages: int = 10) -> str:
        """Extract text from PDF URL"""
        
        try:
            response = self.session.get(pdf_url, timeout=30)
            if response.status_code != 200:
                return ""
            
            pdf_file = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            num_pages = min(len(pdf_reader.pages), max_pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return self._clean_text(text)
            
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        
        if len(text) > 8000:
            text = text[:8000] + "\n\n[Content truncated]"
        
        return text.strip()
    
    # ========== DEAL SOURCING ==========
    
    def scrape_startup_data(self, platform: str = "demo") -> List[Dict[str, Any]]:
        """Scrape startup data from various platforms"""
        
        if platform == "demo":
            # Demo data for testing
            return [
                {
                    'name': 'AI Analytics Corp',
                    'industry': 'Artificial Intelligence',
                    'stage': 'Series A',
                    'funding': '$8M',
                    'location': 'San Francisco, CA',
                    'description': 'Next-gen AI-powered business analytics platform for enterprises',
                    'website': 'aianalytics.example.com',
                    'founded': '2022'
                },
                {
                    'name': 'GreenTech Energy',
                    'industry': 'CleanTech',
                    'stage': 'Seed',
                    'funding': '$3M',
                    'location': 'Austin, TX',
                    'description': 'Smart renewable energy management and optimization solutions',
                    'website': 'greentech.example.com',
                    'founded': '2023'
                },
                {
                    'name': 'MediCare AI',
                    'industry': 'HealthTech',
                    'stage': 'Series B',
                    'funding': '$20M',
                    'location': 'Boston, MA',
                    'description': 'AI-driven diagnostic and patient management platform',
                    'website': 'medicare-ai.example.com',
                    'founded': '2021'
                },
                {
                    'name': 'FinStream',
                    'industry': 'FinTech',
                    'stage': 'Series A',
                    'funding': '$12M',
                    'location': 'New York, NY',
                    'description': 'Real-time payment processing and fraud detection system',
                    'website': 'finstream.example.com',
                    'founded': '2022'
                }
            ]
        
        # Add real platform scraping here (Crunchbase, AngelList, etc.)
        return []
    
    # ========== MARKET RESEARCH ==========
    
    def search_market_data(self, query: str, sources: List[str] = None) -> Dict[str, Any]:
        """Search for market data and news"""
        
        results = []
        
        # Demo market data
        market_keywords = ['trends', 'growth', 'market size', 'forecast', 'competition']
        
        for keyword in market_keywords:
            results.append({
                'title': f'{query} - {keyword.title()} Analysis',
                'source': 'Market Research Database',
                'summary': f'Comprehensive {keyword} analysis for {query} sector',
                'relevance': 0.85,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
        
        return {
            'query': query,
            'results': results,
            'total_found': len(results)
        }
    
    def get_company_info(self, company_name: str, company_website: str = None) -> Dict[str, Any]:
        """Retrieve basic company information"""
        
        info = {
            'name': company_name,
            'website': company_website or 'N/A',
            'founded': 'N/A',
            'employees': 'N/A',
            'funding': 'N/A',
            'description': f'Company profile for {company_name}'
        }
        
        # If website provided, try to extract data
        if company_website:
            try:
                extracted = self.extract_company_data(company_website, company_name)
                
                if 'fact_sheet' in extracted:
                    info['description'] = extracted['fact_sheet'][:500]
                
            except Exception as e:
                print(f"Could not extract company info: {e}")
        
        return info
    
    # ========== UTILITY METHODS ==========
    
    def format_for_analysis(self, extracted_data: Dict[str, str], company_name: str) -> str:
        """Format extracted data for LLM analysis"""
        
        section_titles = {
            'financial_statements': '## FINANCIAL STATEMENTS',
            'annual_reports': '## ANNUAL REPORTS',
            'governance': '## CORPORATE GOVERNANCE',
            'sustainability': '## SUSTAINABILITY & ESG',
            'presentations': '## INVESTOR PRESENTATIONS',
            'fact_sheet': '## COMPANY FACT SHEET',
            'share_info': '## SHARE INFORMATION'
        }
        
        formatted = f"""
# EXTRACTED DATA: {company_name.upper()}
**Extraction Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

"""
        
        for category, content in extracted_data.items():
            if content and len(content) > 100:
                title = section_titles.get(category, f"## {category.upper().replace('_', ' ')}")
                formatted += f"{title}\n\n{content}\n\n---\n\n"
        
        return formatted
