from poker import Card, Suit

from typing import List
from random import randint


class Deck:

    # TODO: make this a hash list if we need to save time
    cards: List[Card]

    def __init__(self, full_decks=0):
        self.cards = list()
        for _ in range(full_decks):
            for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.SPADES, Suit.CLUBS]:
                for value in range(1, 14):
                    self.add_card(Card(suit, value))

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, target: Card):
        target_idx = -1
        for i in range(len(self.cards)):
            if self.cards[i] == target:
                target_idx = i
                break

        if target_idx == -1:
            raise ValueError(f"Deck does not contain card: {target}")
        return self.cards.pop(target_idx)

    def draw_card(self) -> Card:
        draw_idx: int = randint(0, len(self.cards) - 1)
        return self.cards.pop(draw_idx)

    def get_prob_of_card(self, target_card: Card):
        matches = 0
        for card in self.cards:
            matches += int(card == target_card)
        return matches / len(self.cards)

    def get_prob_of_hand(self, hand: List[Card]):
        prob = 1
        removed = list()
        for card in hand:
            card_prob = self.get_prob_of_card(card)
            if card_prob == 0:
                return 0
            prob *= card_prob
            self.remove_card(card)
            removed.append(card)

        for card in removed:
            self.add_card(card)
        return prob

    def __len__(self):
        return len(self.cards)
