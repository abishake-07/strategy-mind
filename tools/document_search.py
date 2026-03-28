"""
Document search tool used by LangGraph agent.

Provides `document_search(query, k=5)` which performs semantic search over the persisted Chroma collection.
"""
import os
from typing import List
from dotenv import load_dotenv

from langchain_core.documents import Document

from rag.chroma_index import load_chroma, CHROMA_DB_PATH

load_dotenv()


def document_search(query: str, k: int = 5) -> List[Document]:
    """Return top-k documents (LangChain Document objects) matching the query.

    Args:
        query: user query string.
        k: number of results to return.
    """
    vectordb = load_chroma(persist_directory=CHROMA_DB_PATH)
    results = vectordb.similarity_search(query, k=k)
    return results
