from player import Player

# -------------------------
# ADVANCED UPGRADE SYSTEM
# -------------------------

def upgrade_cost(base_cost, level, multiplier=1.25):
    """
    Calculates dynamic upgrade cost.
    Example:
        base_cost = 50
        level = current click power
        multiplier = 1.25 (25% increase per level)
    """
    return int(base_cost * (multiplier ** level))


def upgrade_click_power(user_id):
    player = Player(user_id)

    cost = upgrade_cost(50, player.click_power)

    if player.coins < cost:
        return f"❌ Not enough coins. You need {cost}."

    player.add_coins(-cost)
    player.upgrade_click_power(1)

    return (
        f"⛏️ Click Power upgraded!\n"
        f"New Click Power: {player.click_power}\n"
        f"Cost was: {cost} coins"
    )


def upgrade_auto_mine(user_id):
    player = Player(user_id)

    cost = upgrade_cost(200, player.auto_mine)

    if player.coins < cost:
        return f"❌ Not enough coins. You need {cost}."

    player.add_coins(-cost)
    player.upgrade_auto_mine(1)

    return (
        f"🤖 Auto-Mine upgraded!\n"
        f"New Auto-Mine: {player.auto_mine}/min\n"
        f"Cost was: {cost} coins"
    )


def upgrade_energy(user_id):
    player = Player(user_id)

    cost = upgrade_cost(150, player.max_energy // 5)

    if player.coins < cost:
        return f"❌ Not enough coins. You need {cost}."

    player.add_coins(-cost)
    player.upgrade_max_energy(5)

    return (
        f"⚡ Max Energy increased!\n"
        f"New Max Energy: {player.max_energy}\n"
        f"Cost was: {cost} coins"
    )


def upgrades_menu(user_id):
    player = Player(user_id)

    click_cost = upgrade_cost(50, player.click_power)
    auto_cost = upgrade_cost(200, player.auto_mine)
    energy_cost = upgrade_cost(150, player.max_energy // 5)

    return (
        "⚙️ *Upgrades*\n\n"
        f"1️⃣ Upgrade Click Power — {click_cost} coins\n"
        f"2️⃣ Upgrade Auto-Mine — {auto_cost} coins\n"
        f"3️⃣ Upgrade Max Energy — {energy_cost} coins\n"
    )