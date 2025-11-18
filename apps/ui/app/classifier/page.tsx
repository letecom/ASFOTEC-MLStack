"use client";

import { useState } from "react";
import { FeatureForm } from "@/components/classifier/feature-form";
import { ResultPanel } from "@/components/classifier/result-panel";
import { useClassifierMutation, useMeta } from "@/lib/queries";
import { Card } from "@/components/ui/card";
import { Table } from "@/components/ui/table";
import { Button } from "@/components/ui/button";

interface HistoryRow {
  timestamp: string;
  payload: Record<string, unknown>;
}

export default function ClassifierPage() {
  const { data: meta } = useMeta();
  const mutation = useClassifierMutation();
  const [result, setResult] = useState(mutation.data);
  const [history, setHistory] = useState<HistoryRow[]>([]);

  const handleSubmit = async (features: Record<string, unknown>) => {
    const response = await mutation.mutateAsync({ ...features });
    setResult(response);
    setHistory((prev) => [
      { timestamp: new Date().toISOString(), payload: { features, response } },
      ...prev,
    ].slice(0, 10));
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <section className="lg:col-span-2 space-y-4">
        <Card className="shadow-none">
          <h1 className="text-xl font-semibold">Classifier Playground</h1>
          <p className="text-sm text-slate-500">Model: {meta?.models?.classifier?.framework}</p>
        </Card>
        <FeatureForm schema={meta?.feature_schema} disabled={mutation.isPending} onSubmit={handleSubmit} />
      </section>
      <section className="space-y-4">
        <ResultPanel result={result} />
        <Card className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">History</h3>
            <Button variant="ghost" size="sm" onClick={() => setHistory([])}>
              Clear
            </Button>
          </div>
          <Table>
            <thead>
              <tr className="text-xs uppercase text-slate-500">
                <th className="p-2 text-left">Timestamp</th>
                <th className="p-2 text-left">Prediction</th>
                <th className="p-2 text-left">Event</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row) => (
                <tr key={row.timestamp} className="border-t text-xs">
                  <td className="p-2">{new Date(row.timestamp).toLocaleString()}</td>
                  <td className="p-2">
                    {(row.payload.response as any)?.prediction === 1 ? "Churn" : "Retain"}
                    <span className="ml-2 text-xs text-slate-400">
                      ({((row.payload.response as any)?.proba * 100).toFixed(1)}%)
                    </span>
                  </td>
                  <td className="p-2 font-mono">{(row.payload.response as any)?.event_id ?? "--"}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card>
      </section>
    </div>
  );
}
