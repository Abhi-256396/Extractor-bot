import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

def run_bot():
    os.system("python main.py")

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    p = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=p)
