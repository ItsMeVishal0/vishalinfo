import { Router, type IRouter } from "express";

const router: IRouter = Router();

const TOOLS: Record<string, string> = {
  // Phone
  num:       "https://api.b77bf911.workers.dev/mobile?number={input}",
  phone:     "https://abbas-apis.vercel.app/api/phone?number={input}",
  pak:       "https://abbas-apis.vercel.app/api/pakistan?number={input}",
  // Social
  instagram: "https://abbas-apis.vercel.app/api/instagram?username={input}",
  github:    "https://abbas-apis.vercel.app/api/github?username={input}",
  // Gaming
  ff:        "https://abbas-apis.vercel.app/api/ff-info?uid={input}",
  ffban:     "https://abbas-apis.vercel.app/api/ff-ban?uid={input}",
  // Financial
  ifsc:      "https://abbas-apis.vercel.app/api/ifsc?ifsc={input}",
  // Tech / Network
  ip:        "https://abbas-apis.vercel.app/api/ip?ip={input}",
  email:     "https://abbas-apis.vercel.app/api/email?mail={input}",
  // Indian Documents
  aadhaar:   "https://adhaar.khna04221.workers.dev/?aadhaar={input}",
  vehicle:   "https://vehicle-info-api-abhi.vercel.app/?rc_number={input}",
  pincode:   "https://api.postalpincode.in/pincode/{input}",
};

router.post("/lookup", async (req, res) => {
  const { tool_id, input } = req.body as { tool_id: string; input: string };

  if (!tool_id || !TOOLS[tool_id]) {
    res.status(400).json({ error: `Unknown tool: ${tool_id}` });
    return;
  }

  if (!input || !input.trim()) {
    res.status(400).json({ error: "Input is required" });
    return;
  }

  const url = TOOLS[tool_id].replace("{input}", encodeURIComponent(input.trim()));

  try {
    const response = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0 (compatible; VISHAL-INFO-CYBER/1.0)",
        "Accept": "application/json, text/plain, */*",
      },
      signal: AbortSignal.timeout(12000),
    });

    const contentType = response.headers.get("content-type") ?? "";
    let result: unknown;

    if (contentType.includes("application/json")) {
      result = await response.json();
    } else {
      const text = await response.text();
      try {
        result = JSON.parse(text);
      } catch {
        result = text;
      }
    }

    if (!response.ok) {
      res.status(502).json({ error: `API returned ${response.status}: ${response.statusText}` });
      return;
    }

    res.json({ result });
  } catch (err: any) {
    if (err?.name === "TimeoutError" || err?.code === "UND_ERR_CONNECT_TIMEOUT") {
      res.status(504).json({ error: "Request timed out — the external API did not respond in time." });
    } else {
      res.status(502).json({ error: `Failed to reach external API: ${err?.message ?? "Unknown error"}` });
    }
  }
});

export default router;
