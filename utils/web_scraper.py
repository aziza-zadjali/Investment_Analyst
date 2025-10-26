"""
Unified Web Scraping & Data Extraction – Regulus
Handles: Deal sourcing & IR content retrieval (annual, financial, ESG)
Failsafe mock for demo URLs. LLM‑ready clean outputs.
"""

import requests, re, time, PyPDF2
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
from io import BytesIO
from typing import List, Dict, Any
from config.constants import REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT

class WebScraper:
    def __init__(self):
        self.s=requests.Session(); self.s.headers.update({'User-Agent':USER_AGENT})
        self.report_categories={
            'financial_statements':['financial','earnings','quarterly','result'],
            'annual_reports':['annual','interim','report'],
            'governance':['governance','board','management'],
            'sustainability':['sustainability','csr','esg'],
            'presentations':['presentation','overview'],
            'fact_sheet':['fact','profile'],
        }

    def scrape_url(self,url,extract_links=True):
        for i in range(MAX_RETRIES):
            try:
                r=self.s.get(url,timeout=REQUEST_TIMEOUT)
                r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
                [t.decompose() for t in soup(['script','style','footer','nav','header'])]
                text=soup.get_text(separator='\n',strip=True)
                out={'url':url,'text':text,'success':True}
                if extract_links: out['links']=[a['href'] for a in soup.find_all('a',href=True)]
                return out
            except Exception as e:
                if i==MAX_RETRIES-1:return{'url':url,'error':str(e),'success':False}
                time.sleep(2**i)

    def discover_investor_relations(self,company_url):
        found={k:[] for k in self.report_categories}; found['home']=[]
        if '.example.com' in company_url:  # Demo safeguard
            for c in self.report_categories: found[c]=[f"{company_url}/{c}"]
            found['home']=[company_url]; return found
        if not company_url.startswith('http'): company_url='https://'+company_url
        base=company_url.rstrip('/')
        try:
            res=self.s.get(base,timeout=REQUEST_TIMEOUT)
            soup=BeautifulSoup(res.text,'html.parser')
            for a in soup.find_all('a',href=True):
                h=a['href']; f=urljoin(base,h)
                if urlparse(f).netloc!=urlparse(base).netloc: continue
                l=h.lower()+a.get_text().lower()
                for cat,kws in self.report_categories.items():
                    if any(k in l for k in kws) and f not in found[cat]: found[cat].append(f)
                if 'invest' in l: found['home'].append(f)
        except Exception as e: print('IR discovery fail',e)
        return found

    def extract_company_data(self,site,name):
        data=self.discover_investor_relations(site); out={}
        for cat,urls in data.items():
            if cat=='home': continue
            blocks=[]
            for u in urls[:2]:
                try:
                    if u.endswith('.pdf'): t=self._extract_pdf(u)
                    else:
                        r=self.scrape_url(u,False)
                        t=r['text'] if r.get('success') else ''
                        t+=self._find_pdf(u,t)
                    if len(t)>200: blocks.append(self._clean(t))
                except Exception as e: print('Extract fail',e)
            if blocks: out[cat]='\n\n'.join(blocks)
        return out

    def _find_pdf(self,page,html):
        try:
            s=BeautifulSoup(html,'html.parser')
            p=[a['href'] for a in s.find_all('a',href=True) if a['href'].lower().endswith('.pdf')]
            if p:return self._extract_pdf(urljoin(page,p[0]))
        except: pass
        return ''

    def _extract_pdf(self,url,maxp=10):
        try:
            r=self.s.get(url,timeout=20)
            reader=PyPDF2.PdfReader(BytesIO(r.content))
            txt=''.join([pg.extract_text() or '' for pg in reader.pages[:maxp]])
            return self._clean(txt)
        except Exception as e: print('PDF err',e); return ''

    def _clean(self,t):
        t=re.sub(r'\s+',' ',t).strip()
        return t[:8000]+'...[Truncated]' if len(t)>8000 else t

    def scrape_startup_data(self):
        return [
            {'name':'AI Analytics Corp','industry':'Artificial Intelligence','stage':'Series A','funding':'$8M',
             'location':'San Francisco','description':'Next‑gen analytics platform','website':'aianalytics.example.com'},
            {'name':'GreenTech Energy','industry':'CleanTech','stage':'Seed','funding':'$3M',
             'location':'Austin','description':'Smart renewable optimization','website':'greentech.example.com'},
            {'name':'MediCare AI','industry':'HealthTech','stage':'Series B','funding':'$20M',
             'location':'Boston','description':'AI‑diagnostic platform','website':'medicare-ai.example.com'},
            {'name':'FinStream','industry':'FinTech','stage':'Series A','funding':'$12M',
             'location':'New York','description':'Payment fraud detection','website':'finstream.example.com'},
        ]
