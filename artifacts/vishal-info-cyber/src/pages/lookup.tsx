import { useState, useEffect } from "react";
import { useRoute, useLocation, Link } from "wouter";
import { Search, AlertCircle, Loader2, ChevronRight, ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { TOOLS, CATEGORIES, getToolsByCategory, getToolById } from "@/lib/tools";
import { useLookup } from "@/hooks/use-lookup";
import { JsonViewer } from "@/components/json-viewer";
import { cn } from "@/lib/utils";

export function Lookup() {
  const [match, params] = useRoute("/lookup/:id");
  const [, setLocation] = useLocation();
  const toolId = params?.id || "";

  const [inputValue, setInputValue] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeTool = getToolById(toolId);
  const { data, isLoading, error, execute, reset } = useLookup(activeTool?.id || "");

  useEffect(() => {
    setInputValue("");
    reset();
  }, [toolId, reset]);

  useEffect(() => {
    if (!toolId && TOOLS.length > 0) {
      setLocation(`/lookup/${TOOLS[0].id}`);
    }
  }, [toolId, setLocation]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      execute(inputValue);
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-5">
      {/* Sidebar — desktop always visible, mobile collapsible */}
      <div className="md:w-56 flex-shrink-0">
        {/* Mobile toggle */}
        <button
          className="md:hidden w-full flex items-center justify-between px-4 py-3 bg-card border border-border rounded-xl text-sm font-medium text-foreground mb-3"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          data-testid="button-toggle-sidebar"
        >
          <span className="flex items-center gap-2">
            {activeTool && <activeTool.icon className="h-4 w-4 text-primary" />}
            {activeTool ? activeTool.name : "Select a Tool"}
          </span>
          <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform", sidebarOpen && "rotate-180")} />
        </button>

        {/* Sidebar content */}
        <div className={cn(
          "bg-card border border-border rounded-xl overflow-hidden",
          "md:block",
          sidebarOpen ? "block" : "hidden md:block"
        )}>
          {CATEGORIES.map(category => (
            <div key={category} className="border-b border-border last:border-b-0">
              <div className="px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
                {category}
              </div>
              <div className="pb-1">
                {getToolsByCategory(category).map(tool => {
                  const isActive = tool.id === toolId;
                  return (
                    <Link key={tool.id} href={`/lookup/${tool.id}`}>
                      <div
                        className={cn(
                          "flex items-center gap-2 mx-2 mb-0.5 px-2.5 py-2 rounded-lg text-sm font-medium cursor-pointer transition-colors",
                          isActive
                            ? "bg-primary/10 text-primary"
                            : "text-muted-foreground hover:bg-muted hover:text-foreground"
                        )}
                        onClick={() => setSidebarOpen(false)}
                        data-testid={`sidebar-tool-${tool.id}`}
                      >
                        <tool.icon className={cn("h-3.5 w-3.5 flex-shrink-0", isActive ? "text-primary" : "opacity-60")} />
                        <span className="truncate">{tool.name}</span>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main panel */}
      <div className="flex-1 min-w-0 space-y-4">
        <AnimatePresence mode="wait">
          {activeTool && (
            <motion.div
              key={activeTool.id}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.15 }}
              className="space-y-4"
            >
              {/* Tool header + input */}
              <div className="bg-card border border-border rounded-xl p-4 sm:p-5">
                {/* Breadcrumb */}
                <div className="flex items-center gap-1 text-xs text-muted-foreground mb-3">
                  <span>{activeTool.category}</span>
                  <ChevronRight className="h-3 w-3" />
                  <span className="text-foreground font-medium">{activeTool.name}</span>
                </div>

                {/* Title */}
                <div className="flex items-center gap-2.5 mb-1">
                  <div className="w-9 h-9 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <activeTool.icon className="h-4 w-4 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-foreground leading-tight">{activeTool.name}</h2>
                    <p className="text-xs text-muted-foreground">{activeTool.desc}</p>
                  </div>
                </div>

                {/* Input form */}
                <form onSubmit={handleSearch} className="flex gap-2 mt-4">
                  <input
                    type="text"
                    placeholder={activeTool.placeholder}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    className="flex-1 min-w-0 h-10 px-3 text-sm border border-border rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-all"
                    data-testid={`input-${activeTool.id}`}
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !inputValue.trim()}
                    className="h-10 px-4 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1.5 whitespace-nowrap"
                    data-testid={`button-search-${activeTool.id}`}
                  >
                    {isLoading
                      ? <Loader2 className="h-4 w-4 animate-spin" />
                      : <><Search className="h-3.5 w-3.5" />Search</>
                    }
                  </button>
                </form>
              </div>

              {/* Results */}
              <div className="bg-card border border-border rounded-xl overflow-hidden min-h-[200px]">
                {isLoading && (
                  <div className="flex flex-col items-center justify-center py-16 gap-3 text-muted-foreground">
                    <Loader2 className="h-7 w-7 animate-spin text-primary" />
                    <span className="text-sm">Fetching data...</span>
                  </div>
                )}

                {!isLoading && error && (
                  <div className="p-5">
                    <div className="flex items-start gap-3 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive">
                      <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                      <div>
                        <div className="text-sm font-semibold mb-0.5">Lookup Failed</div>
                        <div className="text-xs opacity-80">{error}</div>
                      </div>
                    </div>
                  </div>
                )}

                {!isLoading && !error && data && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.2 }}
                  >
                    <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-muted/40">
                      <span className="text-xs font-medium text-muted-foreground">Result</span>
                      <span className="text-xs text-emerald-600 font-medium bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                        Success
                      </span>
                    </div>
                    <div className="p-4">
                      <JsonViewer data={data} />
                    </div>
                  </motion.div>
                )}

                {!isLoading && !error && !data && (
                  <div className="flex flex-col items-center justify-center py-16 gap-2 text-muted-foreground">
                    <Search className="h-8 w-8 opacity-30" />
                    <span className="text-sm">Enter a value above and press Search</span>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
