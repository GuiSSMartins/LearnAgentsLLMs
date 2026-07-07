"""
ChromaDB database management.

Responsible for:
- Initializing the vector database
- Storing documents
- Performing similarity search
"""

from functools import lru_cache
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.embeddings import get_embeddings


@lru_cache(maxsize=1)
def get_database() -> Chroma:
    """
    Create (or load) the Chroma database.

    If the database already exists on disk,
    it will simply be reopened.
    """

    return Chroma(
        collection_name=settings.COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.CHROMA_PATH)
    )


def add_documents(documents: List[Document]) -> None:
    """
    Store documents in Chroma.
    """

    db = get_database()

    db.add_documents(documents)

def get_retriever():
    db = get_database()

    return db.as_retriever(
        search_kwargs={
            "k": settings.TOP_K
        }
    )

def similarity_search(
    query: str,
    k: int | None = None
) -> List[Document]:
    """
    Search the vector database.

    Returns the most relevant documents.
    """

    db = get_database()

    return db.similarity_search(
        query,
        k=k or settings.TOP_K
    )


def clear_database() -> None:
    """
    Delete every document from the collection.

    Useful when rebuilding the knowledge base.
    """

    db = get_database()

    db.delete_collection()

    get_database.cache_clear()