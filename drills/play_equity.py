from argparse import ArgumentParser

from drills.utils import clear_screen
from poker import Game
from simulation.monte_carlo import run_monte_carlo


def play_equity(num_rounds=5):
    total_errors = {
        "pre-flop": 0,
        "post-flop": 0,
        "turn": 0,
        "river": 0,
    }

    for i in range(num_rounds):
        game = Game(num_players=6)
        streets = [
            ("pre-flop", game.deal_starting_cards),
            ("post-flop", game.flop),
            ("turn", game.turn),
            ("river", game.river),
        ]

        for name, func in streets:
            clear_screen()
            if name == "pre-flop":
                print(f"Round {i + 1} out of {num_rounds}")
            func()
            game.print_hero_board()

            guess = get_player_guess()
            equity = run_monte_carlo(
                game.player_hands[0].hole_cards,
                game.community_cards,
                num_players=6
            ) * 100
            error = abs(equity - guess)
            total_errors[name] += error
            print(f"Simulated pot equity: {equity:.2f}%")
            print(f"Absolute error: {error:.2f}")
            input("\nPress Enter to continue...")

    clear_screen()
    for k, v in total_errors.items():
        print(f"Absolute error, {k}: {v / num_rounds:.2f}")
    input("\nPress Enter to exit...")


def get_player_guess() -> float:
    guess: float = -1.
    while guess < 0 or guess > 100:
        if guess < 0 or guess > 100:
            print("Please enter a number between 0 and 100")
        try:
            guess = float(input("Estimate your current pot equity (%)  >> "))
        except ValueError:
            print("Please enter a valid number")
    return guess


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num_rounds", "-r", default=2, type=int, help="Number of players")
    args = parser.parse_args()

    play_equity(num_rounds=args.num_rounds)
