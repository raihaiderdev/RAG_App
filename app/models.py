import datetime
from app import db
from pgvector.sqlalchemy import Vector
from sqlalchemy import Text, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Document(db.Model):
    """Represents an uploaded PDF document."""

    __tablename__ = "documents"

    id = db.Column(Integer, primary_key=True)
    filename = db.Column(String(255), nullable=False)
    original_name = db.Column(String(255), nullable=False)
    uploaded_at = db.Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to chunks
    chunks = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self):
        return f"<Document id={self.id} filename={self.filename}>"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.original_name,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "chunk_count": len(self.chunks),
        }


class Chunk(db.Model):
    """Represents a text chunk derived from a Document, with its embedding vector."""

    __tablename__ = "chunks"

    id = db.Column(Integer, primary_key=True)
    document_id = db.Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = db.Column(Integer, nullable=False)       # position within document
    content = db.Column(Text, nullable=False)              # raw text of the chunk
    embedding = db.Column(Vector(3072))                    # pgvector — gemini-embedding-001

    # Relationship back to document
    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        return f"<Chunk id={self.id} doc_id={self.document_id} index={self.chunk_index}>"

    def to_dict(self):
        return {
            "id": self.id,
            "document_id": self.document_id,
            "chunk_index": self.chunk_index,
            "content": self.content,
        }
