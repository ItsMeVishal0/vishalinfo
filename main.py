#!/usr/bin/env python3
# ============================================================
#   VISHAL INFO CYBER - Single File Python Web App
#   Developer: @VISHAL_INFO_CYBER
#   Run: pip install flask requests && python main.py
# ============================================================

from flask import Flask, request, jsonify, render_template_string
import requests as req
import json

app = Flask(__name__)

# ===================== TOOL DEFINITIONS =====================
TOOLS = [
    # Phone Lookups
    {"id": "num",       "name": "Number Name",    "category": "Phone Lookups",    "desc": "Lookup phone number for name info",    "url": "https://abbas-apis.vercel.app/api/num-name?number={input}",               "placeholder": "Enter phone number"},
    {"id": "phone",     "name": "Phone Details",  "category": "Phone Lookups",    "desc": "Full phone number details",            "url": "https://abbas-apis.vercel.app/api/phone?number={input}",                  "placeholder": "Enter phone number"},
    {"id": "pak",       "name": "Pakistan Number","category": "Phone Lookups",    "desc": "Pakistan-specific number lookup",      "url": "https://abbas-apis.vercel.app/api/pakistan?number={input}",               "placeholder": "Enter PK number"},
    {"id": "global",    "name": "Global Number",  "category": "Phone Lookups",    "desc": "Global number lookup",                 "url": "https://erox.shop/numapi.php?mobile={input}&key=KRISH",                   "placeholder": "Enter global number"},
    # Social Media
    {"id": "instagram", "name": "Instagram",      "category": "Social Media",     "desc": "Instagram profile lookup",             "url": "https://abbas-apis.vercel.app/api/instagram?username={input}",            "placeholder": "Enter Instagram username"},
    {"id": "github",    "name": "GitHub",         "category": "Social Media",     "desc": "GitHub profile info",                  "url": "https://abbas-apis.vercel.app/api/github?username={input}",               "placeholder": "Enter GitHub username"},
    {"id": "telegram",  "name": "Telegram",       "category": "Social Media",     "desc": "Telegram user info",                   "url": "https://api.b77bf911.workers.dev/telegram?user={input}",                  "placeholder": "Enter Telegram ID/username"},
    # Gaming
    {"id": "ff",        "name": "Free Fire Info", "category": "Gaming",           "desc": "Free Fire UID lookup",                 "url": "https://abbas-apis.vercel.app/api/ff-info?uid={input}",                   "placeholder": "Enter FF UID"},
    {"id": "ffban",     "name": "FF Ban Check",   "category": "Gaming",           "desc": "Check if FF account is banned",        "url": "https://abbas-apis.vercel.app/api/ff-ban?uid={input}",                    "placeholder": "Enter FF UID"},
    # Financial
    {"id": "pan",       "name": "PAN Card",       "category": "Financial",        "desc": "Indian PAN card lookup",               "url": "https://pan.amorinthz.workers.dev/?key=AMORINTH&pan={input}",            "placeholder": "Enter PAN number"},
    {"id": "ifsc",      "name": "IFSC Code",      "category": "Financial",        "desc": "Bank IFSC details",                    "url": "https://abbas-apis.vercel.app/api/ifsc?ifsc={input}",                     "placeholder": "Enter IFSC code"},
    {"id": "fampay",    "name": "UPI / FamPay",   "category": "Financial",        "desc": "UPI ID lookup",                        "url": "https://api.b77bf911.workers.dev/upi2?id={input}",                       "placeholder": "Enter UPI ID"},
    # Tech / Network
    {"id": "ip",        "name": "IP Lookup",      "category": "Tech / Network",   "desc": "IP address geolocation and info",      "url": "https://abbas-apis.vercel.app/api/ip?ip={input}",                        "placeholder": "Enter IP address"},
    {"id": "email",     "name": "Email Lookup",   "category": "Tech / Network",   "desc": "Email investigation",                  "url": "https://abbas-apis.vercel.app/api/email?mail={input}",                   "placeholder": "Enter email address"},
    # Indian Documents
    {"id": "aadhaar",   "name": "Aadhaar",        "category": "Indian Documents", "desc": "Aadhaar number lookup",                "url": "https://adhaar.khna04221.workers.dev/?aadhaar={input}",                  "placeholder": "Enter Aadhaar number"},
    {"id": "vehicle",   "name": "Vehicle RC",     "category": "Indian Documents", "desc": "Vehicle registration lookup",          "url": "https://vehicle-info-api-abhi.vercel.app/?rc_number={input}",            "placeholder": "Enter Vehicle RC number"},
    {"id": "pincode",   "name": "Pincode",        "category": "Indian Documents", "desc": "Postal pincode info",                  "url": "https://api.postalpincode.in/pincode/{input}",                           "placeholder": "Enter Pincode"},
]

