from flask import Blueprint, request, jsonify, current_app
from app.services.embedder import embed_texts
from app.services.retriever import retrieve_chunks
from app.services.generator import generate_answer

query_bp = Blueprint("query", __name__)


@query_bp.route("/ask", methods=["POST"])
def ask():
    """
    POST /ask
    JSON body: { "question": "What is ...?" }
    Returns:   { "answer": "...", "sources": [...] }
    """
    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Request body must include a 'question' field"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"error": "'question' must not be empty"}), 400

    top_k = data.get("top_k", current_app.config["TOP_K"])

    try:
        # 1. Embed the question
        question_embedding = embed_texts([question])[0]

        # 2. Retrieve the most relevant chunks
        chunks = retrieve_chunks(question_embedding, top_k=top_k)

        # 3. Generate an answer with Claude
        answer = generate_answer(question, chunks)

    except Exception as exc:
        current_app.logger.error("Query failed: %s", exc)
        return jsonify({"error": str(exc)}), 500

    return jsonify(
        {
            "answer": answer,
            "sources": [c.to_dict() for c in chunks],
        }
    ), 200
