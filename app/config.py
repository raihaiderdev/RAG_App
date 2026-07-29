import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Database (PostgreSQL + pgvector)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/rag_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini — used for BOTH embeddings and answer generation
    GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL     = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    # Chunking
    CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

    # Embeddings — gemini-embedding-001 outputs 3072 dims
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
    EMBEDDING_DIM   = int(os.getenv("EMBEDDING_DIM", 3072))

    # Retrieval
    TOP_K = int(os.getenv("TOP_K", 5))

    # File uploads
    UPLOAD_FOLDER       = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH  = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS  = {"pdf"}
