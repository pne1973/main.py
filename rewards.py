from datetime import datetime, timedelta
from player import Player
from database import update_user, db_get

# -------------------------
# DAILY REWARD SYSTEM
# -------------------------

def get_reward_info(user_id):
    """
    Returns last_claim and streak for the user.
    If fields don't exist yet, initialize them.
    """

    data = db_get("users", f"?id=eq.{user_id}&select=last_claim,streak")

    if not data:
        return None, 0

    row = data[0]

    last_claim = row.get("last_claim")
    streak = row.get("streak", 0)

    return last_claim, streak


def daily_reward(user_id):
    """
    Gives a daily reward with streak bonus.
    """

    player = Player(user_id)
    last_claim, streak = get_reward_info(user_id)

    today = datetime.utcnow().date()

    # First time claiming
    if last_claim is None:
        streak = 1
        reward = 50
        update_user(user_id, {
            "last_claim": today.isoformat(),
            "streak": streak
        })
        player.add_coins(reward)
        return f"🎁 First daily reward! +{reward} coins"

    # Convert last_claim to date
    last_date = datetime.fromisoformat(last_claim).date()

    # Already claimed today
    if last_date == today:
        return "❌ You already claimed your daily reward today."

    # Missed a day → reset streak
    if (today - last_date).days > 1:
        streak = 1
    else:
        streak += 1

    # Reward increases with streak
    reward = 50 + (streak * 10)

    # Update DB
    update_user(user_id, {
        "last_claim": today.isoformat(),
        "streak": streak
    })

    # Give reward
    player.add_coins(reward)

    return (
        f"🎁 Daily reward collected!\n"
        f"🔥 Streak: {streak} days\n"
        f"💰 You received {reward} coins"
    )