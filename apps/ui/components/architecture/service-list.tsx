import { Card } from "@/components/ui/card";
import { ServiceSummary } from "@/lib/types";

export function ServiceList({ services }: { services?: ServiceSummary[] }) {
  if (!services?.length) return null;
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {services.map((service) => (
        <Card key={service.name} className="space-y-1 text-sm">
          <p className="text-xs uppercase text-slate-500">{service.name}</p>
          <p className="font-semibold text-slate-900">
            {service.tech ?? service.purpose ?? "Service"}
          </p>
          <pre className="text-xs text-slate-500">
            {JSON.stringify(service, null, 2)}
          </pre>
        </Card>
      ))}
    </div>
  );
}
