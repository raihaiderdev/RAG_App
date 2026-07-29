"""
retriever.py
Performs a nearest-neighbour similarity search against pgvector.
"""
from typing import List
from app import db
from app.models import Chunk
from pgvector.sqlalchemy import Vector
from sqlalchemy import cast


def retrieve_chunks(query_embedding: List[float], top_k: int = 5) -> List[Chunk]:
    """
    Find the *top_k* most semantically similar Chunk rows to *query_embedding*
    using the pgvector cosine-distance operator (<=>).

    Args:
        query_embedding: Plain Python list of floats (embedding of the user question).
        top_k:           Number of results to return.

    Returns:
        List of Chunk ORM objects ordered by similarity (closest first).
    """
    # Cast the Python list to a pgvector Vector so SQLAlchemy emits the right SQL
    vector_query = cast(query_embedding, Vector(3072))

    results = (
        db.session.query(Chunk)
        .order_by(Chunk.embedding.cosine_distance(vector_query))
        .limit(top_k)
        .all()
    )
    return results
