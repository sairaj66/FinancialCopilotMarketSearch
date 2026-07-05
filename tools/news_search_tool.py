from typing import List

from langchain.tools import tool

from utils.finance_clients import TavilyNewsClient


class NewsSearchTool:
    """Financial news search tool using Tavily when API key is configured."""

    def __init__(self):
        self.client = TavilyNewsClient()
        self.news_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def search_financial_news(query: str) -> str:
            """Search recent financial news for a company, ticker, market, or financial topic."""
            result = self.client.search(query=f"latest financial news {query}", max_results=5)

            if "error" in result:
                return result["error"]

            answer = result.get("answer", "")
            results = result.get("results", [])

            lines = []
            if answer:
                lines.append(f"Summary: {answer}")

            for item in results[:5]:
                title = item.get("title", "Untitled")
                url = item.get("url", "N/A")
                content = item.get("content", "")
                lines.append(f"- {title}\n  URL: {url}\n  Summary: {content[:500]}")

            return "\n".join(lines) if lines else "No financial news results found."

        return [search_financial_news]
