# ⚡️ NEO OSINT BOT - ULTIMATE WORKING VERSION ⚡️
# Developer: @NEOBLADE701
# All Features Working + Force Channel + Advanced Admin

import logging
import os
import sys
import time
import json
import asyncio
import sqlite3
import requests
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.error import BadRequest, Forbidden
from io import BytesIO

# ===================== CONFIGURATION =====================
BOT_TOKEN = "8585585297:AAH1Z7Dt8nt4pBwM275MDJFvHaO3DSBMTeA"
ADMIN_ID = 8125487901
OWNER_USERNAME = "@NEOBLADE701"
DEVELOPER_TAG = "@NEOBLADE701"
GROUP_LINK = "https://t.me/NEO_X_RAJ"

# Anti-Tamper Check
if DEVELOPER_TAG != "@NEOBLADE701":
    sys.exit("⚠️ Developer tag modified. Bot exiting.")

# Database File
DB_FILE = "neo_osint_ultimate.db"

# ===================== ALL WORKING APIS =====================
NEO_APIS = {
    # Number Lookups
    "num": "https://abbas-apis.vercel.app/api/num-name?number={}",
    "phone": "https://abbas-apis.vercel.app/api/phone?number={}",
    "pak": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "global": "http://erox.shop/numapi.php?mobile={}&key=KRISH",
    
    # Social Media
    "instagram": "https://abbas-apis.vercel.app/api/instagram?username={}",
    "instagram2": "https://mediafire.m2hgamerz.workers.dev/api/instagram?username={}",
    "github": "https://abbas-apis.vercel.app/api/github?username={}",
    "telegram": "https://api.b77bf911.workers.dev/telegram?user={}",
    
    # Gaming
    "ff": "https://abbas-apis.vercel.app/api/ff-info?uid={}",
    "ffban": "https://abbas-apis.vercel.app/api/ff-ban?uid={}",
    
    # Financial
    "pan": "https://pan.amorinthz.workers.dev/?key=AMORINTH&pan={}",
    "ifsc": "https://abbas-apis.vercel.app/api/ifsc?ifsc={}",
    "fampay": "https://api.b77bf911.workers.dev/upi2?id={}",
    
    # Tech
    "ip": "https://abbas-apis.vercel.app/api/ip?ip={}",
    "email": "https://abbas-apis.vercel.app/api/email?mail={}",
    
    # Indian Documents
    "aadhaar": "https://adhaar.khna04221.workers.dev/?aadhaar={}",
    "vehicle": "https://vehicle-info-api-abhi.vercel.app/?rc_number={}",
    "pincode": "https://api.postalpincode.in/pincode/{}",
}

