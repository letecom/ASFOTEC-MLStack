import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, formatNumber, latencyColor } from "@/lib/utils";
import { ClassifierResponse } from "@/lib/types";

interface ResultPanelProps {
  result?: ClassifierResponse;
  show?: boolean;
}

export function ResultPanel({ result, show = true }: ResultPanelProps) {
  if (!result || !show) {
    return (
      <Card className="flex flex-col items-center justify-center text-center text-sm text-slate-500">
        Run the classifier to see predictions and metadata.
      </Card>
    );
  }

  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase text-slate-500">Latest prediction</p>
          <p className="text-3xl font-semibold">{result.prediction === 1 ? "Churn" : "Retain"}</p>
        </div>
        <Badge label={result.model_version} />
      </div>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-xs uppercase text-slate-500">Probability</p>
          <p className="text-lg font-semibold">{formatNumber(result.proba * 100, 1)}%</p>
        </div>
        <div>
          <p className="text-xs uppercase text-slate-500">Latency</p>
          <p className={cn("text-lg font-semibold", latencyColor(result.latency_ms))}>
            {formatNumber(result.latency_ms)} ms
          </p>
        </div>
        <div>
          <p className="text-xs uppercase text-slate-500">Artifact Source</p>
          <p className="font-medium">{result.artifact_source}</p>
        </div>
        <div>
          <p className="text-xs uppercase text-slate-500">Kafka Event</p>
          <p className="font-mono text-xs">{result.event_id ?? "Kafka disabled"}</p>
        </div>
      </div>
      <Button
        variant="outline"
        size="sm"
        onClick={() =>
          typeof navigator !== "undefined" && navigator.clipboard.writeText(JSON.stringify(result, null, 2))
        }
      >
        Copy JSON
      </Button>
    </Card>
  );
}
