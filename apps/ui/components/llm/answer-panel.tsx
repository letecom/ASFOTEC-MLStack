import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LlmResponse } from "@/lib/types";
import { formatNumber } from "@/lib/utils";

export function AnswerPanel({ response }: { response?: LlmResponse }) {
  if (!response) {
    return (
      <Card className="text-sm text-slate-500">Ask a question to see grounded answers.</Card>
    );
  }
  return (
    <Card className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <Badge label={response.llm_tier} />
        <Badge label={response.model_provider} />
        <Badge label={`${response.context_tokens_estimate} tokens`} />
      </div>
      <p className="whitespace-pre-line text-slate-900">{response.answer}</p>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-xs uppercase text-slate-500">Latency</p>
          <p className="font-semibold">{formatNumber(response.latency_ms)} ms</p>
        </div>
        <div>
          <p className="text-xs uppercase text-slate-500">Embedding Model</p>
          <p className="font-semibold">{response.embedding_model}</p>
        </div>
      </div>
    </Card>
  );
}
