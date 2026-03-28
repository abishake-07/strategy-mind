"""
Chroma index builder for StrategyMind RAG.

Creates a persistent Chroma vector store from PDFs in a directory.
"""
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from .pdf_loader import load_and_split_pdfs
from .embeddings import get_local_sentence_transformer_embeddings

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'chroma_db'))


def build_chroma_from_pdfs(pdf_dir: str, persist_directory: str = None, embedding_model: Embeddings = None, collection_name: str = 'strategymind'):
    """Load PDFs, embed, and persist a Chroma collection.

    Args:
        pdf_dir: directory with PDF files.
        persist_directory: where Chroma will persist vectors (defaults to `CHROMA_DB_PATH`).
        embedding_model: LangChain embeddings instance. If None, uses local SentenceTransformer.
        collection_name: Chroma collection name.
    """
    persist_directory = persist_directory or CHROMA_DB_PATH
    embeddings = embedding_model or get_local_sentence_transformer_embeddings()

    docs = load_and_split_pdfs(pdf_dir)
    if not docs:
        raise ValueError(f'No documents found in {pdf_dir}')

    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name)
    return vectordb


def load_chroma(persist_directory: str = None, embedding_model: Embeddings = None, collection_name: str = 'strategymind'):
    persist_directory = persist_directory or CHROMA_DB_PATH
    embeddings = embedding_model or get_local_sentence_transformer_embeddings()
    return Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
