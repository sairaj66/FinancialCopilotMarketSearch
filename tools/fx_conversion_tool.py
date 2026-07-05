from typing import List

from langchain.tools import tool

from utils.finance_clients import ExchangeRateClient


class FXConversionTool:
    """Currency conversion tool for portfolio and international finance questions."""

    def __init__(self):
        self.client = ExchangeRateClient()
        self.fx_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
            """Convert money from one currency to another."""
            result = self.client.convert(amount, from_currency, to_currency)

            if "error" in result:
                return result["error"]

            converted = result.get("conversion_result")
            rate = result.get("conversion_rate")
            return (
                f"{amount} {from_currency.upper()} = {converted} {to_currency.upper()}\n"
                f"Exchange Rate: 1 {from_currency.upper()} = {rate} {to_currency.upper()}"
            )

        return [convert_currency]
