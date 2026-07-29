"""
embedder.py
Converts a list of text strings into embedding vectors via Google Gemini.
Uses the new `google-genai` SDK (google.genai), NOT the deprecated google-generativeai.
Model: models/text-embedding-004  →  768-dimensional vectors
"""
from typing import List
from flask import current_app
from google import genai
from google.genai import types


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts using Gemini's embedding API.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (each a plain Python list of 768 floats).
    """
    if not texts:
        return []

    api_key = current_app.config.get("GEMINI_API_KEY", "")
    model = current_app.config.get("EMBEDDING_MODEL", "models/text-embedding-004")

    client = genai.Client(api_key=api_key)

    embeddings: List[List[float]] = []

    # Gemini embed_content handles one text at a time or a batch via contents list
    response = client.models.embed_content(
        model=model,
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )

    for emb in response.embeddings:
        embeddings.append(list(emb.values))

    return embeddings
