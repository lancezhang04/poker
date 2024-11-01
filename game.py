from card import Card
from deck import Deck

from typing import List


class Game:
    deck: Deck
    community_cards: List[Card]
    # TODO: create player object
    player_hands: List[List[Card]]
    verbose: bool

    def __init__(self, num_players=2, full_decks=1, verbose=False):
        self.deck = Deck(full_decks=full_decks)
        self.community_cards = list()
        self.verbose = verbose

        self.player_hands = list()
        for _ in range(num_players):
            self.player_hands.append(list())
            for _ in range(2):
                self.player_hands[-1].append(self.deck.draw_card())

        if self.verbose:
            for i, hand in enumerate(self.player_hands):
                print(f"Hand of player {i}: {hand[0]}, {hand[1]}")
            print()

    def flop(self) -> List[Card]:
        if len(self.community_cards) != 0:
            raise RuntimeError("Current round has already flopped")
        for _ in range(3):
            self.community_cards.append(self.deck.draw_card())

        if self.verbose:
            for i, card in enumerate(self.community_cards):
                print(f"Card {i}: {card}")
            print()
        return self.community_cards

    def turn(self) -> List[Card]:
        if len(self.community_cards) != 3:
            raise RuntimeError("Cannot turn in the current stage of the round")
        self.community_cards.append(self.deck.draw_card())

        if self.verbose:
            print(f"Card 3: {self.community_cards[-1]}\n")
        return self.community_cards

    def river(self) -> List[Card]:
        if len(self.community_cards) != 4:
            raise RuntimeError("Cannot river in the current stage of the round")
        self.community_cards.append(self.deck.draw_card())

        if self.verbose:
            print(f"Card 4: {self.community_cards[-1]}\n")
        return self.community_cards


if __name__ == "__main__":
    game: Game = Game(verbose=True)
    game.flop()
    game.turn()
    game.river()
