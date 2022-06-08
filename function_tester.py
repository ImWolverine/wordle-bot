from colorama import Fore, Back, Style
import json
from os import system
import wordle
import time
import random
from collections import Counter


money = 0
monthly_interest = 0.2 / 12
weekly_rate = 10

for day in range(365 * 10):
    day += 1
    if day % 7 == 0:
        print(str(day) + ", " + str(money))
        money += weekly_rate
        print(str(day) + ", " + str(money))
    if day % round(365 / 12) == 0:
        print(str(day) + ", " + str(money))
        money *= 1 + monthly_interest
        print(str(day) + ", " + str(money))

GUESSES = json.load(open("nerdle/guesses.json"))
SOLUTIONS = json.load(open("nerdle/solutions.json"))

# SOLUTIONS = wordle.get_possible_words(SOLUTIONS, [{"word": "crate", "colors": [0, 0, 0, 0, 0]}])
#
#
#
random.shuffle(GUESSES)
random.shuffle(SOLUTIONS)
#
# freq = {letter: 0 for letter in list("abcdefghijklmnopqrstuvwxyz")}
#
# freqs = [dict(freq), dict(freq), dict(freq), dict(freq), dict(freq)]
#
# for solution in SOLUTIONS:
#     for i in range(5):
#         freqs[i][solution[i]] += 1
#
# for i in range(5):
#     freqs[i] = dict(sorted(freqs[i].items(), key=lambda item: item[1]))
#
# # print(freqs)
#
# scores = {new_guess: 0 for new_guess in GUESSES}
#
# for guess in SOLUTIONS:
#     for i in range(5):
#         scores[guess] += freqs[i][guess[i]]
#
# print(dict(sorted(scores.items(), key=lambda item: item[1])))

# reais, duply, thang
#
# SOLUTIONS = wordle.get_possible_words(SOLUTIONS, [{"word": "reais", "colors": [0, 0, 0, 0, 0]},{"word": "duply", "colors": [0, 1, 0, 0, 0]},{"word": "thang", "colors": [0, 1, 0, 0, 1]},{"word": "kibes", "colors": [0, 0, 0, 0, 0]}])
#
# scores = {new_guess: 0 for new_guess in GUESSES}
#
# for guess in GUESSES:
#     scores[guess] = wordle.get_percent_removed_worst(guess, SOLUTIONS)
#     #print(list(dict(sorted(scores.items(), key=lambda item: item[1])).items())[-1])
#
# print(dict(sorted(scores.items(), key=lambda item: item[1])))
# print(SOLUTIONS)

# crate, lions, bumpy, hedge, vowel



#
# scores = {new_guess: 0 for new_guess in GUESSES}
#
#
# for solution in SOLUTIONS:
#     new_solutions = wordle.get_possible_words(SOLUTIONS, [
#     {"word": "52-34=18", "colors": wordle.get_color_combo("52-34=18", solution)}
#     ])
#     for guess in GUESSES:
#         scores[guess] += wordle.get_percent_removed(guess, new_solutions)
#     print(list(dict(sorted(scores.items(), key=lambda item: item[1])).items())[-10:])
#
# print(dict(sorted(scores.items(), key=lambda item: item[1])))



#
# for combo in combos:
#     new_solutions =
#     best_next_guess = max([{"word": guess1, "score": get_word_score_deep(guess1, GUESSES, new_solutions)} for guess1 in GUESSES[:1000]], key=lambda x:x["score"])
#
#
# for guess1 in GUESSES:
#     new_solutions = wordle.get_possible_words(SOLUTIONS, [{"word": guess1, "colors": [1, 0, 0, 0, 1]}])
#     for guess2 in GUESSES:
#
#
# def get_word_score_deep(guess, guesses, solutions):
#     solutions_length = len(solutions)
#     combos = get_combo_distribution(guess, solutions)
#     deep_score = 0
#     for combo in combos:
#         new_solutions = get_possible_words(solutions, [{"word": guess, "colors": combo[0]}])
#         if len(new_solutions) == 1:
#             continue
#         next_guess_scores = [{"word": new_guess, "score": get_word_score(new_guess, new_solutions)} for new_guess in guesses]
#         best_next_guess = max(next_guess_scores, key=lambda x:x["score"])
#         remaining_solutions_length = get_average_length_remaining(best_next_guess["word"], new_solutions)
#         deep_score += remaining_solutions_length * combo[1]
#     return (1 - (deep_score / solutions_length))
#
#
# print(wordle.get_word_score_deep(guess, GUESSES, SOLUTIONS))

