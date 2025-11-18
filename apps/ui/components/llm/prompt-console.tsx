"use client";

import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

interface PromptConsoleProps {
  onSubmit: (query: string) => void;
  loading?: boolean;
}

export function PromptConsole({ onSubmit, loading }: PromptConsoleProps) {
  const [prompt, setPrompt] = useState("Explain the ASFOTEC MLOps lifecycle");

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!prompt.trim()) return;
    onSubmit(prompt.trim());
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <Textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} placeholder="Ask me anything about the stack..." />
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Querying..." : "Send"}
      </Button>
    </form>
  );
}
