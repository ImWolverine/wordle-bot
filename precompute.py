from colorama import Fore, Back, Style
import json
from os import system
import wordle
import time
import random

PRECOMPUTED_TURNS = []
GUESSES = json.load(open("wordle/guesses.json"))
SOLUTIONS = json.load(open("wordle/solutions.json"))

first_guess = "salet"

COLORS = wordle.get_possible_combos(first_guess, SOLUTIONS)

random.shuffle(COLORS)

data = []

solutions_length = len(SOLUTIONS)

start_time = time.time()
n = 0

try:
    for color in COLORS:
        past_guesses = [{"word": first_guess, "colors": color}]

        current_time = time.time()
        eta = round(((current_time - start_time) / (n + 1) * len(COLORS)) * (1 - ((n + 1) / len(COLORS))))
        system('clear')
        wordle.print_wordle(past_guesses)
        print(f"{Style.BRIGHT}{Fore.GREEN}\nPROGRESS: {Style.RESET_ALL}{str(round(float(n) / float(len(COLORS)) * 100))}% {Fore.WHITE}({str(eta)}s)")

        new_solutions = wordle.get_possible_words(SOLUTIONS, past_guesses)
        if len(new_solutions) > 0:
            best_guesses = wordle.get_best_next_guesses(GUESSES, new_solutions, [], past_guesses, False)
            data.append({
                "past_guesses": past_guesses,
                "best_guesses": best_guesses
            })
        n += 1
        with open("wordle/salet_precomputed.json", "w") as outfile:
            json.dump(data, outfile)
except KeyboardInterrupt:
    with open("wordle/salet_precomputed.json", "w") as outfile:
        json.dump(data, outfile)
