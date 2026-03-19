import telebot
import requests
import os
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS
    )

    if r.json() == []:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/users",
            headers=HEADERS,
            json={"id": user_id, "coins": 0}
        )
        bot.reply_to(message, "Conta criada! Bem‑vindo ao Miner Clicker.")
    else:
        bot.reply_to(message, "Bem‑vindo de volta ao Miner Clicker.")

@bot.message_handler(commands=['mine'])
def mine(message):
    user_id = message.from_user.id

    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS
    )

    data = r.json()
    if data == []:
        bot.reply_to(message, "Ainda não tens conta. Usa /start primeiro.")
        return

    coins = data[0]["coins"] + 1

    requests.patch(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS,
        json={"coins": coins}
    )

    bot.reply_to(message, f"Minaste 1 moeda! Total: {coins}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=10000)