#!/usr/bin/env python
"""Ingest markdown/txt docs into the persistent vector store."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.config import get_rag_settings
from rag.service import RAGService


def main() -> None:
    settings = get_rag_settings()
    service = RAGService()

    docs_path = settings.docs_path
    if not docs_path.exists():
        raise SystemExit(f'RAG docs directory {docs_path} does not exist.')

    doc_paths = [docs_path]
    chunks = service.ingest_documents(doc_paths)
    print(f'✅ Indexed {chunks} chunks into {settings.vectorstore_path}')


if __name__ == '__main__':
    main()
