"""
Local LLM client.

Responsible only for communicating
with the Ollama server.
"""

from functools import lru_cache
from ollama import Client
from ollama import ResponseError
from httpx import ConnectError
from app.config import settings


@lru_cache(maxsize=1)
def get_llm() -> Client:
    """
    Return a singleton Ollama client.
    """
    return Client(
        host=settings.OLLAMA_HOST
    )


def generate(
    prompt: str,
    system: str | None = None,
    temperature: float | None = None
) -> str:
    """
    Generate a response from the local LLM.
    """

    client = get_llm()
    messages = []
    if system:
        messages.append(
            {
                "role": "system",
                "content": system
            }
        )
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:
        response = client.chat(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            options={
                "temperature": (
                    temperature
                    if temperature is not None
                    else settings.TEMPERATURE
                ),
                "num_predict": settings.MAX_TOKENS,
                "num_thread": settings.OLLAMA_NUM_THREAD
            }
        )

    except ConnectError:
        raise RuntimeError(
            "Cannot connect to Ollama."
        )

    except ResponseError as exc:
        raise RuntimeError(
            f"Ollama error: {exc}"
        )

    return response.message.content

def is_available() -> bool:

    try:
        get_llm().ps()
        return True

    except Exception:
        return False