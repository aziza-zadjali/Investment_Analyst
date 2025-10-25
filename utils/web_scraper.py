"""
Unified Web Scraping & Data Extraction System – Regulus Edition
Performs: Deal sourcing, IR data extraction, governance, ESG, and company intelligence.
Integrated with LLMHandler & TemplateGenerator for AI summarization in Deal Sourcing.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any
import re
import PyPDF2
from io import BytesIO
import time
from datetime import datetime
from config.constants import REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT


class WebScraper:
    """Unified scraping for IR pages, startup deals, and corporate intelligence."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})

        self.ir_keywords = [
            'investor', 'financial', 'annual-report', 'governance',
            'sustainability', 'esg', 'shareholder', 'report'
        ]

        self.report_categories = {
            'financial_statements': ['financial-statement', 'quarterly-result', 'earnings'],
            'annual_reports': ['annual-report', 'yearly-report'],
            'governance': ['corporate-governance', 'board', 'governance-report'],
            'sustainability': ['sustainability', 'esg-report', 'csr'],
            'presentations': ['investor-presentation', 'company-presentation'],
            'fact_sheet': ['fact-sheet', 'company-profile'],
        }

    # ==========================
    # GENERIC SCRAPER
    # ==========================
    def scrape_url(self, url: str, extract_links: bool = True) -> Dict[str, Any]:
        """Scrape HTML content safely with retry"""
        for attempt in range(MAX_RETRIES):
            try:
                res = self.session.get(url, timeout=REQUEST_TIMEOUT)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')

                for t in soup(['script', 'style', 'nav', 'footer', 'header']): 
                    t.decompose()
                text = soup.get_text(separator='\n', strip=True)
                data = {'url': url, 'text': text, 'success': True, 'status': res.status_code}
                if extract_links:
                    data['links'] = [a.get('href') for a in soup.find_all('a', href=True)]
                return data
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    return {'url': url, 'success': False, 'error': str(e)}
                time.sleep(2 ** attempt)
        return {'url': url, 'success': False}

    # ==========================
    # INVESTOR RELATIONS DISCOVERY
    # ==========================
    def discover_investor_relations(self, base_url: str) -> Dict[str, List[str]]:
        """Find investor relations pages categorized by content type"""
        found = {cat: [] for cat in self.report_categories.keys()}
        found['home'] = []
        if not base_url.startswith('http'):
            base_url = 'https://' + base_url

        try:
            site = self.session.get(base_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(site.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]

            for href in links:
                full = urljoin(base_url, href)
                if urlparse(full).netloc != urlparse(base_url).netloc: 
                    continue
                lower = href.lower()
                for cat, kws in self.report_categories.items():
                    if any(k in lower for k in kws):
                        found[cat].append(full)
                if any(k in lower for k in self.ir_keywords):
                    found['home'].append(full)
        except Exception as e:
            print(f"IR discovery failed for {base_url}: {e}")

        return found

    # ==========================
    # COMPANY IR DATA EXTRACTION
    # ==========================
    def extract_company_data(self, base_url: str, name: str) -> Dict[str, str]:
        """Extract textual information across IR categories"""
        all_data = {}
        discovered = self.discover_investor_relations(base_url)
        for category, urls in discovered.items():
            texts = []
            for u in urls[:2]:
                try:
                    if u.endswith(".pdf"):
                        txt = self._extract_pdf_from_url(u)
                    else:
                        result = self.scrape_url(u, extract_links=False)
                        txt = result.get("text", "")
                    if txt and len(txt) > 40:
                        texts.append(txt[:4000])
                except Exception as e:
                    print(f"Error extracting {u}: {e}")
            if texts:
                all_data[category] = "\n\n".join(texts)
        return all_data

    # ==========================
    # PDF EXTRACTION UTILITIES
    # ==========================
    def _extract_pdf_from_url(self, pdf_url: str, max_pages: int = 10) -> str:
        """Extract text from PDF link"""
        try:
            resp = self.session.get(pdf_url, timeout=30)
            if resp.status_code != 200: 
                return ""
            pdf = BytesIO(resp.content)
            reader = PyPDF2.PdfReader(pdf)
            text = ""
            for p in reader.pages[:max_pages]:
                text += p.extract_text() or ""
            return self._clean_text(text)
        except Exception as e:
            print(f"PDF extract error for {pdf_url}: {e}")
            return ""

    def _clean_text(self, txt: str) -> str:
        txt = re.sub(r'\n+', '\n', txt)
        txt = re.sub(r' +', ' ', txt)
        return txt[:6000]

    # ==========================
    # DEAL SOURCING (MULTI-PLATFORM)
    # ==========================
    def scrape_startup_data(self, platform: str = "demo") -> List[Dict[str, Any]]:
        """
        Fetch startup deal metadata from global sources.
        In production: integrate with Crunchbase, AngelList, PitchBook APIs.
        """
        if platform == "demo":
            return [
                {
                    "name": "FinStream AI",
                    "industry": "FinTech",
                    "stage": "Series A",
                    "funding": "$10M",
                    "location": "New York, USA",
                    "description": "AI‑driven fintech platform specializing in credit scoring.",
                    "website": "finstream.ai",
                    "founded": "2021"
                },
                {
                    "name": "GreenPower Tech",
                    "industry": "CleanTech",
                    "stage": "Seed",
                    "funding": "$4M",
                    "location": "Berlin, Germany",
                    "description": "Smart systems for re‑energy optimization.",
                    "website": "greenpower.tech",
                    "founded": "2022"
                },
                {
                    "name": "MediAI Diagnostics",
                    "industry": "HealthTech",
                    "stage": "Series B",
                    "funding": "$22M",
                    "location": "Boston, USA",
                    "description": "AI‑powered diagnostics improving clinical performance.",
                    "website": "mediaidiagnostics.com",
                    "founded": "2020"
                },
                {
                    "name": "EcoSmart Materials",
                    "industry": "Manufacturing",
                    "stage": "Growth",
                    "funding": "$15M",
                    "location": "Dubai, UAE",
                    "description": "Next‑gen sustainable material manufacturing.",
                    "website": "ecosmartmaterials.com",
                    "founded": "2019"
                }
            ]
        else:
            # Placeholder for future integration with APIs
            return []

    # ==========================
    # MARKET RESEARCH (Basic Demo)
    # ==========================
    def search_market_data(self, query: str) -> Dict[str, Any]:
        keywords = ["size", "growth", "investment", "trends"]
        results = [
            {
                "topic": f"{query} {k}",
                "summary": f"Market research on {k} aspects of {query}, showing consistent upward demand.",
                "confidence": 0.9,
                "timestamp": datetime.now().isoformat()
            }
            for k in keywords
        ]
        return {"query": query, "results": results, "count": len(results)}
