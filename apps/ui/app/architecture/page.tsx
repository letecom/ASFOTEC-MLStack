"use client";

import { useMemo } from "react";
import { useMeta } from "@/lib/queries";
import { Card } from "@/components/ui/card";
import { MermaidDiagram } from "@/components/architecture/mermaid-diagram";
import { ServiceList } from "@/components/architecture/service-list";

export default function ArchitecturePage() {
  const { data } = useMeta();
  const diagram = useMemo(
    () => `flowchart LR
    Client[Next.js UI]
    API[FastAPI]
    Model[MLflow Production]
    Kafka[Kafka Topic]
    Postgres[(Postgres Metrics)]
    RAG[Chroma RAG Store]
    Client --> API
    API --> Model
    API --> Kafka
    Kafka --> Postgres
    API --> RAG`,
    []
  );

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-xl font-semibold">Runtime Architecture</h1>
        <MermaidDiagram diagram={diagram} />
      </Card>
      <ServiceList services={data?.services} />
      <Card>
        <h2 className="text-lg font-semibold">Raw payload</h2>
        <pre className="mt-2 text-xs text-slate-600">{JSON.stringify(data, null, 2)}</pre>
      </Card>
    </div>
  );
}
