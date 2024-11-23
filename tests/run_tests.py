import unittest

from poker.pattern import *
from poker.card import Card, Suit
from poker.hand import Hand, PATTERNS_ORDER


class Tests(unittest.TestCase):

    def test_card_eq(self):
        card1 = Card(1, Suit.WILD)
        card2 = Card(1, Suit.SPADES)
        assert card1 == card2

    def test_wild_1(self):
        card1 = Card(1, Suit.SPADES)
        card2 = Card(-1, Suit.SPADES)
        assert card1 == card2

    def test_wild_2(self):
        card1 = Card(-1, Suit.WILD)
        card2 = Card(-1, Suit.WILD)
        assert card1 == card2

    def test_wild_3(self):
        card1 = Card(-1, Suit.SPADES)
        card2 = Card(5, Suit.DIAMONDS)
        assert card1 != card2

    def test_two_pairs(self):
        community_cards = [
            Card(1, Suit.DIAMONDS),
            Card(2, Suit.SPADES),
            Card(3, Suit.CLUBS),
        ]
        hole_cards = [
            Card(1, Suit.SPADES),
            Card(3, Suit.SPADES),
        ]
        assert TwoPairs.matches(community_cards, hole_cards) == 301

    def test_full_house_1(self):
        community_cards = [
            Card(11, Suit.DIAMONDS),
            Card(2, Suit.SPADES),
            Card(3, Suit.CLUBS),
            Card(3, Suit.DIAMONDS),
            Card(9, Suit.CLUBS),
        ]
        hole_cards = [
            Card(11, Suit.SPADES),
            Card(3, Suit.SPADES),
        ]
        assert FullHouse.matches(community_cards, hole_cards) == 311

    def test_full_house_2(self):
        community_cards = [
            Card(13, Suit.DIAMONDS),
            Card(13, Suit.SPADES),
            Card(13, Suit.CLUBS),
            Card(9, Suit.DIAMONDS),
            Card(9, Suit.CLUBS),
        ]
        hole_cards = [
            Card(9, Suit.SPADES),
            Card(13, Suit.HEARTS),
        ]
        assert FullHouse.matches(community_cards, hole_cards) == 1309

    def test_flush(self):
        community_cards = [
            Card(1, Suit.SPADES),
            Card(2, Suit.SPADES),
            Card(3, Suit.SPADES),
        ]
        hole_cards = [
            Card(4, Suit.SPADES),
            Card(5, Suit.SPADES),
        ]
        assert Flush.matches(community_cards, hole_cards) == 5

    def test_royal_flush_1(self):
        hand = [
            Card(9, Suit.DIAMONDS),
            Card(10, Suit.DIAMONDS),
            Card(11, Suit.DIAMONDS),
            Card(12, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS),
        ]
        assert RoyalFlush.matches(hand[:3], hand[3:]) == 0

    def test_royal_flush_2(self):
        hand = [
            Card(9, Suit.DIAMONDS),
            Card(10, Suit.DIAMONDS),
            Card(11, Suit.DIAMONDS),
            Card(12, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS),
            Card(8, Suit.DIAMONDS)
        ]
        assert RoyalFlush.matches(hand[:3], hand[3:]) == 0

    def test_royal_flush_3(self):
        hand = [
            Card(9, Suit.DIAMONDS),
            Card(10, Suit.DIAMONDS),
            Card(11, Suit.CLUBS),
            Card(12, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS),
            Card(8, Suit.DIAMONDS)
        ]
        assert RoyalFlush.matches(hand[:3], hand[3:]) == -1

    def test_straight_1(self):
        hand = [
            Card(9, Suit.DIAMONDS),
            Card(10, Suit.SPADES),
            Card(11, Suit.DIAMONDS),
            Card(12, Suit.CLUBS),
            Card(13, Suit.HEARTS),
        ]
        assert Straight.matches(hand[:3], hand[3:]) == 9

    def test_straight_2(self):
        community_cards = [
            Card(9, Suit.DIAMONDS),
            Card(10, Suit.SPADES),
            Card(11, Suit.DIAMONDS),
            Card(12, Suit.CLUBS),
            Card(13, Suit.HEARTS),
        ]
        hole_cards = [
            Card(7, Suit.SPADES),
            Card(8, Suit.CLUBS),
        ]
        assert Straight.matches(community_cards, hole_cards) == 9

    def test_straight_3(self):
        community_cards = [
            Card(13, Suit.DIAMONDS),
            Card(3, Suit.SPADES),
            Card(3, Suit.DIAMONDS),
            Card(2, Suit.CLUBS),
            Card(9, Suit.HEARTS),
        ]
        hole_cards = [
            Card(1, Suit.SPADES),
            Card(4, Suit.CLUBS),
        ]
        assert Straight.matches(community_cards, hole_cards) == 0

    def test_straight_flush_1(self):
        hand = [
            Card(4, Suit.SPADES),
            Card(5, Suit.SPADES),
            Card(6, Suit.SPADES),
            Card(7, Suit.SPADES),
            Card(8, Suit.SPADES),
        ]
        assert StraightFlush.matches(hand[:3], hand[3:]) == 4

    def test_straight_flush_2(self):
        hand = [
            Card(4, Suit.SPADES),
            Card(5, Suit.CLUBS),
            Card(6, Suit.SPADES),
            Card(7, Suit.SPADES),
            Card(8, Suit.SPADES),
            Card(2, Suit.SPADES)
        ]
        assert StraightFlush.matches(hand[:3], hand[3:]) == -1

    def test_hand_compare_1(self):
        hand1 = Hand([Card(1, Suit.SPADES)], [])
        hand2 = Hand([Card(2, Suit.SPADES)], [])
        assert hand2 > hand1

    def test_hand_compare_2(self):
        hand1 = Hand([Card(4, Suit.SPADES)], [Card(5, Suit.SPADES)])
        hand2 = Hand([Card(5, Suit.SPADES)], [])
        assert hand2 == hand1

    def test_hand_compare_3(self):
        community_cards = [
            Card(3, Suit.SPADES),
            Card(4, Suit.CLUBS),
            Card(5, Suit.DIAMONDS),
        ]
        hole_cards1 = [
            Card(1, Suit.SPADES),
            Card(2, Suit.HEARTS),
        ]
        hole_cards2 = [
            Card(6, Suit.SPADES),
            Card(7, Suit.CLUBS),
        ]
        hand1 = Hand(community_cards, hole_cards1)
        assert hand1.order == 1
        hand2 = Hand(community_cards, hole_cards2)
        assert hand2.order == 3
        assert hand1 < hand2

    def test_hand_compare_4(self):
        community_cards = [
            Card(9, Suit.SPADES),
            Card(10, Suit.SPADES),
            Card(11, Suit.SPADES),
        ]
        hole_cards1 = [
            Card(12, Suit.SPADES),
            Card(13, Suit.SPADES),
        ]
        hole_cards2 = [
            Card(7, Suit.SPADES),
            Card(8, Suit.CLUBS),
        ]
        hand1 = Hand(community_cards, hole_cards1)
        assert hand1.order == 0
        hand2 = Hand(community_cards, hole_cards2)
        assert hand2.order == 7
        assert hand1 > hand2

    def test_hand_match_1(self):
        community_cards = [
            Card(9, Suit.SPADES),
            Card(9, Suit.DIAMONDS),
            Card(9, Suit.CLUBS),
            Card(8, Suit.HEARTS),
        ]
        hole_cards = [
            Card(9, Suit.HEARTS),
            Card(2, Suit.HEARTS),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == FourOfAKind
        assert hand.order == 9

    def test_hand_match_2(self):
        community_cards = [
            Card(7, Suit.HEARTS),
            Card(8, Suit.HEARTS),
            Card(9, Suit.HEARTS),
        ]
        hole_cards = [
            Card(10, Suit.HEARTS),
            Card(11, Suit.HEARTS),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == StraightFlush
        assert hand.order == 7

    def test_hand_match_3(self):
        community_cards = [
            Card(4, Suit.SPADES),
            Card(6, Suit.SPADES),
            Card(9, Suit.SPADES),
            Card(2, Suit.HEARTS),
        ]
        hole_cards = [
            Card(10, Suit.SPADES),
            Card(12, Suit.SPADES),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == Flush
        assert hand.order == 12

    def test_hand_match_4(self):
        community_cards = [
            Card(5, Suit.CLUBS),
            Card(5, Suit.DIAMONDS),
            Card(7, Suit.HEARTS),
            Card(9, Suit.SPADES),
            Card(2, Suit.HEARTS),
        ]
        hole_cards = [
            Card(5, Suit.HEARTS),
            Card(6, Suit.CLUBS),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == ThreeOfAKind
        assert hand.order == 5

    def test_hand_match_5(self):
        community_cards = [
            Card(1, Suit.SPADES),
            Card(4, Suit.HEARTS),
            Card(8, Suit.DIAMONDS),
        ]
        hole_cards = [
            Card(6, Suit.CLUBS),
            Card(13, Suit.HEARTS),
        ]
        hand = Hand(community_cards, hole_cards)
        assert PATTERNS_ORDER[hand.type] == HighCard
        assert hand.order == 13


if __name__ == '__main__':
    unittest.main()
