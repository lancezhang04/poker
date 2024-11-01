from abc import ABC, abstractmethod
from typing import List

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


class Flush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        hand = community_cards + hole_cards
        if len(hand) < 5:
            return -1
        suit = hand[0].suit
        card_pattern = Card(suit, -1)
        if not all(map(lambda c: c == card_pattern, hand)):
            return -1
        return max([card.value for card in hand])


class Straight(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        values = [c.value for c in community_cards + hole_cards]
        cur = bottom = min(values)
        values.remove(cur)
        for dv in range(1, 5):
            if cur + dv not in values:
                return -1
            values.remove(cur + dv)
        return bottom


class HighCard(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        cards = community_cards + hole_cards
        if len(cards) == 0:
            return -1
        return max([card.value for card in cards])
