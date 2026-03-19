# -------------------------
# ECONOMY / BALANCING SYSTEM
# -------------------------

def coin_reward(click_power):
    """
    Formula for coin reward per click.
    Allows easy balancing later.
    """
    return click_power


def xp_reward():
    """
    XP gained per mining action.
    """
    return 1


def auto_mine_reward(auto_mine_level):
    """
    Coins gained per auto-mine tick.
    """
    return auto_mine_level


def energy_cost():
    """
    Energy spent per mining action.
    """
    return 1


def anti_exploit_limit():
    """
    Maximum actions per minute allowed.
    (Optional: you can implement this later)
    """
    return 120