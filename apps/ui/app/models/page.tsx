"use client";

import { useMemo } from "react";
import { useMeta } from "@/lib/queries";
import { Card } from "@/components/ui/card";
import { ModelMetricsChart } from "@/components/charts/model-metrics-chart";

export default function ModelsPage() {
  const { data } = useMeta();
  const metrics = (data?.models?.classifier?.latest_metrics as Record<string, number>) || {};
  const chartData = useMemo(
    () => [
      {
        label: "Test",
        accuracy: metrics.test_accuracy,
        f1: metrics.test_f1,
      },
    ],
    [metrics]
  );

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <Card>
        <h2 className="text-lg font-semibold">Classifier Metrics</h2>
        <ModelMetricsChart data={chartData} />
        <pre className="text-xs text-slate-600">{JSON.stringify(metrics, null, 2)}</pre>
      </Card>
      <Card>
        <h2 className="text-lg font-semibold">RAG Model</h2>
        <pre className="text-xs text-slate-600">{JSON.stringify(data?.models?.rag_llm ?? {}, null, 2)}</pre>
      </Card>
    </div>
  );
}
