"use client";

import { useEffect, useRef, useState } from "react";
import { useMetrics } from "@/lib/queries";
import { Card } from "@/components/ui/card";
import { KafkaVolumeChart } from "@/components/charts/kafka-volume-chart";
import { EventTable, KafkaDelta } from "@/components/kafka/event-table";

const POLL_MS = 5000;

export default function KafkaPage() {
  const { data: metrics } = useMetrics(POLL_MS);
  const [history, setHistory] = useState<KafkaDelta[]>([]);
  const prev = useRef({ count: 0, errors: 0 });

  useEffect(() => {
    if (!metrics?.classifier) return;
    const now = new Date();
    const delta = Math.max(0, metrics.classifier.count - prev.current.count);
    const errorDelta = Math.max(0, metrics.classifier.errors - prev.current.errors);
    prev.current = { count: metrics.classifier.count, errors: metrics.classifier.errors };
    setHistory((prevRows: KafkaDelta[]) => [
      ...prevRows,
      {
        timestamp: now.toLocaleTimeString(),
        delta,
        errorRate: delta === 0 ? 0 : errorDelta / delta,
      },
    ].slice(-30));
  }, [metrics]);

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <Card>
        <h2 className="text-lg font-semibold">Kafka Throughput</h2>
        <KafkaVolumeChart
          data={history.map((row: KafkaDelta) => ({
            timestamp: row.timestamp,
            eventsPerSecond: Number((row.delta / (POLL_MS / 1000)).toFixed(2)),
          }))}
        />
      </Card>
      <Card>
        <h2 className="text-lg font-semibold">Event Explorer</h2>
        <EventTable rows={history.slice().reverse()} />
      </Card>
    </div>
  );
}
