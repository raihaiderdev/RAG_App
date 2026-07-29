# RAG Flask App

A Retrieval-Augmented Generation (RAG) API built with Flask, PostgreSQL + pgvector, OpenAI embeddings, and Claude (Anthropic) for answer generation.

---

## Project Structure

```
rag-flask-app/
├── app/
│   ├── __init__.py          # App factory, extension init
│   ├── config.py            # DB URL, API keys, chunk settings
│   ├── models.py            # SQLAlchemy models: Document, Chunk
│   ├── routes/
│   │   ├── ingest.py        # POST /upload  — PDF ingestion pipeline
│   │   └── query.py         # POST /ask     — question answering
│   ├── services/
│   │   ├── extractor.py     # PDF → raw text (PyMuPDF)
│   │   ├── chunker.py       # text → overlapping chunks
│   │   ├── embedder.py      # text → embedding vectors (OpenAI)
│   │   ├── retriever.py     # cosine similarity search (pgvector)
│   │   └── generator.py     # RAG prompt + Claude API call
│   └── templates/
│       └── index.html       # Minimal browser UI
├── migrations/              # Alembic migration files
├── scripts/
│   └── init_db.py           # Create pgvector extension + tables
├── tests/
│   ├── test_chunker.py
│   ├── test_retriever.py
│   └── test_ingest.py
├── uploads/                 # Temp storage for incoming PDFs
├── .env                     # Secrets (never commit this)
├── requirements.txt
├── run.py                   # Entry point
└── README.md
```

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- PostgreSQL with the `pgvector` extension installed
- An OpenAI API key (for embeddings)
- An Anthropic API key (for Claude)

### 2. Clone & install

```bash
cd "d:\Haider ali\RAG_app"
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env` and fill in your real values:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_db
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
SECRET_KEY=some-random-string
```

### 4. Initialise the database

```bash
python scripts/init_db.py
```

This creates the `vector` extension and all tables.

### 5. Run

```bash
python run.py
```

App is available at `http://localhost:5000`.

---

## API Reference

### `POST /upload`

Upload a PDF for ingestion.

**Request:** `multipart/form-data` with field `file` (PDF only, max 16 MB).

**Response:**
```json
{
  "message": "Document ingested successfully",
  "document": {
    "id": 1,
    "filename": "my_doc.pdf",
    "uploaded_at": "2024-07-01T10:00:00",
    "chunk_count": 42
  }
}
```

---

### `POST /ask`

Ask a question against all ingested documents.

**Request:**
```json
{ "question": "What is the capital of France?" }
```

**Response:**
```json
{
  "answer": "According to the documents, ...",
  "sources": [
    { "id": 7, "document_id": 1, "chunk_index": 6, "content": "..." }
  ]
}
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Database Migrations

After changing models, generate and apply a migration:

```bash
flask db migrate -m "describe change"
flask db upgrade
```
