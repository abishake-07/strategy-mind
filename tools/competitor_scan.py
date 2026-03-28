"""Competitor scan tool: compares companies in an industry by strategy and capability.

Function: `competitor_scan(industry_name)` returns a list of companies with strategies and capabilities.
"""
from typing import List, Dict
from graph.neo4j_client import run_read


def competitor_scan(industry_name: str) -> List[Dict]:
    q = (
        "MATCH (i:Industry {name: $industry})<-[:OPERATES_IN]-(c:Company) "
        "OPTIONAL MATCH (c)-[:PURSUES]->(s:Strategy) "
        "OPTIONAL MATCH (c)-[:HAS_CAPABILITY]->(cap:Capability) "
        "RETURN c.name AS company, collect(DISTINCT s.name) AS strategies, collect(DISTINCT cap.name) AS capabilities"
    )
    rows = run_read(q, {"industry": industry_name})
    return [{"company": r.get('company'), "strategies": r.get('strategies'), "capabilities": r.get('capabilities')} for r in rows]
