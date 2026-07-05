# Agentic Financial Information Copilot

An end-to-end Agentic AI application built using **Streamlit + FastAPI + LangGraph + LangChain tools**.

This project is adapted from the AI Trip Planner architecture pattern:
- Streamlit frontend sends a user query to FastAPI.
- FastAPI invokes a LangGraph agent.
- LangGraph decides whether to answer directly or call finance tools.
- Tools fetch market data, company financials, FX conversion, news, filings/RAG, and financial calculations.
- Final answer is returned as a structured financial report.

> Disclaimer: This application is for financial information and education only. It does not provide investment, tax, or legal advice.

---

## Features

- Stock price and market summary
- Company profile and financial metrics
- Financial ratio calculations
- Currency conversion
- Financial news search
- SEC filing / internal document RAG search
- Portfolio risk summary
- Streamlit report UI
- FastAPI backend
- LangGraph ReAct-style tool loop
- Groq/OpenAI model support

---

## Project Structure

```text
agentic_financial_copilot/
├── agent/
│   └── finance_agentic_workflow.py
├── config/
│   └── config.yaml
├── data/
│   ├── financial_docs/
│   │   └── .gitkeep
│   └── vector_store/
│       └── .gitkeep
├── prompt_library/
│   └── finance_prompt.py
├── scripts/
│   └── ingest_documents.py
├── tools/
│   ├── company_financials_tool.py
│   ├── financial_calculator_tool.py
│   ├── fx_conversion_tool.py
│   ├── market_data_tool.py
│   ├── news_search_tool.py
│   ├── portfolio_risk_tool.py
│   └── sec_filing_rag_tool.py
├── utils/
│   ├── config_loader.py
│   ├── document_loader.py
│   ├── finance_clients.py
│   ├── model_loader.py
│   └── rag_store.py
├── .env.example
├── main.py
├── pyproject.toml
├── requirements.txt
└── streamlit_app.py
```

---

## Setup

### 1. Create virtual environment

```bash
python -m venv env
```

Windows:

```bash
env\Scripts\activate
```

Mac/Linux:

```bash
source env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy:

```bash
cp .env.example .env
```

Add at least one LLM key:

```bash
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Optional:

```bash
TAVILY_API_KEY=your_key_here
EXCHANGE_RATE_API_KEY=your_key_here
```

---

## Run Backend

```bash
uvicorn main:app --reload --port 8000
```

Health check:

```bash
http://localhost:8000/health
```

---

## Run Streamlit UI

In another terminal:

```bash
streamlit run streamlit_app.py
```

---

## Example Questions

```text
Analyze Apple stock and give me price, market cap, P/E ratio, latest news, and risk flags.
```

```text
Compare MSFT and NVDA based on market cap, revenue, profit margin, and business risk.
```

```text
Calculate debt-to-equity ratio if debt is 1200000 and equity is 3500000.
```

```text
Convert 25000 USD to INR.
```

```text
Summarize risk factors from uploaded financial documents for Apple.
```

```text
My portfolio is AAPL 40%, MSFT 30%, NVDA 30%. Give me a risk summary.
```

---

## Ingest Financial Documents for RAG

Put PDFs, TXT, or MD files into:

```text
data/financial_docs/
```

Then run:

```bash
python scripts/ingest_documents.py
```

This creates a local FAISS vector index in:

```text
data/vector_store/
```

---

## Notes

- `yfinance` is used for market data and company financials.
- `Tavily` is optional for web/news search.
- ExchangeRate API is optional. If no API key is provided, FX conversion returns a clear error.
- The RAG tool works after document ingestion.
- The copilot should not invent numbers. If data is unavailable, it should say so.
