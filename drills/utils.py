import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_ending_message(win_rate: float, threshold: float=0.9):
    clear_screen()
    passed_threshold = win_rate >= threshold
    print(f"You final accuracy is {win_rate * 100:.2f}%", end="!!\n" if passed_threshold else "\n")
    if passed_threshold:
        print("Congratulations – good work!")
    else:
        print("We can do better next time :(")
    input(f"\nPress enter to exit...")
    clear_screen()
    exit(0)
