import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { cn } from "@/lib/utils";

interface JsonViewerProps {
  data: any;
  className?: string;
}

export function JsonViewer({ data, className }: JsonViewerProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderValue = (value: any, depth = 0): React.ReactNode => {
    if (value === null) return <span className="text-muted-foreground italic text-xs">null</span>;
    if (typeof value === "boolean") return <span className="text-amber-500 font-medium">{value.toString()}</span>;
    if (typeof value === "number") return <span className="text-violet-400">{value}</span>;
    if (typeof value === "string") return <span className="text-emerald-500">"{value}"</span>;

    if (Array.isArray(value)) {
      if (value.length === 0) return <span className="text-muted-foreground">[ ]</span>;
      return (
        <div className={cn("ml-4 pl-3 border-l-2 border-border mt-0.5 space-y-0.5", depth > 2 && "text-xs")}>
          {value.map((item, index) => (
            <div key={index} className="flex gap-1">
              <span className="text-muted-foreground text-xs select-none">{index}</span>
              <span className="text-muted-foreground">:</span>
              <div>{renderValue(item, depth + 1)}</div>
            </div>
          ))}
        </div>
      );
    }

    if (typeof value === "object") {
      if (Object.keys(value).length === 0) return <span className="text-muted-foreground">{"{ }"}</span>;
      return (
        <div className={cn("ml-4 pl-3 border-l-2 border-border mt-0.5 space-y-0.5", depth > 2 && "text-xs")}>
          {Object.entries(value).map(([k, v]) => (
            <div key={k} className="flex flex-wrap gap-x-1">
              <span className="text-primary font-medium">{k}</span>
              <span className="text-muted-foreground">:</span>
              <div>{renderValue(v, depth + 1)}</div>
            </div>
          ))}
        </div>
      );
    }

    return <span className="text-foreground">{String(value)}</span>;
  };

  const isObject = typeof data === "object" && data !== null;

  return (
    <div className={cn("relative rounded-lg border border-border overflow-hidden bg-muted/30 text-sm", className)}>
      {/* Copy button */}
      <button
        onClick={copyToClipboard}
        className="absolute top-2 right-2 flex items-center gap-1 text-xs px-2 py-1 bg-card border border-border rounded-md text-muted-foreground hover:text-foreground hover:shadow-sm transition-all z-10"
        data-testid="button-copy-json"
      >
        {copied ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
        {copied ? "Copied" : "Copy"}
      </button>

      <div className="p-4 overflow-x-auto font-mono text-[13px] leading-relaxed">
        {isObject ? (
          <div>
            {Object.entries(data).map(([k, v]) => (
              <div key={k} className="py-0.5 flex flex-wrap gap-x-1">
                <span className="text-primary font-semibold">{k}</span>
                <span className="text-muted-foreground">:</span>
                <div className="min-w-0">{renderValue(v, 1)}</div>
              </div>
            ))}
          </div>
        ) : (
          <pre className="text-emerald-500 whitespace-pre-wrap break-words">{String(data)}</pre>
        )}
      </div>
    </div>
  );
}
