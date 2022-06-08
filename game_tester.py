from colorama import Fore, Back, Style
import json
from os import system
import wordle
import time
import random

PRECOMPUTED_TURNS = []#json.load(open("wordle/salet_precomputed.json"))
GUESSES = json.load(open("wordle/guesses.json"))
SOLUTIONS = json.load(open("wordle/solutions.json"))

# past_guesses = [{"word": "salet", "colors": [0, 0, 0, 2, 0]}]
# SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
#
# # print(wordle.get_word_score("salet", SOLUTIONS))
#
# print(wordle.entropy_to_percent(wordle.get_word_score_entropy_deep("drown", GUESSES, SOLUTIONS)))
# print(wordle.entropy_to_percent(wordle.get_word_score_entropy_deep("rownd", GUESSES, SOLUTIONS)))

# print(wordle.get_best_next_guesses(GUESSES, SOLUTIONS, [], past_guesses, True))


# Entropy 1 Depth 3.431
# Combo 1 Depth 3.428

HARD_MODE = False

# crate lions 3.673
# nasty liver 3.846
# salet corni 3.670
# crate lions bumpy 4.243
# nasty liver gumbo 4.369
# salet corni bumph 4.222

#

# 52-34=18 6*95=570

random.shuffle(SOLUTIONS)
#random.shuffle(GUESSES)

# crate, lions, bumpy, hedge, awful 6.029
# cimex, grypt, blunk, waqfs, vozhd 6.016

solutions_length = len(SOLUTIONS)
start_time = time.time()
first_guess = "salet"

turn_data = []

for index, solution in enumerate(SOLUTIONS):
    past_guesses = [{
        "word": first_guess,
        "colors": wordle.get_color_combo(first_guess, solution)
    }]

    solved_guesses = wordle.solve(GUESSES, SOLUTIONS, solution, PRECOMPUTED_TURNS, past_guesses, False, HARD_MODE)
    turn_data.append(len(solved_guesses))

    current_time = time.time()
    eta = round(((current_time - start_time) / (index + 1) * solutions_length) * (1 - ((index + 1) / solutions_length)))

    system('clear')
    wordle.print_wordle(solved_guesses)
    print(f"{Style.BRIGHT}{Fore.GREEN}\nPROGRESS: {Style.RESET_ALL}{str(round(float(index) / float(solutions_length) * 100))}% {Fore.WHITE}({str(eta)}s)")
    print(f"{Style.BRIGHT}{Fore.GREEN}AVERAGE: {Style.RESET_ALL}{str(round(sum(turn_data) / len(turn_data), 3))} turns")
    wordle.print_hist(turn_data)

system('clear')
wordle.print_wordle(solved_guesses)
print(f"{Style.BRIGHT}{Fore.GREEN}\nPROGRESS: {Style.RESET_ALL}{str(round(float(index) / float(solutions_length) * 100))}% {Fore.WHITE}({str(eta)}s)")
print(f"{Style.BRIGHT}{Fore.GREEN}AVERAGE: {Style.RESET_ALL}{str(round(sum(turn_data) / len(turn_data), 3))} turns")
wordle.print_hist(turn_data)
