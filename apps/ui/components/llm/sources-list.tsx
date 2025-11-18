import { Card } from "@/components/ui/card";

export function SourcesList({ sources }: { sources?: string[] }) {
  if (!sources?.length) return null;
  return (
    <Card className="space-y-2 text-sm">
      <p className="text-xs uppercase text-slate-500">Sources</p>
      <ul className="list-disc pl-5">
        {sources.map((source) => (
          <li key={source} className="break-all text-slate-800">
            {source}
          </li>
        ))}
      </ul>
    </Card>
  );
}
