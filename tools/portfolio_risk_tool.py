from typing import List

from langchain.tools import tool


class PortfolioRiskTool:
    """Simple portfolio concentration and risk helper."""

    def __init__(self):
        self.portfolio_risk_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def analyze_portfolio_concentration(holdings: str) -> str:
            """
            Analyze portfolio concentration risk.
            Input format example: AAPL:40, MSFT:30, NVDA:30
            Values are percentages.
            """
            try:
                parsed = []
                for item in holdings.split(","):
                    ticker, weight = item.strip().split(":")
                    parsed.append((ticker.strip().upper(), float(weight.strip())))

                total_weight = sum(weight for _, weight in parsed)
                largest = max(parsed, key=lambda x: x[1])
                top_three = sorted(parsed, key=lambda x: x[1], reverse=True)[:3]
                top_three_weight = sum(weight for _, weight in top_three)

                risk_flags = []
                if largest[1] > 35:
                    risk_flags.append(f"High single-name concentration: {largest[0]} is {largest[1]}%.")
                if top_three_weight > 70:
                    risk_flags.append(f"Top 3 holdings are {top_three_weight}%, which may indicate concentration risk.")
                if abs(total_weight - 100) > 1:
                    risk_flags.append(f"Portfolio weights sum to {total_weight}%, not 100%.")

                if not risk_flags:
                    risk_flags.append("No major concentration flags detected from weights alone.")

                holdings_text = "\n".join([f"- {ticker}: {weight}%" for ticker, weight in parsed])
                flags_text = "\n".join([f"- {flag}" for flag in risk_flags])

                return f"Holdings:\n{holdings_text}\n\nRisk Flags:\n{flags_text}"
            except Exception as exc:
                return (
                    "Could not parse holdings. Use format like: AAPL:40, MSFT:30, NVDA:30. "
                    f"Error: {exc}"
                )

        return [analyze_portfolio_concentration]
