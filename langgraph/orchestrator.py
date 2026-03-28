"""Simple orchestrator that routes queries to tools and assembles a final answer.

This module provides a `orchestrate_query(query)` function which implements
conditional routing:
 - Run `document_search` to gather relevant documents
 - If a company name is detected in the query, run `graph_traverse`
 - Else if an industry is detected, run `competitor_scan`
 - Optionally lookup playbooks or KPIs when strategies/use-cases are referenced
 - Generate final answer with HF inference API

This is written so it can be converted to LangGraph nodes later; it also works standalone.
"""

import os
from typing import Optional
from tools.document_search import document_search
from tools.graph_traverse import graph_traverse
from tools.competitor_scan import competitor_scan
from tools.playbook_lookup import playbook_lookup
from tools.kpi_benchmark import kpi_benchmark
from graph.neo4j_client import run_read
from rag.hf_llm import generate as hf_generate

# Tracing
from opentelemetry import trace
tracer = trace.get_tracer("strategymind.orchestrator")


def _detect_companies_in_query(query: str):
    q = "MATCH (c:Company) RETURN c.name AS name"
    rows = run_read(q)
    names = [r['name'] for r in rows]
    matches = [n for n in names if n.lower() in query.lower()]
    return matches


def _detect_industries_in_query(query: str):
    q = "MATCH (i:Industry) RETURN i.name AS name"
    rows = run_read(q)
    names = [r['name'] for r in rows]
    matches = [n for n in names if n.lower() in query.lower()]
    return matches


def _assemble_prompt(query: str, docs=None, traversal=None, competitors=None, playbooks=None, kpis=None) -> str:
    parts = [f"User query: {query}"]
    if docs:
        parts.append("\nRelevant documents and excerpts:\n")
        for d in docs[:5]:
            src = d.metadata.get('source') if hasattr(d, 'metadata') else getattr(d, 'source', 'unknown')
            parts.append(f"Source: {src}\n{d.page_content[:800]}\n---\n")
    if traversal:
        parts.append("\nGraph traversal results:\n")
        parts.append(str(traversal))
    if competitors:
        parts.append("\nCompetitor scan:\n")
        parts.append(str(competitors))
    if playbooks:
        parts.append("\nPlaybooks:\n")
        parts.append(str(playbooks))
    if kpis:
        parts.append("\nKPIs:\n")
        parts.append(str(kpis))

    parts.append("\nPlease synthesize a concise, actionable consulting-style answer combining the graph insights and document evidence. Highlight recommended playbooks and KPIs when relevant.")
    return "\n".join(parts)


def orchestrate_query(query: str, hf_model: Optional[str] = None) -> str:
    """Orchestrate a query across RAG and graph tools, return generated answer string."""
    with tracer.start_as_current_span("orchestrate_query", attributes={"query": query}) as span:
        # Step 1: semantic doc search
        with tracer.start_as_current_span("document_search") as doc_span:
            try:
                docs = document_search(query, k=6)
            except Exception as e:
                docs = []
            doc_span.set_attribute("num_docs", len(docs))

        # Step 2: detect entities
        companies = _detect_companies_in_query(query)
        industries = _detect_industries_in_query(query)

        traversal = None
        competitors = None
        playbooks = None
        kpis = None

        if companies:
            with tracer.start_as_current_span("graph_traverse") as gt_span:
                traversal = graph_traverse(companies[0])
                gt_span.set_attribute("company", companies[0])
            # look up playbooks for strategies found
            if traversal.get('strategies'):
                strategy_names = [s.get('strategy') for s in traversal.get('strategies') if s.get('strategy')]
                if strategy_names:
                    playbooks = []
                    for sname in strategy_names:
                        with tracer.start_as_current_span("playbook_lookup") as pb_span:
                            pb_span.set_attribute("strategy", sname)
                            playbooks.extend(playbook_lookup(sname))
        elif industries:
            with tracer.start_as_current_span("competitor_scan") as cs_span:
                competitors = competitor_scan(industries[0])
                cs_span.set_attribute("industry", industries[0])

        # If use cases mentioned, fetch KPI benchmarks (simple heuristic: look for use case names)
        # Query graph for use cases and see if any are present in the query
        uc_rows = run_read("MATCH (uc:UseCase) RETURN uc.name AS name")
        uc_names = [r['name'] for r in uc_rows]
        uc_matches = [u for u in uc_names if u.lower() in query.lower()]
        if uc_matches:
            kpis = []
            for uc in uc_matches:
                with tracer.start_as_current_span("kpi_benchmark") as kpi_span:
                    kpi_span.set_attribute("use_case", uc)
                    kpis.extend(kpi_benchmark(uc))

        # Assemble prompt and generate
        prompt = _assemble_prompt(query, docs=docs, traversal=traversal, competitors=competitors, playbooks=playbooks, kpis=kpis)
        with tracer.start_as_current_span("hf_generate") as llm_span:
            llm_span.set_attribute("model", hf_model or "default")
            try:
                answer = hf_generate(prompt, model=hf_model)
            except Exception as e:
                # Fallback if HF API fails
                answer = f"Unable to generate response via HF API: {str(e)}. Here's the context:\n\n{prompt[:500]}"
            llm_span.set_attribute("answer_length", len(answer) if answer else 0)
        return answer
