import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# -------------------------
# BASIC REQUEST HELPERS
# -------------------------

def db_get(table, filters=""):
    """GET rows from a table."""
    url = f"{SUPABASE_URL}/rest/v1/{table}{filters}"
    r = requests.get(url, headers=HEADERS)
    return r.json()

def db_insert(table, data):
    """INSERT a new row."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    requests.post(url, headers=HEADERS, json=data)

def db_update(table, filters, data):
    """UPDATE rows matching filters."""
    url = f"{SUPABASE_URL}/rest/v1/{table}{filters}"
    requests.patch(url, headers=HEADERS, json=data)

# -------------------------
# USER HELPERS
# -------------------------

def get_user(user_id):
    """Return user row or None."""
    data = db_get("users", f"?id=eq.{user_id}")
    return data[0] if data else None

def create_user(user_id):
    """Create a new user with default stats."""
    user = {
        "id": user_id,
        "coins": 0,
        "gems": 0,
        "click_power": 1,
        "auto_mine": 0,
        "last_auto_mine": datetime.utcnow().isoformat(),
        "energy": 20,
        "max_energy": 20,
        "level": 1,
        "xp": 0,
        "total_mined": 0
    }
    db_insert("users", user)
    return user

def update_user(user_id, fields):
    """Update user fields."""
    db_update("users", f"?id=eq.{user_id}", fields)