"""Playbook lookup tool: find playbooks covering a strategy and recommended use cases.

Function: `playbook_lookup(strategy_name)` returns playbooks and recommended use cases.
"""
from typing import List, Dict
from graph.neo4j_client import run_read


def playbook_lookup(strategy_name: str) -> List[Dict]:
    q = (
        "MATCH (pb:Playbook)-[:COVERS]->(s:Strategy {name: $strategy}) "
        "OPTIONAL MATCH (pb)-[:RECOMMENDS]->(uc:UseCase) "
        "RETURN pb.name AS playbook, collect(DISTINCT uc.name) AS recommended_use_cases"
    )
    rows = run_read(q, {"strategy": strategy_name})
    return [{"playbook": r.get('playbook'), "recommended_use_cases": r.get('recommended_use_cases')} for r in rows]
