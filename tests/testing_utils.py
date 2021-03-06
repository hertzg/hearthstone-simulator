import copy
import collections
import sys
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.game_objects import Deck, Game

if sys.version_info.major is 3:
    if sys.version_info.minor <= 2:
        import mock  # pragma: no cover
    else:
        from unittest import mock  # pragma: no cover

__all__ = ["mock", "StackedDeck", "generate_game_for"]


class StackedDeck(Deck):
    def __init__(self, card_pattern, character_class):
        cards = []
        while len(cards) + len(card_pattern) < 30:
            cards.extend(copy.deepcopy(card_pattern))

        cards.extend(card_pattern[:30 - len(cards)])
        super().__init__(cards, character_class)

    def draw(self, random_func):
        for card_index in range(0, 30):
            if not self.used[card_index]:
                self.used[card_index] = True
                self.left -= 1
                return self.cards[card_index]


def generate_game_for(card1, card2, first_agent_type, second_agent_type):
    if not isinstance(card1, collections.Sequence):
        card_set1 = [card1()]
    else:
        card_set1 = [card() for card in card1]
    class1 = CHARACTER_CLASS.MAGE
    for card in card_set1:
        if card.character_class != CHARACTER_CLASS.ALL:
            class1 = card.character_class
            break

    if not isinstance(card2, collections.Sequence):
        card_set2 = [card2()]
    else:
        card_set2 = [card() for card in card2]

    class2 = CHARACTER_CLASS.MAGE
    for card in card_set2:
        if card.character_class != CHARACTER_CLASS.ALL:
            class2 = card.character_class
            break

    deck1 = StackedDeck(card_set1, class1)
    deck2 = StackedDeck(card_set2, class2)
    game = Game([deck1, deck2], [first_agent_type(), second_agent_type()])
    game.current_player = game.players[1]
    game.other_player = game.players[0]
    game.pre_game()
    return game
