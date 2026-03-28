"""Graph traversal tool: Company -> Strategy -> Capability -> UseCase -> Outcome -> KPI

Exposes `graph_traverse(company_name)` which returns a structured dict with the paths found.
"""
from typing import Dict, List
from graph.neo4j_client import run_read


def graph_traverse(company_name: str) -> Dict[str, List[dict]]:
    """Traverse the graph starting from a company and return connected entities.

    Returns a dict with keys: strategies, capabilities, use_cases, outcomes, kpis
    """
    # Find strategies pursued by the company
    q_strat = (
        "MATCH (c:Company {name: $company})-[:PURSUES]->(s:Strategy) "
        "OPTIONAL MATCH (s)-[:REQUIRES]->(cap:Capability) "
        "RETURN s.name AS strategy, collect(DISTINCT cap.name) AS capabilities"
    )
    strat_rows = run_read(q_strat, {"company": company_name})

    strategies = []
    for r in strat_rows:
        strategies.append({"strategy": r.get('strategy'), "capabilities": r.get('capabilities')})

    # Capabilities -> UseCases -> Outcomes -> KPIs
    q_paths = (
        "MATCH (c:Company {name: $company})-[:PURSUES]->(s:Strategy)-[:REQUIRES]->(cap:Capability)-[:ENABLES]->(uc:UseCase)-[:DELIVERS]->(o:Outcome)-[:MEASURED_BY]->(k:KPI) "
        "RETURN s.name AS strategy, cap.name AS capability, uc.name AS use_case, o.name AS outcome, k.name AS kpi"
    )
    path_rows = run_read(q_paths, {"company": company_name})

    use_cases = {}
    outcomes = {}
    kpis = {}
    for r in path_rows:
        strat = r.get('strategy')
        cap = r.get('capability')
        uc = r.get('use_case')
        out = r.get('outcome')
        kpi = r.get('kpi')

        use_cases.setdefault(uc, {'use_case': uc, 'capabilities': set(), 'strategies': set()})
        use_cases[uc]['capabilities'].add(cap)
        use_cases[uc]['strategies'].add(strat)

        outcomes.setdefault(out, {'outcome': out})
        kpis.setdefault(kpi, {'kpi': kpi})

    # Normalize sets to lists
    for uc in use_cases.values():
        uc['capabilities'] = list(uc['capabilities'])
        uc['strategies'] = list(uc['strategies'])

    return {
        'company': company_name,
        'strategies': strategies,
        'use_cases': list(use_cases.values()),
        'outcomes': list(outcomes.values()),
        'kpis': list(kpis.values()),
    }
