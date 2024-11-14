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
        self.player_hands = [Hand() for _ in range(num_players)]
        self.num_players = num_players
        self.verbose = verbose

    def deal_starting_cards(self):
        for i in range(self.num_players):
            self.player_hands[i].add_hole_card(self.deck.draw_card())
            self.player_hands[i].add_hole_card(self.deck.draw_card())

        if self.verbose:
            for i, hand in enumerate(self.player_hands):
                print(f"Hand of player {i}: {hand.hole_cards[0]}, {hand.hole_cards[1]}")
            print()
        return self.player_hands

    def flop(self) -> List[Card]:
        if len(self.community_cards) != 0:
            raise RuntimeError("Current round has already flopped")
        for i in range(3):
            self.deal_card(i)

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
        for player_hand in self.player_hands:
            player_hand.add_community_card(card)
        return self.community_cards

    def turn(self) -> List[Card]:
        return self.deal_card(3)

    def river(self) -> List[Card]:
        return self.deal_card(4)

    def set_state(self, hole_cards_list: List[List[Card]], community_cards: List[Card]=None):
        if len(hole_cards_list) > self.num_players:
            raise ValueError("Too many hole cards for the number of players")
        if len(community_cards) not in [0, 3, 4, 5]:
            raise ValueError("Invalid number of community cards:", len(community_cards))

        # set remaining deck to match dealt cards
        self.deck = Deck(full_decks=self.full_decks)
        if community_cards is not None:
            for card in community_cards:
                self.deck.remove_card(card)
        for hole_cards in hole_cards_list:
            for card in hole_cards:
                self.deck.remove_card(card)

        # set player hands to match
        for i, hole_cards in enumerate(hole_cards_list):
            self.player_hands[i] = Hand(community_cards, hole_cards)
        # draw pairs that are not provided
        for i in range(len(hole_cards_list), self.num_players):
            self.player_hands[i] = Hand(community_cards, [
                self.deck.draw_card(), self.deck.draw_card()
            ])

        # set community cards to match
        self.community_cards = community_cards.copy()

    def cur_winner(self) -> int:
        best_hand = self.player_hands[0]
        best_player_idx = 0

        for i in range(1, self.num_players):
            if self.player_hands[i] > best_hand:
                best_hand = self.player_hands[i]
                best_player_idx = i

        if self.verbose:
            print("\nCommunity cards:")
            for i, card in enumerate(self.community_cards):
                print(f"Card {i}: {card}")
            print()
            for i in range(self.num_players):
                print(f"Player {i} type: {self.player_hands[i].type}, "
                      f"order: {self.player_hands[i].order}")
            print(f"Player {best_player_idx} is winning\n")
        return best_player_idx
