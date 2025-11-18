"""RAG-aware LLM orchestrator used by the FastAPI layer."""

from __future__ import annotations

from typing import Callable, Dict, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage

from apps.api.config.settings import AppSettings, get_settings
from rag.service import RAGService


class LLMOrchestrator:
    """Provide an interface to answer queries via RAG + LLM (or mock)."""

    def __init__(self, settings: Optional[AppSettings] = None):
        self.settings = settings or get_settings()
        self.rag_service = RAGService(self.settings)
        self.llm_provider = self.settings.llm_provider
        self.api_key = self.settings.google_api_key
        self._model = None
        self._llm_fn = self._build_llm_fn()

    def _build_llm_fn(self) -> Optional[Callable[[str, str], str]]:
        if self.llm_provider == 'sherlock':
            return None  # default mock answer handled by RAG service
        if self.llm_provider == 'google':
            if not self.api_key:
                raise ValueError('GOOGLE_API_KEY required for google provider')
            self._model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=self.api_key)

            def _call(context: str, question: str) -> str:
                prompt = (
                    'Answer the user question using only the provided ASFOTEC context.\n'
                    f'Context:\n{context}\nQuestion: {question}'
                )
                response = self._model.invoke(prompt)
                if isinstance(response, AIMessage):
                    if isinstance(response.content, str):
                        return response.content
                    return ' '.join(
                        getattr(part, 'text', '') for part in response.content if getattr(part, 'text', '')
                    ).strip()
                if isinstance(response, dict):
                    return response.get('text') or response.get('content', '')
                return str(response)

            return _call
        raise ValueError(f'Unsupported llm_provider: {self.llm_provider}')

    def query(self, query: str) -> Dict[str, object]:
        tier = 'mock-local' if self.llm_provider == 'sherlock' else 'google-flash'
        payload = self.rag_service.answer(
            query,
            llm_fn=self._llm_fn,
            tier=tier,
            top_k=self.settings.rag_top_k,
        )
        payload['model_provider'] = self.llm_provider
        return payload
