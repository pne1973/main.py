from datetime import datetime, timedelta

# -------------------------
# GENERAL UTILITY FUNCTIONS
# -------------------------

def format_number(n):
    """
    Formats large numbers:
    1500 -> 1.5K
    2000000 -> 2M
    """
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def now():
    """
    Returns current UTC datetime.
    """
    return datetime.utcnow()


def seconds_since(timestamp_iso):
    """
    Returns seconds passed since a given ISO timestamp.
    """
    t = datetime.fromisoformat(timestamp_iso)
    return (datetime.utcnow() - t).total_seconds()


def cooldown_ready(last_time_iso, cooldown_seconds):
    """
    Returns True if cooldown has passed.
    """
    return seconds_since(last_time_iso) >= cooldown_seconds


def time_left(last_time_iso, cooldown_seconds):
    """
    Returns how many seconds remain until cooldown ends.
    """
    elapsed = seconds_since(last_time_iso)
    remaining = cooldown_seconds - elapsed
    return max(0, int(remaining))