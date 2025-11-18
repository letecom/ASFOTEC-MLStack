"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "children"> {
  label?: React.ReactNode;
  children?: React.ReactNode;
}

export function Switch({ className, label, children, ...props }: SwitchProps) {
  return (
    <label className={cn("inline-flex cursor-pointer items-center", className)}>
      <input type="checkbox" className="peer sr-only" {...props} />
      <span className="h-5 w-9 rounded-full bg-input transition peer-checked:bg-primary" />
      <span className="ml-2 text-sm text-muted-foreground">{label ?? children}</span>
    </label>
  );
}
