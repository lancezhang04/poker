from enum import Enum
from typing import Dict


class Suit(Enum):

    WILD = -1  # wild suit (used for matching)
    CLUBS = 0  # black, even
    DIAMONDS = 1  # red, odd
    SPADES = 2
    HEART = 3

    @staticmethod
    def get_color(suit: "Suit") -> int:
        if suit.value == -1:
            raise ValueError("Card with wild suit does not have a color")
        return suit.value % 2


class Card:

    suit: Suit
    value: int

    VALUES_TO_NAMES: Dict[int, str] = {
        -1: "?",  # wild value, matches with all
        1: "two", 2: "three", 3: "four", 4: "five", 5: "six",
        6: "seven", 7: "eight", 8: "nine", 9: "ten",
        10: "jack", 11: "queen", 12: "king", 13: "ace"
    }
    NAMES_TO_VALUES: Dict[str, int] = {v: k for k, v in VALUES_TO_NAMES.items()}

    def __init__(self, suit: Suit, value: int):
        assert 1 <= value <= 13 or value == -1
        self.suit = suit
        self.value = value

    def __str__(self):
        return self.VALUES_TO_NAMES[self.value] + " of " + self.suit.name.lower()

    def __eq__(self, other: "Card"):
        assert type(other) == Card
        value_eq = (self.value == other.value) or (self.value == -1 or other.value == -1)
        suit_eq = (self.suit == other.suit) or (self.suit == Suit.WILD or other.suit == Suit.WILD)
        return value_eq and suit_eq

    def __gt__(self, other: "Card"):
        assert type(other) == Card
        return self.value > other.value

    def __hash__(self):
        return str(self).__hash__()
