from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY
from hearthbreaker.game_objects import WeaponCard, Weapon, Minion


class FieryWarAxe(WeaponCard):
    def __init__(self):
        super().__init__("Fiery War Axe", 2, CHARACTER_CLASS.WARRIOR, CARD_RARITY.FREE)

    def create_weapon(self, player):
        weapon = Weapon(3, 2)
        return weapon


class ArcaniteReaper(WeaponCard):
    def __init__(self):
        super().__init__("Arcanite Reaper", 5, CHARACTER_CLASS.WARRIOR, CARD_RARITY.COMMON)

    def create_weapon(self, player):
        weapon = Weapon(5, 2)
        return weapon


class Gorehowl(WeaponCard):
    def __init__(self):
        super().__init__("Gorehowl", 7, CHARACTER_CLASS.WARRIOR, CARD_RARITY.EPIC)

    def create_weapon(self, player):
        def maybe_increase_durability(target):
            if isinstance(target, Minion):
                weapon.durability += 1
        weapon = Weapon(7, 1)
        player.hero.bind("attack", maybe_increase_durability)
        return weapon
