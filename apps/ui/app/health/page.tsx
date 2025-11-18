"use client";

import { useHealth, useMeta } from "@/lib/queries";
import { Card } from "@/components/ui/card";

export default function HealthPage() {
  const { data: health, refetch } = useHealth();
  const { data: meta } = useMeta();
  return (
    <div className="space-y-4">
      <Card className="space-y-2">
        <h1 className="text-xl font-semibold">Service Health</h1>
        <p className="text-sm text-slate-500">Status: {health?.status ?? "unknown"}</p>
        <button className="text-sm text-blue-600" onClick={() => refetch()}>
          Refresh
        </button>
      </Card>
      <Card>
        <h2 className="text-lg font-semibold">Dependencies</h2>
        <pre className="mt-2 text-xs text-slate-600">{JSON.stringify(meta?.dependencies ?? {}, null, 2)}</pre>
      </Card>
    </div>
  );
}
