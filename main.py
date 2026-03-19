import telebot
import requests
import os
from flask import Flask
import threading

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

# -------------------------
# MENU PRINCIPAL
# -------------------------

def menu_principal(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()

    btn_mine = telebot.types.InlineKeyboardButton("⛏️ Minerar", callback_data="mine")
    btn_shop = telebot.types.InlineKeyboardButton("🛒 Loja", callback_data="shop")
    btn_profile = telebot.types.InlineKeyboardButton("📊 Perfil", callback_data="profile")
    btn_rank = telebot.types.InlineKeyboardButton("🏆 Ranking", callback_data="rank")
    btn_upgrades = telebot.types.InlineKeyboardButton("⚙️ Upgrades", callback_data="upgrades")

    markup.add(btn_mine)
    markup.add(btn_shop)
    markup.add(btn_profile)
    markup.add(btn_rank)
    markup.add(btn_upgrades)

    bot.send_message(chat_id, "⛏️ *Miner Clicker*\nEscolhe uma opção:", parse_mode="Markdown", reply_markup=markup)

# -------------------------
# START
# -------------------------

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

    menu_principal(message.chat.id)

# -------------------------
# CALLBACKS DO MENU
# -------------------------

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "mine":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⛏️ A minerar... envia /mine para ganhar moedas.")

    elif call.data == "shop":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🛒 A loja ainda está em construção.")

    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📊 O teu perfil será mostrado aqui.")

    elif call.data == "rank":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🏆 O ranking será adicionado em breve.")

    elif call.data == "upgrades":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⚙️ Os upgrades estão a caminho!")

# -------------------------
# MINERAR
# -------------------------

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

    bot.reply_to(message, f"⛏️ Minaste 1 moeda! Total: {coins}")

# -------------------------
# THREADS
# -------------------------

def start_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)