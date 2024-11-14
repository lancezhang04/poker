import random


with open("hole_cards_percentiles.txt", 'r') as f:
    lines = f.readlines()

rankings = dict()
for i, line in enumerate(lines):
    hole_cards_pairs = line.split()
    for pair in hole_cards_pairs:
        rankings[pair] = i
print(f"Total pairs recorded: {len(rankings)}")
print("Rank is defined as a pair of hole cards being the top _% of all possibilities")
pairs = list(rankings.keys())

total_abs_error = 0
total = 0
while True:
    pair = random.choice(pairs)
    ans = input(f"What is the ranking for {pair}? >> ")
    rank = -1
    while rank == -1:
        try:
            if ans.lower() == "quit":
                exit(0)
            rank = int(ans)
        except ValueError:
            ans = input("Please enter a valid rank >> ")
    print(f"Answer is: {rankings[pair]}")

    total_abs_error += abs(rank - rankings[pair])
    total += 1
    print(f"Mean absolute error: {total_abs_error / total:.3f}")
