"""
Constants and configuration values
"""

# File processing constants
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'txt', 'csv']

# LLM Configuration
DEFAULT_MODEL = "gpt-4-turbo-preview"
EMBEDDING_MODEL = "text-embedding-3-small"
MAX_TOKENS = 4000
TEMPERATURE = 0.3

# Vector store settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SIMILARITY_THRESHOLD = 0.7
TOP_K_RESULTS = 5

# Financial modeling
PROJECTION_YEARS = 5
DEFAULT_DISCOUNT_RATE = 0.10
GROWTH_RATES = {
    'conservative': 0.05,
    'moderate': 0.15,
    'aggressive': 0.30
}

# Web scraping
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
USER_AGENT = "Investment-Analyst-Bot/1.0"

# Data sources
ACCELERATOR_URLS = [
    "https://www.ycombinator.com/companies",
    "https://techstars.com/portfolio"
]

FUNDING_PLATFORM_URLS = [
    "https://www.crunchbase.com",
    "https://www.angellist.com"
]

# Report sections
MEMO_SECTIONS = [
    "Executive Summary",
    "Company Overview",
    "Market Analysis",
    "Competitive Landscape",
    "Financial Analysis",
    "Risk Assessment",
    "Investment Recommendation",
    "Appendix"
]

# Status messages
STATUS_PROCESSING = "🔄 Processing..."
STATUS_SUCCESS = "✅ Success!"
STATUS_ERROR = "❌ Error"
STATUS_WARNING = "⚠️ Warning"

# MENA-Specific URLs (from Links file)
MENA_DATA_SOURCES = {
    'qatar_stock_exchange': 'https://www.qe.com.qa/',
    'qfma': 'https://www.qfma.org.qa/english/pages/index.html',
    'magnitt': 'https://magnitt.com/',
    'wamda': 'https://www.wamda.com/',
    'zawya': 'https://www.zawya.com/',
    'arabian_business': 'https://www.arabianbusiness.com/',
    'gulf_business': 'https://gulfbusiness.com/',
    'al_jazeera_finance': 'https://www.aljazeera.com/tag/financial-markets/'
}

# GCC Countries
GCC_COUNTRIES = [
    'Saudi Arabia',
    'United Arab Emirates',
    'Qatar',
    'Kuwait',
    'Bahrain',
    'Oman'
]

# MENA Sectors
MENA_SECTORS = [
    'FinTech',
    'E-commerce',
    'Food & Beverage',
    'HealthTech',
    'PropTech',
    'EdTech',
    'Logistics',
    'AgriTech'
]
