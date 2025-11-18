"use client";

import { useState } from "react";
import { useMetrics } from "@/lib/queries";
import { MetricsTable } from "@/components/metrics/metrics-table";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";

const INTERVAL_ON = 5000;

export default function MetricsPage() {
  const [autoRefresh, setAutoRefresh] = useState(true);
  const { data } = useMetrics(autoRefresh ? INTERVAL_ON : undefined);
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Metrics Overview</h1>
        <Switch checked={autoRefresh} onChange={(event) => setAutoRefresh(event.currentTarget.checked)}>
          Auto-refresh
        </Switch>
      </div>
      <Card>
        <MetricsTable data={data} />
      </Card>
    </div>
  );
}
