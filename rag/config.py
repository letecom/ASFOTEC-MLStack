"""Configuration helpers for the RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from apps.api.config.settings import AppSettings, get_settings


@dataclass(frozen=True)
class RAGSettings:
    """Subset of settings needed for RAG ingestion/retrieval."""

    docs_path: Path
    vectorstore_path: Path
    embedding_model_name: str
    top_k: int

    @classmethod
    def from_app(cls, settings: AppSettings) -> "RAGSettings":
        return cls(
            docs_path=settings.rag_docs_path,
            vectorstore_path=settings.rag_vectorstore_path,
            embedding_model_name=settings.embedding_model_name,
            top_k=settings.rag_top_k,
        )


def get_rag_settings() -> RAGSettings:
    """Convenience accessor mirroring `apps.api.config.settings.get_settings`."""

    return RAGSettings.from_app(get_settings())
