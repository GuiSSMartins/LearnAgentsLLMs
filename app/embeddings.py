"""
Embedding model.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Return the embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu" # "cuda"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )