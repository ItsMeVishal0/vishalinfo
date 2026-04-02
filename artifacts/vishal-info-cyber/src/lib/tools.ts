import { 
  Phone, 
  PhoneCall, 
  MapPin, 
  Hash, 
  Mail, 
  Building, 
  ShieldAlert, 
  Gamepad2,
  FileText,
  Car,
  Map
} from "lucide-react";
import { SiInstagram, SiGithub } from "react-icons/si";

export type ToolCategory = "Phone Lookups" | "Social Media" | "Gaming" | "Financial" | "Tech / Network" | "Indian Documents";

export interface ToolDef {
  id: string;
  name: string;
  category: ToolCategory;
  desc: string;
  url: string;
  icon: any;
  placeholder: string;
}

export const TOOLS: ToolDef[] = [
  // Phone Lookups
  { id: "num",   name: "Number Name",    category: "Phone Lookups", desc: "Phone number se naam aur details",     url: "https://api.b77bf911.workers.dev/mobile?number={input}",        icon: Phone,      placeholder: "10-digit mobile number dalein..." },
  { id: "phone", name: "Phone Details",  category: "Phone Lookups", desc: "Full phone number details",            url: "https://abbas-apis.vercel.app/api/phone?number={input}",        icon: PhoneCall,  placeholder: "10-digit mobile number dalein..." },
  { id: "pak",   name: "Pakistan Number",category: "Phone Lookups", desc: "Pakistan number lookup",               url: "https://abbas-apis.vercel.app/api/pakistan?number={input}",     icon: Hash,       placeholder: "Pakistan number dalein..." },

  // Social Media
  { id: "instagram", name: "Instagram",  category: "Social Media",  desc: "Instagram profile OSINT",             url: "https://abbas-apis.vercel.app/api/instagram?username={input}",  icon: SiInstagram,placeholder: "Instagram username dalein..." },
  { id: "github",    name: "GitHub",     category: "Social Media",  desc: "GitHub user profile info",            url: "https://abbas-apis.vercel.app/api/github?username={input}",     icon: SiGithub,   placeholder: "GitHub username dalein..." },

  // Gaming
  { id: "ff",    name: "Free Fire Info", category: "Gaming",        desc: "Free Fire UID info",                  url: "https://abbas-apis.vercel.app/api/ff-info?uid={input}",         icon: Gamepad2,   placeholder: "Free Fire UID dalein..." },
  { id: "ffban", name: "FF Ban Check",   category: "Gaming",        desc: "Free Fire ban check",                 url: "https://abbas-apis.vercel.app/api/ff-ban?uid={input}",          icon: ShieldAlert,placeholder: "Free Fire UID dalein..." },

  // Financial
  { id: "ifsc",  name: "IFSC Code",      category: "Financial",     desc: "Bank branch IFSC details",            url: "https://abbas-apis.vercel.app/api/ifsc?ifsc={input}",           icon: Building,   placeholder: "IFSC code dalein (e.g. SBIN0001234)..." },

  // Tech / Network
  { id: "ip",    name: "IP Lookup",      category: "Tech / Network",desc: "IP address geolocation",              url: "https://abbas-apis.vercel.app/api/ip?ip={input}",               icon: MapPin,     placeholder: "IP address dalein..." },
  { id: "email", name: "Email Lookup",   category: "Tech / Network",desc: "Email address investigation",         url: "https://abbas-apis.vercel.app/api/email?mail={input}",          icon: Mail,       placeholder: "Email address dalein..." },

  // Indian Documents
  { id: "aadhaar", name: "Aadhaar",      category: "Indian Documents", desc: "Aadhaar card details",             url: "https://adhaar.khna04221.workers.dev/?aadhaar={input}",         icon: FileText,   placeholder: "12-digit Aadhaar number dalein..." },
  { id: "vehicle", name: "Vehicle RC",   category: "Indian Documents", desc: "Vehicle registration info",        url: "https://vehicle-info-api-abhi.vercel.app/?rc_number={input}",   icon: Car,        placeholder: "RC number dalein (e.g. MH01AB1234)..." },
  { id: "pincode", name: "Pincode",      category: "Indian Documents", desc: "Postal pincode area info",         url: "https://api.postalpincode.in/pincode/{input}",                  icon: Map,        placeholder: "6-digit pincode dalein..." },
];

export const CATEGORIES = Array.from(new Set(TOOLS.map(t => t.category)));

export const getToolById = (id: string) => TOOLS.find(t => t.id === id);
export const getToolsByCategory = (category: string) => TOOLS.filter(t => t.category === category);
