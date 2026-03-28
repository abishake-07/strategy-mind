"""KPI benchmark tool: returns KPI metrics related to a use case from the graph.

Function: `kpi_benchmark(use_case_name)` returns KPIs associated with the use case.
"""
from typing import List, Dict
from graph.neo4j_client import run_read


def kpi_benchmark(use_case_name: str) -> List[Dict]:
    q = (
        "MATCH (uc:UseCase {name: $use_case})-[:DELIVERS]->(o:Outcome)-[:MEASURED_BY]->(k:KPI) "
        "RETURN collect(DISTINCT k.name) AS kpis"
    )
    rows = run_read(q, {"use_case": use_case_name})
    if not rows:
        return []
    return [{"kpi": k} for k in rows[0].get('kpis', [])]