#
# mega_rankings = []
#
# for i in range(11):
#     WORD_LENGTH = i + 1
#
#     NEW_GUESSES = [guess for guess in GUESSES if len(guess) == WORD_LENGTH]
#     NEW_SOLUTIONS = [solution for solution in SOLUTIONS if len(solution) == WORD_LENGTH]
#
#     if len(NEW_GUESSES) == 0:
#         continue
#
#     rankings = []
#
#     for guess in NEW_GUESSES:
#         rankings.append({"word": guess, "score": wordle.get_approximate_word_score(guess, NEW_SOLUTIONS)})
#         print(guess)
#
#     rankings.sort(key = lambda x: x["score"], reverse = True)
#     mega_rankings = mega_rankings + rankings
#     with open("nerdle_rankings.json", "w") as outfile:
#         json.dump(mega_rankings, outfile)
#
# with open("nerdle_rankings.json", "w") as outfile:
#     json.dump(mega_rankings, outfile)
# #
#
# RANKINGS = json.load(open("wordle_rankings.json"))
#
# i = 1
# for rank in RANKINGS:
#     percent = round(100 - (((i - 1) / (len(RANKINGS) - 1)) * 100), 2)
#     if rank["word"] in SOLUTIONS:
#         print(str(i).rjust(5, '0') + ". " + rank["word"] + "* | " + str(percent) + "%")
#     else:
#         print(str(i).rjust(5, '0') + ". " + rank["word"] + "  | " + str(percent) + "%")
#     i += 1

#
# new_words = []
#
# wanted_letters = "earotlisncuydhp"
#
# for word in WORDS:
#     # count = 0
#     # for letter in wanted_letters:
#     #     if letter in word:
#     #         count += 1
#     if (len(set(word)) >= 5):
#         new_words.append(word)
# WORDS = new_words
#
# data = {guess: 0 for guess in WORDS}
#
# for guess in WORDS:
#     for solution in SOLUTIONS:
#         greens = pow(Counter(wordle.get_color_combo(guess, solution))[2], 2) + Counter(wordle.get_color_combo(guess, solution))[1]
#         data[guess] += greens
#
# data = sorted(data.items(), key=lambda x: x[1], reverse=True)
#
# new_words = []
#
# for d in data:
#     new_words.append(d[0])
#
# WORDS = new_words
#
# data = {}
#
# ['stare', 'phony', 'lucid']
#
# for word1 in WORDS:
#     if len(set(word1)) == 5:
#         for word2 in WORDS:
#             if len(set(word1+word2)) == 10:
#                 for word3 in WORDS:
#                     if len(set(word1+word2+word3)) == 15:
#                         print([word1,word2,word3])
#                         # print(sorted(data.items(), key=lambda x: x[1], reverse=True)[0])


# scores = []
#
# for word in WORDS:
#     first_guess = word
#     new_words = []
#     for word2 in WORDS:
#         for letter in word:
#             if not letter in word2:
#                 new_words.append(word2)
#
#     new_words = wordle.get_possible_words(new_words, {""})
#
#
# print(set(WORDS) - set(WORDS2))
#
# new_words = []
# for word in WORDS2:
#     if not "'" in word:
#         new_words.append(word)
#
# with open("words2.json", "w") as outfile:
#     json.dump(new_words, outfile)

#print(wordle.get_color_combo("memorial", "word"))

#
# new_solutions = []
# new_guesses = []
#
# for rank in RANKINGS:
#     if rank["word"] in SOLUTIONS:
#         new_solutions.append(rank["word"])
#     new_guesses.append(rank["word"])
#
# #


# SOLUTIONS = json.load(open("wordle/solutions_raw.json"))

#
# print(wordle.get_word_score_entropy_deep("soare", GUESSES, SOLUTIONS))
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
