from typing import List

from langchain.tools import tool


class FinancialCalculatorTool:
    """Financial calculation tools used by the agent."""

    def __init__(self):
        self.financial_calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def calculate_pe_ratio(price: float, eps: float) -> str:
            """Calculate price-to-earnings ratio. Formula: price / EPS."""
            if eps == 0:
                return "P/E ratio cannot be calculated because EPS is zero."
            result = price / eps
            return f"P/E Ratio = Price / EPS = {price} / {eps} = {result:.2f}"

        @tool
        def calculate_debt_to_equity(total_debt: float, total_equity: float) -> str:
            """Calculate debt-to-equity ratio. Formula: total debt / total equity."""
            if total_equity == 0:
                return "Debt-to-equity ratio cannot be calculated because total equity is zero."
            result = total_debt / total_equity
            return f"Debt-to-Equity = Total Debt / Total Equity = {total_debt} / {total_equity} = {result:.2f}"

        @tool
        def calculate_profit_margin(net_income: float, revenue: float) -> str:
            """Calculate net profit margin percentage. Formula: net income / revenue * 100."""
            if revenue == 0:
                return "Profit margin cannot be calculated because revenue is zero."
            result = (net_income / revenue) * 100
            return f"Net Profit Margin = Net Income / Revenue * 100 = {result:.2f}%"

        @tool
        def calculate_revenue_growth(current_revenue: float, previous_revenue: float) -> str:
            """Calculate revenue growth percentage."""
            if previous_revenue == 0:
                return "Revenue growth cannot be calculated because previous revenue is zero."
            result = ((current_revenue - previous_revenue) / previous_revenue) * 100
            return f"Revenue Growth = ((Current - Previous) / Previous) * 100 = {result:.2f}%"

        @tool
        def calculate_portfolio_return(initial_value: float, current_value: float) -> str:
            """Calculate portfolio return percentage."""
            if initial_value == 0:
                return "Portfolio return cannot be calculated because initial value is zero."
            result = ((current_value - initial_value) / initial_value) * 100
            return f"Portfolio Return = ((Current - Initial) / Initial) * 100 = {result:.2f}%"

        return [
            calculate_pe_ratio,
            calculate_debt_to_equity,
            calculate_profit_margin,
            calculate_revenue_growth,
            calculate_portfolio_return,
        ]
