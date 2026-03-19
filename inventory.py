import random
from player import Player
from database import db_get, db_insert

# -------------------------
# ITEM DROP SYSTEM
# -------------------------

RARITIES = {
    "common": 70,     # 70%
    "uncommon": 20,   # 20%
    "rare": 8,        # 8%
    "epic": 2         # 2%
}

ITEM_POOL = {
    "common": ["Stone", "Copper Nugget", "Old Gear"],
    "uncommon": ["Iron Chunk", "Silver Shard", "Sturdy Cog"],
    "rare": ["Gold Fragment", "Ruby Chip", "Ancient Relic"],
    "epic": ["Diamond Core", "Mythic Ore", "Quantum Shard"]
}

def choose_rarity():
    roll = random.randint(1, 100)
    cumulative = 0

    for rarity, chance in RARITIES.items():
        cumulative += chance
        if roll <= cumulative:
            return rarity

    return "common"


def generate_item():
    rarity = choose_rarity()
    item = random.choice(ITEM_POOL[rarity])
    return item, rarity


# -------------------------
# INVENTORY SYSTEM
# -------------------------

def add_item(user_id, item_name, rarity):
    """
    Adds an item to the user's inventory table.
    """

    db_insert("inventory", {
        "user_id": user_id,
        "item": item_name,
        "rarity": rarity
    })


def drop_item(user_id):
    """
    Generates a random item and adds it to the inventory.
    """

    item, rarity = generate_item()
    add_item(user_id, item, rarity)

    return f"🎁 You found a *{rarity.upper()}* item: {item}!"


def show_inventory(user_id):
    """
    Returns a formatted inventory list.
    """

    data = db_get("inventory", f"?user_id=eq.{user_id}")

    if not data:
        return "🎒 Your inventory is empty."

    text = "🎒 *Your Inventory*\n\n"

    for entry in data:
        text += f"- {entry['item']} ({entry['rarity']})\n"

    return text