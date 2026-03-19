from player import Player

# -------------------------
# PROFILE SYSTEM
# -------------------------

def profile_text(user_id):
    """
    Returns a formatted profile for the player.
    """

    player = Player(user_id)

    return (
        "👤 *Your Profile*\n\n"
        f"💰 Coins: {player.coins}\n"
        f"💎 Gems: {player.gems}\n"
        f"⛏️ Click Power: {player.click_power}\n"
        f"🤖 Auto-Mine: {player.auto_mine}/min\n"
        f"⚡ Energy: {player.energy}/{player.max_energy}\n"
        f"⭐ Level: {player.level}\n"
        f"📈 XP: {player.xp}/100\n"
        f"🪨 Total Mined: {player.total_mined}\n"
    )