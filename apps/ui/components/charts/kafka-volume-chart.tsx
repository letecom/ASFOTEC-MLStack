"use client";

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface KafkaPoint {
  timestamp: string;
  eventsPerSecond: number;
}

export function KafkaVolumeChart({ data }: { data: KafkaPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data} margin={{ top: 20, right: 20, left: 0, bottom: 0 }}>
        <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Area type="monotone" dataKey="eventsPerSecond" stroke="#0284c7" fill="#bae6fd" />
      </AreaChart>
    </ResponsiveContainer>
  );
}
