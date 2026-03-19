import telebot
import requests
import os
from flask import Flask
import threading
import time
from datetime import datetime, timedelta

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

# -------------------------
# DATABASE HELPERS
# -------------------------

def get_user(user_id):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS
    )
    data = r.json()
    return data[0] if data else None

def update_user(user_id, fields):
    requests.patch(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS,
        json=fields
    )

def create_user(user_id):
    user = {
        "id": user_id,
        "coins": 0,
        "gems": 0,
        "click_power": 1,
        "auto_mine": 0,
        "last_auto_mine": datetime.utcnow().isoformat(),
        "energy": 20,
        "max_energy": 20,
        "level": 1,
        "xp": 0,
        "total_mined": 0
    }
    requests.post(
        f"{SUPABASE_URL}/rest/v1/users",
        headers=HEADERS,
        json=user
    )
    return user

# -------------------------
# MAIN MENU
# -------------------------

def main_menu(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton("⛏️ Mine", callback_data="mine"))
    markup.add(telebot.types.InlineKeyboardButton("🛒 Shop", callback_data="shop"))
    markup.add(telebot.types.InlineKeyboardButton("⚙️ Upgrades", callback_data="upgrades"))
    markup.add(telebot.types.InlineKeyboardButton("📊 Profile", callback_data="profile"))
    markup.add(telebot.types.InlineKeyboardButton("🏆 Ranking", callback_data="ranking"))
    markup.add(telebot.types.InlineKeyboardButton("🎁 Rewards", callback_data="rewards"))

    bot.send_message(chat_id, "⛏️ *Miner Clicker*\nChoose an option:", parse_mode="Markdown", reply_markup=markup)

# -------------------------
# START COMMAND
# -------------------------

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user = get_user(user_id)

    if not user:
        create_user(user_id)
        bot.reply_to(message, "Account created! Welcome to Miner Clicker.")
    else:
        bot.reply_to(message, "Welcome back to Miner Clicker!")

    main_menu(message.chat.id)

# -------------------------
# MINING
# -------------------------

@bot.callback_query_handler(func=lambda call: call.data == "mine")
def mine_button(call):
    bot.answer_callback_query(call.id)
    mine(call.message)

@bot.message_handler(commands=['mine'])
def mine(message):
    user_id = message.from_user.id
    user = get_user(user_id)

    if not user:
        bot.reply_to(message, "You don't have an account yet. Use /start first.")
        return

    if user["energy"] <= 0:
        bot.reply_to(message, "⚡ You are out of energy! Wait for regeneration.")
        return

    new_coins = user["coins"] + user["click_power"]
    new_energy = user["energy"] - 1
    new_total = user["total_mined"] + user["click_power"]

    update_user(user_id, {
        "coins": new_coins,
        "energy": new_energy,
        "total_mined": new_total
    })

    bot.reply_to(message, f"⛏️ You mined {user['click_power']} coins!\n💰 Total: {new_coins}")

# -------------------------
# PROFILE
# -------------------------

@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile(call):
    bot.answer_callback_query(call.id)
    user = get_user(call.from_user.id)

    text = (
        f"📊 *Your Profile*\n\n"
        f"💰 Coins: {user['coins']}\n"
        f"💎 Gems: {user['gems']}\n"
        f"⛏️ Click Power: {user['click_power']}\n"
        f"🤖 Auto-Mine: {user['auto_mine']} / min\n"
        f"⚡ Energy: {user['energy']} / {user['max_energy']}\