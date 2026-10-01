import telebot
import sqlite3
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

COACHINGS = {
    "wifistudy": {"name": "📚 Wifistudy"},
    "toprankers": {"name": "🏆 Toprankers"},
    "allen": {"name": "🎯 Allen Digital"},
    "resonance": {"name": "🌀 Resonance"},
    "aakash": {"name": "🔷 Aakash Digital"},
    "fiitjee": {"name": "🔥 FIITJEE"},
    "competishun": {"name": "🧠 Competishun"},
    "apni_kaksha": {"name": "🎓 Apni Kaksha"},
    "physics_galaxy": {"name": "🌌 Physics Galaxy"},
    "neon_classes": {"name": "✨ Neon Classes"},
    "gagan_pratap": {"name": "📊 Maths by Gagan Pratap"},
    "cuemath": {"name": "🧮 Cuemath"},
    "magnet_brains": {"name": "🧲 Magnet Brains"},
    "biomentors": {"name": "🧬 Biomentors"},
    "skjha": {"name": "👨‍🏫 S.K. Jha Sir"},
    "ankush_lamba": {"name": "🏦 Ankush Lamba"},
    "puneet_sir": {"name": "💡 Puneet Sir"},
    "arun_sir": {"name": "🔢 Arun Sir"},
    "vishal_parihar": {"name": "📝 Vishal Parihar"},
    "studified": {"name": "🧠 Studified"},
    "success_ease": {"name": "🏆 Success Ease"},
    "made_easy": {"name": "🏛️ Made Easy"},
    "ace_academy": {"name": "⭐ ACE Academy"},
    "gate_academy": {"name": "🚀 Gate Academy"},
}

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

def init_db():
    conn = sqlite3.connect('extractor.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS extracted_data (id INTEGER PRIMARY KEY, coaching TEXT, data TEXT)')
    conn.commit()
    conn.close()

def is_allowed(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "🤖 **√EXTRACTOR BOT**\n\nWelcome! Use /xtract to start.")

@bot.message_handler(commands=['xtract'])
def xtract_panel(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "🔒 Access Denied!")
        return
    markup = telebot.types.InlineKeyboardMarkup()
    btn_power = telebot.types.InlineKeyboardButton("⚡ Power", callback_data="list_coaching")
    btn_flash = telebot.types.InlineKeyboardButton("⚡ Flash", callback_data="go_main")
    markup.add(btn_power, btn_flash)
    bot.send_message(message.chat.id, "**√EXTRACTOR PANEL**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id

    if call.data == "list_coaching":
        markup = telebot.types.InlineKeyboardMarkup()
        flash_keys = ["exampur", "awadh_ojha", "abhinay", "studyiq", "apnacollege", "wifistudy"]
        buttons = []
        for key in flash_keys:
            if key in COACHINGS:
                buttons.append(telebot.types.InlineKeyboardButton(COACHINGS[key]["name"], callback_data=f"flash_{key}"))
        markup.add(*buttons)

        btn_back = telebot.types.InlineKeyboardButton("⬅️ Back", callback_data="go_main")
        btn_home = telebot.types.InlineKeyboardButton("🏠 Home", callback_data="go_main")
        markup.row(btn_back, btn_home)

        btn_support = telebot.types.InlineKeyboardButton("🆘 Support", callback_data="go_main")
        markup.row(btn_support)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="**Select Coaching:**", reply_markup=markup)

    elif call.data == "go_main":
        markup = telebot.types.InlineKeyboardMarkup()
        btn_power = telebot.types.InlineKeyboardButton("⚡ Power", callback_data="list_coaching")
        btn_flash = telebot.types.InlineKeyboardButton("⚡ Flash", callback_data="list_coaching")
        markup.add(btn_power, btn_flash)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="**√EXTRACTOR PANEL**", reply_markup=markup)

    elif call.data.startswith("flash_"):
        coaching_selected = call.data.replace("flash_", "")
        conn = sqlite3.connect('extractor.db')
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM extracted_data WHERE coaching=?", (coaching_selected,))
        result = cursor.fetchone()
        conn.close()
        if result:
            bot.send_message(chat_id, f"Data for {coaching_selected}: {result[0]}")
        else:
            bot.send_message(chat_id, f"🔍 Extracting for {coaching_selected}...")

if __name__ == "__main__":
    init_db()
    print("Bot Started...")
    bot.infinity_polling()
