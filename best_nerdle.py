from colorama import Fore, Back, Style
import json
from os import system
import wordle
import time
import random

# RANKINGS = json.load(open("rankings.json"))
GUESSES = json.load(open("words.json"))
SOLUTIONS = json.load(open("words.json"))

GUESSES = [solution for solution in GUESSES if len(solution) == 5]


guesses_length = len(GUESSES)
#
# new_solutions = []
# new_guesses = []
#
# for rank in RANKINGS:
#     if rank["word"] in SOLUTIONS:
#         new_solutions.append(rank["word"])
#     new_guesses.append(rank["word"])
#

rankings = []

i = 0

for guess in GUESSES:
    i += 1
    rankings.append({"word": guess, "score": wordle.get_word_combo_score(guess, SOLUTIONS)})
    print(guess + " (" + str(round(i / guesses_length * 100, 2)) + "%)")

rankings.sort(key = lambda x: x["score"], reverse = True)

with open("rankings.json", "w") as outfile:
    json.dump(rankings, outfile)


# SOLUTIONS = json.load(open("wordle/solutions_raw.json"))
#
# i = 1
# for rank in RANKINGS:
#     percent = round(100 - (((i - 1) / (len(RANKINGS) - 1)) * 100), 2)
#
#     if rank["word"] in SOLUTIONS:
#         print(str(i).rjust(5, '0') + ". " + rank["word"] + "* | " + str(percent) + "%")
#     else:
#         print(str(i).rjust(5, '0') + ". " + rank["word"] + "  | z" + str(percent) + "%")
#     i += 1

#print(wordle.get_word_score_entropy_deep("soare", GUESSES, SOLUTIONS))
#
# for guess in GUESSES:
#     print(str(wordle.get_worst_case_score(guess, SOLUTIONS)) + " " + guess)

# past_guesses = [{"word": "salet", "colors": [1, 0, 0, 0, 1]}]
# SOLUTIONS = wordle.get_possible_words(SOLUTIONS, past_guesses)
# print(SOLUTIONS)
# #print(wordle.get_accurate_word_score("smelt", SOLUTIONS))
# print(wordle.get_best_next_guesses(GUESSES, SOLUTIONS, [], past_guesses, True))
# #print(wordle.entropy_to_percent(wordle.get_word_score_entropy_deep("beard", GUESSES, SOLUTIONS)))
#print(wordle.get_accurate_word_score("salet", SOLUTIONS))

#print(wordle.entropy_to_percent(wordle.get_word_score_entropy("smelt", SOLUTIONS)))

#
#
# test_words = ["frorn", "rownd"]
#
# data = []
#
# for test_word in test_words:
#     data.append((test_word, wordle.get_word_score_entropy_deep(test_word, GUESSES, SOLUTIONS)))
#     print(data[len(data) - 1])
#
# data.sort(key = lambda x: x[1], reverse = True)
# print(data)
