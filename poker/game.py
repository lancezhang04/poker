from math import trunc

from poker.card import Card
from poker.hand import Hand
from poker.deck import Deck

from typing import List


class Game:

    deck: Deck
    community_cards: List[Card]
    # TODO: create player object
    player_hands: List[Hand]
    verbose: bool

    def __init__(self, num_players=2, full_decks=1, verbose=False):
        self.full_decks = full_decks
        self.deck = Deck(full_decks=full_decks)
        self.community_cards = list()
        self.player_hands = list()
        self.num_players = num_players
        self.verbose = verbose

    def deal_starting_cards(self):
        for _ in range(self.num_players):
            self.player_hands.append(Hand(self.community_cards))
            for _ in range(2):
                self.player_hands[-1].add_hole_card(self.deck.draw_card())

        if self.verbose:
            for i, hand in enumerate(self.player_hands):
                print(f"Hand of player {i}: {hand.hole_cards[0]}, {hand.hole_cards[1]}")
            print()

    def flop(self) -> List[Card]:
        if len(self.community_cards) != 0:
            raise RuntimeError("Current round has already flopped")
        for _ in range(3):
            card = self.deck.draw_card()
            self.community_cards.append(card)
            self.player_hands[0].add_community_card(card)
            self.player_hands[1].add_community_card(card)

        if self.verbose:
            for i, card in enumerate(self.community_cards):
                print(f"Card {i}: {card}")
            print()
        return self.community_cards

    def deal_card(self, card_idx: int):
        if len(self.community_cards) != card_idx:
            raise RuntimeError
        card = self.deck.draw_card()
        self.community_cards.append(card)
        self.player_hands[0].add_community_card(card)
        self.player_hands[1].add_community_card(card)

        if self.verbose:
            print(f"Card {card_idx}: {self.community_cards[-1]}\n")
        return self.community_cards

    def turn(self) -> List[Card]:
        return self.deal_card(3)

    def river(self) -> List[Card]:
        return self.deal_card(4)

    def cur_winner(self, verbose=False) -> int:
        # TODO: support multiple players
        if self.num_players != 2:
            raise NotImplementedError("Currently only supports 2 players")

        if verbose:
            print(f"Player 0 type: {self.player_hands[0].type}, order: {self.player_hands[0].order}")
            print(f"Player 1 type: {self.player_hands[1].type}, order: {self.player_hands[1].order}")
        if self.player_hands[0] > self.player_hands[1]:
            if verbose:
                print("Player 0 is winning\n")
            return 0
        elif self.player_hands[0] < self.player_hands[1]:
            if verbose:
                print("Player 1 is winning\n")
            return 1
        else:
            if verbose:
                print("Players are tied\n")
            return 2
