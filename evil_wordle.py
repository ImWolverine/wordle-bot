from colorama import Fore, Back, Style
import json
from os import system
import wordle
import random

PRECOMPUTED_TURNS = []#json.load(open("wordle/salet_precomputed.json"))
GUESSES = json.load(open("words.json"))
SOLUTIONS = json.load(open("words.json"))

MAX_LENGTH = 5
MIN_LENGTH = 5

GUESSES = [guess for guess in GUESSES if (len(guess) <= MAX_LENGTH) & (len(guess) >= MIN_LENGTH)]
SOLUTIONS = [solution for solution in SOLUTIONS if (len(solution) <= MAX_LENGTH) & (len(solution) >= MIN_LENGTH)]

past_guesses = []

expected = 0

def calc_luck(expected, actual):
    if expected <= 1:
        return 1
    return (1 / pow(2, (actual - 1) / (expected - 1)))

worst_combo = []

luck = 0

while True:
    system('clear')
    # print(worst_combo)
    # print(len(SOLUTIONS))
    next_guess = wordle.prompt_wordle_game(GUESSES, SOLUTIONS, past_guesses, False, round(calc_luck(expected, len(SOLUTIONS)) * 100))
    expected = wordle.get_average_length_remaining(next_guess, SOLUTIONS)
    combo_chances = wordle.get_combo_distribution(next_guess, SOLUTIONS)

    # print(combo_chances)

    combo_luck = [{"combo": combo_chance[0], "luck": calc_luck(expected, len(SOLUTIONS) * combo_chance[1])} for combo_chance in combo_chances]
    # print(combo_luck)

    green_combos = []

    for combo in combo_luck:
        if all(color == 2 for color in combo["combo"]):
            green_combos.append(combo)

    if len(green_combos) != len(combo_luck):
        for combo in green_combos:
            combo_luck.remove(combo)

    closest = [combo_luck[0]]

    for combo in combo_luck:
        if abs(closest[0]["luck"] - (luck / 100)) > abs(combo["luck"] - (luck / 100)):
            closest = [combo]
        elif abs(closest[0]["luck"] - (luck / 100)) == abs(combo["luck"] - (luck / 100)):
            closest.append(combo)


    # print(closest)
    #
    #
    #
    # top_combo_chances = [combo_chance for combo_chance in combo_chances if combo_chance[1] == combo_chances[0][1]]
    #
    # if len(top_combo_chances) == len(combo_chances) and len(top_combo_chances) != 1:
    #     for combo_chance in top_combo_chances:
    #         if combo_chance[0] == ([2] * len(next_guess)):
    #             top_combo_chances.remove(combo_chance)



    new_combo = random.choice(closest)
    past_guesses.append({"word": next_guess, "colors": new_combo["combo"]})
    SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
    # print(SOLUTIONS)

wordle.print_wordle(past_guesses)
