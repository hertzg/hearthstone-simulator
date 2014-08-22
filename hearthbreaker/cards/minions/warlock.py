from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY, MINION_TYPE
from hearthbreaker.game_objects import MinionCard, Minion, WeaponCard, Weapon
from hearthbreaker.cards.battlecries import deal_one_damage_all_characters, \
    destroy_own_crystal, discard_one, discard_two, flame_imp, pit_lord, put_minion_on_board_from_hand
import copy
from hearthbreaker.powers import JaraxxusPower


class FlameImp(MinionCard):
    def __init__(self):
        super().__init__("Flame Imp", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(3, 2, battlecry=flame_imp)


class PitLord(MinionCard):
    def __init__(self):
        super().__init__("Pit Lord", 4, CHARACTER_CLASS.WARLOCK, CARD_RARITY.EPIC, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(5, 6, battlecry=pit_lord)


class VoidWalker(MinionCard):
    def __init__(self):
        super().__init__("Voidwalker", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.FREE, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(1, 3, taunt=True)


class DreadInfernal(MinionCard):
    def __init__(self):
        super().__init__("Dread Infernal", 6, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(6, 6, battlecry=deal_one_damage_all_characters)


class Felguard(MinionCard):
    def __init__(self):
        super().__init__("Felguard", 3, CHARACTER_CLASS.WARLOCK, CARD_RARITY.RARE, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(3, 5, battlecry=destroy_own_crystal, taunt=True)


class Doomguard(MinionCard):
    def __init__(self):
        super().__init__("Doomguard", 5, CHARACTER_CLASS.WARLOCK, CARD_RARITY.RARE, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(5, 7, battlecry=discard_two, charge=True)


class Succubus(MinionCard):
    def __init__(self):
        super().__init__("Succubus", 2, CHARACTER_CLASS.WARLOCK, CARD_RARITY.FREE, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(4, 3, battlecry=discard_one)


class SummoningPortal(MinionCard):
    def __init__(self):
        super().__init__("Summoning Portal", 4, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON)

    def create_minion(self, player):
        class Filter:
            def __init__(self):
                self.amount = 2
                self.filter = lambda c: isinstance(c, MinionCard)
                self.min = 1

        mana_filter = Filter()
        minion = Minion(0, 4)
        minion.bind_once("silenced", lambda: player.mana_filters.remove(mana_filter))
        player.mana_filters.append(mana_filter)
        return minion


class BloodImp(MinionCard):
    def __init__(self):
        super().__init__("Blood Imp", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON, MINION_TYPE.DEMON)

    def create_minion(self, player):
        def buff_ally_health():
            targets = copy.copy(player.game.current_player.minions)
            targets.remove(minion)
            if len(targets) > 0:
                target = targets[player.game.random(0, len(targets) - 1)]
                target.increase_health(1)

        minion = Minion(0, 1)
        minion.stealth = True
        player.bind("turn_ended", buff_ally_health)
        minion.bind_once("silenced", lambda: player.unbind("turn_ended", buff_ally_health))
        return minion


class LordJaraxxus(MinionCard):
    def __init__(self):
        super().__init__("Lord Jaraxxus", 9, CHARACTER_CLASS.WARLOCK, CARD_RARITY.LEGENDARY, MINION_TYPE.DEMON)

    def create_minion(self, player):
        def summon_jaraxxus(minion):
            class BloodFury(WeaponCard):
                def __init__(self):
                    super().__init__("Blood Fury", 3, CHARACTER_CLASS.LORD_JARAXXUS, CARD_RARITY.SPECIAL)

                def create_weapon(self, player):
                    return Weapon(3, 8)

            minion.remove_from_board()
            player.trigger("minion_played", minion)
            player.hero.health = minion.health
            player.hero.base_health = 15
            player.hero.character_class = CHARACTER_CLASS.LORD_JARAXXUS
            player.hero.power = JaraxxusPower(player.hero)
            blood_fury = BloodFury()
            weapon = blood_fury.create_weapon(player)
            weapon.card = blood_fury
            weapon.player = player
            weapon.game = player.game
            weapon.equip(player)

        return Minion(3, 15, battlecry=summon_jaraxxus)


class VoidTerror(MinionCard):
    def __init__(self):
        super().__init__("Void Terror", 3, CHARACTER_CLASS.WARLOCK, CARD_RARITY.RARE, MINION_TYPE.DEMON)

    def create_minion(self, player):
        def consume_adjacent(m):
            bonus_attack = 0
            bonus_health = 0
            if m.index > 0:
                minion = m.player.minions[m.index - 1]
                bonus_attack += minion.calculate_attack()
                bonus_health += minion.health
                minion.die(None)

            if m.index < len(m.player.minions) - 1:
                minion = m.player.minions[m.index + 1]
                bonus_attack += minion.calculate_attack()
                bonus_health += minion.health
                minion.die(None)

            m.change_attack(bonus_attack)
            m.increase_health(bonus_health)
        return Minion(3, 3, battlecry=consume_adjacent)


class Voidcaller(MinionCard):
    def __init__(self):
        super().__init__("Voidcaller", 4, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(3, 4, deathrattle=put_minion_on_board_from_hand)
