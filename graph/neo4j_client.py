"""Neo4j client helper for StrategyMind.

Provides a simple driver singleton and helpers for read/write transactions.
"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
            raise RuntimeError('NEO4J_URI, NEO4J_USER and NEO4J_PASSWORD must be set in .env')
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def run_read(query: str, params: dict = None):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]


def run_write(query: str, params: dict = None):
    driver = get_driver()
    with driver.session() as session:
        session.run(query, params or {})
