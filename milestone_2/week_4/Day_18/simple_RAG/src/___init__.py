"""
WEF Financial Policy RAG Chatbot Package
"""

from .rag_pipeline import FinancialPolicyRAG
from .embeddings import get_embedding
from .utils import load_and_chunk_pdf

__version__ = "1.0.0"
__all__ = [
    "FinancialPolicyRAG",
    "get_embedding",
    "load_and_chunk_pdf"
]