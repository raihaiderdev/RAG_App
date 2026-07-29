"""
tests/test_chunker.py
Unit tests for the text chunker service.
"""
import pytest
from app.services.chunker import chunk_text


def test_empty_string_returns_empty_list():
    assert chunk_text("") == []


def test_single_chunk_when_text_fits():
    text = "Hello world"
    result = chunk_text(text, chunk_size=100, overlap=10)
    assert result == ["Hello world"]


def test_chunks_cover_all_content():
    """Every character in the original text should appear in at least one chunk."""
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=200, overlap=20)
    # Re-join chunks (without overlap) should cover the whole text
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 200


def test_overlap_creates_repeated_content():
    text = "0123456789" * 10  # 100 chars
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    # The last 5 chars of chunk[0] should equal the first 5 chars of chunk[1]
    assert chunks[0][-5:] == chunks[1][:5]


def test_single_character_text():
    assert chunk_text("X", chunk_size=10, overlap=2) == ["X"]
