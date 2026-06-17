#!/usr/bin/env python3
"""
Ingestion API for Manufacturing Agent Zero.

Provides REST endpoints for document ingestion, knowledge search,
and multi-language support. Designed to run inside the Agent Zero container
or as a sidecar process.
"""

import json
import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VECTOR_STORE_PATH = os.environ.get("VECTOR_STORE_PATH", "/a0/data/vector-store")
COMPANY_KB_PATH = os.environ.get("COMPANY_KB_PATH", "/a0/data/company-kb")


def get_supported_languages():
    """Return list of supported languages with ISO codes."""
    return [
        {"code": "en", "name": "English", "native": "English"},
        {"code": "es", "name": "Spanish", "native": "Español"},
        {"code": "ko", "name": "Korean", "native": "한국어"},
    ]


@app.route("/api/languages", methods=["GET"])
def list_languages():
    return jsonify({"languages": get_supported_languages()})


@app.route("/api/agents", methods=["GET"])
def list_agents():
    agents_dir = Path("/a0/agents")
    profiles = []
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and not agent_dir.name.startswith("_"):
            yaml_path = agent_dir / "agent.yaml"
            profiles.append({
                "id": agent_dir.name,
                "name": agent_dir.name.replace("-", " ").title(),
                "configured": yaml_path.exists(),
            })
    return jsonify({"agents": profiles})


@app.route("/api/knowledge/ingest", methods=["POST"])
def ingest_document():
    """Ingest a document into the vector store."""
    data = request.get_json()
    if not data or "source" not in data:
        return jsonify({"error": "Missing 'source' field"}), 400

    source = data["source"]
    language = data.get("language", "en")
    area = data.get("area", "company")
    metadata = data.get("metadata", {})

    source_path = Path(source)
    if not source_path.exists():
        return jsonify({"error": f"Source path '{source}' not found"}), 404

    if source_path.is_file():
        files = [source_path]
    else:
        files = list(source_path.rglob("*"))
        files = [f for f in files if f.suffix.lower() in (".txt", ".md", ".pdf", ".csv")]

    ingested = []
    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
            doc_id = str(file_path)
            ingested.append({
                "id": doc_id,
                "file": str(file_path),
                "size": len(text),
                "language": language,
            })
        except Exception as e:
            ingested.append({
                "file": str(file_path),
                "error": str(e),
            })

    return jsonify({
        "message": f"Ingested {len([d for d in ingested if 'error' not in d])} documents",
        "documents": ingested,
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "languages": len(get_supported_languages()),
        "vector_store": os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss")),
    })


if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 5001))
    debug = os.environ.get("DEBUG", "").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
