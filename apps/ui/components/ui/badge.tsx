import { cn } from "@/lib/utils";

export function Badge({ label, tone = "neutral" }: { label: string; tone?: "neutral" | "success" | "warning" | "danger" }) {
  const map = {
    neutral: "bg-secondary text-secondary-foreground",
    success: "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
    warning: "bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300",
    danger: "bg-destructive text-destructive-foreground",
  } as const;
  return <span className={cn("rounded-full px-2 py-1 text-xs font-medium", map[tone])}>{label}</span>;
}
