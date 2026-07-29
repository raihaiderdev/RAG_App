import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Document, Chunk
from app.services.extractor import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts

ingest_bp = Blueprint("ingest", __name__)


def allowed_file(filename: str) -> bool:
    allowed = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@ingest_bp.route("/upload", methods=["POST"])
def upload():
    """
    POST /upload
    Accepts a multipart/form-data request with a 'file' field (PDF).
    Extracts text, chunks it, embeds each chunk, and stores everything in the DB.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Save file to uploads/
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    safe_name = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, safe_name)
    file.save(file_path)

    doc = None  # ensure it's defined for the finally-scoped return
    try:
        # 1. Extract raw text from PDF
        raw_text = extract_text(file_path)

        # 2. Split into chunks
        chunk_size = current_app.config["CHUNK_SIZE"]
        chunk_overlap = current_app.config["CHUNK_OVERLAP"]
        chunks = chunk_text(raw_text, chunk_size=chunk_size, overlap=chunk_overlap)

        if not chunks:
            return jsonify({"error": "No text could be extracted from the PDF"}), 422

        # 3. Embed all chunks in one batch call
        embeddings = embed_texts(chunks)

        # 4. Persist document + chunks
        doc = Document(filename=safe_name, original_name=file.filename)
        db.session.add(doc)
        db.session.flush()  # get doc.id before inserting chunks

        # SQLAlchemy 2.x removed bulk_save_objects — use add_all instead
        chunk_objects = [
            Chunk(
                document_id=doc.id,
                chunk_index=i,
                content=text,
                embedding=embedding,
            )
            for i, (text, embedding) in enumerate(zip(chunks, embeddings))
        ]
        db.session.add_all(chunk_objects)
        db.session.commit()

    except Exception as exc:
        db.session.rollback()
        current_app.logger.error("Ingest failed: %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500
    finally:
        # Always clean up the temp file
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify({"message": "Document ingested successfully", "document": doc.to_dict()}), 201
