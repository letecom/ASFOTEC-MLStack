"use client";

import { useState } from "react";
import { PromptConsole } from "@/components/llm/prompt-console";
import { AnswerPanel } from "@/components/llm/answer-panel";
import { SourcesList } from "@/components/llm/sources-list";
import { useLlmMutation } from "@/lib/queries";
import { Card } from "@/components/ui/card";

export default function LlmPage() {
  const mutation = useLlmMutation();
  const [response, setResponse] = useState(mutation.data);

  const handleSubmit = async (prompt: string) => {
    const result = await mutation.mutateAsync(prompt);
    setResponse(result);
  };

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <PromptConsole onSubmit={handleSubmit} loading={mutation.isPending} />
      <div className="space-y-4">
        <AnswerPanel response={response} />
        <SourcesList sources={response?.sources} />
        <Card className="text-xs text-slate-500">
          Capture latency, provider tier, embedding model, and context token estimates straight from
          the `/predict/llm` endpoint.
        </Card>
      </div>
    </div>
  );
}
