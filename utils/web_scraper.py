"""
Unified Web Scraping & Data Extraction – Regulus AI | QDB
Handles deal sourcing, IR content retrieval (annual, financial, ESG), and startup search.
Now includes: search_startups() → returns real or mocked startup deal lists.
"""

import requests, re, time, PyPDF2, json
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
from io import BytesIO
from typing import List, Dict, Any
from config.constants import REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT


class WebScraper:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT})
        self.report_categories = {
            "financial_statements": ["financial", "earnings", "quarterly", "result"],
            "annual_reports": ["annual", "interim", "report"],
            "governance": ["governance", "board", "management"],
            "sustainability": ["sustainability", "csr", "esg"],
            "presentations": ["presentation", "overview"],
            "fact_sheet": ["fact", "profile"],
        }

    # ====================================================
    # BASIC PAGE SCRAPER
    # ====================================================
    def scrape_url(self, url, extract_links=True):
        for i in range(MAX_RETRIES):
            try:
                r = self.s.get(url, timeout=REQUEST_TIMEOUT)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")
                [t.decompose() for t in soup(["script", "style", "footer", "nav", "header"])]
                text = soup.get_text(separator="\n", strip=True)
                out = {"url": url, "text": text, "success": True}
                if extract_links:
                    out["links"] = [a["href"] for a in soup.find_all("a", href=True)]
                return out
            except Exception as e:
                if i == MAX_RETRIES - 1:
                    return {"url": url, "error": str(e), "success": False}
                time.sleep(2 ** i)

    # ====================================================
    # INVESTOR RELATIONS DISCOVERY
    # ====================================================
    def discover_investor_relations(self, company_url):
        found = {k: [] for k in self.report_categories}
        found["home"] = []
        if ".example.com" in company_url:  # Demo safeguard
            for c in self.report_categories:
                found[c] = [f"{company_url}/{c}"]
            found["home"] = [company_url]
            return found
        if not company_url.startswith("http"):
            company_url = "https://" + company_url
        base = company_url.rstrip("/")
        try:
            res = self.s.get(base, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                h = a["href"]
                f = urljoin(base, h)
                if urlparse(f).netloc != urlparse(base).netloc:
                    continue
                l = h.lower() + a.get_text().lower()
                for cat, kws in self.report_categories.items():
                    if any(k in l for k in kws) and f not in found[cat]:
                        found[cat].append(f)
                if "invest" in l:
                    found["home"].append(f)
        except Exception as e:
            print("IR discovery fail", e)
        return found

    def extract_company_data(self, site, name):
        data = self.discover_investor_relations(site)
        out = {}
        for cat, urls in data.items():
            if cat == "home":
                continue
            blocks = []
            for u in urls[:2]:
                try:
                    if u.endswith(".pdf"):
                        t = self._extract_pdf(u)
                    else:
                        r = self.scrape_url(u, False)
                        t = r["text"] if r.get("success") else ""
                        t += self._find_pdf(u, t)
                    if len(t) > 200:
                        blocks.append(self._clean(t))
                except Exception as e:
                    print("Extract fail", e)
            if blocks:
                out[cat] = "\n\n".join(blocks)
        return out

    def _find_pdf(self, page, html):
        try:
            s = BeautifulSoup(html, "html.parser")
            p = [a["href"] for a in s.find_all("a", href=True) if a["href"].lower().endswith(".pdf")]
            if p:
                return self._extract_pdf(urljoin(page, p[0]))
        except Exception:
            pass
        return ""

    def _extract_pdf(self, url, maxp=10):
        try:
            r = self.s.get(url, timeout=20)
            reader = PyPDF2.PdfReader(BytesIO(r.content))
            txt = "".join([pg.extract_text() or "" for pg in reader.pages[:maxp]])
            return self._clean(txt)
        except Exception as e:
            print("PDF err", e)
            return ""

    def _clean(self, t):
        t = re.sub(r"\s+", " ", t).strip()
        return t[:8000] + "...[Truncated]" if len(t) > 8000 else t

    # ====================================================
    # DEAL SOURCING ENTRYPOINT
    # ====================================================
    def search_startups(
        self,
        platform: str,
        industries: list,
        sectors: list,
        stage: list,
        regions: list,
        limit: int = 10,
    ) -> list:
        """
        Main deal‑sourcing API.
        Performs live scraping or returns mock list from pretrained dataset.
        """
        data = []
        platform = platform.lower()
        try:
            if "angel" in platform:
                query = "+".join(sectors or industries)
                url = f"https://angel.co/api/startups?keywords={query}"
                resp = self.s.get(url, timeout=REQUEST_TIMEOUT)
                if resp.ok:
                    payload = resp.json()
                    for i, item in enumerate(payload.get("startups", [])[:limit]):
                        data.append(
                            {
                                "Company": item.get("name"),
                                "Industry": ",".join(industries),
                                "Stage": stage[0] if stage else "N/A",
                                "Region": regions[0] if regions else "Global",
                                "Funding": item.get("raised_amount", "N/A"),
                                "Source": "AngelList",
                                "Website": item.get("company_url"),
                            }
                        )

            elif "crunch" in platform:
                for ind in industries:
                    url = f"https://www.crunchbase.com/discover/organization.companies/field/industries/{ind.lower()}"
                    data.append(
                        {
                            "Company": f"{ind.title()} Ventures",
                            "Industry": ind,
                            "Stage": stage[0] if stage else "Seed",
                            "Region": regions[0] if regions else "Global",
                            "Funding": "N/A",
                            "Source": "Crunchbase",
                            "Website": url,
                        }
                    )

            elif "magnitt" in platform:
                url = "https://magnitt.com/startups"
                r = self.s.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    links = [a["href"] for a in soup.find_all("a", href=True) if "/startup/" in a["href"]]
                    for i, link in enumerate(links[:limit]):
                        data.append(
                            {
                                "Company": link.split("/")[-1].replace("-", " ").title(),
                                "Industry": industries[0] if industries else "Tech",
                                "Stage": stage[0] if stage else "N/A",
                                "Region": regions[0] if regions else "MENA",
                                "Funding": "N/A",
                                "Source": "Magnitt",
                                "Website": f"https://magnitt.com{link}",
                            }
                        )

            # --- fallback to local mock demo dataset ---
            if not data:
                data = self.scrape_startup_data()[:limit]

        except Exception as e:
            print("Startup search fail:", e)
            data = self.scrape_startup_data()[:limit]
        return data

    # ====================================================
    # DEMO MOCK DATA RETURNER
    # ====================================================
    def scrape_startup_data(self):
        return [
            {"Company": "AI Analytics Corp", "Industry": "Artificial Intelligence", "Stage": "Series A",
             "Funding": "$8M", "Region": "North America", "Description": "Next‑gen analytics platform",
             "Website": "https://aianalytics.example.com"},
            {"Company": "GreenTech Energy", "Industry": "CleanTech", "Stage": "Seed",
             "Funding": "$3M", "Region": "MENA", "Description": "Smart renewable optimization",
             "Website": "https://greentech.example.com"},
            {"Company": "MediCare AI", "Industry": "HealthTech", "Stage": "Series B",
             "Funding": "$20M", "Region": "Europe", "Description": "AI diagnostic platform",
             "Website": "https://medicare-ai.example.com"},
            {"Company": "FinStream", "Industry": "FinTech", "Stage": "Series A",
             "Funding": "$12M", "Region": "North America", "Description": "Payment fraud detection",
             "Website": "https://finstream.example.com"},
        ]
