from datetime import datetime, timedelta
from database import db_get, db_insert, db_update
from player import Player

# -------------------------
# QUEST DEFINITIONS
# -------------------------

DAILY_QUESTS = [
    {"id": "d_mine_50", "desc": "Mine 50 times", "goal": 50, "reward": 100},
    {"id": "d_energy_20", "desc": "Spend 20 energy", "goal": 20, "reward": 80},
    {"id": "d_auto_10", "desc": "Trigger auto-mine 10 times", "goal": 10, "reward": 120},
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

ALL_QUESTS = DAILY_QUESTS + WEEKLY_QUESTS + PROGRESSION_QUESTS


# -------------------------
# HELPERS
# -------------------------

def _find_quest_def(quest_id):
    return next((q for q in ALL_QUESTS if q["id"] == quest_id), None)


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


# -------------------------
# ASSIGNMENT
# -------------------------

def assign_daily_quests(user_id):
    today = datetime.utcnow().date()
    user = db_get("users", f"?id=eq.{user_id}&select=last_daily")

    last_daily = None
    if user and user[0].get("last_daily"):
        last_daily = datetime.fromisoformat(user[0]["last_daily"]).date()

    if last_daily == today:
        return

    db_update("users", f"id=eq.{user_id}", {"last_daily": today.isoformat()})

    for q in DAILY_QUESTS:
        add_quest(user_id, q["id"], "daily")


def assign_weekly_quests(user_id):
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())

    user = db_get("users", f"?id=eq.{user_id}&select=last_weekly")

    last_weekly = None
    if user and user[0].get("last_weekly"):
        last_weekly = datetime.fromisoformat(user[0]["last_weekly"]).date()

    if last_weekly == week_start:
        return

    db_update("users", f"id=eq.{user_id}", {"last_weekly": week_start.isoformat()})

    for q in WEEKLY_QUESTS:
        add_quest(user_id, q["id"], "weekly")


def assign_progression_quests(user_id):
    existing = get_user_quests(user_id)
    existing_ids = [q["quest_id"] for q in existing]

    for q in PROGRESSION_QUESTS:
        if q["id"] not in existing_ids:
            add_quest(user_id, q["id"], "progression")


def ensure_quests_assigned(user_id):
    assign_daily_quests(user_id)
    assign_weekly_quests(user_id)
    assign_progression_quests(user_id)


# -------------------------
# QUEST MENU TEXT
# -------------------------

def quest_menu_text(user_id):
    quests = get_user_quests(user_id)
    if not quests:
        return "No quests available."

    text = "📜 *Your Quests:*\n\n"
    for q in quests:
        qdef = _find_quest_def(q["quest_id"])
        if not qdef:
            continue

        status = "✅ Completed" if q["completed"] else f"{q['progress']}/{qdef['goal']}"
        claimed = "🎁 Claimed" if q["claimed"] else ""
        text += f"• *{qdef['desc']}* — {status} {claimed}\n"

    return text


# -------------------------
# CLAIM QUEST
# -------------------------

def claim_quest(user_id, quest_id):
    quests = get_user_quests(user_id)
    quest = next((q for q in quests if q["quest_id"] == quest_id), None)

    if not quest:
        return "Quest not found."

    if not quest["completed"]:
        return "You haven't completed this quest yet."

    if quest["claimed"]:
        return "You already claimed this reward."

    qdef = _find_quest_def(quest_id)
    if not qdef:
        return "Quest definition missing."

    reward = qdef["reward"]

    user = db_get("users", f"?id=eq.{user_id}")
    if user:
        coins = user[0]["coins"] + reward
        db_update("users", f"id=eq.{user_id}", {"coins": coins})

    db_update("quests", f"id=eq.{quest['id']}", {"claimed": True})

    return f"You claimed {reward} coins!"
