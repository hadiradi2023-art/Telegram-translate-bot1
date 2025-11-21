import logging, threading, os
from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters
from googletrans import Translator

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
translator = Translator()

def is_farsi(text):
    return any(char in "اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی" for char in text)

def translate_message(update, context):
    text = update.message.text
    try:
        target = 'en' if is_farsi(text) else 'fa'
        result = translator.translate(text, dest=target)
        update.message.reply_text(f"ترجمه به {'انگلیسی' if target == 'en' else 'فارسی'}:\n{result.text}")
    except Exception as e:
        update.message.reply_text("خطا در ترجمه. بعداً دوباره تلاش کن.")

def start_bot():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("توکن تنظیم نشده است.")
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))
    updater.start_polling()
    updater.idle()

app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    keep_alive()
    start_bot()
