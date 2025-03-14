import telebot
import sqlite3
import requests

TOKEN = "7717065833:AAExaSLGfyH3DpMQN96aMQN96aSLGfyH3DpMQN96a"
ADSTERRA_API = "6a721fecc1202564cad23ae79f5074ba"

bot = telebot.TeleBot(TOKEN)

# SQLite Database Connection
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        balance REAL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ad_views (
        user_id INTEGER,
        ad_link TEXT,
        PRIMARY KEY (user_id, ad_link)
    )
""")
conn.commit()

# Function to fetch ads from Adsterra API
def get_adsterra_ad():
    url = "https://api3.adsterratop.com/api/v3/6a721fecc1202564cad23ae79f5074ba"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["url"], data[0]["title"]
    except Exception as e:
        print("Error fetching ad:", e)
        return None, None

# /start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    cursor.execute("INSERT OR IGNORE INTO users (id, balance) VALUES (?, 0)", (user_id,))
    conn.commit()
    bot.send_message(user_id, "🤖 Welcome! Earn money by watching ads. Use /watch to get started!", parse_mode="Markdown")

# /watch command to display ads
@bot.message_handler(commands=["watch"])
def send_ad(message):
    user_id = message.chat.id
    ad_url, description = pegar_anuncio_adsterra()
    
    if not ad_url:
        bot.reply_to(message, "No ads available at the moment. Please try again later! ⏳")
        return

    bot.send_message(user_id, f"💰 Earn money by watching ads!\n🔗 [Click here to watch]({ad_url})", parse_mode="Markdown")
    cursor.execute("INSERT OR IGNORE INTO ad_views (user_id, ad_link) VALUES (?, ?)", (user_id, anuncio_url))
    conn.commit()

# Start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    cursor.execute("INSERT OR IGNORE INTO users (id, balance) VALUES (?, 0)")
    conn.commit()
    bot.send_message(user_id, "🤖 Welcome to the AdBot! Earn money by watching ads! Use /watch to get started.", parse_mode="Markdown")

# Command /watch to send an ad
@bot.message_handler(commands=["watch"])
def send_advertisement(message):
    user_id = message.chat.id
    ad_url, description = pegar_anuncio_adsterra()
    
    if not ad_url:
        bot.reply_to(message, "Currently, no ads are available. Please check back later! ⏳")
        return
    
    bot.send_message(user_id, f"💰 Earn money by watching ads! [Click here to watch]({ad_url})", parse_mode="Markdown")
    cursor.execute("INSERT OR IGNORE INTO views (user_id, ad_link) VALUES (?, ?)", (user_id, ad_url))
    conn.commit()

# Run the bot
bot.polling()
