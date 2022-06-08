from colorama import Fore, Back, Style
import json
from os import system
import wordle
import time
import random
from collections import Counter

GUESSES = json.load(open("wordle/guesses.json"))
SOLUTIONS = json.load(open("wordle/solutions.json"))


letters = {'e': 6653, 's': 6649, 'a': 5983, 'o': 4428, 'r': 4154, 'i': 3752, 'l': 3366, 't': 3292, 'n': 2948, 'u': 2508, 'd': 2448, 'y': 2066, 'c': 2021, 'p': 2013, 'm': 1975, 'h': 1754, 'g': 1639, 'b': 1624, 'k': 1495, 'f': 1112, 'w': 1037, 'v': 693, 'z': 434, 'j': 291, 'x': 288, 'q': 112}

banned = "patchmatesqiblawetly"


# SOLUTIONS = wordle.get_possible_words(SOLUTIONS, [
#     # {"word": "techy", "colors": [0, 0, 0, 1, 0]},
#     # {"word": "towse", "colors": [0, 0, 1, 1, 0]},
#     # {"word": "plane", "colors": [0, 1, 2, 0, 0]},
#     # {"word": "taler", "colors": [0, 1, 1, 0, 0]}
# ])

solution = "natal"
combo = [0, 0, 1, 0, 1]

possible_guesses = []
for guess in GUESSES:
    if wordle.get_color_combo(guess, solution) == combo:
        possible_guesses.append(guess)

guess_scores = []
for guess in possible_guesses:
    score = 0
    used = ""
    for letter in guess:
        if (letter not in banned) and (letter not in used):
            score += (1 - (letters[letter] / 64735))
        used += letter
    guess_scores.append({"word": guess, "score": score})


guess_scores.sort(key = lambda x: x["score"], reverse = True)
# print(guess_scores)

best_guess = max(guess_scores, key=lambda x:x["score"])
print(best_guess["word"])
