from poker.pattern import *
from poker.card import Card

from functools import total_ordering


# TODO: implement all other patterns
PATTERNS_ORDER = [
    RoyalFlush, StraightFlush, FourOfAKind,
    Flush, Straight,
    ThreeOfAKind, Pair,
    HighCard,
]


@total_ordering
class Hand:
    community_cards: List[Card]
    hole_cards: List[Card]
    type: int
    order: int

    def __init__(self, community_cards, hole_cards=None):
        self.community_cards = community_cards.copy()
        if hole_cards is None:
            self.hole_cards = list()
        else:
            self.hole_cards = hole_cards
        self._evaluate_hand()

    def _evaluate_hand(self):
        for i, pattern in enumerate(PATTERNS_ORDER):
            match_res = pattern.matches(self.community_cards, self.hole_cards)
            if match_res != -1:
                self.type = i
                self.order = match_res
                break

    def add_hole_card(self, card: Card):
        self.hole_cards.append(card)
        self._evaluate_hand()

    def add_community_card(self, card: Card):
        self.community_cards.append(card)
        self._evaluate_hand()

    def __eq__(self, other: object):
        if not isinstance(other, Hand):
            return False
        return self.type == other.type and self.order == other.order

    def __gt__(self, other: object):
        if not isinstance(other, Hand):
            return False
        if self.type != other.type:
            return self.type < other.type
        return self.order > other.order
