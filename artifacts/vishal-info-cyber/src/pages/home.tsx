import { Link } from "wouter";
import { Search, Shield, Zap } from "lucide-react";
import { SiInstagram, SiTelegram } from "react-icons/si";

export function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center space-y-8 py-10">

      {/* Badge */}
      <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary/10 text-primary text-xs font-semibold rounded-full">
        <Shield className="h-3 w-3" />
        Cyber Intelligence Platform
      </div>

      {/* Title */}
      <div className="space-y-3">
        <h1 className="text-4xl sm:text-5xl font-bold text-foreground tracking-tight">
          VISHAL <span className="text-primary">CYBER</span> INFO
        </h1>
        <p className="text-muted-foreground text-base max-w-sm mx-auto leading-relaxed">
          Advanced OSINT lookup tools for phone numbers, social profiles, IP addresses, Indian documents, and more.
        </p>
      </div>

      {/* Feature pills */}
      <div className="flex flex-wrap justify-center gap-2">
        {["Phone Lookup", "Social OSINT", "IP Tracer", "Indian Docs", "Gaming", "Banking"].map(tag => (
          <span
            key={tag}
            className="px-3 py-1 bg-muted text-muted-foreground text-xs font-medium rounded-full border border-border"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* CTA buttons */}
      <div className="flex justify-center w-full max-w-xs mx-auto">
        <Link href="/lookup">
          <button
            className="inline-flex items-center gap-2 px-8 py-2.5 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/90 transition-colors justify-center"
            data-testid="button-start"
          >
            <Zap className="h-4 w-4" />
            Get Details
          </button>
        </Link>
      </div>

      {/* Divider */}
      <div className="flex items-center gap-3 w-full max-w-xs mx-auto">
        <div className="flex-1 h-px bg-border" />
        <span className="text-xs text-muted-foreground">Contact</span>
        <div className="flex-1 h-px bg-border" />
      </div>

      {/* Contact buttons */}
      <div className="flex flex-col sm:flex-row gap-3 w-full max-w-xs mx-auto">
        <a
          href="https://t.me/Its_MeVishalll"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#229ED9] text-white text-sm font-medium rounded-lg hover:bg-[#1a8bbf] transition-colors w-full justify-center"
          data-testid="button-telegram"
        >
          <SiTelegram className="h-4 w-4" />
          Telegram
        </a>
        <a
          href="https://www.instagram.com/user_ban0308_?igsh=MTd2cWJ6aHhycHV5dQ=="
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#833AB4] via-[#E1306C] to-[#F77737] text-white text-sm font-medium rounded-lg hover:opacity-90 transition-opacity w-full justify-center"
          data-testid="button-instagram"
        >
          <SiInstagram className="h-4 w-4" />
          Instagram
        </a>
      </div>

      {/* All Tools button */}
      <div className="w-full max-w-xs mx-auto">
        <Link href="/lookup">
          <button
            className="inline-flex items-center gap-2 px-5 py-2.5 border border-border text-foreground text-sm font-medium rounded-lg hover:bg-muted transition-colors w-full justify-center"
            data-testid="button-all-tools"
          >
            <Search className="h-4 w-4" />
            All Tools
          </button>
        </Link>
      </div>

    </div>
  );
}
