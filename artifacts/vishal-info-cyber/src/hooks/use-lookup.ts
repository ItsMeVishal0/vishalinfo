import { useState, useCallback } from "react";

interface UseLookupResult {
  data: any | null;
  isLoading: boolean;
  error: string | null;
  execute: (input: string) => Promise<void>;
  reset: () => void;
}

export function useLookup(toolId: string): UseLookupResult {
  const [data, setData] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (input: string) => {
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(`${import.meta.env.BASE_URL}api/lookup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool_id: toolId, input: input.trim() }),
      });

      const json = await response.json();

      if (!response.ok || json.error) {
        setError(json.error ?? `Error ${response.status}: ${response.statusText}`);
      } else {
        setData(json.result);
      }
    } catch (err: any) {
      setError("Network error — make sure the server is running.");
    } finally {
      setIsLoading(false);
    }
  }, [toolId]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return { data, isLoading, error, execute, reset };
}
