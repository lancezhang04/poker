from poker import Game, Card
from typing import List
from tqdm import tqdm


def run_monte_carlo(hole_cards: List[Card], community_cards: List[Card]=None,
                    num_players: int=6, num_iters: int=5000, verbose=False):
    if verbose:
        print("Hole cards: " + ", ".join([str(c) for c in hole_cards]))
        print("Community cards: " + ", ".join([str(c) for c in community_cards]))

    # assumes player 0 is the hero
    wins: int = 0
    for _ in tqdm(range(num_iters), ncols=80):
        game = Game(num_players=num_players)
        game.set_state([hole_cards], community_cards)

        # deal the rest of the cards
        if len(community_cards) == 0:
            game.flop()
        if len(community_cards) < 4:
            game.turn()
        if len(community_cards) < 5:
            game.river()

        if game.cur_winner() == 0:
            wins += 1
    return wins / num_iters
