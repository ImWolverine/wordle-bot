from colorama import Fore, Back, Style
import json
from os import system
import wordle

PRECOMPUTED_TURNS = []
GUESSES = json.load(open("primel/guesses.json"))
SOLUTIONS = json.load(open("primel/solutions.json"))

HARD_MODE = False

system('clear')
next_guess = wordle.prompt_next_guess(SOLUTIONS, [{"word": "21739", "score": 1}], [])

past_guesses = next_guess
SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
if HARD_MODE:
    GUESSES = SOLUTIONS

while len(SOLUTIONS) > 1:
    system('clear')
    wordle.print_wordle(past_guesses)
    print("")

    skip_calculation = input(f"{Style.BRIGHT}{Fore.YELLOW}SKIP CALCULATION? (Y / N): {Style.RESET_ALL}")
    if skip_calculation.upper() != "Y":
        best_guesses = wordle.get_best_next_guesses(GUESSES, SOLUTIONS, PRECOMPUTED_TURNS, past_guesses, True)
    else:
        best_guesses = []

    system('clear')
    wordle.print_wordle(past_guesses)
    print("")

    past_guesses = wordle.prompt_next_guess(SOLUTIONS, best_guesses, past_guesses)
    SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
    if HARD_MODE:
        GUESSES = SOLUTIONS

system('clear')
wordle.print_wordle(past_guesses + [{"word": SOLUTIONS[0], "colors": [2] * len(SOLUTIONS[0])}])
print(f"\n{Style.BRIGHT}{Fore.GREEN}SOLUTION: {Style.RESET_ALL}{SOLUTIONS[0]}\n")
