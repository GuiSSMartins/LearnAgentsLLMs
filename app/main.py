"""
FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.chatbot import Chatbot
from app.ingest import ingest_documents
from app.llm import is_available
from app.models import (
    ChatRequest,
    ChatResponse,
)

# Singleton chatbot instance
chatbot = Chatbot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    """

    print("Starting RAG Chatbot...")

    yield

    print("Stopping RAG Chatbot...")


app = FastAPI(
    title="Offline RAG Chatbot",
    description="Local Retrieval-Augmented Generation API using Ollama and ChromaDB.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():

    return {
        "application": "Offline RAG Chatbot",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "llm": is_available()
    }


@app.post(
    "/chat",
    response_model=None
)
def chat(
    request: ChatRequest
):

    response = chatbot.ask(request)

    return response


@app.post("/ingest")
def ingest(
    rebuild: bool = False
):

    ingest_documents(
        rebuild=rebuild
    )

    return {
        "status": "completed",
        "rebuild": rebuild
    }


@app.exception_handler(Exception)
async def global_exception_handler(
    request,
    exc
):

    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc)
        }
    )