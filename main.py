import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from supabase import create_client, Client

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Criar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    result = supabase.table("users").select("*").eq("id", user_id).execute()

    if not result.data:
        supabase.table("users").insert({"id": user_id, "coins": 0}).execute()
        await update.message.reply_text("Conta criada! Bem‑vindo ao Miner Clicker.")
    else:
        await update.message.reply_text("Bem‑vindo de volta ao Miner Clicker.")

# /mine
async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    result = supabase.table("users").select("*").eq("id", user_id).execute()

    if not result.data:
        await update.message.reply_text("Ainda não tens conta. Usa /start primeiro.")
        return

    coins = result.data[0]["coins"] + 1

    supabase.table("users").update({"coins": coins}).eq("id", user_id).execute()

    await update.message.reply_text(f"Minaste 1 moeda! Total: {coins}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mine", mine))
    app.run_polling()

if __name__ == "__main__":
    main()