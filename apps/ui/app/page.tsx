"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useHealth, useMeta, useMetrics } from "@/lib/queries";
import { Card } from "@/components/ui/card";
import { formatNumber, latencyColor } from "@/lib/utils";
import { LatencyTrend } from "@/components/charts/latency-trend";
import { KafkaVolumeChart } from "@/components/charts/kafka-volume-chart";

const POLL_MS = 5000;

export default function OverviewPage() {
  const { data: health } = useHealth();
  const { data: meta } = useMeta();
  const { data: metrics } = useMetrics(POLL_MS);
  const [latencyHistory, setLatencyHistory] = useState<Array<{ timestamp: string; avg: number; p95: number }>>([]);
  const [kafkaHistory, setKafkaHistory] = useState<Array<{ timestamp: string; eventsPerSecond: number }>>([]);
  const prevCount = useRef(0);

  useEffect(() => {
    if (!metrics) return;
    const timestamp = new Date().toLocaleTimeString();
    const classifier = metrics["classifier"];
    if (classifier) {
      setLatencyHistory((prev) =>
        [...prev, { timestamp, avg: classifier.avg_latency_ms, p95: classifier.p95_latency_ms }].slice(-24)
      );
      const delta = Math.max(0, classifier.count - prevCount.current);
      prevCount.current = classifier.count;
      const eventsPerSecond = Number((delta / (POLL_MS / 1000)).toFixed(2));
      setKafkaHistory((prev) => [...prev, { timestamp, eventsPerSecond }].slice(-24));
    }
  }, [metrics]);

  const classifierCard = useMemo(() => metrics?.classifier, [metrics]);
  const llmCard = useMemo(() => metrics?.llm, [metrics]);

  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <p className="text-xs uppercase text-slate-500">API Health</p>
          <p className="text-2xl font-semibold text-slate-900">{health?.status ?? "--"}</p>
          <p className="text-sm text-slate-500">FastAPI gateway</p>
        </Card>
        <Card>
          <p className="text-xs uppercase text-slate-500">Classifier Avg Latency</p>
          <p className={`text-2xl font-semibold ${latencyColor(classifierCard?.avg_latency_ms)}`}>
            {formatNumber(classifierCard?.avg_latency_ms)} ms
          </p>
          <p className="text-sm text-slate-500">p95 {formatNumber(classifierCard?.p95_latency_ms)} ms</p>
        </Card>
        <Card>
          <p className="text-xs uppercase text-slate-500">LLM Avg Latency</p>
          <p className={`text-2xl font-semibold ${latencyColor(llmCard?.avg_latency_ms)}`}>
            {formatNumber(llmCard?.avg_latency_ms)} ms
          </p>
          <p className="text-sm text-slate-500">p95 {formatNumber(llmCard?.p95_latency_ms)} ms</p>
        </Card>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Latency Trend</h2>
              <p className="text-sm text-slate-500">Rolling history</p>
            </div>
          </div>
          <LatencyTrend data={latencyHistory} />
        </Card>
        <Card>
          <div className="mb-4">
            <h2 className="text-lg font-semibold">Kafka Volume</h2>
            <p className="text-sm text-slate-500">Derived from classifier count deltas</p>
          </div>
          <KafkaVolumeChart data={kafkaHistory} />
        </Card>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card>
          <h2 className="text-lg font-semibold">Model Snapshot</h2>
          <pre className="mt-2 text-xs text-slate-600">{JSON.stringify(meta?.models?.classifier ?? {}, null, 2)}</pre>
        </Card>
        <Card>
          <h2 className="text-lg font-semibold">RAG Snapshot</h2>
          <pre className="mt-2 text-xs text-slate-600">{JSON.stringify(meta?.models?.rag_llm ?? {}, null, 2)}</pre>
        </Card>
      </section>
    </div>
  );
}
