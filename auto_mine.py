from datetime import datetime, timedelta
from player import Player
from database import update_user
from energy import regenerate_energy
from economy import auto_mine_reward

# -------------------------
# AUTO-MINE SYSTEM
# -------------------------

AUTO_MINE_INTERVAL = 60  # seconds

def process_auto_mine(user_id):
    """
    Processes auto-mine for a single user.
    Called by the global loop.
    """

    player = Player(user_id)

    # If user has no auto-mine, skip
    if player.auto_mine <= 0:
        return

    last_time = datetime.fromisoformat(player.data["last_auto_mine"])
    now = datetime.utcnow()

    elapsed = (now - last_time).total_seconds()

    # Not enough time passed
    if elapsed < AUTO_MINE_INTERVAL:
        return

    # How many ticks passed
    ticks = int(elapsed // AUTO_MINE_INTERVAL)

    # Reward per tick
    reward = auto_mine_reward(player.auto_mine) * ticks

    # Add coins
    player.add_coins(reward)

    # Regenerate energy per tick
    for _ in range(ticks):
        regenerate_energy(user_id)

    # Update last_auto_mine
    update_user(user_id, {"last_auto_mine": now.isoformat()})
    player.data["last_auto_mine"] = now.isoformat()

    return f"🤖 Auto-mined {reward} coins while you were away!"