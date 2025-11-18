"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface ModelMetricPoint {
  label: string;
  accuracy?: number;
  f1?: number;
}

export function ModelMetricsChart({ data }: { data: ModelMetricPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <XAxis dataKey="label" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 1]} tick={{ fontSize: 12 }} />
        <Tooltip />
        <Line type="monotone" dataKey="accuracy" stroke="#0f172a" strokeWidth={2} />
        <Line type="monotone" dataKey="f1" stroke="#22c55e" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