# ===================== LOGGING =====================
logging.basicConfig(
    format='%(asctime)s - ⚡️ NEO - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ===================== DATABASE FUNCTIONS =====================
def neo_init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_searches INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0
    )''')
    
    # Groups table
    c.execute('''CREATE TABLE IF NOT EXISTS groups (
        chat_id INTEGER PRIMARY KEY,
        title TEXT,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_searches INTEGER DEFAULT 0
    )''')
    
    # Force channels
    c.execute('''CREATE TABLE IF NOT EXISTS force_channels (
        channel_id TEXT PRIMARY KEY,
        channel_name TEXT,
        invite_link TEXT,
        added_by INTEGER,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Authorized users for DM
    c.execute('''CREATE TABLE IF NOT EXISTS auth_users (
        user_id INTEGER PRIMARY KEY,
        added_by INTEGER,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Settings
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Hidden commands
    c.execute('''CREATE TABLE IF NOT EXISTS hidden_commands (
        command TEXT PRIMARY KEY,
        hidden INTEGER DEFAULT 0,
        hidden_by INTEGER,
        hidden_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # API settings (for custom URLs)
    c.execute('''CREATE TABLE IF NOT EXISTS api_settings (
        api_name TEXT PRIMARY KEY,
        custom_url TEXT,
        enabled INTEGER DEFAULT 1,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insert default APIs
    for api_name in NEO_APIS.keys():
        c.execute("INSERT OR IGNORE INTO api_settings (api_name) VALUES (?)", (api_name,))
    
    # Insert default commands for hiding
    default_commands = ['num', 'phone', 'instagram', 'github', 'ip', 'pan', 'ifsc', 
                       'vehicle', 'ff', 'ffban', 'email', 'aadhaar', 'pincode', 
                       'global', 'pak', 'telegram', 'fampay', 'instagram2']
    for cmd in default_commands:
        c.execute("INSERT OR IGNORE INTO hidden_commands (command) VALUES (?)", (cmd,))
    
    # Default settings
    default_settings = [
        ('maintenance', '0'),
        ('maintenance_msg', '🚧 Bot is under maintenance. Please try again later.'),
        ('owner_pic', 'https://graph.org/file/52b6e6f7163fd6f7184b3.jpg'),
        ('bot_status', '✅ ONLINE'),
        ('welcome_msg', 'Welcome to NEO OSINT Bot!'),
        ('broadcast_last', ''),
        ('clone_price', '500 Stars ⭐'),
        ('payment_link', f'https://t.me/{DEVELOPER_TAG.replace("@", "")}')
    ]
    
    for key, value in default_settings:
        c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, value))
    
    # Insert default force channels
    default_channels = [
        ("NEO PRIVATE", "https://t.me/+5C34V2aG5_I3ZWQ1", "-1001234567890"),
        ("NEON X PUBLIC", "https://t.me/NEON_X_PUBLIC", "-1001234567891"),
        ("SANIYA SUPPORT", "https://t.me/SANIYA_BOT_SUPPORT", "-1001234567892"),
        ("THE SANIYA BOTS", "https://t.me/TheSaniyaBots", "-1001234567893")
    ]
    
    for name, link, cid in default_channels:
        c.execute('''INSERT OR IGNORE INTO force_channels 
                    (channel_id, channel_name, invite_link, added_by) 
                    VALUES (?, ?, ?, ?)''', 
                 (cid, name, link, ADMIN_ID))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized with all tables")

def neo_get_db():
    return sqlite3.connect(DB_FILE)

def neo_update_stats():
    conn = neo_get_db()
    c = conn.cursor()
    
    user_count = c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 0").fetchone()[0]
    group_count = c.execute("SELECT COUNT(*) FROM groups").fetchone()[0]
    
    c.execute("UPDATE settings SET value = ? WHERE key = 'total_users'", (str(user_count),))
    c.execute("UPDATE settings SET value = ? WHERE key = 'total_groups'", (str(group_count),))
    
    conn.commit()
    conn.close()

# ===================== HELPER FUNCTIONS =====================
def neo_is_admin(user_id):
    return user_id == ADMIN_ID

def neo_is_auth(user_id):
    if neo_is_admin(user_id):
        return True
    conn = neo_get_db()
    c = conn.cursor()
    result = c.execute("SELECT 1 FROM auth_users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return bool(result)

def neo_get_setting(key):
    conn = neo_get_db()
    c = conn.cursor()
    result = c.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return result[0] if result else None

def neo_set_setting(key, value):
    conn = neo_get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def neo_is_maintenance():
    return neo_get_setting('maintenance') == '1'

def neo_get_maintenance_msg():
    return neo_get_setting('maintenance_msg') or "🚧 Bot is under maintenance."

def neo_is_command_hidden(command):
    conn = neo_get_db()
    c = conn.cursor()
    result = c.execute("SELECT hidden FROM hidden_commands WHERE command = ?", (command,)).fetchone()
    conn.close()
    return bool(result and result[0] == 1)

def neo_get_api_url(api_name):
    """Get API URL - custom if set, otherwise default"""
    conn = neo_get_db()
    c = conn.cursor()
    result = c.execute("SELECT custom_url, enabled FROM api_settings WHERE api_name = ?", (api_name,)).fetchone()
    conn.close()
    
    if result and result[0] and result[1] == 1:  # Custom URL exists and API is enabled
        return result[0]
    elif result and result[1] == 0:  # API disabled
        return None
    else:
        return NEO_APIS.get(api_name)

def neo_set_api_url(api_name, url):
    conn = neo_get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO api_settings (api_name, custom_url) VALUES (?, ?)", (api_name, url))
    conn.commit()
    conn.close()

def neo_toggle_api(api_name, enable=True):
    conn = neo_get_db()
    c = conn.cursor()
    c.execute("UPDATE api_settings SET enabled = ? WHERE api_name = ?", (1 if enable else 0, api_name))
    conn.commit()
    conn.close()

def neo_get_force_channels():
    conn = neo_get_db()
    c = conn.cursor()
    channels = c.execute("SELECT channel_name, invite_link, channel_id FROM force_channels WHERE is_active = 1").fetchall()
    conn.close()
    return channels

def neo_add_force_channel(channel_name, invite_link, channel_id, added_by):
    conn = neo_get_db()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO force_channels 
                (channel_id, channel_name, invite_link, added_by) 
                VALUES (?, ?, ?, ?)''', 
             (channel_id, channel_name, invite_link, added_by))
    conn.commit()
    conn.close()
    return True

def neo_remove_force_channel(channel_id):
    conn = neo_get_db()
    c = conn.cursor()
    c.execute("DELETE FROM force_channels WHERE channel_id = ?", (channel_id,))
    conn.commit()
    conn.close()
    return True

async def neo_check_channels(user_id, bot):
    """Check if user has joined all force channels"""
    if neo_is_admin(user_id):
        return True, []
    
    channels = neo_get_force_channels()
    if not channels:
        return True, []
    
    missing_channels = []
    
    for channel_name, invite_link, channel_id in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                missing_channels.append((channel_name, invite_link))
        except Exception as e:
            logger.error(f"Error checking channel {channel_id}: {e}")
            missing_channels.append((channel_name, invite_link))
    
    return len(missing_channels) == 0, missing_channels

def neo_channels_keyboard(missing_channels):
    """Create keyboard with channel join buttons"""
    keyboard = []
    
    for channel_name, invite_link in missing_channels:
        keyboard.append([InlineKeyboardButton(f"📢 Join {channel_name}", url=invite_link)])
    
    keyboard.append([InlineKeyboardButton("✅ I'VE JOINED ALL", callback_data="verify_join")])
    
    return InlineKeyboardMarkup(keyboard)

# ===================== ASCII ART & UI =====================
def neo_ascii_art():
    return """
╔══════════════════════════════════════╗
║    🕵️‍♂️ 𝗡𝗘𝗢 𝗢𝗦𝗜𝗡𝗧 𝗕𝗢𝗧 𝗩𝟱.𝟬 ⚡️      ║
║                                      ║
║  🔓 𝗦𝗬𝗦𝗧𝗘𝗠𝗦: 𝗢𝗡𝗟𝗜𝗡𝗘             ║
║  📡 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗢𝗡: 𝗘𝗦𝗧𝗔𝗕𝗟𝗜𝗦𝗛𝗘𝗗   ║
║  ⚙️ 𝗠𝗢𝗗𝗘: 𝗙𝗨𝗟𝗟𝗬 𝗔𝗖𝗧𝗜𝗩𝗘        ║
║                                      ║
║    𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗡𝗘𝗢 𝗡𝗘𝗧𝗪𝗢𝗥𝗞      ║
╚══════════════════════════════════════╝
"""

# ===================== START COMMAND =====================
async def neo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    # Update user in database
    conn = neo_get_db()
    c = conn.cursor()
    
    if chat.type == 'private':
        c.execute('''INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_active) 
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)''',
                 (user.id, user.username, user.first_name))
    else:
        c.execute('''INSERT OR REPLACE INTO groups 
                    (chat_id, title) 
                    VALUES (?, ?)''',
                 (chat.id, chat.title))
    
    conn.commit()
    conn.close()
    
    neo_update_stats()
    
    # Check maintenance
    if neo_is_maintenance() and not neo_is_admin(user.id):
        await update.message.reply_text(neo_get_maintenance_msg())
        return
    
    # Private chat flow
    if chat.type == 'private':
        # Hacker UI animation
        animation = [
            "⚡ *Initializing NEO Protocol...*",
            "🔄 *Booting OSINT Modules...*",
            "🔓 *Decrypting Security Layers...*",
            "📡 *Establishing Secure Connection...*",
            "✅ *NEO SYSTEM ONLINE*"
        ]
        
        msg = await update.message.reply_text(animation[0], parse_mode="Markdown")
        for text in animation[1:]:
            await asyncio.sleep(0.8)
            await msg.edit_text(text, parse_mode="Markdown")
        await asyncio.sleep(0.5)
        await msg.delete()
        
        # Check channel subscription
        joined, missing_channels = await neo_check_channels(user.id, context.bot)
        if not joined:
            await update.message.reply_text(
                "🔒 *ACCESS RESTRICTED*\n\n"
                "📢 *Join our official channels to unlock all features:*\n\n"
                "*Why join?*\n"
                "• Get latest updates & features\n"
                "• Priority support\n"
                "• Exclusive content\n"
                "• Community access\n\n"
                "⚠️ *You must join ALL channels below:*",
                parse_mode="Markdown",
                reply_markup=neo_channels_keyboard(missing_channels)
            )
            return
    
    # Send owner photo (spoiler)
    owner_pic = neo_get_setting('owner_pic')
    try:
        if owner_pic and chat.type == 'private':
            await update.message.reply_photo(
                photo=owner_pic,
                caption=f"👑 *Bot Owner*\n{OWNER_USERNAME}",
                parse_mode="Markdown",
                has_spoiler=True
            )
    except:
        pass
    
    # Show main menu
    await neo_show_main_menu(update, context)

async def neo_show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    caption = f"""
{neo_ascii_art()}

👤 *USER IDENTIFIED:*
├ Name: {user.first_name or "Unknown"}
├ ID: `{user.id}`
└ Username: @{user.username or "None"}

👑 *OWNER:* {OWNER_USERNAME}
👨‍💻 *DEVELOPER:* {DEVELOPER_TAG}

🔥 *STATUS:* `{neo_get_setting('bot_status')}`
🔓 *ACCESS:* `{'FULL' if update.effective_chat.type != 'private' or neo_is_auth(user.id) else 'RESTRICTED'}`
📊 *VERSION:* 5.0

*FREE OSINT BOT - FULL WORKING*
*BOT DEVELOPER:* {DEVELOPER_TAG}

*AVAILABLE TOOLS (18+):*
• 📱 Number/Phone/PAN/Aadhaar
• 📸 Instagram/GitHub/Telegram
• 🌐 IP/Email Verification
• 🏦 IFSC/Fampay UPI
• 🚗 Vehicle/Pincode Search
• 🎮 Free Fire Info/Ban
• 🌍 Global Search

_Add me to your group for FREE unlimited usage!_
"""
    
    # Stylish buttons with emojis
    keyboard = [
        [InlineKeyboardButton("📱 𝐍𝐔𝐌𝐁𝐄𝐑 𝐈𝐍𝐅𝐎", callback_data="tool_num"),
         InlineKeyboardButton("📸 𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌", callback_data="tool_instagram")],
        [InlineKeyboardButton("📱 𝐏𝐇𝐎𝐍𝐄 𝐈𝐍𝐅𝐎", callback_data="tool_phone"),
         InlineKeyboardButton("🌐 𝐈𝐏 𝐋𝐎𝐎𝐊𝐔𝐏", callback_data="tool_ip")],
        [InlineKeyboardButton("🐙 𝐆𝐈𝐓𝐇𝐔𝐁", callback_data="tool_github"),
         InlineKeyboardButton("💳 𝐏𝐀𝐍 𝐂𝐀𝐑𝐃", callback_data="tool_pan")],
        [InlineKeyboardButton("🏦 𝐈𝐅𝐒𝐂 𝐂𝐎𝐃𝐄", callback_data="tool_ifsc"),
         InlineKeyboardButton("🚗 𝐕𝐄𝐇𝐈𝐂𝐋𝐄", callback_data="tool_vehicle")],
        [InlineKeyboardButton("🎮 𝐅𝐑𝐄𝐄 𝐅𝐈𝐑𝐄", callback_data="tool_ff"),
         InlineKeyboardButton("🚫 𝐅𝐅 𝐁𝐀𝐍", callback_data="tool_ffban")],
        [InlineKeyboardButton("📧 𝐄𝐌𝐀𝐈𝐋", callback_data="tool_email"),
         InlineKeyboardButton("🆔 𝐀𝐀𝐃𝐇𝐀𝐀𝐑", callback_data="tool_aadhaar")],
        [InlineKeyboardButton("📍 𝐏𝐈𝐍𝐂𝐎𝐃𝐄", callback_data="tool_pincode"),
         InlineKeyboardButton("🌍 𝐆𝐋𝐎𝐁𝐀𝐋", callback_data="tool_global")],
        [InlineKeyboardButton("🇵🇰 𝐏𝐀𝐊 𝐍𝐔𝐌𝐁𝐄𝐑", callback_data="tool_pak"),
         InlineKeyboardButton("📱 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌", callback_data="tool_telegram")],
        [InlineKeyboardButton("💰 𝐅𝐀𝐌𝐏𝐀𝐘", callback_data="tool_fampay"),
         InlineKeyboardButton("📸 𝐈𝐍𝐒𝐓𝐀 𝟐", callback_data="tool_instagram2")],
    ]
    
    # Bottom buttons (special styling)
    bottom_buttons = [
        [InlineKeyboardButton("🤖 𝐂𝐋𝐎𝐍𝐄 𝐁𝐎𝐓", callback_data="clone_start"),
         InlineKeyboardButton("❓ 𝐇𝐄𝐋𝐏", callback_data="help_menu")],
        [InlineKeyboardButton("➕ 𝐀𝐃𝐃 𝐌𝐄 𝐈𝐍 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏", url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("🏠 𝐔𝐒𝐄 𝐌𝐄 𝐈𝐍 𝐌𝐘 𝐆𝐑𝐎𝐔𝐏", url=GROUP_LINK)],
    ]
    
    if neo_is_admin(user.id):
        bottom_buttons.insert(0, [InlineKeyboardButton("👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋", callback_data="admin_panel")])
    
    keyboard.extend(bottom_buttons)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===================== TOOL HANDLERS =====================
async def neo_search_api(api_name, query):
    """Search using API"""
    try:
        api_url = neo_get_api_url(api_name)
        if not api_url:
            return "❌ This tool is currently disabled."
        
        url = api_url.format(query)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Format based on API
                result_text = f"✅ *{api_name.upper()} INFO*\n"
                result_text += "━━━━━━━━━━━━━━━━━━━━\n"
                
                if api_name == "instagram":
                    result_text += f"📸 *Instagram: @{query}*\n"
                    result_text += f"• Posts: {data.get('posts', 'N/A')}\n"
                    result_text += f"• Followers: {data.get('followers', 'N/A')}\n"
                    result_text += f"• Following: {data.get('following', 'N/A')}\n"
                    result_text += f"• Full Name: {data.get('full_name', 'N/A')}\n"
                    result_text += f"• Bio: {data.get('bio', 'N/A')[:100]}...\n"
                    result_text += f"• Private: {'✅ Yes' if data.get('is_private') else '❌ No'}\n"
                    result_text += f"• Verified: {'✅ Yes' if data.get('is_verified') else '❌ No'}\n"
                
                elif api_name == "github":
                    result_text += f"🐙 *GitHub: @{query}*\n"
                    result_text += f"• Name: {data.get('name', 'N/A')}\n"
                    result_text += f"• Bio: {data.get('bio', 'N/A')[:100]}...\n"
                    result_text += f"• Followers: {data.get('followers', 0)}\n"
                    result_text += f"• Following: {data.get('following', 0)}\n"
                    result_text += f"• Public Repos: {data.get('public_repos', 0)}\n"
                    result_text += f"• Location: {data.get('location', 'N/A')}\n"
                    result_text += f"• Created: {data.get('created_at', 'N/A')[:10]}\n"
                
                elif api_name == "ip":
                    result_text += f"🌐 *IP: {query}*\n"
                    result_text += f"• Country: {data.get('country', 'N/A')}\n"
                    result_text += f"• Region: {data.get('regionName', 'N/A')}\n"
                    result_text += f"• City: {data.get('city', 'N/A')}\n"
                    result_text += f"• ISP: {data.get('isp', 'N/A')}\n"
                    result_text += f"• Organization: {data.get('org', 'N/A')}\n"
                    result_text += f"• Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n"
                    result_text += f"• Timezone: {data.get('timezone', 'N/A')}\n"
                
                elif api_name == "ifsc":
                    result_text += f"🏦 *IFSC: {query.upper()}*\n"
                    result_text += f"• Bank: {data.get('BANK', 'N/A')}\n"
                    result_text += f"• Branch: {data.get('BRANCH', 'N/A')}\n"
                    result_text += f"• Address: {data.get('ADDRESS', 'N/A')}\n"
                    result_text += f"• City: {data.get('CITY', 'N/A')}\n"
                    result_text += f"• District: {data.get('DISTRICT', 'N/A')}\n"
                    result_text += f"• State: {data.get('STATE', 'N/A')}\n"
                
                elif api_name == "ff":
                    result_text += f"🎮 *Free Fire: UID {query}*\n"
                    result_text += f"• Nickname: {data.get('nickname', 'N/A')}\n"
                    result_text += f"• Level: {data.get('level', 'N/A')}\n"
                    result_text += f"• Exp: {data.get('exp', 'N/A')}\n"
                    result_text += f"• Guild: {data.get('guild', 'N/A')}\n"
                    result_text += f"• Server: {data.get('server', 'N/A')}\n"
                
                elif api_name == "vehicle":
                    result_text += f"🚗 *Vehicle: {query.upper()}*\n"
                    result_text += f"• Owner: {data.get('owner_name', 'N/A')}\n"
                    result_text += f"• Model: {data.get('vehicle_model', 'N/A')}\n"
                    result_text += f"• Registration Date: {data.get('registration_date', 'N/A')}\n"
                    result_text += f"• Fuel Type: {data.get('fuel_type', 'N/A')}\n"
                    result_text += f"• Insurance: {data.get('insurance_status', 'N/A')}\n"
                
                elif api_name == "pincode":
                    if data and data[0].get('Status') == 'Success':
                        office = data[0]['PostOffice'][0] if data[0]['PostOffice'] else {}
                        result_text += f"📍 *Pincode: {query}*\n"
                        result_text += f"• District: {office.get('District', 'N/A')}\n"
                        result_text += f"• State: {office.get('State', 'N/A')}\n"
                        result_text += f"• Region: {office.get('Region', 'N/A')}\n"
                        result_text += f"• Country: India\n"
                        result_text += f"• Delivery: {office.get('DeliveryStatus', 'N/A')}\n"
                    else:
                        return "❌ Invalid pincode"
                
                elif isinstance(data, dict):
                    result_text += f"📊 *{api_name.upper()}: {query}*\n"
                    for key, value in data.items():
                        if value and str(value).strip():
                            formatted_key = key.replace('_', ' ').title()
                            result_text += f"• *{formatted_key}:* `{value}`\n"
                else:
                    result_text += f"📊 *Result*\n```\n{json.dumps(data, indent=2)}\n```\n"
                
                result_text += "━━━━━━━━━━━━━━━━━━━━\n"
                result_text += f"👨‍💻 *Developer:* {DEVELOPER_TAG}"
                
                return result_text
                
            except json.JSONDecodeError:
                return f"✅ *Result*\n\n```\n{response.text[:1500]}\n```\n\n👨‍💻 *Developer:* {DEVELOPER_TAG}"
        else:
            return f"❌ API Error (Status: {response.status_code})"
            
    except requests.exceptions.Timeout:
        return "❌ Request timeout. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)[:200]}"

async def neo_tool_command(update: Update, context: ContextTypes.DEFAULT_TYPE, tool_name: str):
    user = update.effective_user
    chat = update.effective_chat
    
    # Check if command is hidden
    if neo_is_command_hidden(tool_name) and not neo_is_admin(user.id):
        await update.message.reply_text("❌ This command is currently disabled.")
        return
    
    # Access control
    if chat.type == 'private' and not neo_is_auth(user.id):
        # Check channel subscription
        joined, missing_channels = await neo_check_channels(user.id, context.bot)
        if not joined:
            await update.message.reply_text(
                "❌ *ACCESS DENIED IN DM!*\n\n"
                "Join required channels to use in DM or use in groups for free.",
                parse_mode="Markdown",
                reply_markup=neo_channels_keyboard(missing_channels)
            )
            return
    
    if not context.args:
        await update.message.reply_text(f"⚠️ Usage: `/{tool_name} <value>`\n\n*Example:* `/{tool_name} 9876543210`", parse_mode="Markdown")
        return
    
    query = " ".join(context.args)
    
    # Animation
    animation = [
        f"🔍 *Searching {tool_name.upper()}...*",
        "🔄 *Accessing Database...*",
        "⚡ *Processing Request...*",
        "📡 *Fetching Results...*"
    ]
    
    msg = await update.message.reply_text(animation[0], parse_mode="Markdown")
    for text in animation[1:]:
        await asyncio.sleep(0.5)
        await msg.edit_text(text, parse_mode="Markdown")
    
    # Perform search
    result = await neo_search_api(tool_name, query)
    
    # Update stats
    conn = neo_get_db()
    c = conn.cursor()
    
    if chat.type == 'private':
        c.execute("UPDATE users SET total_searches = total_searches + 1, last_active = CURRENT_TIMESTAMP WHERE user_id = ?", 
                 (user.id,))
    else:
        c.execute("UPDATE groups SET total_searches = total_searches + 1 WHERE chat_id = ?", 
                 (chat.id,))
    
    conn.commit()
    conn.close()
    
    # Send result
    await msg.edit_text(result, parse_mode="Markdown")

# Command wrappers
async def cmd_num(update, context): await neo_tool_command(update, context, "num")
async def cmd_phone(update, context): await neo_tool_command(update, context, "phone")
async def cmd_instagram(update, context): await neo_tool_command(update, context, "instagram")
async def cmd_github(update, context): await neo_tool_command(update, context, "github")
async def cmd_ip(update, context): await neo_tool_command(update, context, "ip")
async def cmd_pan(update, context): await neo_tool_command(update, context, "pan")
async def cmd_ifsc(update, context): await neo_tool_command(update, context, "ifsc")
async def cmd_vehicle(update, context): await neo_tool_command(update, context, "vehicle")
async def cmd_ff(update, context): await neo_tool_command(update, context, "ff")
async def cmd_ffban(update, context): await neo_tool_command(update, context, "ffban")
async def cmd_email(update, context): await neo_tool_command(update, context, "email")
async def cmd_aadhaar(update, context): await neo_tool_command(update, context, "aadhaar")
async def cmd_pincode(update, context): await neo_tool_command(update, context, "pincode")
async def cmd_global(update, context): await neo_tool_command(update, context, "global")
async def cmd_pak(update, context): await neo_tool_command(update, context, "pak")
async def cmd_telegram(update, context): await neo_tool_command(update, context, "telegram")
async def cmd_fampay(update, context): await neo_tool_command(update, context, "fampay")
async def cmd_instagram2(update, context): await neo_tool_command(update, context, "instagram2")

# ===================== ADMIN PANEL =====================
async def neo_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not neo_is_admin(update.effective_user.id):
        if update.callback_query:
            await update.callback_query.answer("❌ Admin only!", show_alert=True)
        else:
            await update.message.reply_text("❌ Admin only command.")
        return
    
    conn = neo_get_db()
    c = conn.cursor()
    
    # Get stats
    user_count = c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 0").fetchone()[0]
    group_count = c.execute("SELECT COUNT(*) FROM groups").fetchall()[0]
    total_searches = c.execute("SELECT SUM(total_searches) FROM users").fetchone()[0] or 0
    channel_count = c.execute("SELECT COUNT(*) FROM force_channels WHERE is_active = 1").fetchone()[0]
    
    # Today's activity
    today_users = c.execute("SELECT COUNT(*) FROM users WHERE date(last_active) = date('now')").fetchone()[0]
    
    maint_status = neo_is_maintenance()
    bot_status = neo_get_setting('bot_status')
    
    conn.close()
    
    stats_text = f"""
👑 *NEO ADMIN CONTROL PANEL*
━━━━━━━━━━━━━━━━━━━━━━━

📊 *BOT STATISTICS:*
• Total Users: `{user_count}`
• Active Today: `{today_users}`
• Total Groups: `{group_count}`
• Total Searches: `{total_searches}`
• Force Channels: `{channel_count}`
• Bot Status: `{bot_status}`
• Maintenance: `{'🔴 ON' if maint_status else '🟢 OFF'}`

⚙️ *ADMIN TOOLS:*
"""
    
    keyboard = [
        [InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
         InlineKeyboardButton("🛠 MAINTENANCE", callback_data="admin_maintenance")],
        [InlineKeyboardButton("🔗 CHANNEL MANAGER", callback_data="admin_channels"),
         InlineKeyboardButton("👤 USER MANAGER", callback_data="admin_users")],
        [InlineKeyboardButton("⚙️ API MANAGER", callback_data="admin_apis"),
         InlineKeyboardButton("🚫 HIDE COMMANDS", callback_data="admin_hide")],
        [InlineKeyboardButton("📊 DETAILED STATS", callback_data="admin_stats"),
         InlineKeyboardButton("🖼 CHANGE OWNER PIC", callback_data="admin_pic")],
        [InlineKeyboardButton("➕ ADD FORCE CHANNEL", callback_data="admin_add_channel"),
         InlineKeyboardButton("➕ AUTHORIZE USER", callback_data="admin_add_auth")],
        [InlineKeyboardButton("🏠 MAIN MENU", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===================== ADMIN COMMANDS =====================
async def neo_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not neo_is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command.")
        return
    
    reply = update.message.reply_to_message
    msg_text = " ".join(context.args)
    
    if not reply and not msg_text:
        await update.message.reply_text(
            "📢 *Broadcast System*\n\n"
            "*Methods:*\n"
            "1. Reply to a message with `/broadcast`\n"
            "2. Send `/broadcast <message>`\n\n"
            "✅ *Features:*\n"
            "• Text, Photos, Videos, Documents\n"
            "• Markdown formatting\n"
            "• Sent to all users & groups\n"
            "• DM and group chats\n\n"
            "*Type /cancel to cancel*",
            parse_mode="Markdown"
        )
        return
    
    # Get all recipients
    conn = neo_get_db()
    c = conn.cursor()
    
    users = [row[0] for row in c.execute("SELECT user_id FROM users WHERE is_banned = 0").fetchall()]
    groups = [row[0] for row in c.execute("SELECT chat_id FROM groups").fetchall()]
    
    conn.close()
    
    targets = list(set(users + groups))
    total = len(targets)
    
    progress = await update.message.reply_text(f"📢 *Starting Broadcast...*\nTargets: `{total}`", parse_mode="Markdown")
    
    sent = 0
    failed = 0
    
    for chat_id in targets:
        try:
            if reply:
                await reply.copy(chat_id)
            else:
                await context.bot.send_message(chat_id, msg_text, parse_mode="Markdown")
            sent += 1
            
            if sent % 10 == 0:
                await progress.edit_text(f"📢 Broadcasting...\nSent: `{sent}/{total}`\nFailed: `{failed}`", parse_mode="Markdown")
            
            await asyncio.sleep(0.1)
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast failed for {chat_id}: {e}")
    
    await progress.edit_text(
        f"✅ *BROADCAST COMPLETE*\n\n"
        f"• Total Targets: `{total}`\n"
        f"• Successfully Sent: `{sent}`\n"
        f"• Failed: `{failed}`\n"
        f"• Success Rate: `{(sent/total*100 if total>0 else 0):.1f}%`\n\n"
        f"📊 *Sent to:*\n"
        f"• Users: {len(users)}\n"
        f"• Groups: {len(groups)}",
        parse_mode="Markdown"
    )

async def neo_add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not neo_is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command.")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "🔗 *Add Force Channel*\n\n"
            "*Usage:* `/addchannel <channel_id> <invite_link> <channel_name>`\n\n"
            "*Example:*\n"
            "`/addchannel -100123456789 https://t.me/+ABC123 NEO Channel`\n\n"
            "*Note:* Bot must be admin in the channel.",
            parse_mode="Markdown"
        )
        return
    
    channel_id = context.args[0]
    invite_link = context.args[1]
    channel_name = " ".join(context.args[2:])
    
    # Add to database
    success = neo_add_force_channel(channel_name, invite_link, channel_id, update.effective_user.id)
    
    if success:
        await update.message.reply_text(
            f"✅ *Channel Added Successfully!*\n\n"
            f"• Name: {channel_name}\n"
            f"• ID: `{channel_id}`\n"
            f"• Link: {invite_link}\n\n"
            f"Users must now join this channel to use the bot in DM.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Failed to add channel.")

async def neo_add_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not neo_is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: `/addauth <user_id>`", parse_mode="Markdown")
        return
    
    try:
        user_id = int(context.args[0])
        conn = neo_get_db()
        c = conn.cursor()
        
        # Add to auth users
        c.execute("INSERT OR REPLACE INTO auth_users (user_id, added_by) VALUES (?, ?)", 
                 (user_id, update.effective_user.id))
        
        # Add to users table if not exists
        c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ User `{user_id}` authorized for DM access.", parse_mode="Markdown")
        
        # Notify user if possible
        try:
            await context.bot.send_message(
                user_id,
                f"🎉 *Access Granted!*\n\n"
                f"You've been granted DM access to NEO OSINT Bot!\n"
                f"Use /start to begin.",
                parse_mode="Markdown"
            )
        except:
            pass
            
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Use numbers only.")

# ===================== CLONE SYSTEM =====================
async def neo_clone_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clone_price = neo_get_setting('clone_price') or "500 Stars ⭐"
    payment_link = neo_get_setting('payment_link') or f"https://t.me/{DEVELOPER_TAG.replace('@', '')}"
    
    clone_text = f"""
🤖 *CLONE BOT CREATOR*

💰 *PRICE:* {clone_price}
🎁 *PAYMENT:* Gift to {DEVELOPER_TAG}

*FEATURES INCLUDED:*
• All 18+ lookup tools
• Custom bot token
• Your own admin panel
• No channel requirements
• Full source code
• Lifetime updates

*HOW TO GET:*
1. Send {clone_price} to {DEVELOPER_TAG}
2. Send payment proof
3. Provide your admin ID
4. Receive bot token & setup guide

*CLONE FEATURES:*
• Same UI as main bot
• All APIs working
• Group free usage
• Admin controls
• Broadcast system

*CONTACT:* {DEVELOPER_TAG}
"""
    
    keyboard = [
        [InlineKeyboardButton("💳 PAY NOW", url=payment_link)],
        [InlineKeyboardButton("✅ I HAVE PAID", callback_data="clone_paid")],
        [InlineKeyboardButton("🔙 BACK", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            clone_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            clone_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===================== CALLBACK HANDLERS =====================
async def neo_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    await query.answer()
    
    if data == "main_menu":
        await neo_show_main_menu(update, context)
    
    elif data == "verify_join":
        joined, missing_channels = await neo_check_channels(query.from_user.id, context.bot)
        if joined:
            await query.answer("✅ Access Granted! Welcome to NEO.", show_alert=True)
            await neo_show_main_menu(update, context)
        else:
            await query.answer("❌ Please join ALL channels first!", show_alert=True)
    
    elif data.startswith("tool_"):
        tool = data.replace("tool_", "")
        await query.edit_message_text(
            f"🔍 *{tool.upper()} LOOKUP*\n\n"
            f"Send command: `/{tool} <value>`\n\n"
            f"*Examples:*\n"
            f"• `/{tool} 9876543210` (for numbers)\n"
            f"• `/{tool} username` (for social media)\n"
            f"• `/{tool} example@gmail.com` (for email)\n\n"
            f"*Note:* Free in groups, join channels for DM access",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="main_menu")]])
        )
    
    elif data == "help_menu":
        help_text = f"""
{neo_ascii_art()}

🛠 *NEO OSINT BOT - COMMANDS GUIDE*

🤖 *ABOUT:*
• Developer: {DEVELOPER_TAG}
• Owner: {OWNER_USERNAME}
• Version: 5.0 (Ultimate)
• Status: ✅ Online

🔧 *AVAILABLE COMMANDS:*
/start - Start the bot
/num <number> - Number info lookup
/phone <number> - Phone number info
/instagram <username> - Instagram info
/github <username> - GitHub profile info
/ip <address> - IP address lookup
/pan <number> - PAN card info
/ifsc <code> - IFSC code details
/vehicle <rc> - Vehicle RC info
/ff <uid> - Free Fire player info
/ffban <uid> - Free Fire ban check
/email <address> - Email verification
/aadhaar <number> - Aadhaar validation
/pincode <code> - Pincode details
/global <query> - Global search
/pak <number> - Pakistan number info
/telegram <id> - Telegram info
/fampay <id> - Fampay UPI info
/clone - Create your own bot
/admin - Admin panel (admin only)

📊 *USAGE RULES:*
• Group Usage: FREE for everyone
• DM Usage: Join channels first
• Educational purpose only
• Respect privacy laws

🔗 *OFFICIAL GROUP:* {GROUP_LINK}

⚠️ *DISCLAIMER:*
This bot is for educational purposes only.
We're not responsible for any misuse.
"""
        await query.edit_message_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="main_menu")]])
        )
    
    elif data == "admin_panel":
        await neo_admin_panel(update, context)
    
    elif data == "admin_broadcast":
        context.user_data['admin_action'] = 'broadcast'
        await query.edit_message_text(
            "📢 *Send Broadcast Message:*\n\n"
            "You can send text or reply to any message.\n"
            "Will be sent to all users and groups.\n\n"
            "*Type /cancel to cancel*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]])
        )
    
    elif data == "admin_maintenance":
        maint_status = neo_is_maintenance()
        
        if maint_status:
            keyboard = [
                [InlineKeyboardButton("🟢 DISABLE MAINTENANCE", callback_data="disable_maint")],
                [InlineKeyboardButton("✏️ CHANGE MESSAGE", callback_data="change_maint_msg")],
                [InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]
            ]
            await query.edit_message_text(
                "🛠 *Maintenance Mode: ENABLED*\n\n"
                "Current message:\n`" + neo_get_maintenance_msg() + "`\n\n"
                "Select an option:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("🔴 ENABLE MAINTENANCE", callback_data="enable_maint")],
                [InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]
            ]
            await query.edit_message_text(
                "🛠 *Maintenance Mode: DISABLED*\n\n"
                "Select an option:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    elif data == "enable_maint":
        neo_set_setting('maintenance', '1')
        await query.answer("✅ Maintenance mode ENABLED", show_alert=True)
        await neo_admin_panel(update, context)
    
    elif data == "disable_maint":
        neo_set_setting('maintenance', '0')
        await query.answer("✅ Maintenance mode DISABLED", show_alert=True)
        await neo_admin_panel(update, context)
    
    elif data == "admin_channels":
        channels = neo_get_force_channels()
        
        if channels:
            channels_text = "*📢 FORCE CHANNELS:*\n\n"
            for name, link, cid in channels:
                channels_text += f"• *{name}*\n  ID: `{cid}`\n  Link: {link}\n\n"
        else:
            channels_text = "*No force channels set.*"
        
        keyboard = [
            [InlineKeyboardButton("➕ ADD CHANNEL", callback_data="admin_add_channel_panel"),
             InlineKeyboardButton("➖ REMOVE CHANNEL", callback_data="admin_remove_channel")],
            [InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]
        ]
        
        await query.edit_message_text(
            channels_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "admin_add_channel_panel":
        context.user_data['admin_action'] = 'add_channel'
        await query.edit_message_text(
            "🔗 *Add Force Channel*\n\n"
            "Send in format:\n"
            "`channel_id invite_link channel_name`\n\n"
            "*Example:*\n"
            "`-100123456789 https://t.me/+ABC123 My Channel`\n\n"
            "*Type /cancel to cancel*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="admin_channels")]])
        )
    
    elif data == "admin_apis":
        conn = neo_get_db()
        c = conn.cursor()
        apis = c.execute("SELECT api_name, custom_url, enabled FROM api_settings").fetchall()
        conn.close()
        
        apis_text = "*⚙️ API MANAGER*\n\n"
        for api_name, custom_url, enabled in apis:
            status = "✅" if enabled else "❌"
            apis_text += f"{status} *{api_name.upper()}*\n"
            if custom_url:
                apis_text += f"URL: `{custom_url[:50]}...`\n"
            else:
                apis_text += f"URL: Default\n"
            apis_text += f"[Edit](https://t.me/{context.bot.username}?start=editapi_{api_name}) | "
            apis_text += f"[{'Disable' if enabled else 'Enable'}](https://t.me/{context.bot.username}?start=toggleapi_{api_name})\n\n"
        
        keyboard = [
            [InlineKeyboardButton("➕ ADD NEW API", callback_data="admin_add_api")],
            [InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]
        ]
        
        await query.edit_message_text(
            apis_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    
    elif data == "admin_hide":
        conn = neo_get_db()
        c = conn.cursor()
        commands = c.execute("SELECT command, hidden FROM hidden_commands").fetchall()
        conn.close()
        
        commands_text = "*🚫 HIDE/SHOW COMMANDS*\n\n"
        keyboard = []
        row = []
        
        for cmd, hidden in commands:
            status = "✅" if not hidden else "❌"
            btn_text = f"{status} {cmd}"
            callback_data = f"hide_toggle_{cmd}"
            
            row.append(InlineKeyboardButton(btn_text, callback_data=callback_data))
            if len(row) == 2:
                keyboard.append(row)
                row = []
            
            commands_text += f"{status} `/{cmd}` - {'Visible' if not hidden else 'Hidden'}\n"
        
        if row:
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")])
        
        await query.edit_message_text(
            commands_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data.startswith("hide_toggle_"):
        cmd = data.replace("hide_toggle_", "")
        conn = neo_get_db()
        c = conn.cursor()
        
        # Get current status
        current = c.execute("SELECT hidden FROM hidden_commands WHERE command = ?", (cmd,)).fetchone()
        if current:
            new_status = 0 if current[0] == 1 else 1
            c.execute("UPDATE hidden_commands SET hidden = ? WHERE command = ?", (new_status, cmd))
            conn.commit()
        
        conn.close()
        
        await query.answer(f"✅ Command /{cmd} {'hidden' if new_status == 1 else 'shown'}", show_alert=True)
        
        # Refresh the list
        await neo_callback_handler(update, context)
    
    elif data == "admin_stats":
        conn = neo_get_db()
        c = conn.cursor()
        
        # Detailed stats
        user_count = c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 0").fetchone()[0]
        group_count = c.execute("SELECT COUNT(*) FROM groups").fetchone()[0]
        total_searches = c.execute("SELECT SUM(total_searches) FROM users").fetchone()[0] or 0
        today_users = c.execute("SELECT COUNT(*) FROM users WHERE date(last_active) = date('now')").fetchone()[0]
        today_searches = c.execute("SELECT SUM(total_searches) FROM users WHERE date(last_active) = date('now')").fetchone()[0] or 0
        
        # Top users
        top_users = c.execute("SELECT first_name, username, total_searches FROM users WHERE is_banned = 0 ORDER BY total_searches DESC LIMIT 5").fetchall()
        
        conn.close()
        
        stats_text = f"""
📈 *DETAILED STATISTICS*

👥 *USER ANALYTICS:*
• Total Users: `{user_count}`
• Active Today: `{today_users}`
• Total Searches: `{total_searches}`
• Searches Today: `{today_searches}`
• Avg Searches/User: `{total_searches/user_count if user_count>0 else 0:.1f}`

📢 *GROUP ANALYTICS:*
• Total Groups: `{group_count}`

🏆 *TOP 5 USERS (SEARCHES):*
"""
        for i, (name, username, searches) in enumerate(top_users, 1):
            display_name = name or username or f"User {i}"
            stats_text += f"{i}. {display_name}: `{searches}` searches\n"
        
        stats_text += f"\n⚙️ *SYSTEM INFO:*\n• APIs: `{len(NEO_APIS)}` available\n• Force Channels: `{len(neo_get_force_channels())}`\n• Uptime: `{int(time.time() - START_TIME)}s`"
        
        await query.edit_message_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]])
        )
    
    elif data == "admin_pic":
        context.user_data['admin_action'] = 'change_pic'
        await query.edit_message_text(
            "🖼 *Change Owner Photo*\n\n"
            "Send the new photo URL:\n\n"
            "*Requirements:*\n"
            "• Must be direct image URL\n"
            "• Supported formats: JPG, PNG\n"
            "• Will show as spoiler\n\n"
            "*Type /cancel to cancel*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="admin_panel")]])
        )
    
    elif data == "clone_start":
        await neo_clone_start(update, context)
    
    elif data == "clone_paid":
        await query.edit_message_text(
            "✅ *Payment Verified!*\n\n"
            "Please send your Admin ID (numeric):\n\n"
            "*Example:* `8125487901`\n\n"
            "*Note:* This will be the admin of your clone bot.",
            parse_mode="Markdown"
        )
        context.user_data['clone_step'] = 'admin_id'

