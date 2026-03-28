"""
PDF loader and chunker for RAG.

Functions:
 - `load_and_split_pdfs(dir_path, chunk_size=1000, chunk_overlap=200)`

Produces a list of `langchain.schema.Document` objects with `page_content` and `metadata.source`.
"""
import os
from typing import List
from dotenv import load_dotenv

from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def _extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def load_and_split_pdfs(dir_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Load all PDFs from `dir_path`, extract text, and split into chunks.

    Args:
        dir_path: directory containing PDF files.
        chunk_size: maximum characters per chunk.
        chunk_overlap: overlap between chunks.

    Returns:
        List of `Document` objects ready for embedding/indexing.
    """
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents: List[Document] = []

    for fname in os.listdir(dir_path):
        if not fname.lower().endswith('.pdf'):
            continue
        path = os.path.join(dir_path, fname)
        text = _extract_text_from_pdf(path)
        if not text.strip():
            continue
        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            metadata = {"source": path, "chunk": i}
            documents.append(Document(page_content=chunk, metadata=metadata))

    return documents
