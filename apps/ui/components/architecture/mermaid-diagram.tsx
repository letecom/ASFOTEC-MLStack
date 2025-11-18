"use client";

import mermaid from "mermaid";
import { useEffect, useId, useState } from "react";

interface MermaidDiagramProps {
  diagram: string;
}

export function MermaidDiagram({ diagram }: MermaidDiagramProps) {
  const rawId = useId();
  const containerId = rawId.replace(/:/g, "");
  const [svg, setSvg] = useState<string>("");

  useEffect(() => {
    let mounted = true;
    mermaid.initialize({ startOnLoad: false, theme: "neutral" });
    mermaid
      .render(`mermaid-${containerId}`, diagram)
      .then(({ svg: rendered }) => {
        if (mounted) setSvg(rendered);
      })
      .catch((err) => setSvg(`<pre class='text-xs text-rose-600'>${err.message}</pre>`));
    return () => {
      mounted = false;
    };
  }, [diagram, containerId]);

  return <div className="mermaid" dangerouslySetInnerHTML={{ __html: svg }} />;
}
