import unittest

from pattern import *
from card import Card, Suit
from hand import Hand, PATTERNS_ORDER


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

    def test_hand_compare_1(self):
        hand1 = Hand([Card(Suit.SPADES, 1)], [])
        hand2 = Hand([Card(Suit.SPADES, 2)], [])
        assert hand2 > hand1

    def test_hand_compare_2(self):
        hand1 = Hand([Card(Suit.SPADES, 4)], [Card(Suit.SPADES, 5)])
        hand2 = Hand([Card(Suit.SPADES, 5)], [])
        assert hand2 == hand1

    def test_hand_compare_3(self):
        community_cards = [
            Card(Suit.SPADES, 3),
            Card(Suit.CLUBS, 4),
            Card(Suit.DIAMONDS, 5),
        ]
        hole_cards1 = [
            Card(Suit.SPADES, 1),
            Card(Suit.HEART, 2),
        ]
        hole_cards2 = [
            Card(Suit.SPADES, 6),
            Card(Suit.CLUBS, 7),
        ]
        hand1 = Hand(community_cards, hole_cards1)
        assert hand1.order == 1
        hand2 = Hand(community_cards, hole_cards2)
        assert hand2.order == 3
        assert hand1 < hand2

    def test_hand_compare_4(self):
        community_cards = [
            Card(Suit.SPADES, 9),
            Card(Suit.SPADES, 10),
            Card(Suit.SPADES, 11),
        ]
        hole_cards1 = [
            Card(Suit.SPADES, 12),
            Card(Suit.SPADES, 13),
        ]
        hole_cards2 = [
            Card(Suit.SPADES, 7),
            Card(Suit.CLUBS, 8),
        ]
        hand1 = Hand(community_cards, hole_cards1)
        assert hand1.order == 0
        hand2 = Hand(community_cards, hole_cards2)
        assert hand2.order == 7
        assert hand1 > hand2

    def test_hand_match_1(self):
        community_cards = [
            Card(Suit.SPADES, 9),
            Card(Suit.DIAMONDS, 9),
            Card(Suit.CLUBS, 9),
            Card(Suit.HEART, 8),
        ]
        hole_cards = [
            Card(Suit.HEART, 9),
            Card(Suit.HEART, 2),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == FourOfAKind
        assert hand.order == 9

    def test_hand_match_2(self):
        community_cards = [
            Card(Suit.HEART, 7),
            Card(Suit.HEART, 8),
            Card(Suit.HEART, 9),
        ]
        hole_cards = [
            Card(Suit.HEART, 10),
            Card(Suit.HEART, 11),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == StraightFlush
        assert hand.order == 7

    def test_hand_match_3(self):
        community_cards = [
            Card(Suit.SPADES, 4),
            Card(Suit.SPADES, 6),
            Card(Suit.SPADES, 9),
            Card(Suit.HEART, 2),
        ]
        hole_cards = [
            Card(Suit.SPADES, 10),
            Card(Suit.SPADES, 12),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == Flush
        assert hand.order == 12

    def test_hand_match_4(self):
        community_cards = [
            Card(Suit.CLUBS, 5),
            Card(Suit.DIAMONDS, 5),
            Card(Suit.HEART, 7),
            Card(Suit.SPADES, 9),
            Card(Suit.HEART, 2),
        ]
        hole_cards = [
            Card(Suit.HEART, 5),
            Card(Suit.CLUBS, 6),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == ThreeOfAKind
        assert hand.order == 5

    def test_hand_match_5(self):
        community_cards = [
            Card(Suit.SPADES, 1),
            Card(Suit.HEART, 4),
            Card(Suit.DIAMONDS, 8),
        ]
        hole_cards = [
            Card(Suit.CLUBS, 6),
            Card(Suit.HEART, 13),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == HighCard
        assert hand.order == 13


if __name__ == '__main__':
    unittest.main()
