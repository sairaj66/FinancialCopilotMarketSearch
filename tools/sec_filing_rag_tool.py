from typing import List

from langchain.tools import tool

from utils.rag_store import search_vector_store


class SECFilingRAGTool:
    """RAG tool for SEC filings, annual reports, and internal financial documents."""

    def __init__(self):
        self.sec_filing_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def search_financial_documents(question: str) -> str:
            """Search uploaded SEC filings, annual reports, earnings transcripts, or internal financial documents."""
            return search_vector_store(question=question, k=4)

        return [search_financial_documents]
