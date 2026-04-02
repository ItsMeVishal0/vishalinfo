import { Link } from "wouter";
import { Terminal, ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center space-y-6">
      <div className="relative">
        <ShieldAlert className="h-24 w-24 text-destructive/80" />
        <div className="absolute inset-0 animate-ping opacity-20">
          <ShieldAlert className="h-24 w-24 text-destructive" />
        </div>
      </div>
      
      <div className="space-y-2">
        <h1 className="text-4xl font-mono font-bold tracking-widest text-foreground">
          ERROR_404
        </h1>
        <p className="text-muted-foreground font-mono">
          [SYSTEM WARNING]: Requested module or directory not found in database.
        </p>
      </div>

      <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-md font-mono text-sm max-w-md w-full">
        <div className="text-destructive flex items-center mb-2">
          <Terminal className="h-4 w-4 mr-2" />
          <span>FATAL_EXCEPTION</span>
        </div>
        <div className="text-muted-foreground text-left">
          The node you are trying to access does not exist or has been relocated.
          Please return to a secure zone.
        </div>
      </div>

      <Link href="/">
        <Button size="lg" className="font-mono mt-4">
          RETURN TO DASHBOARD
        </Button>
      </Link>
    </div>
  );
}
