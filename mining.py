from player import Player
from database import update_user

# -------------------------
# MINING SYSTEM
# -------------------------

def mine_action(user_id):
    """
    Handles the mining action:
    - Checks energy
    - Adds coins
    - Adds XP
    - Updates total mined
    """

    player = Player(user_id)

    # Not enough energy
    if player.energy <= 0:
        return "⚡ You are out of energy! Wait for regeneration."

    # Spend 1 energy
    if not player.use_energy(1):
        return "⚡ Not enough energy."

    # Add coins equal to click power
    player.add_coins(player.click_power)

    # Add XP (1 XP per mine)
    player.add_xp(1)

    # Update total mined
    new_total = player.total_mined + player.click_power
    update_user(user_id, {"total_mined": new_total})
    player.data["total_mined"] = new_total

    return (
        f"⛏️ You mined {player.click_power} coins!\n"
        f"💰 Total: {player.coins}"
    )