# ===================== MESSAGE HANDLER =====================
async def neo_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    
    # Handle /cancel
    if text.lower() == "/cancel":
        if 'admin_action' in context.user_data:
            del context.user_data['admin_action']
        if 'clone_step' in context.user_data:
            del context.user_data['clone_step']
        await update.message.reply_text("❌ Action cancelled.")
        return
    
    # Handle clone bot creation
    if 'clone_step' in context.user_data:
        step = context.user_data['clone_step']
        
        if step == 'admin_id':
            try:
                admin_id = int(text)
                context.user_data['clone_admin'] = admin_id
                await update.message.reply_text(
                    "✅ *Admin ID received!*\n\n"
                    "Now send your Bot Token:\n\n"
                    "*Format:* `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`\n"
                    "*Get from:* @BotFather",
                    parse_mode="Markdown"
                )
                context.user_data['clone_step'] = 'token'
            except ValueError:
                await update.message.reply_text("❌ Invalid Admin ID. Send numbers only.")
        
        elif step == 'token':
            token = text.strip()
            admin_id = context.user_data.get('clone_admin')
            
            # Generate clone bot code
            clone_code = f'''# ⚡️ NEO OSINT CLONE BOT
# Generated for Admin ID: {admin_id}
# Developer: {DEVELOPER_TAG}

import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "{token}"
ADMIN_ID = {admin_id}

# APIs
APIS = {json.dumps(NEO_APIS, indent=2)}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🤖 *NEO OSINT CLONE BOT*\\n\\n"
        f"👤 User: {{user.first_name}}\\n"
        f"👑 Admin ID: `{{ADMIN_ID}}`\\n"
        f"🔧 Tools: {{len(APIS)}} available\\n\\n"
        "*Commands:* /num, /phone, /instagram, /github, /ip, /pan, /ifsc, /vehicle, /ff, /email, /help",
        parse_mode="Markdown"
    )

async def tool_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE, api_name: str):
    if not context.args:
        await update.message.reply_text(f"Usage: /{{api_name}} <value>")
        return
    
    query = " ".join(context.args)
    api_url = APIS.get(api_name)
    
    if not api_url:
        await update.message.reply_text("❌ Tool not available.")
        return
    
    msg = await update.message.reply_text("🔍 Searching...")
    
    try:
        url = api_url.format(query)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                result = f"✅ *{{api_name.upper()}} INFO*\\n\\n"
                for key, value in data.items():
                    result += f"• *{{key.replace('_', ' ').title()}}:* `{{value}}`\\n"
                await msg.edit_text(result, parse_mode="Markdown")
            except:
                await msg.edit_text(f"✅ Result:\\n`{{response.text}}`", parse_mode="Markdown")
        else:
            await msg.edit_text("❌ No data found.")
    except Exception as e:
        await msg.edit_text(f"❌ Error: {{e}}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"🤖 *NEO CLONE BOT*\\n\\n"
    help_text += f"👑 Admin: `{{ADMIN_ID}}`\\n"
    help_text += f"🔧 Tools: {{len(APIS)}}\\n\\n"
    help_text += "*Commands:* "
    help_text += ", ".join([f"/{{cmd}}" for cmd in APIS.keys()])
    await update.message.reply_text(help_text, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    
    # Add all tool commands
    for api_name in APIS.keys():
        app.add_handler(CommandHandler(api_name, 
            lambda update, context, api=api_name: tool_cmd(update, context, api)))
    
    print(f"🤖 Clone Bot Started for Admin: {{ADMIN_ID}}")
    app.run_polling()

if __name__ == "__main__":
    main()
'''
            
            # Send as file
            file = BytesIO(clone_code.encode())
            file.name = "neo_clone_bot.py"
            
            await update.message.reply_document(
                document=file,
                caption=f"✅ *Your Clone Bot Code!*\n\n"
                       f"👑 Admin: `{admin_id}`\n"
                       f"🤖 Token: `{token[:10]}...`\n"
                       f"🔧 Tools: {len(NEO_APIS)}\n\n"
                       f"*Instructions:*\n"
                       f"1. Save as `bot.py`\n"
                       f"2. Run: `python bot.py`\n"
                       f"3. Start using your bot!\n\n"
                       f"*Support:* {DEVELOPER_TAG}",
                parse_mode="Markdown"
            )
            
            # Clear clone data
            if 'clone_step' in context.user_data:
                del context.user_data['clone_step']
            if 'clone_admin' in context.user_data:
                del context.user_data['clone_admin']
        
        return
    
    # Handle admin actions
    if 'admin_action' in context.user_data and neo_is_admin(user.id):
        action = context.user_data['admin_action']
        
        if action == 'broadcast':
            context.user_data['broadcast_msg'] = text
            await neo_broadcast(update, context)
            if 'admin_action' in context.user_data:
                del context.user_data['admin_action']
            return
        
        elif action == 'change_maint_msg':
            neo_set_setting('maintenance_msg', text)
            await update.message.reply_text(f"✅ Maintenance message updated!", parse_mode="Markdown")
            if 'admin_action' in context.user_data:
                del context.user_data['admin_action']
            await neo_admin_panel(update, context)
            return
        
        elif action == 'add_channel':
            parts = text.split()
            if len(parts) >= 3:
                channel_id = parts[0]
                invite_link = parts[1]
                channel_name = " ".join(parts[2:])
                
                success = neo_add_force_channel(channel_name, invite_link, channel_id, user.id)
                
                if success:
                    await update.message.reply_text(
                        f"✅ *Channel Added!*\n\n"
                        f"• Name: {channel_name}\n"
                        f"• ID: `{channel_id}`\n"
                        f"• Link: {invite_link}",
                        parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text("❌ Failed to add channel.")
            else:
                await update.message.reply_text("❌ Invalid format. Use: channel_id link name")
            
            if 'admin_action' in context.user_data:
                del context.user_data['admin_action']
            await neo_admin_panel(update, context)
            return
        
        elif action == 'change_pic':
            neo_set_setting('owner_pic', text)
            await update.message.reply_text("✅ Owner photo updated! It will show as spoiler.", parse_mode="Markdown")
            if 'admin_action' in context.user_data:
                del context.user_data['admin_action']
            await neo_admin_panel(update, context)
            return

# ===================== MAIN FUNCTION =====================
START_TIME = time.time()

def main():
    # Initialize database
    neo_init_db()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", neo_start))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("Use /start for menu or click Help button")))
    app.add_handler(CommandHandler("admin", neo_admin_panel))
    app.add_handler(CommandHandler("broadcast", neo_broadcast))
    app.add_handler(CommandHandler("addchannel", neo_add_channel))
    app.add_handler(CommandHandler("addauth", neo_add_auth))
    
    # Add tool command handlers
    app.add_handler(CommandHandler("num", cmd_num))
    app.add_handler(CommandHandler("phone", cmd_phone))
    app.add_handler(CommandHandler("instagram", cmd_instagram))
    app.add_handler(CommandHandler("github", cmd_github))
    app.add_handler(CommandHandler("ip", cmd_ip))
    app.add_handler(CommandHandler("pan", cmd_pan))
    app.add_handler(CommandHandler("ifsc", cmd_ifsc))
    app.add_handler(CommandHandler("vehicle", cmd_vehicle))
    app.add_handler(CommandHandler("ff", cmd_ff))
    app.add_handler(CommandHandler("ffban", cmd_ffban))
    app.add_handler(CommandHandler("email", cmd_email))
    app.add_handler(CommandHandler("aadhaar", cmd_aadhaar))
    app.add_handler(CommandHandler("pincode", cmd_pincode))
    app.add_handler(CommandHandler("global", cmd_global))
    app.add_handler(CommandHandler("pak", cmd_pak))
    app.add_handler(CommandHandler("telegram", cmd_telegram))
    app.add_handler(CommandHandler("fampay", cmd_fampay))
    app.add_handler(CommandHandler("instagram2", cmd_instagram2))
    app.add_handler(CommandHandler("clone", neo_clone_start))
    
    # Add callback handler
    app.add_handler(CallbackQueryHandler(neo_callback_handler))
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, neo_message_handler))
    
    # Start bot
    print("\n" + "="*60)
    print("⚡️ NEO OSINT BOT V5.0 - ULTIMATE WORKING VERSION")
    print(f"👑 Owner: {OWNER_USERNAME}")
    print(f"👨‍💻 Developer: {DEVELOPER_TAG}")
    print(f"🔧 Tools: {len(NEO_APIS)} APIs loaded")
    print(f"🏠 Group: {GROUP_LINK}")
    print("="*60 + "\n")
    
    logger.info("🔥 NEO OSINT BOT STARTED - ALL FEATURES WORKING")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()