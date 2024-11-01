from math import trunc

from card import Card
from hand import Hand
from deck import Deck

from typing import List


class Game:

    deck: Deck
    community_cards: List[Card]
    # TODO: create player object
    player_hands: List[Hand]
    verbose: bool

    def __init__(self, num_players=2, full_decks=1, verbose=False):
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
        self.flop()

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

def play_flop():
    """
    0: folded, would have won
    1: folded, would have lost
    2: folded, would have drawn
    3: bet, won
    4: bet, lost
    5: best, drew
    """
    stats: List[int] = [0, 0, 0, 0, 0, 0]
    balance: int = 0

    num_rounds: int = -1
    while num_rounds == -1:
        try:
            num_rounds = int(input("How many rounds would you like to play?  >> "))
        except ValueError:
            print("Please enter an integer\n")
    print()

    for i in range(num_rounds):
        print(f"Round {i + 1} out of {num_rounds}")
        game = Game()
        game.deal_starting_cards()
        print("Flop:")
        for card in game.community_cards:
            print("  " + str(card))
        print("Hand:")
        for card in game.player_hands[0].hole_cards:
            print("  " + str(card))
        print()

        ans = ""
        while ans not in ["fold", "bet"]:
            ans = input("Would you like to \"fold\" or \"bet\"?  >> ")
        print()

        game.turn()
        game.river()
        winner = game.cur_winner()

        if ans == "fold":
            stats[winner] += 1
        if ans == "bet":
            stats[3 + winner] += 1
            balance -= 1
            if winner == 0:
                balance += 2
            elif winner == 2:
                balance += 1

        # print current stats and credits after each round
        print("Current Stats:")
        print(f"Folded, would have won: {stats[0]}")
        print(f"Folded, would have lost: {stats[1]}")
        print(f"Folded, would have drawn: {stats[2]}")
        print(f"Bet, won: {stats[3]}")
        print(f"Bet, lost: {stats[4]}")
        print(f"Bet, drew: {stats[5]}")
        balance_str = str(balance)
        if balance > 0:
            balance_str = "+" + balance_str
        elif balance < 0:
            balance_str = "-" + balance_str
        print(f"Balance: {balance_str}")
        print()


if __name__ == "__main__":
    # game: Game = Game(verbose=True)
    # game.deal_starting_cards()
    # game.cur_winner(verbose=True)
    # game.turn()
    # game.cur_winner(verbose=True)
    # game.river()
    # game.cur_winner(verbose=True)

    play_flop()
