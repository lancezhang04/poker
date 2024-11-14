from typing import List
from tqdm import tqdm
import matplotlib.pyplot as plt

from poker.game import Game
from poker.deck import Deck
from poker.hand import Hand


def play_flop(simulate=True):
    """
    If simulate == False, stats corresponds to
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
        game = Game(num_players=2)
        game.deal_starting_cards()
        game.flop()
        print("Flop:")
        for card in game.community_cards:
            print("  " + str(card))
        print("Hole cards:")
        for card in game.player_hands[0].hole_cards:
            print("  " + str(card))
        print()

        ans = ""
        while ans not in ["fold", "bet", "f", "b"]:
            ans = input("Would you like to fold (\"f\") or bet (\"b\")?  >> ")
            if ans.lower() == "quit":
                exit(0)

        if simulate:
            win_prob = simulate_win_prob(
                game.player_hands[0].hole_cards,
                game.community_cards[:3]
            )
            print(f"Simulated win probability: {win_prob * 100:.2f}%")
            if win_prob < 0.5:
                print("Folding was the correct decision!")
                if ans in ["fold", "f"]:
                    balance += 1
            else:
                print("Betting was the correct decision!")
                if ans in ["bet", "b"]:
                    balance += 1
            print(f"Record: {balance}/{i + 1} or {balance / (i + 1) * 100:.2f}%\n")
        else:
            game.turn()
            game.river()
            winner = game.cur_winner()

            if ans in ["fold", "f"]:
                stats[winner] += 1
            if ans in ["bet", "b"]:
                stats[3 + winner] += 1
                balance -= 1
                if winner == 0:
                    balance += 2
                elif winner == 2:
                    balance += 1

            # print current stats and credits after each round
            print("\nCurrent Stats:")
            print(f"Folded, would have won: {stats[0]}")
            print(f"Folded, would have lost: {stats[1]}")
            print(f"Folded, would have drawn: {stats[2]}")
            print(f"Bet, won: {stats[3]}")
            print(f"Bet, lost: {stats[4]}")
            print(f"Bet, drew: {stats[5]}")
            balance_str = str(balance)
            if balance > 0:
                balance_str = "+" + balance_str
            print(f"Balance: {balance_str}")
            print()


def simulate_win_prob(hole_cards, flop_cards, num_iters=5000, show_plot=False, verbose=False):
    wins = 0
    data = [list(), list()]

    for i in tqdm(range(num_iters), ncols=80):
        game = Game()
        game.deck = Deck(game.full_decks)
        for card in hole_cards + flop_cards:
            game.deck.remove_card(card)

        game.player_hands.append(Hand(
            flop_cards.copy(),
            hole_cards.copy()
        ))
        game.player_hands.append(Hand(
            flop_cards.copy(),
            [game.deck.draw_card() for _ in range(2)]
        ))
        game.community_cards = flop_cards.copy()

        game.turn()
        game.river()
        if game.cur_winner() == 0:
            wins += 1

        if verbose:
            print("Hero hole cards:")
            for card in game.player_hands[1].community_cards:
                print(card)
            print("Villain hole cards:")
            for card in game.player_hands[1].hole_cards:
                print(card)
            game.cur_winner(verbose=True)
            print()

        if show_plot and (i + 1) % 100 == 0:
            data[0].append(i + 1)
            data[1].append(wins / (i + 1))

    if show_plot:
        plt.plot(data[0], data[1], label=f"Final: {wins / num_iters * 100:.2f}%")
        plt.ylim([0, 1])
        plt.legend()
        plt.show()
    return wins / num_iters


if __name__ == "__main__":
    play_flop()
