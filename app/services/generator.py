"""
generator.py
Builds a RAG prompt from retrieved chunks and calls the Gemini API for answer generation.
Uses the same google-genai SDK and key as the embedder.
"""
from typing import List
from flask import current_app
from google import genai
from app.models import Chunk


def _build_prompt(question: str, chunks: List[Chunk]) -> str:
    """Construct the prompt sent to Gemini."""
    context_parts = []
    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(f"[Source {i}]\n{chunk.content}")

    context_block = "\n\n".join(context_parts)

    return (
        "You are a helpful assistant. Answer the user's question using ONLY the context "
        "provided below. If the answer is not contained in the context, say "
        "'I don't have enough information to answer that.'\n\n"
        f"=== Context ===\n{context_block}\n\n"
        f"=== Question ===\n{question}"
    )


def generate_answer(question: str, chunks: List[Chunk]) -> str:
    """
    Send the question + retrieved context to Gemini and return the response text.

    Args:
        question: The user's original question.
        chunks:   List of Chunk objects retrieved by the retriever.

    Returns:
        Gemini's answer as a plain string.
    """
    api_key = current_app.config.get("GEMINI_API_KEY", "")
    model = current_app.config.get("GEMINI_MODEL", "gemini-2.0-flash")

    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(question, chunks)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text
