from abc import ABC, abstractmethod
from typing import List
from collections import Counter

from card import Card


class PatternInterface(ABC):

    @staticmethod
    @abstractmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        pass


class RoyalFlush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        if Flush.matches(community_cards, hole_cards) == -1:
            return -1
        cards = {9, 10, 11, 12, 13}
        hand = community_cards + hole_cards
        for card in hand:
            if card.value not in cards:
                return -1
            cards.remove(card.value)
        return 0


class StraightFlush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        if not Flush.matches(community_cards, hole_cards):
            return -1
        return Straight.matches(community_cards, hole_cards)

class FourOfAKind(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        return multiple_matches(community_cards, hole_cards, 4)


class Flush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        cards = community_cards + hole_cards
        cards_suits = [card.suit for card in cards]
        suits_count = Counter(cards_suits)
        for suit, count in suits_count.items():
            if count >= 5:
                # two flushes are compared based on high card in flush
                return max([card.value for card in cards if card.suit == suit])
        return -1


class Straight(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        values = [c.value for c in community_cards + hole_cards]
        if len(values) < 5:
            return -1
        cur = bottom = min(values)
        values.remove(cur)
        for dv in range(1, 5):
            if cur + dv not in values:
                return -1
            values.remove(cur + dv)
        return bottom


class ThreeOfAKind(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        return multiple_matches(community_cards, hole_cards, 3)


class Pair(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        return multiple_matches(community_cards, hole_cards, 2)


class HighCard(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        cards = community_cards + hole_cards
        if len(cards) == 0:
            return -1
        return max([card.value for card in cards])


def multiple_matches(community_cards: List[Card], hole_cards: List[Card], multiple: int) -> int:
    cards = community_cards + hole_cards
    cards_values = [card.value for card in cards]
    cards_count = Counter(cards_values)
    res = -1
    for val, count in cards_count.items():
        if count >= multiple:
            res = val
    return res
