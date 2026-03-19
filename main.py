import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from supabase import create_client, Client

# -----------------------------
# CONFIGURAÇÃO DO SUPABASE
# -----------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FUNÇÕES DO JOGADOR
# -----------------------------
async def get_or_create_player(user):
    telegram_id = user.id
    username = user.username or "Jogador"

    result = supabase.table("players").select("*").eq("telegram_id", telegram_id).execute()

    if result.data:
        return result.data[0]

    new_player = {
        "telegram_id": telegram_id,
        "username": username,
        "coins": 100,
        "energy": 10,
        "power": 1,
        "last_energy_update": datetime.utcnow().isoformat()
    }

    inserted = supabase.table("players").insert(new_player).execute()
    return inserted.data[0]


def update_energy(player):
    """Recarrega energia automaticamente a cada 5 minutos."""
    last = datetime.fromisoformat(player["last_energy_update"])
    now = datetime.utcnow()

    minutes_passed = (now - last).total_seconds() // 300  # 5 minutos

    if minutes_passed > 0:
        recovered = int(minutes_passed)
        new_energy = min(10, player["energy"] + recovered)

        supabase.table("players").update({
            "energy": new_energy,
            "last_energy_update": now.isoformat()
        }).eq("id", player["id"]).execute()

        player["energy"] = new_energy

    return player


# -----------------------------
# COMANDOS DO BOT
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = await get_or_create_player(update.effective_user)
    player = update_energy(player)

    keyboard = [
        [InlineKeyboardButton("⛏️ Minar", callback_data="mine")],
        [InlineKeyboardButton("💰 Vender Recursos", callback_data="sell")],
        [InlineKeyboardButton("⚙️ Upgrades", callback_data="upgrades")]
    ]

    await update.message.reply_text(
        f"Bem-vindo, {player['username']}!\n"
        f"Moedas: {player['coins']}\n"
        f"Energia: {player['energy']}/10",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -----------------------------
# AÇÕES DO JOGO
# -----------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    player = await get_or_create_player(query.from_user)
    player = update_energy(player)

    if query.data == "mine":
        if player["energy"] <= 0:
            await query.edit_message_text("⚠️ Sem energia! Aguarde ou compre mais.")
            return

        earned = player["power"]
        new_energy = player["energy"] - 1
        new_coins = player["coins"] + earned

        supabase.table("players").update({
            "energy": new_energy,
            "coins": new_coins
        }).eq("id", player["id"]).execute()

        await query.edit_message_text(
            f"⛏️ Você minerou e ganhou {earned} moedas!\n"
            f"Moedas: {new_coins}\n"
            f"Energia: {new_energy}/10"
        )

    elif query.data == "sell":
        await query.edit_message_text("💰 Sistema de venda será adicionado em breve.")

    elif query.data == "upgrades":
        await query.edit_message_text("⚙️ Loja de upgrades em construção.")


# -----------------------------
# INICIAR BOT
# -----------------------------
def main():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()