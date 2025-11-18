# ASFOTEC MLStack UI

Next.js 14 dashboard covering classifier, LLM/RAG, metrics, Kafka volume, and architecture surfaces for the ASFOTEC stack.

## Getting started

```bash
cd apps/ui
pnpm install # or npm install / yarn
pnpm dev
```

Set `NEXT_PUBLIC_API_URL` to your FastAPI base URL (defaults to `http://localhost:8000`).

## Fast static preview

To host the exported dashboard quickly (useful for sharing visualizations), run:

```bash
cd apps/ui
npm run preview
```

The script rebuilds the static bundle and serves `apps/ui/out` via `serve` on `http://localhost:4000`. Press `Ctrl+C` to stop the preview server.
