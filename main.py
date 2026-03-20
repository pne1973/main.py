import telebot
import threading
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from mining import mine_action
from profile import profile_text
from shop import shop_menu, buy_item
from upgrades import upgrades_menu, upgrade_click_power, upgrade_auto_mine, upgrade_energy
from rewards import daily_reward
from inventory import drop_item, show_inventory
from ranking import global_ranking, weekly_ranking
from auto_mine import process_auto_mine
from database import db_get
from quests import quest_menu_text, claim_quest

TOKEN = "AQUI_O_TELEGRAM_TOKEN"
bot = telebot.TeleBot(TOKEN)

# -------------------------
# MENUS COM BOTÕES INLINE
# -------------------------

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton("⛏️ Mine", callback_data="mine"),
        InlineKeyboardButton("👤 Profile", callback_data="profile")
    )

    markup.row(
        InlineKeyboardButton("🛒 Shop", callback_data="shop"),
        InlineKeyboardButton("⚙️ Upgrades", callback_data="upgrades")
    )

    markup.row(
        InlineKeyboardButton("🎒 Inventory", callback_data="inventory"),
        InlineKeyboardButton("🎁 Daily", callback_data="daily")
    )

    markup.row(
        InlineKeyboardButton("📜 Quests", callback_data="quests"),
        InlineKeyboardButton("🏆 Ranking", callback_data="ranking")
    )

    bot.send_message(chat_id, "📍 *Main Menu*", reply_markup=markup, parse_mode="Markdown")


def show_shop_menu(chat_id):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton("1️⃣ +1 Click Power (50)", callback_data="buy_1")
    )
    markup.row(
        InlineKeyboardButton("2️⃣ +1 Auto-Mine (200)", callback_data="buy_2")
    )
    markup.row(
        InlineKeyboardButton("3️⃣ +5 Max Energy (150)", callback_data="buy_3")
    )
    markup.row(
        InlineKeyboardButton("⬅️ Back", callback_data="back_menu")
    )

    bot.send_message(chat_id, "🛒 *Shop*", reply_markup=markup, parse_mode="Markdown")


def show_upgrades_menu(chat_id):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton("⛏️ Upgrade Click Power", callback_data="upg_click")
    )
    markup.row(
        InlineKeyboardButton("🤖 Upgrade Auto-Mine", callback_data="upg_auto")
    )
    markup.row(
        InlineKeyboardButton("⚡ Upgrade Max Energy", callback_data="upg_energy")
    )
    markup.row(
        InlineKeyboardButton("⬅️ Back", callback_data="back_menu")
    )

    bot.send_message(chat_id, "⚙️ *Upgrades*", reply_markup=markup, parse_mode="Markdown")


# -------------------------
# COMMANDS
# -------------------------

@bot.message_handler(commands=["start"])
def start_cmd(message):
    bot.reply_to(
        message,
        "👋 Welcome to *Mining Bot*!\n"
        "Use /menu to open the main menu.\n\n"
        "Direct commands:\n"
        "/mine, /profile, /shop, /upgrades, /daily, /inventory, /ranking, /quests",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["menu"])
def menu_cmd(message):
    show_main_menu(message.chat.id)


@bot.message_handler(commands=["mine"])
def mine_cmd(message):
    bot.reply_to(message, mine_action(message.from_user.id))


@bot.message_handler(commands=["profile"])
def profile_cmd(message):
    bot.reply_to(message, profile_text(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["shop"])
def shop_cmd(message):
    bot.reply_to(message, shop_menu(), parse_mode="Markdown")


@bot.message_handler(commands=["buy"])
def buy_cmd(message):
    try:
        item_id = int(message.text.split()[1])
        bot.reply_to(message, buy_item(message.from_user.id, item_id))
    except:
        bot.reply_to(message, "Usage: /buy <item_id>")


@bot.message_handler(commands=["upgrades"])
def upgrades_cmd(message):
    bot.reply_to(message, upgrades_menu(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["upgrade"])
def upgrade_cmd(message):
    try:
        option = int(message.text.split()[1])
        uid = message.from_user.id

        if option == 1:
            bot.reply_to(message, upgrade_click_power(uid))
        elif option == 2:
            bot.reply_to(message, upgrade_auto_mine(uid))
        elif option == 3:
            bot.reply_to(message, upgrade_energy(uid))
        else:
            bot.reply_to(message, "Invalid upgrade option.")
    except:
        bot.reply_to(message, "Usage: /upgrade <1|2|3>")


@bot.message_handler(commands=["daily"])
def daily_cmd(message):
    bot.reply_to(message, daily_reward(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["inventory"])
def inventory_cmd(message):
    bot.reply_to(message, show_inventory(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["drop"])
def drop_cmd(message):
    bot.reply_to(message, drop_item(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["ranking"])
def ranking_cmd(message):
    bot.reply_to(message, global_ranking(), parse_mode="Markdown")


@bot.message_handler(commands=["weekly"])
def weekly_cmd(message):
    bot.reply_to(message, weekly_ranking(), parse_mode="Markdown")


@bot.message_handler(commands=["quests"])
def quests_cmd(message):
    bot.reply_to(message, quest_menu_text(message.from_user.id), parse_mode="Markdown")


@bot.message_handler(commands=["claim"])
def claim_cmd(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Usage: /claim <quest_id>")
        return
    qid = parts[1]
    bot.reply_to(message, claim_quest(message.from_user.id, qid), parse_mode="Markdown")


# -------------------------
# CALLBACK HANDLER
# -------------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    cid = call.message.chat.id

    if call.data == "mine":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, mine_action(uid))

    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, profile_text(uid), parse_mode="Markdown")

    elif call.data == "shop":
        bot.answer_callback_query(call.id)
        show_shop_menu(cid)

    elif call.data == "upgrades":
        bot.answer_callback_query(call.id)
        show_upgrades_menu(cid)

    elif call.data == "inventory":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, show_inventory(uid), parse_mode="Markdown")

    elif call.data == "daily":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, daily_reward(uid), parse_mode="Markdown")

    elif call.data == "ranking":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, global_ranking(), parse_mode="Markdown")

    elif call.data == "quests":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, quest_menu_text(uid), parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        bot.answer_callback_query(call.id)
        item = int(call.data.split("_")[1])
        bot.send_message(cid, buy_item(uid, item))

    elif call.data == "upg_click":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, upgrade_click_power(uid))

    elif call.data == "upg_auto":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, upgrade_auto_mine(uid))

    elif call.data == "upg_energy":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, upgrade_energy(uid))

    elif call.data == "back_menu":
        bot.answer_callback_query(call.id)
        show_main_menu(cid)


# -------------------------
# AUTO-MINE LOOP
# -------------------------

def auto_mine_loop():
    while True:
        users = db_get("users", "?select=id")
        for user in users:
            process_auto_mine(user["id"])
        time.sleep(10)


threading.Thread(target=auto_mine_loop, daemon=True).start()

# -------------------------
# BOT START
# -------------------------

print("Bot is running...")
bot.infinity_polling()