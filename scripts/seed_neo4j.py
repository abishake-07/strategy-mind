"""
Neo4j seeding script for StrategyMind
Populates a knowledge graph with realistic sample data for automotive and financial services industries.
Uses .env for secrets.
"""
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def seed_graph(driver):
    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")

        # Industries
        industries = [
            {"name": "Automotive"},
            {"name": "Financial Services"}
        ]
        for ind in industries:
            session.run("CREATE (:Industry {name: $name})", name=ind["name"])

        # Segments
        segments = [
            {"name": "OEM", "industry": "Automotive"},
            {"name": "Supplier", "industry": "Automotive"},
            {"name": "Retail Banking", "industry": "Financial Services"},
            {"name": "Wealth Management", "industry": "Financial Services"}
        ]
        for seg in segments:
            session.run("""
                MATCH (i:Industry {name: $industry})
                CREATE (s:Segment {name: $name})<-[:HAS_SEGMENT]-(i)
            """, name=seg["name"], industry=seg["industry"])

        # Companies
        companies = [
            {"name": "AutoMakers Inc", "industry": "Automotive"},
            {"name": "DriveTech", "industry": "Automotive"},
            {"name": "FinTrust Bank", "industry": "Financial Services"},
            {"name": "SecureWealth", "industry": "Financial Services"},
            {"name": "MobilityX", "industry": "Automotive"}
        ]
        for comp in companies:
            session.run("""
                MATCH (i:Industry {name: $industry})
                CREATE (c:Company {name: $name})-[:OPERATES_IN]->(i)
            """, name=comp["name"], industry=comp["industry"])

        # Strategies
        strategies = [
            {"name": "AI-Driven Manufacturing", "industry": "Automotive"},
            {"name": "Digital Lending", "industry": "Financial Services"},
            {"name": "Connected Mobility", "industry": "Automotive"},
            {"name": "Personalized Banking", "industry": "Financial Services"}
        ]
        for strat in strategies:
            session.run("CREATE (:Strategy {name: $name, industry: $industry})", name=strat["name"], industry=strat["industry"])

        # Capabilities
        capabilities = [
            {"name": "Predictive Maintenance"},
            {"name": "Customer Analytics"},
            {"name": "Automated Underwriting"},
            {"name": "Fleet Management"}
        ]
        for cap in capabilities:
            session.run("CREATE (:Capability {name: $name})", name=cap["name"])

        # UseCases
        use_cases = [
            {"name": "Reduce Downtime"},
            {"name": "Increase Loan Approvals"},
            {"name": "Enhance Customer Experience"},
            {"name": "Optimize Fleet Usage"}
        ]
        for uc in use_cases:
            session.run("CREATE (:UseCase {name: $name})", name=uc["name"])

        # Outcomes
        outcomes = [
            {"name": "Higher Uptime"},
            {"name": "Faster Loan Processing"},
            {"name": "Improved NPS"},
            {"name": "Lower Operating Costs"}
        ]
        for out in outcomes:
            session.run("CREATE (:Outcome {name: $name})", name=out["name"])

        # KPIs
        kpis = [
            {"name": "Uptime %"},
            {"name": "Loan Approval Rate"},
            {"name": "Net Promoter Score"},
            {"name": "Cost per Mile"}
        ]
        for kpi in kpis:
            session.run("CREATE (:KPI {name: $name})", name=kpi["name"])

        # Playbooks
        playbooks = [
            {"name": "AI Manufacturing Playbook"},
            {"name": "Digital Lending Playbook"}
        ]
        for pb in playbooks:
            session.run("CREATE (:Playbook {name: $name})", name=pb["name"])

        # Business Challenges
        challenges = [
            {"name": "Reduce Costs"},
            {"name": "Increase Revenue"}
        ]
        for ch in challenges:
            session.run("CREATE (:BusinessChallenge {name: $name})", name=ch["name"])

        # Relationships
        # Company -> Strategy
        session.run("""
            MATCH (c:Company {name: 'AutoMakers Inc'}), (s:Strategy {name: 'AI-Driven Manufacturing'})
            CREATE (c)-[:PURSUES]->(s)
        """)
        session.run("""
            MATCH (c:Company {name: 'DriveTech'}), (s:Strategy {name: 'Connected Mobility'})
            CREATE (c)-[:PURSUES]->(s)
        """)
        session.run("""
            MATCH (c:Company {name: 'FinTrust Bank'}), (s:Strategy {name: 'Digital Lending'})
            CREATE (c)-[:PURSUES]->(s)
        """)
        session.run("""
            MATCH (c:Company {name: 'SecureWealth'}), (s:Strategy {name: 'Personalized Banking'})
            CREATE (c)-[:PURSUES]->(s)
        """)
        session.run("""
            MATCH (c:Company {name: 'MobilityX'}), (s:Strategy {name: 'Connected Mobility'})
            CREATE (c)-[:PURSUES]->(s)
        """)

        # Company -> Capability
        session.run("""
            MATCH (c:Company {name: 'AutoMakers Inc'}), (cap:Capability {name: 'Predictive Maintenance'})
            CREATE (c)-[:HAS_CAPABILITY]->(cap)
        """)
        session.run("""
            MATCH (c:Company {name: 'FinTrust Bank'}), (cap:Capability {name: 'Automated Underwriting'})
            CREATE (c)-[:HAS_CAPABILITY]->(cap)
        """)

        # Strategy -> Capability
        session.run("""
            MATCH (s:Strategy {name: 'AI-Driven Manufacturing'}), (cap:Capability {name: 'Predictive Maintenance'})
            CREATE (s)-[:REQUIRES]->(cap)
        """)
        session.run("""
            MATCH (s:Strategy {name: 'Digital Lending'}), (cap:Capability {name: 'Automated Underwriting'})
            CREATE (s)-[:REQUIRES]->(cap)
        """)

        # Strategy -> BusinessChallenge
        session.run("""
            MATCH (s:Strategy {name: 'AI-Driven Manufacturing'}), (bc:BusinessChallenge {name: 'Reduce Costs'})
            CREATE (s)-[:ADDRESSES]->(bc)
        """)
        session.run("""
            MATCH (s:Strategy {name: 'Digital Lending'}), (bc:BusinessChallenge {name: 'Increase Revenue'})
            CREATE (s)-[:ADDRESSES]->(bc)
        """)

        # Capability -> UseCase
        session.run("""
            MATCH (cap:Capability {name: 'Predictive Maintenance'}), (uc:UseCase {name: 'Reduce Downtime'})
            CREATE (cap)-[:ENABLES]->(uc)
        """)
        session.run("""
            MATCH (cap:Capability {name: 'Automated Underwriting'}), (uc:UseCase {name: 'Increase Loan Approvals'})
            CREATE (cap)-[:ENABLES]->(uc)
        """)

        # UseCase -> Outcome
        session.run("""
            MATCH (uc:UseCase {name: 'Reduce Downtime'}), (out:Outcome {name: 'Higher Uptime'})
            CREATE (uc)-[:DELIVERS]->(out)
        """)
        session.run("""
            MATCH (uc:UseCase {name: 'Increase Loan Approvals'}), (out:Outcome {name: 'Faster Loan Processing'})
            CREATE (uc)-[:DELIVERS]->(out)
        """)

        # Outcome -> KPI
        session.run("""
            MATCH (out:Outcome {name: 'Higher Uptime'}), (k:KPI {name: 'Uptime %'})
            CREATE (out)-[:MEASURED_BY]->(k)
        """)
        session.run("""
            MATCH (out:Outcome {name: 'Faster Loan Processing'}), (k:KPI {name: 'Loan Approval Rate'})
            CREATE (out)-[:MEASURED_BY]->(k)
        """)

        # Playbook -> Strategy
        session.run("""
            MATCH (pb:Playbook {name: 'AI Manufacturing Playbook'}), (s:Strategy {name: 'AI-Driven Manufacturing'})
            CREATE (pb)-[:COVERS]->(s)
        """)
        session.run("""
            MATCH (pb:Playbook {name: 'Digital Lending Playbook'}), (s:Strategy {name: 'Digital Lending'})
            CREATE (pb)-[:COVERS]->(s)
        """)

        # Playbook -> UseCase
        session.run("""
            MATCH (pb:Playbook {name: 'AI Manufacturing Playbook'}), (uc:UseCase {name: 'Reduce Downtime'})
            CREATE (pb)-[:RECOMMENDS]->(uc)
        """)
        session.run("""
            MATCH (pb:Playbook {name: 'Digital Lending Playbook'}), (uc:UseCase {name: 'Increase Loan Approvals'})
            CREATE (pb)-[:RECOMMENDS]->(uc)
        """)

        # UseCase -> Industry
        session.run("""
            MATCH (uc:UseCase {name: 'Reduce Downtime'}), (i:Industry {name: 'Automotive'})
            CREATE (uc)-[:APPLIES_TO]->(i)
        """)
        session.run("""
            MATCH (uc:UseCase {name: 'Increase Loan Approvals'}), (i:Industry {name: 'Financial Services'})
            CREATE (uc)-[:APPLIES_TO]->(i)
        """)

    print("Neo4j graph seeded successfully.")

def main():
    if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
        print("Please set NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD in your .env file.")
        return
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        seed_graph(driver)
    finally:
        driver.close()

if __name__ == "__main__":
    main()
