"""
RAG chatbot.

Coordinates the Retrieval-Augmented Generation pipeline.
"""

from app.llm import generate
from app.prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)
from app.retriever import Retriever

from app.models import (
    ChatRequest,
    ChatResponse,
)


class Chatbot:

    def __init__(self):
        self.retriever = Retriever()

    def ask(
        self,
        request: ChatRequest
    ) -> ChatResponse:
        """
        Answer a question using RAG.
        """

        retrieved_documents = self.retriever.search(
            request.question
        )
        prompt = build_prompt(
            request.question,
            retrieved_documents
        )
        answer = generate(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            temperature=request.temperature
        )
        response = ChatResponse(
            answer=answer
        )

        if request.include_sources:
            response.sources = self._extract_sources(
                retrieved_documents
            )

        return response

    @staticmethod
    def _extract_sources(
        retrieved_documents
    ) -> list[dict]:
        """
        Convert retrieved documents into source metadata.
        """

        sources = []

        for retrieved in retrieved_documents:
            metadata = dict(
                retrieved.document.metadata
            )
            metadata["rank"] = retrieved.rank
            metadata["score"] = round(
                retrieved.score,
                4 # just to make it simpler and more readable
            )
            sources.append(metadata)

        return sources