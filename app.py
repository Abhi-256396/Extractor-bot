from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running! - Extractor Bot Live"

def run_bot():
    print("Starting Bot...")
    os.system("python -m Extractor")

# Bot ko background me start karo
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
