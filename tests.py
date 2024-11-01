import unittest

from card import Card, Suit


class Tests(unittest.TestCase):

    def test_1(self):
        card1 = Card(Suit.WILD, 1)
        card2 = Card(Suit.SPADES, 1)
        assert card1 == card2

    def test_2(self):
        card1 = Card(Suit.SPADES, 1)
        card2 = Card(Suit.SPADES, -1)
        assert card1 == card2

    def test_3(self):
        card1 = Card(Suit.WILD, -1)
        card2 = Card(Suit.WILD, -1)
        assert card1 == card2

    def test_4(self):
        card1 = Card(Suit.SPADES, -1)
        card2 = Card(Suit.DIAMONDS, 5)
        assert card1 != card2


if __name__ == '__main__':
    unittest.main()
