from database import db_get

# -------------------------
# RANKING SYSTEM
# -------------------------

def global_ranking(limit=10):
    """
    Returns the global leaderboard (top players by total mined).
    """

    data = db_get("users", f"?select=id,total_mined&order=total_mined.desc&limit={limit}")

    if not data:
        return "🏆 No players yet."

    text = "🏆 *Global Ranking*\n\n"

    for i, user in enumerate(data, start=1):
        text += f"{i}. User {user['id']} — {user['total_mined']} mined\n"

    return text


def weekly_ranking(limit=10):
    """
    Weekly ranking placeholder.
    (You can later add a 'weekly_mined' field in Supabase.)
    """

    # For now, use total_mined as a placeholder
    data = db_get("users", f"?select=id,total_mined&order=total_mined.desc&limit={limit}")

    if not data:
        return "🏅 No weekly data yet."

    text = "🏅 *Weekly Ranking*\n\n"

    for i, user in enumerate(data, start=1):
        text += f"{i}. User {user['id']} — {user['total_mined']} mined\n"

    return text