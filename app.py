import os
from flask import Flask
import threading
from Extractor import main as bot_main

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

def run_bot():
    bot_main()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
