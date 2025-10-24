"""
Centralized configuration for all data sources used in deal sourcing and discovery
"""

# ========================================
# FUNDING PLATFORMS & ACCELERATORS
# ========================================
FUNDING_PLATFORMS = {
    "crunchbase": {
        "name": "🔷 Crunchbase",
        "url": "https://www.crunchbase.com/",
        "description": "70M+ profiles, funding rounds, and acquisitions",
        "best_for": "Comprehensive startup database",
        "api_available": True,
        "region": "Global"
    },
    "angellist": {
        "name": "💼 AngelList",
        "url": "https://www.angellist.com/",
        "description": "Startup jobs, funding, and investors",
        "best_for": "Early-stage startups and angel networks",
        "api_available": True,
        "region": "Global"
    },
    "pitchbook": {
        "name": "📊 PitchBook",
        "url": "https://pitchbook.com/",
        "description": "Private equity and VC deal database",
        "best_for": "PE/VC-backed companies",
        "api_available": True,
        "region": "Global"
    },
    "magnitt": {
        "name": "🧭 Magnitt",
        "url": "https://magnitt.com/",
        "description": "MENA startup and investor platform",
        "best_for": "Middle East & North Africa deals",
        "api_available": False,
        "region": "MENA"
    },
    "wamda": {
        "name": "🌍 Wamda",
        "url": "https://www.wamda.com/",
        "description": "MENA ecosystem intelligence",
        "best_for": "Regional market insights",
        "api_available": False,
        "region": "MENA"
    },
    "dealroom": {
        "name": "🏛️ Dealroom",
        "url": "https://dealroom.co/",
        "description": "Global startup intelligence",
        "best_for": "European and global trends",
        "api_available": True,
        "region": "Global"
    },
    "bloomberg": {
        "name": "🏦 Bloomberg",
        "url": "https://www.bloomberg.com/",
        "description": "Financial markets and companies",
        "best_for": "Public market and late-stage data",
        "api_available": True,
        "region": "Global"
    }
}

# ========================================
# QUICK ACCESS LISTS (for dropdowns)
# ========================================
FUNDING_PLATFORM_URLS = [
    "https://www.crunchbase.com/",
    "https://www.angellist.com/",
    "https://www.bloomberg.com/",
    "https://magnitt.com/",
    "https://www.wamda.com/",
    "https://pitchbook.com/",
    "https://dealroom.co/"
]

FUNDING_PLATFORM_NAMES = list(FUNDING_PLATFORMS.keys())

# ========================================
# ACCELERATORS
# ========================================
ACCELERATORS = {
    "y_combinator": {
        "name": "🚀 Y Combinator",
        "url": "https://www.ycombinator.com/companies",
        "region": "North America"
    },
    "techstars": {
        "name": "⭐ Techstars",
        "url": "https://techstars.com/portfolio",
        "region": "Global"
    },
    "500_startups": {
        "name": "5️⃣ 500 Startups",
        "url": "https://500.co/",
        "region": "Global"
    },
    "plug_and_play": {
        "name": "🔌 Plug and Play",
        "url": "https://www.plugandplaytechcenter.com/",
        "region": "Global"
    }
}

# ========================================
# NEWS & MARKET INTELLIGENCE
# ========================================
NEWS_SOURCES = [
    "https://www.techcrunch.com/",
    "https://www.theverge.com/",
    "https://www.forbes.com/",
    "https://www.businessinsider.com/"
]

# ========================================
# SECTOR-SPECIFIC PLATFORMS
# ========================================
SECTOR_PLATFORMS = {
    "fintech": [
        "https://www.cbinsights.com/",
        "https://www.fintech.com/"
    ],
    "climatetech": [
        "https://www.climatetechdb.com/",
        "https://www.climatechallenge.org/"
    ],
    "healthtech": [
        "https://www.healthtech.com/",
        "https://pitchbook.com/"
    ]
}

# ========================================
# HELPER FUNCTION
# ========================================
def get_funding_platform(key: str) -> dict:
    """Get platform details by key"""
    return FUNDING_PLATFORMS.get(key, {})

def get_all_platform_names() -> list:
    """Get all platform names with emojis for UI"""
    return [f"{v['name']}" for v in FUNDING_PLATFORMS.values()]

def get_all_platform_urls() -> list:
    """Get all platform URLs"""
    return [v["url"] for v in FUNDING_PLATFORMS.values()]
