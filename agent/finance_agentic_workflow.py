from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from prompt_library.finance_prompt import FINANCE_SYSTEM_PROMPT
from tools.company_financials_tool import CompanyFinancialsTool
from tools.financial_calculator_tool import FinancialCalculatorTool
from tools.fx_conversion_tool import FXConversionTool
from tools.market_data_tool import MarketDataTool
from tools.news_search_tool import NewsSearchTool
from tools.portfolio_risk_tool import PortfolioRiskTool
from tools.sec_filing_rag_tool import SECFilingRAGTool
from utils.model_loader import ModelLoader


class FinanceGraphBuilder:
    """Builds a LangGraph finance agent with tool-calling capability."""

    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.tools = []

        self.market_data_tools = MarketDataTool()
        self.company_financials_tools = CompanyFinancialsTool()
        self.calculator_tools = FinancialCalculatorTool()
        self.fx_tools = FXConversionTool()
        self.news_tools = NewsSearchTool()
        self.rag_tools = SECFilingRAGTool()
        self.portfolio_tools = PortfolioRiskTool()

        self.tools.extend(
            [
                *self.market_data_tools.market_data_tool_list,
                *self.company_financials_tools.company_financials_tool_list,
                *self.calculator_tools.financial_calculator_tool_list,
                *self.fx_tools.fx_tool_list,
                *self.news_tools.news_tool_list,
                *self.rag_tools.sec_filing_tool_list,
                *self.portfolio_tools.portfolio_risk_tool_list,
            ]
        )

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.system_prompt = FINANCE_SYSTEM_PROMPT
        self.graph = None

    def agent_function(self, state: MessagesState):
        """Main finance agent node."""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("finance_agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "finance_agent")
        graph_builder.add_conditional_edges("finance_agent", tools_condition)
        graph_builder.add_edge("tools", "finance_agent")
        graph_builder.add_edge("finance_agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
