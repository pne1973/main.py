from datetime import datetime, timedelta
from database import db_get, db_insert, update_user
from player import Player

# -------------------------
# QUEST DEFINITIONS
# -------------------------

DAILY_QUESTS = [
    {"id": "d_mine_50", "desc": "Mine 50 times", "goal": 50, "reward": 100},
    {"id": "d_energy_20", "desc": "Spend 20 energy", "goal": 20, "reward": 80},
    {"id": "d_auto_10", "desc": "Earn 10 auto-mine ticks", "goal": 10, "reward": 120},
]

WEEKLY_QUESTS = [
    {"id": "w_mine_500", "desc": "Mine 500 times", "goal": 500, "reward": 500},
    {"id": "w_energy_200", "desc": "Spend 200 energy", "goal": 200, "reward": 400},
]

PROGRESSION_QUESTS = [
    {"id": "p_lvl_5", "desc": "Reach level 5", "goal": 5, "reward": 200},
    {"id": "p_lvl_10", "desc": "Reach level 10", "goal": 10, "reward": 500},
    {"id": "p_lvl_20", "desc": "Reach level 20", "goal": 20, "reward": 1000},
]

# -------------------------
# QUEST STORAGE
# -------------------------

def get_user_quests(user_id):
    data = db_get("quests", f"?user_id=eq.{user_id}")
    return data if data else []


def add_quest(user_id, quest_id, quest_type):
    db_insert("quests", {
        "user_id": user_id,
        "quest_id": quest_id,
        "quest_type": quest_type,
        "progress": 0,
        "completed": False,
        "claimed": False,
        "assigned_at": datetime.utcnow().isoformat()
    })


def assign_daily_quests(user_id):
    today = datetime.utcnow().date()

    data = db_get("users", f"?id=eq.{user_id}&select=last_daily")

    last_daily = None
    if data and data[0]["last_daily"]:
        last_daily = datetime.fromisoformat(data[0]["last_daily"]).date()

    if last_daily == today:
        return  # already assigned

    # reset old daily quests
    update_user(user_id, {"last_daily": today.isoformat()})

    # remove old daily quests
    # (optional: keep history)
    # but for simplicity, delete
    # you can implement soft-delete later
    # db_delete("quests", f"?user_id=eq.{user_id}&quest_type=eq.daily")

    for q in DAILY_QUESTS:
        add_quest(user_id, q["id"], "daily")


def assign_weekly_quests(user_id):
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())  # Monday

    data = db_get("users", f"?id=eq.{user_id}&select=last_weekly")

    last_weekly = None
    if data and data[0]["last_weekly"]:
        last_weekly = datetime.fromisoformat(data[0]["last_weekly"]).date()

    if last_weekly == week_start:
        return

    update_user(user_id, {"last_weekly": week_start.isoformat()})

    for q in WEEKLY_QUESTS:
        add_quest(user_id, q["id"], "weekly")


def assign_progression_quests(user_id):
    existing = get_user_quests(user_id)
    existing_ids = [q["quest_id"] for q in existing]

    for q in PROGRESSION_QUESTS:
        if q["id"] not in existing_ids:
            add_quest(user_id, q["id"], "progression")


# -------------------------
# QUEST PROGRESS
# -------------------------

def update_quest_progress(user_id, quest_id, amount):
    quests = get_user_quests(user_id)

    for q in quests:
        if q["quest_id"] == quest_id and not q["completed"]:
            new_progress = q["progress"] + amount

            # find quest definition
            all_quests = DAILY_QUESTS + WEEKLY_QUESTS + PROGRESSION_QUESTS
            quest_def = next((x for x in all_quests if x["id"] == quest_id), None)

            if not quest_def:
                return

            if new_progress >= quest_def["goal"]:
                update_user(user_id, {"quests": None})  # placeholder
                q["progress"] = quest_def["goal"]
                q["completed"] = True
            else:
                q["progress"] = new_progress

            update_user(user_id, {
                "quests": None  # placeholder to trigger sync
            })


# -------------------------
# CLAIM REWARD
# -------------------------

def claim_quest(user_id, quest_id):
    quests = get_user_quests(user_id)

    for q in quests:
        if q["quest_id"] == quest_id:

            if not q["completed"]:
                return "❌ Quest not completed yet."

            if q["claimed"]:
                return "❌ Reward already claimed."

            # find quest definition
            all_quests = DAILY_QUESTS + WEEKLY_QUESTS + PROGRESSION_QUESTS
            quest_def = next((x for x in all_quests if x["id"] == quest_id), None)

            if not quest_def:
                return "❌ Quest not found."

            reward = quest_def["reward"]

            player = Player(user_id)
            player.add_coins(reward)

            q["claimed"] = True

            update_user(user_id, {"quests": None})

            return f"🎉 Quest completed! You received {reward} coins."

    return "❌ Quest not found."


# -------------------------
# QUEST MENU
# -------------------------

def quest_menu_text(user_id):
    assign_daily_quests(user_id)
    assign_weekly_quests(user_id)
    assign_progression_quests(user_id)

    quests = get_user_quests(user_id)

    text = "📜 *Your Quests*\n\n"

    for q in quests:
        # find definition
        all_quests = DAILY_QUESTS + WEEKLY_QUESTS + PROGRESSION_QUESTS
        quest_def = next((x for x in all_quests if x["id"] == q["quest_id"]), None)

        if not quest_def:
            continue

        status = "✅ Completed" if q["completed"] else f"{q['progress']}/{quest_def['goal']}"

        text += f"- *{quest_def['desc']}* ({q['quest_type']})\n"
        text += f"  Progress: {status}\n"
        text += f"  Reward: {quest_def['reward']} coins\n\n"

    return text