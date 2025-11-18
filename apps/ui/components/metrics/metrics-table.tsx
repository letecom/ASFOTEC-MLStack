import { MetricsOverview } from "@/lib/types";
import { formatNumber } from "@/lib/utils";
import { Table } from "@/components/ui/table";

export function MetricsTable({ data }: { data?: MetricsOverview }) {
  if (!data) return null;
  return (
    <Table>
      <thead>
        <tr className="text-xs uppercase text-slate-500">
          <th className="p-2 text-left">Endpoint</th>
          <th className="p-2 text-left">Count</th>
          <th className="p-2 text-left">Errors</th>
          <th className="p-2 text-left">Avg (ms)</th>
          <th className="p-2 text-left">P95 (ms)</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(data).map(([endpoint, metrics]) => (
          <tr key={endpoint} className="border-t text-sm">
            <td className="p-2 font-medium">{endpoint}</td>
            <td className="p-2">{metrics.count}</td>
            <td className="p-2">{metrics.errors}</td>
            <td className="p-2">{formatNumber(metrics.avg_latency_ms)}</td>
            <td className="p-2">{formatNumber(metrics.p95_latency_ms)}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
