from typing import List

from langchain.tools import tool


class CompanyFinancialsTool:
    """Tools for company profile, income statement, balance sheet, and cash flow."""

    def __init__(self):
        self.company_financials_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def get_company_profile(ticker: str) -> str:
            """Get company profile, sector, industry, website, and business summary."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                info = stock.info or {}

                return (
                    f"Company: {info.get('longName', ticker.upper())}\n"
                    f"Sector: {info.get('sector', 'N/A')}\n"
                    f"Industry: {info.get('industry', 'N/A')}\n"
                    f"Country: {info.get('country', 'N/A')}\n"
                    f"Website: {info.get('website', 'N/A')}\n"
                    f"Business Summary: {info.get('longBusinessSummary', 'N/A')}"
                )
            except Exception as exc:
                return f"Could not fetch company profile for {ticker}. Error: {exc}"

        @tool
        def get_income_statement_summary(ticker: str) -> str:
            """Get recent income statement summary including revenue, gross profit, operating income, and net income."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                financials = stock.financials

                if financials is None or financials.empty:
                    return f"No income statement data found for {ticker}."

                latest_col = financials.columns[0]
                wanted_rows = [
                    "Total Revenue",
                    "Gross Profit",
                    "Operating Income",
                    "Net Income",
                    "Diluted EPS",
                    "Basic EPS",
                ]

                lines = [f"Ticker: {ticker.upper()}", f"Period: {latest_col}"]
                for row in wanted_rows:
                    if row in financials.index:
                        value = financials.loc[row, latest_col]
                        lines.append(f"{row}: {value}")

                return "\n".join(lines)
            except Exception as exc:
                return f"Could not fetch income statement for {ticker}. Error: {exc}"

        @tool
        def get_balance_sheet_summary(ticker: str) -> str:
            """Get recent balance sheet summary including assets, liabilities, debt, cash, and equity."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                balance_sheet = stock.balance_sheet

                if balance_sheet is None or balance_sheet.empty:
                    return f"No balance sheet data found for {ticker}."

                latest_col = balance_sheet.columns[0]
                wanted_rows = [
                    "Total Assets",
                    "Total Liabilities Net Minority Interest",
                    "Total Debt",
                    "Cash And Cash Equivalents",
                    "Stockholders Equity",
                ]

                lines = [f"Ticker: {ticker.upper()}", f"Period: {latest_col}"]
                for row in wanted_rows:
                    if row in balance_sheet.index:
                        value = balance_sheet.loc[row, latest_col]
                        lines.append(f"{row}: {value}")

                return "\n".join(lines)
            except Exception as exc:
                return f"Could not fetch balance sheet for {ticker}. Error: {exc}"

        @tool
        def get_cash_flow_summary(ticker: str) -> str:
            """Get recent cash flow summary including operating cash flow, capex, and free cash flow."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                cashflow = stock.cashflow

                if cashflow is None or cashflow.empty:
                    return f"No cash flow data found for {ticker}."

                latest_col = cashflow.columns[0]
                wanted_rows = [
                    "Operating Cash Flow",
                    "Capital Expenditure",
                    "Free Cash Flow",
                    "Repurchase Of Capital Stock",
                    "Cash Dividends Paid",
                ]

                lines = [f"Ticker: {ticker.upper()}", f"Period: {latest_col}"]
                for row in wanted_rows:
                    if row in cashflow.index:
                        value = cashflow.loc[row, latest_col]
                        lines.append(f"{row}: {value}")

                return "\n".join(lines)
            except Exception as exc:
                return f"Could not fetch cash flow for {ticker}. Error: {exc}"

        return [
            get_company_profile,
            get_income_statement_summary,
            get_balance_sheet_summary,
            get_cash_flow_summary,
        ]
