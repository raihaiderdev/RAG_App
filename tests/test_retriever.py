"""
tests/test_retriever.py
Tests for the pgvector retriever service.
Uses an in-memory SQLite stub — swap for a real PG test DB if needed.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.retriever import retrieve_chunks


@pytest.fixture()
def mock_chunks():
    """Fake Chunk ORM objects."""
    chunks = []
    for i in range(3):
        c = MagicMock()
        c.id = i + 1
        c.content = f"chunk content {i + 1}"
        chunks.append(c)
    return chunks


def test_retrieve_returns_top_k(mock_chunks):
    with patch("app.services.retriever.db") as mock_db:
        mock_query = MagicMock()
        mock_db.session.query.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = mock_chunks[:2]

        result = retrieve_chunks([0.1] * 1536, top_k=2)

        assert len(result) == 2
        mock_query.limit.assert_called_once_with(2)


def test_retrieve_returns_empty_list_when_no_chunks():
    with patch("app.services.retriever.db") as mock_db:
        mock_query = MagicMock()
        mock_db.session.query.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        result = retrieve_chunks([0.0] * 1536, top_k=5)
        assert result == []
