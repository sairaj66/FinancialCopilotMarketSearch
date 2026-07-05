import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

from agent.finance_agentic_workflow import FinanceGraphBuilder

load_dotenv()

app = FastAPI(
    title="Agentic Financial Information Copilot",
    description="FastAPI backend for LangGraph-powered financial copilot",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "agentic-financial-copilot"}


@app.post("/query")
async def query_financial_copilot(query: QueryRequest):
    try:
        provider = os.getenv("MODEL_PROVIDER", "groq")
        graph = FinanceGraphBuilder(model_provider=provider)
        finance_app = graph()

        messages = {"messages": [query.question]}
        output = finance_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})
