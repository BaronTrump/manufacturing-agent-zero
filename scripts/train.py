#!/usr/bin/env python3
"""
Training script for Manufacturing Agent Zero.

Ingests company documents (PDF, text, markdown) into the FAISS vector database
for RAG-based question answering.

Usage:
    python scripts/train.py --source /path/to/docs --language en
    python scripts/train.py --source /path/to/manuals --language ko --chunk-size 256
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
except ImportError:
    print("Installing required packages...")
    os.system("pip install sentence-transformers faiss-cpu numpy 2>/dev/null")
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np


def chunk_text(text, chunk_size=512, overlap=64):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_documents(source_path):
    """Load documents from source directory."""
    docs = []
    path = Path(source_path)
    for file_path in path.rglob("*"):
        if file_path.suffix.lower() in (".txt", ".md", ".pdf", ".csv"):
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
                doc_id = hashlib.md5(str(file_path).encode()).hexdigest()
                docs.append({
                    "id": doc_id,
                    "source": str(file_path.relative_to(path)),
                    "text": text,
                    "path": str(file_path),
                })
                print(f"  Loaded: {file_path.name} ({len(text)} chars)")
            except Exception as e:
                print(f"  Skipped {file_path.name}: {e}")
    return docs


def train(args):
    """Main training pipeline."""
    source = args.source
    language = args.language
    chunk_size = args.chunk_size
    output_dir = args.output or os.environ.get("VECTOR_STORE_PATH", "/a0/data/vector-store")

    print(f"Manufacturing Agent Zero — Training Pipeline")
    print(f"  Source:     {source}")
    print(f"  Language:   {language}")
    print(f"  Chunk size: {chunk_size}")
    print(f"  Output:     {output_dir}")
    print()

    if not os.path.exists(source):
        print(f"Error: Source path '{source}' does not exist.")
        sys.exit(1)

    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"Loading documents from {source}...")
    documents = load_documents(source)
    print(f"  Total documents: {len(documents)}")

    if not documents:
        print("No documents found to train.")
        return

    print("Chunking documents...")
    all_chunks = []
    all_metadata = []
    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                "source": doc["source"],
                "doc_id": doc["id"],
                "chunk_index": i,
                "language": language,
                "area": "company",
            })
    print(f"  Total chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embedding_dim = embeddings.shape[1]

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(embedding_dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    os.makedirs(output_dir, exist_ok=True)

    faiss.write_index(index, os.path.join(output_dir, "index.faiss"))
    with open(os.path.join(output_dir, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(
            [{"text": c, "metadata": m} for c, m in zip(all_chunks, all_metadata)],
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\nDone! Index saved to {output_dir}")
    print(f"  Embedding dimension: {embedding_dim}")
    print(f"  Total vectors: {index.ntotal}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Manufacturing Agent Zero on company data")
    parser.add_argument("--source", required=True, help="Path to company documents directory")
    parser.add_argument("--language", default="en", choices=["en", "es", "ko"], help="Document language")
    parser.add_argument("--chunk-size", type=int, default=512, help="Chunk size in words")
    parser.add_argument("--output", default=None, help="Vector store output path")
    args = parser.parse_args()
    train(args)
