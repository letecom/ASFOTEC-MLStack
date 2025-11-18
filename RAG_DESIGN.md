# RAG Design Document

## Goals

Provide deterministic, low-latency answers to ASFOTEC operational questions by grounding responses on internal Markdown documentation. The system favors transparency (surfacing source files) and supports optional escalation to a hosted LLM (Google Gemini) without changing the FastAPI contract.

## Components

| Component | File | Description |
| --------- | ---- | ----------- |
| Document loader | `rag/service.py` (`_load_path`, `_load_file`) | Recursively loads `.md/.markdown/.txt` files from `rag/docs`. Injects relative `source` metadata into every LangChain `Document`. |
| Text splitter | `RecursiveCharacterTextSplitter` | Splits documents into 800-character chunks with 100-character overlap to retain context across headings. |
| Embeddings | `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) | Provides sentence-level embeddings that balance accuracy vs. CPU load; runs locally without huggingface token. |
| Vector store | `langchain_chroma.Chroma` | Persists chunk embeddings to `chroma_db/`. The FastAPI container mounts this directory for fast retrieval. |
| Retrieval API | `RAGService.retrieve` | Converts the vector store into a retriever (`k = settings.rag_top_k`, default 4). |
| Answer scaffolding | `RAGService.answer` | Formats retrieved context and calls either a mock answer generator or an injected LLM function. |
| Orchestrator | `apps/api/services/llm_orchestrator.py` | Converts API requests into RAG queries, optionally calls Google Gemini via LangChain, and returns the HTTP response. |

## Data Flow

1. **Ingestion time**
   - Operator runs `poetry run python rag/ingest.py --docs-path rag/docs --vector-store chroma_db`.
   - CLI instantiates `RAGService`, loads `rag/docs/**`, splits into chunks, rebuilds `chroma_db/` (removing stale data first), and persists on disk.
   - The resulting directory is committed or baked into deployment artifacts.

2. **Query time**
   - `/predict/llm` receives `{ "query": "How do I retrain the classifier?" }`.
   - `LLMOrchestrator` measures latency and calls `RAGService.answer`.
   - `answer()` retrieves top-k chunks and formats context.
   - If `LLM_PROVIDER=sherlock`, a deterministic mock message is returned (ensures offline functionality). If `LLM_PROVIDER=google`, the orchestrator injects a LangChain Gemini client (model `gemini-1.5-flash`) to generate text from the RAG context.
   - Response merges the LLM result, chunk sources, tier name, and elapsed milliseconds.

## Configuration

All knobs live in `apps/api/config/settings.py`:

- `RAG_DOCS_PATH` – root directory for documentation (default `rag/docs`).
- `RAG_VECTORSTORE_PATH` – Chroma persistence directory (`chroma_db`).
- `RAG_TOP_K` – number of chunks returned per query (default `4`).
- `EMBEDDING_MODEL_NAME` – defaults to `all-MiniLM-L6-v2`, can be swapped for larger HF models if GPU/CPU budgets permit.
- `LLM_PROVIDER` – `sherlock` (mock) or `google`.
- `GOOGLE_API_KEY` – required only when using Gemini.

## Error Handling

- Missing vector store ⇒ `RuntimeError` instructing operators to run `rag/ingest.py`.
- Empty document set ⇒ `ValueError` with helpful message showing the searched paths.
- LLM provider failures ⇒ bubbled up through the FastAPI router as `HTTP 500` with the underlying exception message; metrics collector logs failed request for observability.

## Extensibility

- **Custom retrieval** – swap `Chroma` with another `VectorStore` implementation (e.g., `PGVector`) and update ingestion/retrieval sections accordingly.
- **LLM adapters** – `LLMOrchestrator` already abstracts provider selection; add additional branches to support Azure OpenAI, Anthropic, etc., reusing the same `RAGService` outputs.
- **Guardrails** – integrate toxicity filters or prompt templates before calling the LLM; the `llm_fn` hook inside `answer()` is the insertion point.

## Operational Considerations

- **Versioning** – treat `chroma_db/` as a build artifact. Tag the directory alongside model releases so `/predict/llm` responses line up with specific documentation revisions.
- **Latency** – With `all-MiniLM-L6-v2` embeddings and a few hundred chunks, end-to-end latency stays under 100 ms on commodity CPUs. Gemini calls add ~300 ms; expose this via the `latency_ms` field.
- **Observability** – The metrics collector records success/failure per query type. Combine with structured logs (`LLMOrchestrator`) to trace slow or failed RAG lookups.
