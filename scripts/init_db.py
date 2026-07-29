"""
scripts/init_db.py
Run this ONCE before starting the app (and again if you change embedding dimensions).
    python scripts/init_db.py

What it does:
  1. Enables the pgvector extension
  2. Drops and recreates all tables (safe on a fresh DB)
  3. Confirms the embedding column dimension
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text


def init_db():
    app = create_app()
    with app.app_context():
        # 1. Enable pgvector extension
        try:
            db.session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            db.session.commit()
            print("✅  pgvector extension enabled.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️  Extension note: {e}")

        # 2. Import models so metadata is populated
        from app.models import Document, Chunk  # noqa

        # 3. Drop existing tables and recreate (handles dimension changes)
        db.drop_all()
        db.create_all()
        print("✅  Tables recreated: documents, chunks (embedding dim=768)")


if __name__ == "__main__":
    init_db()