CATEGORIES = list(dict.fromkeys(t["category"] for t in TOOLS))

def get_tool(tool_id):
    return next((t for t in TOOLS if t["id"] == tool_id), None)


# ===================== CATEGORY ICONS (SVG) =====================
CATEGORY_ICONS = {
    "Phone Lookups":    '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z"/>',
    "Social Media":     '<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z"/>',
    "Gaming":           '<path stroke-linecap="round" stroke-linejoin="round" d="M14.25 6.087c0-.355.186-.676.401-.959.221-.29.349-.634.349-1.003 0-1.036-1.007-1.875-2.25-1.875s-2.25.84-2.25 1.875c0 .369.128.713.349 1.003.215.283.401.604.401.959v0a.64.64 0 0 1-.657.643 48.39 48.39 0 0 1-4.163-.3c.186 1.613.293 3.25.315 4.907a.656.656 0 0 1-.658.663v0c-.355 0-.676-.186-.959-.401a1.647 1.647 0 0 0-1.003-.349c-1.036 0-1.875 1.007-1.875 2.25s.84 2.25 1.875 2.25c.369 0 .713-.128 1.003-.349.283-.215.604-.401.959-.401v0c.31 0 .555.26.532.57a48.039 48.039 0 0 1-.642 5.056c1.518.19 3.058.309 4.616.354a.64.64 0 0 0 .657-.643v0c0-.355-.186-.676-.401-.959a1.647 1.647 0 0 1-.349-1.003c0-1.035 1.008-1.875 2.25-1.875 1.243 0 2.25.84 2.25 1.875 0 .369-.128.713-.349 1.003-.215.283-.4.604-.4.959v0c0 .333.277.599.61.58a48.1 48.1 0 0 0 5.427-.63 48.05 48.05 0 0 0 .582-4.717.532.532 0 0 0-.533-.57v0c-.355 0-.676.186-.959.401-.29.221-.634.349-1.003.349-1.035 0-1.875-1.007-1.875-2.25s.84-2.25 1.875-2.25c.37 0 .713.128 1.003.349.283.215.604.401.959.401v0a.656.656 0 0 0 .658-.663 48.422 48.422 0 0 0-.37-5.36c-1.886.342-3.81.574-5.766.689a.578.578 0 0 1-.61-.58v0Z"/>',
    "Financial":        '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z"/>',
    "Tech / Network":   '<path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418"/>',
    "Indian Documents": '<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"/>',
}


