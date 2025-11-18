"use client";

import { useMeta } from "@/lib/queries";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export function Topbar() {
  const { data, isLoading } = useMeta();
  const env = data?.app.environment ?? "--";
  return (
    <header className="flex items-center justify-between border-b bg-card px-6 py-3">
      <div>
        <p className="text-xs uppercase text-muted-foreground">Environment</p>
        <p className="text-lg font-semibold text-foreground">{env}</p>
      </div>
      <div className="flex items-center gap-3">
        <StatusPill
          label="MLflow"
          status={data?.services?.find((s) => s.name === "mlflow") ? "ok" : "pending"}
        />
        <StatusPill
          label="Kafka"
          status={data?.services?.find((s) => s.name === "kafka" && s.bootstrap_servers) ? "ok" : "pending"}
        />
        <StatusPill
          label="Docs Indexed"
          status={data?.models?.rag_llm?.docs_indexed ? "ok" : "warning"}
        />
        {isLoading && <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />}
      </div>
    </header>
  );
}

function StatusPill({ label, status }: { label: string; status: "ok" | "warning" | "pending" }) {
  return (
    <span
      className={cn(
        "rounded-full px-3 py-1 text-xs font-medium",
        status === "ok" && "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
        status === "warning" && "bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300",
        status === "pending" && "bg-secondary text-secondary-foreground"
      )}
    >
      {label}
    </span>
  );
}
