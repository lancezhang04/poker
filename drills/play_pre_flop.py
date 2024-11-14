from typing import List
from tqdm import tqdm
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from poker import Card, Game
from drills.utils import clear_screen


def play_flop(num_players: int=2, verbose: bool=False):
    score: int = 0
    # fair assumption?
    threshold = 1 / num_players

    clear_screen()
    print(f"Starting game with {num_players} players")
    num_rounds: int = -1
    while num_rounds == -1:
        try:
            num_rounds = int(input("How many rounds would you like to play?  >> "))
        except ValueError:
            print("Please enter an integer\n")
    print()

    for i in range(num_rounds):
        clear_screen()
        print(f"Round {i + 1} out of {num_rounds}")
        game = Game(num_players=num_players, verbose=verbose)
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

        win_prob = simulate_win_prob(
            game.player_hands[0].hole_cards,
            game.community_cards[:3],
            num_players=num_players,
            # show_plot=True,
        )
        if win_prob < threshold:
            print(f"Folding was the right decision with threshold {threshold:.3f}")
            if ans in ["fold", "f"]:
                score += 1
        else:
            print(f"Betting was the right decision with threshold {threshold:.3f}")
            if ans in ["bet", "b"]:
                score += 1
        print(f"Record: {score}/{i + 1} or {score / (i + 1) * 100:.2f}%")
        print(f"Simulated win probability: {win_prob * 100:.2f}%\n")

        input(f"Press enter to continue...")


def simulate_win_prob(hole_cards: List[Card], flop_cards: List[Card],
                      num_players: int=2, num_iters: int=5000, show_plot: bool=False):
    wins = 0
    data = [list(), list()]

    for i in tqdm(range(num_iters), ncols=80):
        game = Game(num_players=num_players)
        game.set_state([hole_cards], flop_cards)
        game.turn()
        game.river()
        if game.cur_winner() == 0:
            wins += 1

        if show_plot and (i + 1) % 100 == 0:
            data[0].append(i + 1)
            data[1].append(wins / (i + 1))

    if show_plot:
        plt.plot(data[0], data[1], label=f"Final: {wins / num_iters * 100:.3f}%")
        plt.ylim([0, 1])
        plt.legend()
        plt.show()
    return wins / num_iters


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num_players", "-n", default=2, type=int, help="Number of players")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    play_flop(num_players=args.num_players, verbose=args.verbose)
