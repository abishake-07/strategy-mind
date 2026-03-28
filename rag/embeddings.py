"""
Embedding utilities for StrategyMind RAG pipeline.

- Uses `sentence-transformers` via LangChain's `SentenceTransformerEmbeddings`.
- Reads the embedding model name from `HUGGINGFACE_EMBEDDING_MODEL` in .env (falls back to a sensible default).
"""
import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

HUGGINGFACE_EMBEDDING_MODEL = os.getenv('HUGGINGFACE_EMBEDDING_MODEL', 'all-MiniLM-L6-v2')


def get_local_sentence_transformer_embeddings(model_name: str = None):
    """Return a LangChain HuggingFaceEmbeddings instance for local embedding.

    Args:
        model_name: optional model override (HF model id or short name). If not provided,
                    reads from `HUGGINGFACE_EMBEDDING_MODEL` env var.
    """
    model = model_name or HUGGINGFACE_EMBEDDING_MODEL
    return HuggingFaceEmbeddings(model_name=model)
