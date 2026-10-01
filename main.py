import telebot
import sqlite3
import os
import json
import time
import requests
import gc
import config

BOT_TOKEN = config.BOT_TOKEN
ADMIN_ID = config.ADMIN_ID

COACHING_DATABASE = {
    "exampur": {"name": "🎯 Exampur", "org_code": "expm"},
    "awadh_ojha": {"name": "📝 Awadh Ojha", "org_code": "ojha"},
    "pinnacle": {"name": "🎯 Pinnacle", "org_code": "pinn"},
    "quality_edu": {"name": "🎓 Quality Edu", "org_code": "qedu"},
    "abhinay": {"name": "📘 Abhinay", "org_code": "abny"},
    "toppers_wing": {"name": "🦅 Toppers Wing", "org_code": "twing"},
    "careerwill": {"name": "⚡ Career Will", "org_code": "cwill"},
    "selection_way": {"name": "🎯 SELECTION WAY", "org_code": "sway"},
    "studyiq": {"name": "🧠 Study IQ", "org_code": "stdiq"},
    "dams_delhi": {"name": "⚕️ DAMS DELHI", "org_code": "dams"},
    "khansir": {"name": "🎓 Khan Sir 2", "org_code": "khangs"},
    "future_kul": {"name": "🚀 FUTURE KUL", "org_code": "fkul"},
    "mypathshala": {"name": "🗺️ My Pathshala", "org_code": "mypat"},
    "mind_map": {"name": "🗺️ Mind Map", "org_code": "mmap"},
    "eduteria": {"name": "🎓 Eduteria", "org_code": "edut"},
    "abhyam": {"name": "📖 Abhyam Academy", "org_code": "abhm"},
    "apnacollege": {"name": "💻 Apna College", "org_code": "apna"},
    "kdlive": {"name": "📡 KD Live (VC)", "org_code": "kdlv"},
    "chandra": {"name": "🏛️ Chandra Academy", "org_code": "chan"},
    "tricks_wala": {"name": "🎯 Tricks Wala", "org_code": "twala"},
    "jeetg": {"name": "🔴 Jeet G", "org_code": "jeet"},
    "g_help": {"name": "🌐 G Help", "org_code": "ghelp"},
    "ceramic": {"name": "🔵 Ceramic Academy", "org_code": "cera"},
    "springboard": {"name": "🌱 Spring Board", "org_code": "spng"},
    "avni": {"name": "A Avni Education", "org_code": "avni"},
    "other_coaching": {"name": "📘 Other Coaching", "org_code": "othr"},
    "drishti": {"name": "📷 Drishti IAS", "org_code": "drishti"},
    "vision": {"name": "🌏 Vision IAS", "org_code": "vision"},
    
    "utkarsh": {"name": "🎓 Utkarsh Classes", "org_code": "utk"},
    "pw": {"name": "⚛️ Physics Wallah", "org_code": "pw"},
    "rwa": {"name": "🦁 Rojgar With Ankit", "org_code": "rwa"},
    "testbook": {"name": "📝 Testbook", "org_code": "tstbk"},
    "unacademy": {"name": "🟢 Unacademy", "org_code": "unacd"},
    "vedantu": {"name": "📐 Vedantu", "org_code": "vednt"},
    "byjus": {"name": "🟨 Byjus", "org_code": "byjus"},
    "adda247": {"name": "🔴 Adda247", "org_code": "adda"},
    "nextias": {"name": "🚀 Next IAS", "org_code": "next"},
    "wifistudy": {"name": "📡 Wifistudy", "org_code": "wifi"},
    "toprankers": {"name": "🏆 Toprankers", "org_code": "topr"},
    "allen": {"name": "🎯 Allen Digital", "org_code": "allen"},
    "resonance": {"name": "🌀 Resonance", "org_code": "reso"},
    "aakash": {"name": "🔷 Aakash Digital", "org_code": "aaksh"},
    "fiitjee": {"name": "🔥 FIITJEE", "org_code": "fiit"},
    "competishun": {"name": "🧠 Competishun (MT)", "org_code": "comp"},
    "apni_kaksha": {"name": "🎓 Apni Kaksha", "org_code": "apni"},
    "physics_galaxy": {"name": "🌌 Physics Galaxy", "org_code": "pgax"},
    "neon_classes": {"name": "✨ Neon Classes", "org_code": "neon"},
    "gagan_pratap": {"name": "🔢 Maths By Gagan", "org_code": "gagan"},
    "aditya_ranjan": {"name": "🎯 Rankers Gurukul", "org_code": "rguk"},
    "sriram_ias": {"name": "🏛️ Sriram IAS", "org_code": "srias"},
    "ias_baba": {"name": "🎯 IAS Baba", "org_code": "iasb"},
    "insights_ias": {"name": "💡 Insights IAS", "org_code": "inias"},
    "mrunal": {"name": "📊 Mrunal Patel Eco", "org_code": "mrun"},
    "parcham_classes": {"name": "📚 Parcham Classes", "org_code": "parc"},
    "sleepy_classes": {"name": "💤 Sleepy Classes", "org_code": "slpy"},
    "anuj_jindal": {"name": "💼 Anuj Jindal RBI", "org_code": "anuj"},
    "edutap": {"name": "📈 EduTap", "org_code": "edutp"},
    "oliveboard": {"name": "🟢 Oliveboard", "org_code": "oliv"},
    "practicemock": {"name": "📝 PracticeMock", "org_code": "pmock"},
    "kd_campus": {"name": "📡 KD Campus Neetu", "org_code": "kdcm"},
    "paramount": {"name": "🏛️ Paramount", "org_code": "pmnt"},
    "mathongo": {"name": "🔢 MathonGo", "org_code": "mongo"},
    "motion_kota": {"name": "🌀 Motion Kota", "org_code": "moto"},
    "career_point": {"name": "🎯 Career Point", "org_code": "cpoint"},
    "vibrant_academy": {"name": "⚡ Vibrant Kota", "org_code": "vibr"},
    "nucleus_education": {"name": "🧠 Nucleus Kota", "org_code": "nucl"},
    "toppr": {"name": "🎯 Toppr Learning", "org_code": "toppr"},
    "doubtnut": {"name": "❓ Doubtnut", "org_code": "dbtn"},
    "brainly": {"name": "🧠 Brainly India", "org_code": "brnly"},
    "khan_academy": {"name": "🎓 Khan Academy", "org_code": "khana"},
    "meritnation": {"name": "📈 Meritnation", "org_code": "merit"},
    "cuemath": {"name": "🔢 Cuemath", "org_code": "cue"},
    "magnet_brains": {"name": "🧲 Magnet Brains", "org_code": "mbra"},
    "biomentors": {"name": "🧬 Biomentors Online", "org_code": "biom"},
    "commandoclasses": {"name": "🎖️ Commando Classes", "org_code": "cmdo"},
    "skjha": {"name": "🔬 S.K. Jha Sir", "org_code": "skjha"},
    "nimisha_bansal": {"name": "📚 English By Nimisha", "org_code": "nbans"},
    "tarun_grover": {"name": "📖 Tarun Grover English", "org_code": "tgrov"},
    "ankush_lamba": {"name": "🔢 Banking By Ankush", "org_code": "alamb"},
    "puneet_sir": {"name": "💡 Puneet Sir Reason", "org_code": "psir"},
    "arun_sir": {"name": "🔢 Arun Sir Maths", "org_code": "asir"},
    "vishal_parihar": {"name": "📝 Vishal Parihar", "org_code": "vpari"},
    "studified": {"name": "🧠 Studified Aashish", "org_code": "studf"},
    "success_ease": {"name": "🏆 Success Ease", "org_code": "sease"},
    "dixit_sir": {"name": "🎖️ Dixit Sir (CGL)", "org_code": "dixit"},
    "e1_mathematics": {"name": "🔢 E1 Coaching", "org_code": "e1cc"},
    "rberevolution": {"name": "📊 RBE Shubham Jain", "org_code": "rbe"},
    "made_easy": {"name": "🏛️ Made Easy Prime", "org_code": "measy"},
    "ace_academy": {"name": "🎖️ ACE Engineering", "org_code": "ace"},
    "gate_academy": {"name": "🚀 Gate Academy", "org_code": "gacad"},
}

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

