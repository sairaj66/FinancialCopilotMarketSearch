from typing import List

from langchain.tools import tool


class MarketDataTool:
    """Tools for stock price and market summary using yfinance."""

    def __init__(self):
        self.market_data_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def get_stock_price(ticker: str) -> str:
            """Get latest stock price, daily movement, volume, and market cap for a ticker."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                info = stock.info or {}
                hist = stock.history(period="5d")

                if hist.empty:
                    return f"No market price data found for ticker {ticker}."

                latest_close = float(hist["Close"].iloc[-1])
                previous_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest_close
                change = latest_close - previous_close
                change_pct = (change / previous_close) * 100 if previous_close else 0

                market_cap = info.get("marketCap", "N/A")
                volume = int(hist["Volume"].iloc[-1]) if "Volume" in hist else "N/A"
                currency = info.get("currency", "USD")

                return (
                    f"Ticker: {ticker.upper()}\n"
                    f"Latest Close: {latest_close:.2f} {currency}\n"
                    f"Previous Close: {previous_close:.2f} {currency}\n"
                    f"Daily Change: {change:.2f} ({change_pct:.2f}%)\n"
                    f"Volume: {volume}\n"
                    f"Market Cap: {market_cap}\n"
                )
            except Exception as exc:
                return f"Could not fetch stock price for {ticker}. Error: {exc}"

        @tool
        def get_market_summary(ticker: str) -> str:
            """Get broader market summary for a company ticker."""
            try:
                import yfinance as yf

                stock = yf.Ticker(ticker.upper())
                info = stock.info or {}

                fields = {
                    "Company": info.get("longName"),
                    "Ticker": ticker.upper(),
                    "Sector": info.get("sector"),
                    "Industry": info.get("industry"),
                    "Market Cap": info.get("marketCap"),
                    "Trailing P/E": info.get("trailingPE"),
                    "Forward P/E": info.get("forwardPE"),
                    "Beta": info.get("beta"),
                    "52 Week High": info.get("fiftyTwoWeekHigh"),
                    "52 Week Low": info.get("fiftyTwoWeekLow"),
                    "Dividend Yield": info.get("dividendYield"),
                    "Currency": info.get("currency"),
                }

                return "\n".join([f"{k}: {v}" for k, v in fields.items()])
            except Exception as exc:
                return f"Could not fetch market summary for {ticker}. Error: {exc}"

        return [get_stock_price, get_market_summary]
