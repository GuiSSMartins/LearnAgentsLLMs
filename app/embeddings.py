"""
Embeddings module.

Loads the embedding model once and exposes it
to the rest of the application.
"""

from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Load the embedding model only once.

    The first call downloads (if necessary) and loads
    the model into memory.

    Future calls reuse the same instance.
    """

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        #model_kwargs={
        #    "device": "cpu" # "cuda" in the future with NVIDIA GPU
        #},
        model_kwargs={
            "device": settings.EMBEDDING_DEVICE
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )