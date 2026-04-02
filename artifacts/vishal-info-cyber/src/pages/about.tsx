import { Shield, User, Code, Database } from "lucide-react";

export function About() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 pb-10">
      <div className="text-center space-y-2 py-6">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-primary/10 rounded-2xl mb-2">
          <Shield className="h-7 w-7 text-primary" />
        </div>
        <h1 className="text-2xl font-bold text-foreground">About VISHAL CYBER INFO</h1>
        <p className="text-muted-foreground text-sm">Advanced Cyber Intelligence Platform</p>
      </div>

      <div className="bg-card border border-border rounded-xl p-5 space-y-3">
        <h2 className="font-semibold text-foreground flex items-center gap-2">
          <Shield className="h-4 w-4 text-primary" />
          About the Platform
        </h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          VISHAL CYBER INFO is an OSINT (Open Source Intelligence) aggregator designed for security researchers and investigators.
          It interfaces with multiple external APIs to retrieve public records — phone numbers, social profiles, vehicle registrations, financial codes, and more.
        </p>
        <ul className="space-y-1.5 text-sm text-muted-foreground">
          {[
            "No local logging — queries go directly to external APIs",
            "Server-side proxy — no CORS issues, fully private",
            "Raw JSON output for every lookup",
          ].map(item => (
            <li key={item} className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-card border border-border rounded-xl p-5 space-y-2">
        <h2 className="font-semibold text-foreground flex items-center gap-2">
          <User className="h-4 w-4 text-primary" />
          Developer
        </h2>
        <p className="text-sm text-muted-foreground">
          Built and maintained by <span className="font-semibold text-foreground">@VISHAL_INFO_CYBER</span>.
          For API issues, feature requests, or custom development, contact the developer via Telegram.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-card border border-border rounded-xl p-4 space-y-2">
          <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
            <Code className="h-4 w-4 text-primary" />
            Tech Stack
          </h3>
          <ul className="text-xs text-muted-foreground space-y-1">
            {["React + TypeScript", "Tailwind CSS", "Framer Motion", "Wouter", "Lucide Icons"].map(t => (
              <li key={t} className="flex items-center gap-1.5"><span className="text-primary">–</span>{t}</li>
            ))}
          </ul>
        </div>
        <div className="bg-card border border-border rounded-xl p-4 space-y-2">
          <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
            <Database className="h-4 w-4 text-primary" />
            API Sources
          </h3>
          <ul className="text-xs text-muted-foreground space-y-1">
            {["Cloudflare Workers", "Vercel Serverless", "PHP Endpoints", "Public DB APIs"].map(t => (
              <li key={t} className="flex items-center gap-1.5"><span className="text-primary">–</span>{t}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