# ===================== HTML TEMPLATE =====================
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>VISHAL INFO CYBER</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --primary: #2563eb;
    --primary-light: #eff6ff;
    --primary-dark: #1d4ed8;
    --bg: #f8fafc;
    --white: #ffffff;
    --border: #e2e8f0;
    --text: #0f172a;
    --muted: #64748b;
    --success: #16a34a;
    --danger: #dc2626;
    --danger-bg: #fef2f2;
    --radius: 12px;
    --shadow: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
  }
  body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; font-size: 14px; }

  /* HEADER */
  header { position: sticky; top: 0; z-index: 100; background: var(--white); border-bottom: 1px solid var(--border); box-shadow: var(--shadow); }
  .header-inner { max-width: 1100px; margin: 0 auto; padding: 0 16px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
  .logo { display: flex; align-items: center; gap: 10px; text-decoration: none; cursor: pointer; }
  .logo-icon { width: 32px; height: 32px; background: var(--primary); border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .logo-icon svg { width: 16px; height: 16px; color: white; stroke: white; }
  .logo-text { font-weight: 700; font-size: 15px; color: var(--text); }
  .logo-text span { color: var(--primary); }
  nav.desktop { display: flex; gap: 4px; }
  nav.desktop a { display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 500; color: var(--muted); text-decoration: none; transition: all .15s; cursor: pointer; }
  nav.desktop a:hover { background: var(--bg); color: var(--text); }
  nav.desktop a.active { background: var(--primary-light); color: var(--primary); }
  nav.desktop a svg { width: 14px; height: 14px; stroke: currentColor; }
  #hamburger { display: none; background: none; border: none; cursor: pointer; padding: 8px; border-radius: 8px; color: var(--muted); }
  #hamburger:hover { background: var(--bg); }
  #hamburger svg { width: 20px; height: 20px; stroke: currentColor; }
  #mobile-nav { display: none; border-top: 1px solid var(--border); background: var(--white); padding: 8px 16px; }
  #mobile-nav a { display: flex; align-items: center; gap: 8px; padding: 10px 12px; border-radius: 8px; font-size: 14px; font-weight: 500; color: var(--muted); text-decoration: none; cursor: pointer; transition: all .15s; }
  #mobile-nav a:hover { background: var(--bg); color: var(--text); }
  #mobile-nav a.active { background: var(--primary-light); color: var(--primary); }
  #mobile-nav a svg { width: 16px; height: 16px; stroke: currentColor; }

  /* LAYOUT */
  main { max-width: 1100px; margin: 0 auto; padding: 24px 16px 40px; }
  .page { display: none; }
  .page.active { display: block; }

  /* HOME PAGE */
  .hero { text-align: center; padding: 48px 16px 32px; }
  .hero-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; background: var(--primary-light); color: var(--primary); font-size: 12px; font-weight: 600; border-radius: 999px; margin-bottom: 16px; }
  .hero-badge svg { width: 12px; height: 12px; stroke: currentColor; }
  .hero h1 { font-size: clamp(26px, 6vw, 42px); font-weight: 800; letter-spacing: -.02em; line-height: 1.15; margin-bottom: 12px; }
  .hero h1 span { color: var(--primary); }
  .hero p { color: var(--muted); max-width: 480px; margin: 0 auto 24px; font-size: 15px; line-height: 1.6; }
  .hero-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
  .btn-primary { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: var(--primary); color: white; font-size: 14px; font-weight: 600; border-radius: var(--radius); text-decoration: none; border: none; cursor: pointer; transition: background .15s; }
  .btn-primary:hover { background: var(--primary-dark); }
  .btn-primary svg { width: 16px; height: 16px; stroke: currentColor; }
  .btn-outline { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: var(--white); color: var(--text); font-size: 14px; font-weight: 600; border-radius: var(--radius); border: 1px solid var(--border); text-decoration: none; cursor: pointer; transition: background .15s; }
  .btn-outline:hover { background: var(--bg); }

  .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 40px; }
  .feature-card { display: flex; align-items: flex-start; gap: 12px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; }
  .feature-icon { width: 36px; height: 36px; background: var(--primary-light); border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .feature-icon svg { width: 16px; height: 16px; stroke: var(--primary); }
  .feature-title { font-weight: 600; font-size: 13px; margin-bottom: 3px; }
  .feature-desc { font-size: 12px; color: var(--muted); line-height: 1.5; }

  .tools-section h2 { font-size: 17px; font-weight: 700; margin-bottom: 20px; }
  .category-group { margin-bottom: 28px; }
  .category-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-bottom: 12px; }
  .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 10px; }
  .tool-card { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); cursor: pointer; transition: all .15s; text-decoration: none; color: inherit; }
  .tool-card:hover { border-color: rgba(37,99,235,.35); box-shadow: 0 2px 8px rgba(37,99,235,.08); }
  .tool-card-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
  .tool-card-icon { width: 32px; height: 32px; background: var(--bg); border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: background .15s; }
  .tool-card:hover .tool-card-icon { background: var(--primary-light); }
  .tool-card-icon svg { width: 15px; height: 15px; stroke: var(--muted); transition: stroke .15s; }
  .tool-card:hover .tool-card-icon svg { stroke: var(--primary); }
  .tool-card-name { font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .tool-card-desc { font-size: 11px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .tool-card-arrow { color: var(--border); flex-shrink: 0; transition: all .15s; }
  .tool-card:hover .tool-card-arrow { color: var(--primary); transform: translateX(2px); }
  .tool-card-arrow svg { width: 14px; height: 14px; stroke: currentColor; }

  /* LOOKUP PAGE */
  .lookup-layout { display: flex; gap: 20px; align-items: flex-start; }
  .sidebar { width: 220px; flex-shrink: 0; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; position: sticky; top: 76px; max-height: calc(100vh - 100px); overflow-y: auto; }
  .sidebar-cat { border-bottom: 1px solid var(--border); }
  .sidebar-cat:last-child { border-bottom: none; }
  .sidebar-cat-label { padding: 10px 14px 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
  .sidebar-item { display: flex; align-items: center; gap: 8px; margin: 2px 6px; padding: 7px 10px; border-radius: 8px; font-size: 12.5px; font-weight: 500; color: var(--muted); cursor: pointer; transition: all .15s; }
  .sidebar-item:hover { background: var(--bg); color: var(--text); }
  .sidebar-item.active { background: var(--primary-light); color: var(--primary); }
  .sidebar-item svg { width: 13px; height: 13px; stroke: currentColor; flex-shrink: 0; }
  .lookup-main { flex: 1; min-width: 0; }

  /* Mobile tool selector */
  .mobile-tool-selector { display: none; margin-bottom: 14px; }
  .mobile-tool-selector select { width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: var(--radius); background: var(--white); font-size: 14px; font-weight: 500; color: var(--text); appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 36px; }
  .mobile-tool-selector select:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,.1); }

  /* Tool panel */
  .tool-panel { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin-bottom: 16px; }
  .tool-breadcrumb { font-size: 11px; color: var(--muted); margin-bottom: 12px; display: flex; align-items: center; gap: 4px; }
  .tool-breadcrumb svg { width: 10px; height: 10px; stroke: currentColor; }
  .tool-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
  .tool-header-icon { width: 40px; height: 40px; background: var(--primary-light); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .tool-header-icon svg { width: 18px; height: 18px; stroke: var(--primary); }
  .tool-title { font-size: 18px; font-weight: 700; }
  .tool-desc { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .search-form { display: flex; gap: 8px; }
  .search-input { flex: 1; min-width: 0; height: 40px; padding: 0 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px; transition: all .15s; background: var(--bg); }
  .search-input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: var(--white); }
  .search-btn { height: 40px; padding: 0 18px; background: var(--primary); color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: background .15s; white-space: nowrap; flex-shrink: 0; }
  .search-btn:hover:not(:disabled) { background: var(--primary-dark); }
  .search-btn:disabled { opacity: .5; cursor: not-allowed; }
  .search-btn svg { width: 14px; height: 14px; stroke: currentColor; }

  /* Result area */
  .result-box { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; min-height: 180px; }
  .result-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; color: var(--muted); gap: 10px; text-align: center; }
  .result-empty svg { width: 36px; height: 36px; stroke: currentColor; opacity: .4; }
  .result-empty span { font-size: 13px; }
  .result-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; gap: 12px; }
  .spinner { width: 28px; height: 28px; border: 3px solid var(--border); border-top-color: var(--primary); border-radius: 50%; animation: spin .7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .loading-text { font-size: 13px; color: var(--muted); }
  .result-error { padding: 20px; }
  .error-box { display: flex; align-items: flex-start; gap: 10px; padding: 14px 16px; background: var(--danger-bg); border: 1px solid #fecaca; border-radius: 8px; }
  .error-box svg { width: 16px; height: 16px; stroke: var(--danger); flex-shrink: 0; margin-top: 1px; }
  .error-title { font-size: 13px; font-weight: 600; color: var(--danger); margin-bottom: 3px; }
  .error-msg { font-size: 12px; color: #b91c1c; }
  .result-success { }
  .result-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; border-bottom: 1px solid var(--border); background: #f8fafc; }
  .result-label { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
  .success-badge { font-size: 11px; font-weight: 600; color: var(--success); background: #f0fdf4; border: 1px solid #bbf7d0; padding: 2px 10px; border-radius: 999px; }
  .result-body { padding: 16px; overflow-x: auto; }

  /* JSON Viewer */
  .json-viewer { font-family: 'Menlo', 'Monaco', 'Courier New', monospace; font-size: 12.5px; line-height: 1.7; }
  .json-key { color: var(--primary); font-weight: 600; }
  .json-str { color: #15803d; }
  .json-num { color: #7c3aed; }
  .json-bool { color: #d97706; font-weight: 600; }
  .json-null { color: var(--muted); font-style: italic; }
  .json-brace { color: var(--muted); }
  .json-row { display: flex; flex-wrap: wrap; gap: 4px; align-items: baseline; margin: 1px 0; }
  .json-nested { margin-left: 20px; padding-left: 12px; border-left: 2px solid var(--border); }
  .copy-btn { display: flex; align-items: center; gap: 5px; padding: 4px 10px; background: var(--white); border: 1px solid var(--border); border-radius: 6px; font-size: 11px; font-weight: 500; color: var(--muted); cursor: pointer; transition: all .15s; }
  .copy-btn:hover { background: var(--bg); color: var(--text); }
  .copy-btn svg { width: 12px; height: 12px; stroke: currentColor; }
  .copy-btn.copied { color: var(--success); border-color: #bbf7d0; background: #f0fdf4; }

  /* ABOUT PAGE */
  .about-page { max-width: 680px; margin: 0 auto; }
  .about-hero { text-align: center; padding: 40px 16px 24px; }
  .about-icon { width: 56px; height: 56px; background: var(--primary-light); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; }
  .about-icon svg { width: 28px; height: 28px; stroke: var(--primary); }
  .about-hero h1 { font-size: 22px; font-weight: 800; margin-bottom: 6px; }
  .about-hero p { color: var(--muted); font-size: 14px; }
  .about-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin-bottom: 14px; }
  .about-card-title { font-size: 14px; font-weight: 700; display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
  .about-card-title svg { width: 16px; height: 16px; stroke: var(--primary); }
  .about-card p { font-size: 13px; color: var(--muted); line-height: 1.7; }
  .about-list { list-style: none; margin-top: 10px; }
  .about-list li { display: flex; align-items: flex-start; gap: 8px; font-size: 13px; color: var(--muted); padding: 3px 0; }
  .about-list li::before { content: '•'; color: var(--primary); font-weight: 700; flex-shrink: 0; }
  .about-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }

  /* FOOTER */
  footer { border-top: 1px solid var(--border); background: var(--white); padding: 16px; text-align: center; font-size: 12px; color: var(--muted); margin-top: auto; }

  /* RESPONSIVE */
  @media (max-width: 700px) {
    nav.desktop { display: none; }
    #hamburger { display: flex; align-items: center; justify-content: center; }
    .lookup-layout { flex-direction: column; }
    .sidebar { display: none; }
    .mobile-tool-selector { display: block; }
    .hero { padding: 32px 8px 20px; }
    .search-btn span { display: none; }
  }
  @media (min-width: 701px) {
    #mobile-nav { display: none !important; }
  }
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-inner">
    <div class="logo" onclick="showPage('home')">
      <div class="logo-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"/></svg>
      </div>
      <span class="logo-text">VISHAL <span>INFO</span> CYBER</span>
    </div>
    <nav class="desktop">
      <a id="nav-home" class="active" onclick="showPage('home')">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/></svg>
        Home
      </a>
      <a id="nav-lookup" onclick="showPage('lookup')">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
        Tools
      </a>
      <a id="nav-about" onclick="showPage('about')">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"/></svg>
        About
      </a>
    </nav>
    <button id="hamburger" onclick="toggleMobileNav()">
      <svg id="hamburger-open" viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      <svg id="hamburger-close" style="display:none" viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/></svg>
    </button>
  </div>
  <div id="mobile-nav">
    <a id="mnav-home" class="active" onclick="showPage('home');toggleMobileNav()">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/></svg>
      Home
    </a>
    <a id="mnav-lookup" onclick="showPage('lookup');toggleMobileNav()">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
      Tools
    </a>
    <a id="mnav-about" onclick="showPage('about');toggleMobileNav()">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"/></svg>
      About
    </a>
  </div>
</header>

<!-- MAIN -->
<main>

  <!-- ==================== HOME PAGE ==================== -->
  <div id="page-home" class="page active">
    <div class="hero">
      <div class="hero-badge">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"/></svg>
        Cyber Intelligence Platform
      </div>
      <h1>VISHAL <span>INFO</span> CYBER</h1>
      <p>Advanced OSINT lookup tools for phone numbers, social profiles, IP addresses, Indian documents, and more.</p>
      <div class="hero-btns">
        <button class="btn-primary" onclick="showPage('lookup')">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
          Start Lookup
        </button>
        <button class="btn-outline" onclick="showPage('about')">Learn More</button>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"/></svg></div>
        <div><div class="feature-title">Direct & Private</div><div class="feature-desc">Queries go straight to the source — no middlemen or logging.</div></div>
      </div>
      <div class="feature-card">
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg></div>
        <div><div class="feature-title">15+ Tools</div><div class="feature-desc">Phone, social, banking, documents, gaming lookups and more.</div></div>
      </div>
      <div class="feature-card">
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg></div>
        <div><div class="feature-title">Instant Results</div><div class="feature-desc">Fast responses with clean formatted JSON output.</div></div>
      </div>
    </div>

    <div class="tools-section">
      <h2>All Lookup Tools</h2>
      {% for category in categories %}
      <div class="category-group">
        <div class="category-label">{{ category }}</div>
        <div class="tools-grid">
          {% for tool in tools_by_cat[category] %}
          <div class="tool-card" onclick="openTool('{{ tool.id }}')">
            <div class="tool-card-left">
              <div class="tool-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5">{{ cat_icons[category]|safe }}</svg>
              </div>
              <div>
                <div class="tool-card-name">{{ tool.name }}</div>
                <div class="tool-card-desc">{{ tool.desc }}</div>
              </div>
            </div>
            <div class="tool-card-arrow"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/></svg></div>
          </div>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- ==================== LOOKUP PAGE ==================== -->
  <div id="page-lookup" class="page">
    <div class="lookup-layout">
      <!-- Desktop Sidebar -->
      <div class="sidebar" id="desktop-sidebar">
        {% for category in categories %}
        <div class="sidebar-cat">
          <div class="sidebar-cat-label">{{ category }}</div>
          {% for tool in tools_by_cat[category] %}
          <div class="sidebar-item" id="sitem-{{ tool.id }}" onclick="selectTool('{{ tool.id }}')">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5">{{ cat_icons[category]|safe }}</svg>
            {{ tool.name }}
          </div>
          {% endfor %}
        </div>
        {% endfor %}
      </div>

      <!-- Main content -->
      <div class="lookup-main">
        <!-- Mobile dropdown -->
        <div class="mobile-tool-selector">
          <select id="mobile-tool-select" onchange="selectTool(this.value)">
            {% for category in categories %}
            <optgroup label="{{ category }}">
              {% for tool in tools_by_cat[category] %}
              <option value="{{ tool.id }}">{{ tool.name }}</option>
              {% endfor %}
            </optgroup>
            {% endfor %}
          </select>
        </div>

        <!-- Tool panel -->
        <div id="tool-panel" class="tool-panel">
          <div class="tool-breadcrumb" id="tool-breadcrumb">
            <span id="bc-cat"></span>
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5"/></svg>
            <strong id="bc-name"></strong>
          </div>
          <div class="tool-header">
            <div class="tool-header-icon" id="tool-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" id="tool-icon-svg"></svg>
            </div>
            <div>
              <div class="tool-title" id="tool-title"></div>
              <div class="tool-desc" id="tool-desc"></div>
            </div>
          </div>
          <form class="search-form" onsubmit="doLookup(event)">
            <input class="search-input" id="search-input" type="text" placeholder="Enter value..." autocomplete="off"/>
            <button class="search-btn" type="submit" id="search-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
              <span>Search</span>
            </button>
          </form>
        </div>

        <!-- Result box -->
        <div class="result-box" id="result-box">
          <div class="result-empty" id="result-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
            <span>Enter a value above and press Search</span>
          </div>
          <div class="result-loading" id="result-loading" style="display:none">
            <div class="spinner"></div>
            <div class="loading-text">Fetching data...</div>
          </div>
          <div class="result-error" id="result-error" style="display:none">
            <div class="error-box">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"/></svg>
              <div>
                <div class="error-title">Lookup Failed</div>
                <div class="error-msg" id="error-msg"></div>
              </div>
            </div>
          </div>
          <div class="result-success" id="result-success" style="display:none">
            <div class="result-header">
              <span class="result-label">Result</span>
              <div style="display:flex;gap:8px;align-items:center">
                <button class="copy-btn" id="copy-btn" onclick="copyResult()">
                  <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"/></svg>
                  Copy
                </button>
                <span class="success-badge">Success</span>
              </div>
            </div>
            <div class="result-body">
              <div class="json-viewer" id="json-output"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== ABOUT PAGE ==================== -->
  <div id="page-about" class="page">
    <div class="about-page">
      <div class="about-hero">
        <div class="about-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"/></svg>
        </div>
        <h1>About VISHAL INFO CYBER</h1>
        <p>Advanced Cyber Intelligence Platform</p>
      </div>

      <div class="about-card">
        <div class="about-card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"/></svg>
          About the Platform
        </div>
        <p>VISHAL INFO CYBER is an OSINT (Open Source Intelligence) aggregator designed for security researchers and investigators. It interfaces with multiple external APIs to retrieve public records across phone numbers, social profiles, vehicle registrations, financial codes, and more.</p>
        <ul class="about-list">
          <li>No local logging — queries go directly to external APIs</li>
          <li>Server-side proxy to avoid CORS issues</li>
          <li>Clean, formatted JSON output for every lookup</li>
          <li>17+ lookup tools across 6 categories</li>
        </ul>
      </div>

      <div class="about-card">
        <div class="about-card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/></svg>
          Developer
        </div>
        <p>Built and maintained by <strong>@VISHAL_INFO_CYBER</strong>. For API issues, feature requests, or custom development, contact the developer via Telegram.</p>
      </div>

      <div class="about-grid">
        <div class="about-card">
          <div class="about-card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5"/></svg>
            Tech Stack
          </div>
          <ul class="about-list">
            <li>Python + Flask</li><li>Vanilla JavaScript</li><li>Tailwind-inspired CSS</li><li>Single-file architecture</li>
          </ul>
        </div>
        <div class="about-card">
          <div class="about-card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125"/></svg>
            API Sources
          </div>
          <ul class="about-list">
            <li>Cloudflare Workers</li><li>Vercel Serverless</li><li>PHP Endpoints</li><li>Public DB APIs</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

</main>

<footer>VISHAL INFO CYBER &mdash; Developed by @VISHAL_INFO_CYBER</footer>

<script>
// ==================== DATA ====================
const TOOLS = {{ tools_json|safe }};
const TOOL_MAP = {};
TOOLS.forEach(t => TOOL_MAP[t.id] = t);

let currentToolId = TOOLS[0].id;
let lastResultData = null;

// ==================== NAVIGATION ====================
function showPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-' + name).classList.add('active');
  ['home','lookup','about'].forEach(n => {
    const active = (n === name);
    const d = document.getElementById('nav-' + n);
    const m = document.getElementById('mnav-' + n);
    if (d) d.classList.toggle('active', active);
    if (m) m.classList.toggle('active', active);
  });
  if (name === 'lookup' && currentToolId) {
    selectTool(currentToolId);
  }
  window.scrollTo(0, 0);
}

function toggleMobileNav() {
  const nav = document.getElementById('mobile-nav');
  const open = document.getElementById('hamburger-open');
  const close = document.getElementById('hamburger-close');
  const visible = nav.style.display === 'block';
  nav.style.display = visible ? 'none' : 'block';
  open.style.display = visible ? '' : 'none';
  close.style.display = visible ? 'none' : '';
}

function openTool(toolId) {
  showPage('lookup');
  selectTool(toolId);
}

// ==================== TOOL SELECTION ====================
function selectTool(toolId) {
  currentToolId = toolId;
  const tool = TOOL_MAP[toolId];
  if (!tool) return;

  // Update sidebar
  document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
  const sitem = document.getElementById('sitem-' + toolId);
  if (sitem) sitem.classList.add('active');

  // Update mobile select
  const sel = document.getElementById('mobile-tool-select');
  if (sel) sel.value = toolId;

  // Update panel
  document.getElementById('bc-cat').textContent = tool.category;
  document.getElementById('bc-name').textContent = tool.name;
  document.getElementById('tool-title').textContent = tool.name;
  document.getElementById('tool-desc').textContent = tool.desc;
  document.getElementById('search-input').placeholder = tool.placeholder || 'Enter value...';
  document.getElementById('search-input').value = '';

  // Reset results
  showResult('empty');
  lastResultData = null;
}

// ==================== LOOKUP ====================
async function doLookup(e) {
  e.preventDefault();
  const input = document.getElementById('search-input').value.trim();
  if (!input) return;

  showResult('loading');
  const btn = document.getElementById('search-btn');
  btn.disabled = true;

  try {
    const resp = await fetch('/api/lookup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tool_id: currentToolId, input: input })
    });
    const data = await resp.json();
    if (!resp.ok || data.error) {
      showResult('error', data.error || 'Unknown error occurred');
    } else {
      lastResultData = data.result;
      showResult('success', null, data.result);
    }
  } catch (err) {
    showResult('error', 'Network error: ' + err.message);
  } finally {
    btn.disabled = false;
  }
}

function showResult(state, errorMsg, data) {
  document.getElementById('result-empty').style.display = state === 'empty' ? '' : 'none';
  document.getElementById('result-loading').style.display = state === 'loading' ? '' : 'none';
  document.getElementById('result-error').style.display = state === 'error' ? '' : 'none';
  document.getElementById('result-success').style.display = state === 'success' ? '' : 'none';
  if (state === 'error') {
    document.getElementById('error-msg').textContent = errorMsg || '';
  }
  if (state === 'success' && data !== undefined) {
    document.getElementById('json-output').innerHTML = renderJson(data);
  }
}

// ==================== JSON RENDERER ====================
function renderJson(value, depth) {
  depth = depth || 0;
  if (value === null) return '<span class="json-null">null</span>';
  if (typeof value === 'boolean') return '<span class="json-bool">' + value + '</span>';
  if (typeof value === 'number') return '<span class="json-num">' + value + '</span>';
  if (typeof value === 'string') return '<span class="json-str">&quot;' + escHtml(value) + '&quot;</span>';
  if (Array.isArray(value)) {
    if (!value.length) return '<span class="json-brace">[ ]</span>';
    let html = '<div class="json-nested">';
    value.forEach((item, i) => {
      html += '<div class="json-row"><span class="json-num">' + i + '</span><span class="json-brace">:</span>' + renderJson(item, depth+1) + '</div>';
    });
    return html + '</div>';
  }
  if (typeof value === 'object') {
    const keys = Object.keys(value);
    if (!keys.length) return '<span class="json-brace">{ }</span>';
    let html = '<div class="json-nested">';
    keys.forEach(k => {
      html += '<div class="json-row"><span class="json-key">' + escHtml(k) + '</span><span class="json-brace">:</span>' + renderJson(value[k], depth+1) + '</div>';
    });
    return html + '</div>';
  }
  return '<span>' + escHtml(String(value)) + '</span>';
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ==================== COPY ====================
function copyResult() {
  if (!lastResultData) return;
  const text = typeof lastResultData === 'string' ? lastResultData : JSON.stringify(lastResultData, null, 2);
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('copy-btn');
    btn.classList.add('copied');
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5"/></svg> Copied';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"/></svg> Copy';
    }, 2000);
  });
}

// Init
selectTool(TOOLS[0].id);
</script>
</body>
</html>"""


# ===================== FLASK ROUTES =====================

@app.route("/")
def index():
    tools_by_cat = {}
    for cat in CATEGORIES:
        tools_by_cat[cat] = [t for t in TOOLS if t["category"] == cat]
    return render_template_string(
        HTML,
        tools=TOOLS,
        categories=CATEGORIES,
        tools_by_cat=tools_by_cat,
        tools_json=json.dumps(TOOLS),
        cat_icons=CATEGORY_ICONS,
    )


@app.route("/api/lookup", methods=["POST"])
def lookup():
    data = request.get_json(force=True)
    tool_id = data.get("tool_id", "")
    user_input = data.get("input", "").strip()

    tool = get_tool(tool_id)
    if not tool:
        return jsonify({"error": f"Unknown tool: {tool_id}"}), 400
    if not user_input:
        return jsonify({"error": "Input is required"}), 400

    url = tool["url"].replace("{input}", req.utils.quote(str(user_input), safe=""))

    try:
        response = req.get(url, timeout=12, headers={
            "User-Agent": "Mozilla/5.0 (compatible; VISHAL-INFO-CYBER/1.0)",
            "Accept": "application/json, text/plain, */*",
        })
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type:
            result = response.json()
        else:
            text = response.text.strip()
            try:
                result = json.loads(text)
            except Exception:
                result = text
        return jsonify({"result": result})
    except req.exceptions.Timeout:
        return jsonify({"error": "Request timed out. The API did not respond in time."}), 504
    except req.exceptions.ConnectionError:
        return jsonify({"error": "Connection failed. The API server may be down or unreachable."}), 502
    except req.exceptions.HTTPError as e:
        return jsonify({"error": f"API returned error: {e.response.status_code} {e.response.reason}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===================== ENTRY POINT =====================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"""
╔══════════════════════════════════════════╗
║      VISHAL INFO CYBER - Web Server      ║
║  Developer: @VISHAL_INFO_CYBER           ║
╠══════════════════════════════════════════╣
║  Running at: http://0.0.0.0:{port:<5}        ║
║  Open in browser: http://localhost:{port:<5}  ║
╚══════════════════════════════════════════╝
""")
    app.run(host="0.0.0.0", port=port, debug=False)
