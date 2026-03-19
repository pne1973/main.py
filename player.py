from datetime import datetime
from database import get_user, update_user, create_user

class Player:
    def __init__(self, user_id):
        self.id = user_id
        data = get_user(user_id)

        if not data:
            data = create_user(user_id)

        self.data = data

    # -------------------------
    # BASIC GETTERS
    # -------------------------

    @property
    def coins(self):
        return self.data["coins"]

    @property
    def gems(self):
        return self.data["gems"]

    @property
    def click_power(self):
        return self.data["click_power"]

    @property
    def auto_mine(self):
        return self.data["auto_mine"]

    @property
    def energy(self):
        return self.data["energy"]

    @property
    def max_energy(self):
        return self.data["max_energy"]

    @property
    def level(self):
        return self.data["level"]

    @property
    def xp(self):
        return self.data["xp"]

    @property
    def total_mined(self):
        return self.data["total_mined"]

    # -------------------------
    # XP / LEVEL SYSTEM
    # -------------------------

    def add_xp(self, amount):
        new_xp = self.xp + amount
        new_level = self.level

        # Level up every 100 XP
        while new_xp >= 100:
            new_xp -= 100
            new_level += 1

        update_user(self.id, {
            "xp": new_xp,
            "level": new_level
        })

        self.data["xp"] = new_xp
        self.data["level"] = new_level

    # -------------------------
    # COINS / GEMS
    # -------------------------

    def add_coins(self, amount):
        new_value = self.coins + amount
        update_user(self.id, {"coins": new_value})
        self.data["coins"] = new_value

    def add_gems(self, amount):
        new_value = self.gems + amount
        update_user(self.id, {"gems": new_value})
        self.data["gems"] = new_value

    # -------------------------
    # ENERGY
    # -------------------------

    def use_energy(self, amount):
        if self.energy < amount:
            return False

        new_energy = self.energy - amount
        update_user(self.id, {"energy": new_energy})
        self.data["energy"] = new_energy
        return True

    def restore_energy(self, amount):
        new_energy = min(self.energy + amount, self.max_energy)
        update_user(self.id, {"energy": new_energy})
        self.data["energy"] = new_energy

    # -------------------------
    # UPGRADES
    # -------------------------

    def upgrade_click_power(self, amount):
        new_value = self.click_power + amount
        update_user(self.id, {"click_power": new_value})
        self.data["click_power"] = new_value

    def upgrade_auto_mine(self, amount):
        new_value = self.auto_mine + amount
        update_user(self.id, {"auto_mine": new_value})
        self.data["auto_mine"] = new_value

    def upgrade_max_energy(self, amount):
        new_value = self.max_energy + amount
        update_user(self.id, {
            "max_energy": new_value,
            "energy": new_value
        })
        self.data["max_energy"] = new_value
        self.data["energy"] = new_value