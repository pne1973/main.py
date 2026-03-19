from player import Player
from database import update_user
from datetime import datetime, timedelta

# -------------------------
# ENERGY SYSTEM
# -------------------------

ENERGY_REGEN_INTERVAL = 60  # seconds per +1 energy

def regenerate_energy(user_id):
    """
    Regenerates 1 energy every ENERGY_REGEN_INTERVAL seconds.
    This function is called by the auto-mine loop.
    """

    player = Player(user_id)

    # Already full
    if player.energy >= player.max_energy:
        return

    # Add 1 energy
    new_energy = player.energy + 1
    update_user(user_id, {"energy": new_energy})
    player.data["energy"] = new_energy


def energy_status(user_id):
    """
    Returns a formatted string showing the player's energy.
    """

    player = Player(user_id)
    return f"⚡ Energy: {player.energy}/{player.max_energy}"