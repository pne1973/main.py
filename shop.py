from player import Player

# -------------------------
# SHOP SYSTEM
# -------------------------

def shop_menu():
    """
    Returns the shop menu text.
    """
    return (
        "🛒 *Shop*\n"
        "Choose an upgrade:\n\n"
        "1️⃣ +1 Click Power — 50 coins\n"
        "2️⃣ +1 Auto-Mine — 200 coins\n"
        "3️⃣ +5 Max Energy — 150 coins\n"
    )


def buy_item(user_id, item_id):
    """
    Handles purchases.
    item_id:
        1 = +1 click power
        2 = +1 auto-mine
        3 = +5 max energy
    """

    player = Player(user_id)

    if item_id == 1:
        cost = 50
        if player.coins < cost:
            return "❌ Not enough coins."
        player.add_coins(-cost)
        player.upgrade_click_power(1)
        return "⛏️ Click Power upgraded!"

    elif item_id == 2:
        cost = 200
        if player.coins < cost:
            return "❌ Not enough coins."
        player.add_coins(-cost)
        player.upgrade_auto_mine(1)
        return "🤖 Auto-Mine upgraded!"

    elif item_id == 3:
        cost = 150
        if player.coins < cost:
            return "❌ Not enough coins."
        player.add_coins(-cost)
        player.upgrade_max_energy(5)
        return "⚡ Max Energy increased!"

    else:
        return "❌ Invalid item."