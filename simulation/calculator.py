from typing import List
from poker import Suit, Card
from drills.utils import clear_screen
from simulation import run_monte_carlo


str_to_val = {str(i + 1): i for i in range(0, 10)}
str_to_val.update({
    "j": 10, "q": 11, "k": 12, "a": 13
})
str_to_suit = {
    "s": Suit.SPADES, "c": Suit.CLUBS,
    "d": Suit.DIAMONDS, "h": Suit.HEARTS,
}


def str_to_cards(s: str) -> List[Card]:
    s = s.lower()
    cards = list()
    for card_s in s.split():
        val = str_to_val[card_s[:-1]]
        suit = str_to_suit[card_s[-1]]
        cards.append(Card(val, suit))
    return cards


def run_calculator():
    while True:
        clear_screen()
        num_players = -1
        while num_players < 0:
            try:
                num_players = int(input("Enter number of players: "))
            except ValueError:
                pass

        hole_cards = list()
        community_cards = list()
        print_equity = lambda: print(f"Simulated equity: {run_monte_carlo(
            hole_cards, community_cards,
            num_players=num_players, verbose=True
        ) * 100:.2f}%\n")

        while len(hole_cards) != 2:
            s = input("Enter hole cards: ")
            hole_cards = str_to_cards(s)
        print_equity()

        while len(community_cards) != 3:
            s = input("Enter flop: ")
            community_cards = str_to_cards(s)
        print_equity()

        while len(community_cards) != 4:
            s = input("Enter turn: ")
            new_cards = str_to_cards(s)
            if len(new_cards) != 1:
                continue
            community_cards.append(new_cards[0])
        print_equity()

        while len(community_cards) != 5:
            s = input("Enter river: ")
            new_cards = str_to_cards(s)
            if len(new_cards) != 1:
                continue
            community_cards.append(new_cards[0])
        print_equity()

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_calculator()
