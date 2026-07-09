"""
Shared data models.
"""

from dataclasses import dataclass, field
from langchain_core.documents import Document

# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------

@dataclass(slots=True)
class RetrievedDocument:
    """
    A document returned from the vector database.
    """
    document: Document
    score: float
    rank: int

# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

@dataclass(slots=True)
class ChatRequest:
    """
    Incoming chat request.
    """

    question: str
    top_k: int | None = None
    temperature: float | None = None
    include_sources: bool = True
    conversation_id: str | None = None

@dataclass(slots=True)
class ChatResponse:
    """
    Chatbot response.
    """
    answer: str
    sources: list[dict] = field(default_factory=list)