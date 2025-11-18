import { Table } from "@/components/ui/table";

export interface KafkaDelta {
  timestamp: string;
  delta: number;
  errorRate: number;
}

export function EventTable({ rows }: { rows: KafkaDelta[] }) {
  return (
    <Table>
      <thead>
        <tr className="text-xs uppercase text-slate-500">
          <th className="p-2">Timestamp</th>
          <th className="p-2">Events / Interval</th>
          <th className="p-2">Error %</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.timestamp} className="border-t">
            <td className="p-2 text-sm">{row.timestamp}</td>
            <td className="p-2 text-sm">{row.delta}</td>
            <td className="p-2 text-sm">{(row.errorRate * 100).toFixed(2)}%</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
