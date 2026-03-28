"""FastAPI wrapper for StrategyMind.

Endpoints:
 - POST /query  -> { "query": str, "hf_model": Optional[str] }

This module appends the project root to `sys.path` so imports work when running
via `uvicorn api.main:app --reload` from the project root.
"""
import os
import sys
from typing import Optional


from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

# Ensure project root is on path so package imports resolve when run from repo root
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)


# Tracing setup
from config.tracing import setup_tracing
setup_tracing()

from opentelemetry import trace
tracer = trace.get_tracer("strategymind.api")

from langgraph.orchestrator import orchestrate_query

app = FastAPI(title="StrategyMind API", version="0.1")


class QueryRequest(BaseModel):
    query: str
    hf_model: Optional[str] = None



@app.post("/query")
async def query(req: QueryRequest, request: Request):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query must be a non-empty string")
    with tracer.start_as_current_span("/query", attributes={"http.method": "POST", "http.route": "/query", "user_agent": request.headers.get("user-agent", "")}) as span:
        span.set_attribute("query", req.query)
        try:
            answer = orchestrate_query(req.query, hf_model=req.hf_model)
            span.set_attribute("success", True)
            return {"answer": answer}
        except Exception as e:
            span.set_attribute("success", False)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))
