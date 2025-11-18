"use client";

import { type ChangeEvent, type FormEvent, useMemo, useState } from "react";
import { FeatureSchema } from "@/lib/types";
import { SAMPLE_FEATURES } from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

interface FeatureFormProps {
  schema?: FeatureSchema;
  disabled?: boolean;
  onSubmit: (features: Record<string, unknown>) => void;
}

export function FeatureForm({ schema, disabled, onSubmit }: FeatureFormProps) {
  const [features, setFeatures] = useState<Record<string, string | number>>(() => SAMPLE_FEATURES);

  const numerical = schema?.numerical_features ?? Object.keys(SAMPLE_FEATURES).filter((key) => typeof SAMPLE_FEATURES[key] === "number");
  const categorical = schema?.categorical_features ?? Object.keys(SAMPLE_FEATURES).filter((key) => typeof SAMPLE_FEATURES[key] === "string");

  const handleChange = (key: string, value: string) => {
    setFeatures((prev: Record<string, string | number>) => ({
      ...prev,
      [key]: numerical.includes(key) ? Number(value) : value,
    }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(features);
  };

  const resetSample = () => setFeatures(SAMPLE_FEATURES);

  const orderedFields = useMemo(() => ({ numerical, categorical }), [numerical, categorical]);

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <section>
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-sm font-semibold uppercase text-slate-500">Numerical</h3>
          <Button type="button" variant="ghost" size="sm" onClick={resetSample}>
            Load Sample
          </Button>
        </div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {orderedFields.numerical.map((field) => (
            <div key={field} className="space-y-1">
              <Label htmlFor={field}>{field}</Label>
              <Input
                id={field}
                type="number"
                value={features[field] ?? ""}
                onChange={(event: ChangeEvent<HTMLInputElement>) => handleChange(field, event.target.value)}
                step="any"
                disabled={disabled}
              />
            </div>
          ))}
        </div>
      </section>
      <section>
        <h3 className="mb-2 text-sm font-semibold uppercase text-slate-500">Categorical</h3>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {orderedFields.categorical.map((field) => (
            <div key={field} className="space-y-1">
              <Label htmlFor={field}>{field}</Label>
              <Input
                id={field}
                value={features[field]?.toString() ?? ""}
                onChange={(event: ChangeEvent<HTMLInputElement>) => handleChange(field, event.target.value)}
                disabled={disabled}
              />
            </div>
          ))}
        </div>
      </section>
      <Button type="submit" disabled={disabled} className="w-full">
        {disabled ? "Scoring..." : "Run Inference"}
      </Button>
    </form>
  );
}
