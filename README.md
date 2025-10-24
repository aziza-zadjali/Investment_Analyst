```markdown
# 💼 Investment Analyst AI Agent

A comprehensive AI-powered platform designed to assist investment analysts in due diligence, financial modeling, and investment memo generation. This tool accelerates deal sourcing, reduces manual effort, and improves decision-making quality.

## 🎯 Features

### 1. 🔍 AI-Powered Deal Sourcing
- Scrapes startup data from accelerators and funding platforms
- Generates daily qualified deal lists
- Filters based on custom criteria

### 2. 📄 Automated DD Document Analysis
- Ingests legal and financial documents (PDF, DOCX, XLSX)
- Extracts key data and summarizes content
- Highlights red flags automatically
- Produces analyst-ready summary reports

### 3. 🌐 Market & Competitive Analysis
- Pulls data from internal and external sources
- Generates market overviews and trend analysis
- Evaluates competitor performance
- Provides market positioning insights

### 4. 📊 Financial Modeling & Scenario Planning
- Generates projection models from raw data
- Runs what-if scenarios
- Creates editable forecasts and financial tables
- Performs sensitivity analysis

### 5. 📝 Investment Memo & Presentation Draft
- Auto-drafts memo sections and slides
- Uses consistent, professional formatting
- Generates pitch decks for analyst review

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/investment-analyst-ai.git
cd investment-analyst-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
investment-analyst-ai/
├── streamlit_app.py          # Main application entry point
├── requirements.txt           # Python dependencies
├── config.yaml               # Configuration settings
├── utils/                    # Core utility modules
│   ├── file_processor.py    # Document processing
│   ├── web_scraper.py       # Web scraping utilities
│   ├── llm_handler.py       # LLM interaction layer
│   ├── vector_store.py      # Vector storage & retrieval
│   ├── financial_analyzer.py # Financial modeling
│   └── report_generator.py  # Report generation
├── pages/                    # Streamlit pages
│   ├── 1_🔍_Deal_Sourcing.py
│   ├── 2_📄_Document_Analysis.py
│   ├── 3_🌐_Market_Analysis.py
│   ├── 4_📊_Financial_Modeling.py
│   └── 5_📝_Investment_Memo.py
└── config/                   # Configuration files
    ├── prompts.py           # LLM prompts
    └── constants.py         # Constants
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **AI Models**: OpenAI GPT-4
- **Document Processing**: PyMuPDF, python-docx, openpyxl
- **Vector Store**: FAISS
- **Data Analysis**: Pandas, NumPy
- **Web Scraping**: BeautifulSoup4, Requests
- **Visualization**: Plotly

## 💡 Usage

### Deal Sourcing
Navigate to the "Deal Sourcing" page to:
- Configure search criteria
- Scrape startup databases
- View and filter qualified deals

### Document Analysis
Upload documents for automated analysis:
- Legal contracts
- Financial statements
- Business plans
- Market reports

### Financial Modeling
Build and analyze financial models:
- Upload historical data
- Generate projections
- Run scenario analysis
- Export results

### Investment Memo Generation
Create professional investment memos:
- Select analyzed companies
- Customize sections
- Generate draft memos
- Export to PDF/DOCX

## 🔒 Security

- API keys stored in `.streamlit/secrets.toml` (not tracked by git)
- File uploads sanitized and validated
- No data stored permanently without user consent

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is designed to assist investment analysts but should not replace professional judgment. Always conduct thorough due diligence and consult with qualified professionals before making investment decisions.
```
