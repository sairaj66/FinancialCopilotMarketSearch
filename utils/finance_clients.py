import os
from typing import Any, Dict, Optional

import requests


class ExchangeRateClient:
    """Simple ExchangeRate API client."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("EXCHANGE_RATE_API_KEY")

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "error": "EXCHANGE_RATE_API_KEY is missing. Add it to .env to enable FX conversion."
            }

        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            return {"error": str(exc)}


class TavilyNewsClient:
    """Optional Tavily client for recent finance/news search."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "error": "TAVILY_API_KEY is missing. Add it to .env to enable financial news search."
            }

        try:
            from tavily import TavilyClient

            client = TavilyClient(api_key=self.api_key)
            return client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_answer=True,
            )
        except Exception as exc:
            return {"error": str(exc)}
