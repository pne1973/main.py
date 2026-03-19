import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json"
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verificar se existe
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS
    )

    if r.json() == []:
        # Criar utilizador
        requests.post(
            f"{SUPABASE_URL}/rest/v1/users",
            headers=HEADERS,
            json={"id": user_id, "coins": 0}
        )
        await update.message.reply_text("Conta criada! Bem‑vindo ao Miner Clicker.")
    else:
        await update.message.reply_text("Bem‑vindo de volta ao Miner Clicker.")

# /mine
async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS
    )

    data = r.json()
    if data == []:
        await update.message.reply_text("Ainda não tens conta. Usa /start primeiro.")
        return

    coins = data[0]["coins"] + 1

    requests.patch(
        f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
        headers=HEADERS,
        json={"coins": coins}
    )

    await update.message.reply_text(f"Minaste 1 moeda! Total: {coins}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mine", mine))
    app.run_polling()

if __name__ == "__main__":
    main()