def init_db():
    conn = sqlite3.connect('extractor_master.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sessions (coaching_name TEXT PRIMARY KEY, token TEXT, updated_at TEXT)')
    conn.commit()
    conn.close()

def is_allowed(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "🤖 **√EXTRACTOR-X™ Engine Ready**\n\nUse `/xtract` to run panels.")

@bot.message_handler(commands=['xtract'])
def xtract_panel(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "🔒 Access Denied.")
        return
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_power = telebot.types.InlineKeyboardButton("🔓 POWER MODE (110+ Coaching UI)", callback_data="power_page_0")
    btn_flash = telebot.types.InlineKeyboardButton("⚡ FLASH MODE (30 Coaching Grid)", callback_data="list_coaching")
    markup.add(btn_power, btn_flash)
    bot.send_message(message.chat.id, "🗺️ ─── **【 🚀 MAIN PANEL 】** ───\n\nChoose extraction mode:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    
    if call.data == "list_coaching":
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        flash_keys = [
            "exampur", "awadh_ojha", "pinnacle", "quality_edu",
            "abhinay", "toppers_wing", "careerwill", "selection_way",
            "studyiq", "dams_delhi", "khansir", "future_kul",
            "mypathshala", "mind_map", "eduteria", "abhyam",
            "apnacollege", "kdlive", "chandra", "tricks_wala",
            "jeetg", "g_help", "ceramic", "springboard", "avni", "other_coaching",
        ]
        buttons = [telebot.types.InlineKeyboardButton(COACHING_DATABASE[key]["name"], callback_data=f"flash_{key}") for key in flash_keys if key in COACHING_DATABASE]
        markup.add(*buttons)
        
        btn_back = telebot.types.InlineKeyboardButton("⬅️ Back", callback_data="go_main")
        btn_home = telebot.types.InlineKeyboardButton("🏠 Home", callback_data="go_main")
        markup.row(btn_back, btn_home)
        
        btn_drishti = telebot.types.InlineKeyboardButton(COACHING_DATABASE["drishti"]["name"], callback_data="flash_drishti")
        btn_vision = telebot.types.InlineKeyboardButton(COACHING_DATABASE["vision"]["name"], callback_data="flash_vision")
        markup.row(btn_drishti, btn_vision)
        
        btn_support = telebot.types.InlineKeyboardButton("🧭 Contact Support ↗️", url="https://t.me")
        markup.row(btn_support)
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                result = cursor.fetchone()
        conn.close()
        bot.answer_callback_query(call.id, f"Selected: {coaching_selected}")

if __name__ == "__main__":
    init_db()
    bot.infinity_polling()                      text="💬 **Need access? Contact Admin**\n──────────────────\n⚡ **SELECT COACHING FOR FLASH EXTRACT:**", reply_markup=markup)
    
    elif call.data == "go_main":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn_power = telebot.types.InlineKeyboardButton("🔓 POWER MODE (110+ Coaching UI)", callback_data="power_page_0")
        btn_flash = telebot.types.InlineKeyboardButton("⚡ FLASH MODE (30 Coaching Grid)", callback_data="list_coaching")
        markup.add(btn_power, btn_flash)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🗺️ ─── **【 🚀 MAIN PANEL 】** ───\n\nChoose extraction mode:", reply_markup=markup)

    elif call.data.startswith("flash_"):
        coaching_selected = call.data.replace("flash_", "")
        conn = sqlite3.connect('extractor_master.db')
        cursor = conn.cursor()
        cursor.execute('SELECT token FROM sessions WHERE coaching_name = ?', (coaching_selected,))
if __name__ == "__main__":
    init_db()
    bot.infinity_polling()
