from argparse import ArgumentParser
from drills.utils import clear_screen, print_ending_message

from poker import Game
from simulation import run_monte_carlo


def play_pre_flop(num_players: int=2, verbose: bool=False):
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
        game.print_hero_board()

        ans = ""
        while ans not in ["fold", "bet", "f", "b"]:
            ans = input("Would you like to fold (\"f\") or bet (\"b\")?  >> ")
            if ans.lower() == "quit":
                exit(0)

        win_prob = run_monte_carlo(
            game.player_hands[0].hole_cards,
            game.community_cards,
            num_players=num_players,
            num_iters=5000
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
    print_ending_message(score / num_rounds)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num_players", "-n", default=2, type=int, help="Number of players")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    play_pre_flop(num_players=args.num_players, verbose=args.verbose)
