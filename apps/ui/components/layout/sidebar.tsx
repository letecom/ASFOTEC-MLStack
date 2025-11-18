"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Gauge, Layers, MessageSquare, Network, Radio, Shield, Workflow } from "lucide-react";

const LINKS = [
  { href: "/", label: "Overview", icon: Gauge },
  { href: "/classifier", label: "Classifier", icon: Layers },
  { href: "/llm", label: "LLM + RAG", icon: MessageSquare },
  { href: "/architecture", label: "Architecture", icon: Network },
  { href: "/models", label: "Models", icon: Workflow },
  { href: "/kafka", label: "Kafka", icon: Radio },
  { href: "/metrics", label: "Metrics", icon: Shield },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="hidden w-64 flex-col border-r bg-card p-4 md:flex">
      <div className="mb-6 text-lg font-semibold text-foreground">ASFOTEC MLStack</div>
      <nav className="space-y-1">
        {LINKS.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
