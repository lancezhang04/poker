from pattern import *
from card import Card

from functools import total_ordering


# TODO: implement all other patterns
patterns_order = [
    RoyalFlush, StraightFlush,
    Flush, Straight,
    HighCard,
]


@total_ordering
class Hand:
    community_cards: List[Card]
    hole_cards: List[Card]
    type: int
    order: int

    def __init__(self, community_cards, hole_cards):
        self.community_cards = community_cards
        self.hole_cards = hole_cards

        for i, pattern in enumerate(patterns_order):
            match_res = pattern.matches(self.community_cards, self.hole_cards)
            if match_res != -1:
                self.type = i
                self.order = match_res
                break

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
