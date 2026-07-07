"""
Application configuration.

This module is the ONLY place that should read environment variables.
Every other module imports the `settings` object.
"""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Load .env from the project root
load_dotenv()


@dataclass(frozen=True)
class Settings:

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    APP_NAME: str = os.getenv("APP_NAME", "Local RAG Chatbot")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    

    # --------------------------------------------------
    # Ollama
    # --------------------------------------------------

    OLLAMA_HOST: str = os.getenv(
        "OLLAMA_HOST",
        "http://ollama:11434"
    )

    OLLAMA_MODEL: str = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:3b"
    )

    # --------------------------------------------------
    # Chroma
    # --------------------------------------------------

    CHROMA_PATH: Path = Path(
        os.getenv("CHROMA_PATH", "/app/chroma")
    )

    COLLECTION_NAME: str = os.getenv(
        "COLLECTION_NAME",
        "knowledge"
    )

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5"
    )

    EMBEDDING_DEVICE: str = os.getenv(
        "EMBEDDING_DEVICE",
        "cpu"
    )

    # --------------------------------------------------
    # Documents
    # --------------------------------------------------

    DATA_PATH: Path = Path(
        os.getenv("DATA_PATH", "/app/data")
    )

    CHUNK_SIZE: int = int(
        os.getenv("CHUNK_SIZE", 800)
    )

    CHUNK_OVERLAP: int = int(
        os.getenv("CHUNK_OVERLAP", 120)
    )

    TOP_K: int = int(
        os.getenv("TOP_K", 5)
    )

    # --------------------------------------------------
    # Generation
    # --------------------------------------------------

    TEMPERATURE: float = float(
        os.getenv("TEMPERATURE", 0.2)
    )

    MAX_TOKENS: int = int(
        os.getenv("MAX_TOKENS", 2048)
    )

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

def create_directories(settings: Settings) -> None:
    settings.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    settings.DATA_PATH.mkdir(parents=True, exist_ok=True)

settings = Settings()

create_directories(settings)