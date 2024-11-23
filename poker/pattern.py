from abc import ABC, abstractmethod
from typing import List
from collections import Counter

from poker.card import Card


class PatternInterface(ABC):

    @staticmethod
    @abstractmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        pass


class RoyalFlush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        if StraightFlush.matches(community_cards, hole_cards) == 9:
            return 0
        return -1


class StraightFlush(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        cards = community_cards + hole_cards
        for suit in range(4):
            matching_cards = [card for card in cards if card.suit.value == suit]
            if len(matching_cards) < 5:
                continue
            straight_match_res = Straight.matches(matching_cards, list())
            if straight_match_res != -1:
                return straight_match_res
        return -1

class FourOfAKind(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        return multiple_matches(community_cards, hole_cards, 4)


class FullHouse(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        # TODO: test edge case – 2 x three of a kind
        cards = community_cards + hole_cards
        cards_values = [card.value for card in cards]
        cards_count = Counter(cards_values)

        triplets = set()
        pairs = set()
        for val, count in cards_count.items():
            if count >= 3:
                triplets.add(val)
            if count >= 2:
                pairs.add(val)

        if len(triplets) == 0 or len(pairs) < 2:
            return -1

        triplet_val = max(triplets)
        pairs.remove(triplet_val)
        pair_val = max(pairs)
        return triplet_val * 100 + pair_val


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
        # account for ace as bottom card
        if 13 in values:
            values.append(0)

        # remove duplicates and sort values
        values = list(set(values))
        values.sort()
        for bottom in range(len(values) - 5, -1, -1):
            bottom_val = values[bottom]
            made_straight = False
            if values[bottom + 4] != bottom_val + 4:
                continue
            return bottom_val
        return -1


class ThreeOfAKind(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        return multiple_matches(community_cards, hole_cards, 3)


class TwoPairs(PatternInterface):

    @staticmethod
    def matches(community_cards: List[Card], hole_cards: List[Card]) -> int:
        cards = community_cards + hole_cards
        cards_values = [card.value for card in cards]
        cards_count = Counter(cards_values)

        pairs = list()
        for val, count in cards_count.items():
            if count >= 2:
                pairs.append(val)

        if len(pairs) < 2:
            return -1
        pairs.sort(reverse=True)
        return pairs[0] * 100 + pairs[1]


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
