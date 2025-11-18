"""RAG service responsible for ingestion, retrieval, and answer scaffolding."""

from __future__ import annotations

import logging
import shutil
import time
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps.api.config.settings import AppSettings, get_settings

logger = logging.getLogger(__name__)

SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt"}


class RAGService:
    """Encapsulates vector store ingestion/retrieval and lightweight answering."""

    def __init__(self, settings: Optional[AppSettings] = None):
        self.settings = settings or get_settings()
        self.docs_path = Path(self.settings.rag_docs_path)
        self.vectorstore_path = Path(self.settings.rag_vectorstore_path)
        self.embedding_model_name = self.settings.embedding_model_name
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        self._vectorstore: Optional[Chroma] = None

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------
    def ingest_documents(self, doc_paths: Sequence[Path]) -> int:
        """Ingest markdown/text documents, rebuild vector store, and persist it."""

        documents: List[Document] = []
        for path in doc_paths:
            documents.extend(self._load_path(path))

        if not documents:
            raise ValueError(
                f'No documents found under {[str(p) for p in doc_paths]}. '
                'Ensure markdown/txt files exist before ingestion.'
            )

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        if not chunks:
            raise ValueError('Document splitting yielded 0 chunks; check the source files.')

        if self.vectorstore_path.exists():
            shutil.rmtree(self.vectorstore_path)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(self.vectorstore_path),
        )
        if hasattr(vectorstore, 'persist'):
            vectorstore.persist()
        self._vectorstore = vectorstore
        logger.info('Persisted %s chunks to vector store %s', len(chunks), self.vectorstore_path)
        return len(chunks)

    def _load_path(self, path: Path) -> List[Document]:
        if path.is_dir():
            docs: List[Document] = []
            for file_path in path.rglob('*'):
                if file_path.suffix.lower() in SUPPORTED_SUFFIXES:
                    docs.extend(self._load_file(file_path))
            return docs
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            return self._load_file(path)
        logger.debug('Skipping unsupported path: %s', path)
        return []

    def _load_file(self, file_path: Path) -> List[Document]:
        loader = TextLoader(str(file_path), encoding='utf-8')
        docs = loader.load()
        for doc in docs:
            doc.metadata.setdefault('source', str(file_path.relative_to(self.docs_path)))
        return docs

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------
    def _ensure_vectorstore(self) -> Chroma:
        if self._vectorstore:
            return self._vectorstore
        if not self.vectorstore_path.exists():
            raise RuntimeError(
                f'No vector store found at {self.vectorstore_path}. '
                'Run `poetry run python rag/ingest.py` first.'
            )
        self._vectorstore = Chroma(
            persist_directory=str(self.vectorstore_path),
            embedding_function=self.embeddings,
        )
        return self._vectorstore

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """Retrieve relevant chunks for a query."""

        retriever = self._ensure_vectorstore().as_retriever(
            search_kwargs={'k': top_k or self.settings.rag_top_k}
        )
        return retriever.invoke(query)

    # ------------------------------------------------------------------
    # Answer scaffolding
    # ------------------------------------------------------------------
    def answer(
        self,
        query: str,
        *,
        llm_fn: Optional[Callable[[str, str], str]] = None,
        tier: str = 'mock-local',
        top_k: Optional[int] = None,
    ) -> dict:
        start = time.time()
        docs = self.retrieve(query, top_k=top_k)
        context = self._format_context(docs)
        context_tokens = self._estimate_tokens(context)

        if llm_fn:
            answer_text = llm_fn(context, query)
        else:
            answer_text = self._default_answer(context, query)

        latency_ms = (time.time() - start) * 1000
        sources = [doc.metadata.get('source', 'unknown') for doc in docs]

        return {
            'answer': answer_text,
            'sources': sources,
            'llm_tier': tier,
            'latency_ms': round(latency_ms, 2),
            'context_tokens_estimate': context_tokens,
            'embedding_model': self.embedding_model_name,
        }

    @staticmethod
    def _format_context(documents: Iterable[Document]) -> str:
        return '\n\n'.join(doc.page_content for doc in documents)

    @staticmethod
    def _default_answer(context: str, query: str) -> str:
        if not context:
            return 'No knowledge base context is available yet. Please ingest documents first.'
        return (
            'Based on the ASFOTEC knowledge base, here is a concise answer to your query:\n'
            f'Question: {query}\n'
            f'Key Points: {context[:800]}'
        )

    @staticmethod
    def _estimate_tokens(context: str) -> int:
        if not context:
            return 0
        # Rough heuristic: 4 characters per token for english technical text
        return max(1, len(context) // 4)
