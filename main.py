import telebot
import threading
import time

from mining import mine_action
from profile import profile_text
from shop import shop_menu, buy_item
from upgrades import upgrades_menu, upgrade_click_power, upgrade_auto_mine, upgrade_energy
from rewards import daily_reward
from inventory import drop_item, show_inventory
from ranking import global_ranking, weekly_ranking
from auto_mine import process_auto_mine
from database import db_get

TOKEN = "AQUI_O_TELEGRAM_TOKEN"
bot = telebot.TeleBot(TOKEN)

# -------------------------
# COMMANDS
# -------------------------

@bot.message_handler(commands=["start"])
def start_cmd(message):
    bot.reply_to(message,
        "👋 Welcome to *Mining Bot*!\n"
        "Use /mine to start mining.\n"
        "Use /profile to see your stats.\n"
        "Use /shop to buy upgrades.\n"
        "Use /upgrades for advanced upgrades.\n"
        "Use /daily for daily rewards.\n"
        "Use /inventory to see your items.\n"
        "Use /ranking to see the leaderboard.",
        parse_mode="Markdown"
    )


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


# -------------------------
# AUTO-MINE LOOP
# -------------------------

def auto_mine_loop():
    while True:
        users = db_get("users", "?select=id")
        for user in users:
            process_auto_mine(user["id"])
        time.sleep(10)  # check every 10 seconds


threading.Thread(target=auto_mine_loop, daemon=True).start()

# -------------------------
# BOT START
# -------------------------

print("Bot is running...")
bot.infinity_polling()