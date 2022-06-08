from colorama import Fore, Back, Style
import json
from os import system
import wordle

PRECOMPUTED_TURNS = []#json.load(open("wordle/salet_precomputed.json"))
GUESSES = json.load(open("wordle/guesses.json"))
SOLUTIONS = json.load(open("wordle/solutions.json"))

WORD_LENGTH = 5

GUESSES = [guess for guess in GUESSES if len(guess) == WORD_LENGTH]
SOLUTIONS = [solution for solution in SOLUTIONS if len(solution) == WORD_LENGTH]

HARD_MODE = False



#
# new_solutions = wordle.get_possible_words(SOLUTIONS, [{"word": "raine", "colors": [2, 1, 0, 0, 0]}])
#
# print(wordle.get_turn_solve_counts(GUESSES, new_solutions))


# print(wordle.get_entropy("quads", SOLUTIONS))

# 0.5777392810740576
# 0.586401039411

# joker, foyer, boxer
#
# def calc_luck(expected, actual):
#     if actual > expected:
#         return expected / actual / 2
#     else:
#         return 1 - (actual / expected / 2)


# def calc_luck_2(expected, actual, max):
#     if actual > expected:
#         return -((actual - max) / (2 * (max - expected)))
#     else:
#         return (2 * expected - 1 - actual) / (2 * (expected - 1))
def calc_luck(expected, actual):
    return (1 / pow(2, (actual - 1) / (expected- 1)))

system('clear')
next_guess = wordle.prompt_next_guess(SOLUTIONS, [{"word": "salet", "score": 0.9693}], [])

past_guesses = next_guess
# distrobution = wordle.get_combo_distribution(past_guesses[-1]["word"], SOLUTIONS)
expected = wordle.get_average_length_remaining(past_guesses[-1]["word"], SOLUTIONS)
worst = (1 - wordle.get_percent_removed_worst(past_guesses[-1]["word"], SOLUTIONS)) * len(SOLUTIONS)
# solution_distrobution = {}

# max_remaining = 0
#
# for x in distrobution:
#     max_remaining = max(max_remaining, x[1] * len(SOLUTIONS))
#     # print(str(x[0]) + "," + str(x[1] * 100))
#     try:
#         solution_distrobution[round(x[1] * len(SOLUTIONS))] += x[1]
#     except:
#         solution_distrobution[round(x[1] * len(SOLUTIONS))] = x[1]
#
# sum = 0
#
# for x in solution_distrobution.items():
#     print(str(x[0]) + "," + str(x[1] * 100) + ", " + str(calc_luck(expected, x[0])))
#     sum += calc_luck(expected, x[0]) * x[1]

# print(solution_distrobution)
# print(sum)
# print(expected)
SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
if HARD_MODE:
    GUESSES = wordle.get_possible_words(GUESSES, past_guesses)

while True:
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
    # print(len(SOLUTIONS))
    # print(expected)
    # print(worst)
    # print(round(calc_luck(expected, len(SOLUTIONS)) * 100))
        # if x[0] == past_guesses[-1]["colors"]:
        #     print(x)
    past_guesses = wordle.prompt_next_guess(SOLUTIONS, best_guesses, past_guesses)
    expected = wordle.get_average_length_remaining(past_guesses[-1]["word"], SOLUTIONS)
    # distrobution = wordle.get_combo_distribution(past_guesses[-1]["word"], SOLUTIONS)
    worst = (1 - wordle.get_percent_removed_worst(past_guesses[-1]["word"], SOLUTIONS)) * len(SOLUTIONS)
    SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)

    if HARD_MODE:
        GUESSES = wordle.get_possible_words(GUESSES, past_guesses)

system('clear')
wordle.print_wordle(past_guesses + [{"word": SOLUTIONS[0], "colors": [2] * len(SOLUTIONS[0])}])
print(f"\n{Style.BRIGHT}{Fore.GREEN}SOLUTION: {Style.RESET_ALL}{SOLUTIONS[0]}\n")
