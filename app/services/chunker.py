"""
chunker.py
Splits raw text into overlapping fixed-size character chunks.
"""
from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split *text* into chunks of *chunk_size* characters with *overlap* characters
    of context carried over between consecutive chunks.

    Args:
        text:       The raw text to split.
        chunk_size: Maximum number of characters per chunk.
        overlap:    Number of characters repeated at the start of the next chunk.

    Returns:
        A list of non-empty text chunks.
    """
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        # Advance by (chunk_size - overlap) so the next chunk starts earlier
        start += chunk_size - overlap

    return chunks
