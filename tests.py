import unittest

from card import Card, Suit
from pattern import *


class Tests(unittest.TestCase):

    def test_card_eq(self):
        card1 = Card(Suit.WILD, 1)
        card2 = Card(Suit.SPADES, 1)
        assert card1 == card2

    def test_wild_1(self):
        card1 = Card(Suit.SPADES, 1)
        card2 = Card(Suit.SPADES, -1)
        assert card1 == card2

    def test_wild_2(self):
        card1 = Card(Suit.WILD, -1)
        card2 = Card(Suit.WILD, -1)
        assert card1 == card2

    def test_wild_3(self):
        card1 = Card(Suit.SPADES, -1)
        card2 = Card(Suit.DIAMONDS, 5)
        assert card1 != card2

    def test_flush(self):
        community_cards = [
            Card(Suit.SPADES, 1),
            Card(Suit.SPADES, 2),
            Card(Suit.SPADES, 3),
        ]
        hole_cards = [
            Card(Suit.SPADES, 4),
            Card(Suit.SPADES, 5),
        ]
        assert Flush.matches(community_cards, hole_cards) == 5

    def test_royal_flush(self):
        hand = [
            Card(Suit.DIAMONDS, 9),
            Card(Suit.DIAMONDS, 10),
            Card(Suit.DIAMONDS, 11),
            Card(Suit.DIAMONDS, 12),
            Card(Suit.DIAMONDS, 13),
        ]
        assert RoyalFlush.matches(hand[:3], hand[3:]) == 0

    def test_straight(self):
        hand = [
            Card(Suit.DIAMONDS, 9),
            Card(Suit.SPADES, 10),
            Card(Suit.DIAMONDS, 11),
            Card(Suit.CLUBS, 12),
            Card(Suit.HEART, 13),
        ]
        assert Straight.matches(hand[:3], hand[3:]) == 9

    def test_straight_flush(self):
        hand = [
            Card(Suit.SPADES, 4),
            Card(Suit.SPADES, 5),
            Card(Suit.SPADES, 6),
            Card(Suit.SPADES, 7),
            Card(Suit.SPADES, 8),
        ]
        assert StraightFlush.matches(hand[:3], hand[3:]) == 4


if __name__ == '__main__':
    unittest.main()
