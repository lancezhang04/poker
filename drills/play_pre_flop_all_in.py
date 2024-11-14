from typing import List
from poker.game import Game


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
