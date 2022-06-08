from collections import Counter
from colorama import Fore, Back, Style
import json
import time
from os import system
import wordle
import math
import random

# global PRECOMPUTED_COLORS
# PRECOMPUTED_COLORS = json.load(open("wordle/color_combo_data.json"))

def old_get_color_combo(guess, solution):
    not_green = [i for i, letter in enumerate(guess) if letter != solution[i]]
    counts = Counter(solution[i] for i in not_green)
    color_combo = [2] * len(guess)

    for letter_index in not_green:
        letter = guess[letter_index]
        if counts[letter] > 0:
            color_combo[letter_index] = 1
            counts[letter] -= 1
        else:
            color_combo[letter_index] = 0

    return color_combo

def get_color_combo(guess, solution):
    guess_length = len(guess)
    solution_length = len(solution)

    not_green = [i for i, letter in enumerate(guess) if (i >= solution_length) or (letter != solution[i])]

    long_not_green = not_green + list(range(guess_length, solution_length))

    counts = Counter(solution[i] for i in long_not_green if i < solution_length)

    color_combo = [2] * len(guess)

    for letter_index in not_green:
        letter = guess[letter_index]
        if counts[letter] > 0:
            color_combo[letter_index] = 1
            counts[letter] -= 1
        else:
            color_combo[letter_index] = 0

    return color_combo


def get_possible_words(words, past_guesses):
    for past_guess in past_guesses:
        words = [word for word in words if get_color_combo(past_guess["word"], word) == past_guess["colors"]]
    return words

def get_possible_combos(guess, solutions):
    return [list(x) for x in list(Counter(tuple(get_color_combo(guess, solution)) for solution in solutions).keys())]

def get_combo_distribution(guess, solutions):
    counts = Counter(tuple(get_color_combo(guess, solution)) for solution in solutions)
    total = len(solutions)
    combos = [(list(count[0]), count[1] / total) for count in counts.items()]
    combos.sort(key = lambda x: x[1], reverse = True)
    return combos

def old_get_percent_removed(guess, solutions):
    return (1 - (sum([len(get_possible_words(solutions, [{"word": guess, "colors": get_color_combo(guess, solution)}])) for solution in solutions]) / (len(solutions) ** 2)))

def get_percent_removed_worst(guess, solutions):
    total = len(solutions)

    counts = list(Counter(tuple(get_color_combo(guess, solution)) for solution in solutions).values())
    if len(counts) == 1:
        return 0
    return (1 - max([(count / total) for count in counts]))

def get_percent_removed(guess, solutions):
    total = len(solutions)

    counts = list(Counter(tuple(get_color_combo(guess, solution)) for solution in solutions).values())
    if len(counts) == 1:
        return 0
    return (1 - sum([(count / total) ** 2 for count in counts]))

def get_entropy(guess, solutions):
    total = len(solutions)
    counts = list(Counter(tuple(get_color_combo(guess, solution)) for solution in solutions).values())
    return sum([(count / total) * math.log(total / count, 2) for count in counts])

def get_average_length_remaining(guess, solutions):
    return (1 - get_percent_removed(guess, solutions)) * len(solutions)

# def get_word_score(guess, solutions):
#     return len(set(tuple(get_color_combo(guess, solution)) for solution in solutions))

def get_word_score(guess, solutions):
    # return get_percent_removed(guess, solutions)
    return len(set([tuple(get_color_combo(guess, solution)) for solution in solutions]))
    # total = len(solutions)
    #
    # counts = list(Counter(tuple(get_color_combo(guess, solution)) for solution in solutions).values())
    # if len(counts) == 1:
    #     return 0
    # return ((1 - sum([(count / total) ** 2 for count in counts]))) * len(counts)

def get_word_score_deep(guess, guesses, solutions):
    solutions_length = len(solutions)
    combos = get_combo_distribution(guess, solutions)
    deep_score = 0
    for combo in combos:
        new_solutions = get_possible_words(solutions, [{"word": guess, "colors": combo[0]}])
        if len(new_solutions) == 1:
            continue
        next_guess_scores = [{"word": new_guess, "score": get_word_score(new_guess, new_solutions)} for new_guess in guesses]
        best_next_guess = max(next_guess_scores, key=lambda x:x["score"])
        deep_score += best_next_guess["score"] * combo[1]
    return deep_score

def rank_next_guesses(guesses, solutions, precomputed_turns, past_guesses, display_progress):
    solutions = get_possible_words(solutions, past_guesses)
    if len(solutions) == 1:
        return [{"word": solutions[0], "score": 1}]
    precomputed_guesses = [dict["past_guesses"] for dict in precomputed_turns]
    if past_guesses in precomputed_guesses:
        index = precomputed_guesses.index(past_guesses)
        return precomputed_turns[index]["best_guesses"]

    guesses_length = len(guesses)
    solutions_length = len(solutions)
    best_guesses = []
    prev_precent = -1

    if display_progress:
        start_time = time.time()

    if display_progress:
        for index, guess in enumerate(guesses):
            percent = str(round(float(index) / float(guesses_length) * 100))
            if percent != prev_precent:
                current_time = time.time()
                eta = round(((current_time - start_time) / (index + 1) * guesses_length) * (1 - ((index + 1) / guesses_length)))

                system('clear')
                print_wordle(past_guesses)
                print(f"{Style.BRIGHT}{Fore.GREEN}\nPROGRESS: {Style.RESET_ALL}{str(round(float(index) / float(guesses_length) * 100))}% {Fore.WHITE}({str(eta)}s)")
                print(f"{Style.BRIGHT}{Fore.GREEN}SOLUTIONS: {Style.RESET_ALL}{'{:,}'.format(solutions_length)}")

                prev_precent = percent

            best_guesses.append({
                "word": guess,
                "score": get_word_score(guess, solutions)
            })
    else:
        best_guesses = [{
            "word": guess,
            "score": get_word_score(guess, solutions)
        } for guess in guesses]

    best_guesses.sort(key = lambda x: x["score"], reverse = True)

    return best_guesses

def get_best_next_guesses(guesses, solutions, precomputed_turns, past_guesses, display_progress):
    solutions = get_possible_words(solutions, past_guesses)

    best_guesses = rank_next_guesses(guesses, solutions, precomputed_turns, past_guesses, display_progress)

    # top_best_guesses = best_guesses[:round(len(best_guesses) * 0.001) + 1]
    # best_guesses = [{
    #     "word": best_guess["word"],
    #     "score": get_word_score_deep(best_guess["word"], guesses, solutions)
    # } for best_guess in top_best_guesses]
    # best_guesses.sort(key = lambda x: x["score"], reverse = True)

    # print(solutions)

    best_guesses = [best_guess for best_guess in best_guesses if best_guess["score"] == best_guesses[0]["score"]]
    top_solution_gesses = [best_guess for best_guess in best_guesses if best_guess["word"] in solutions]
    if len(top_solution_gesses) != 0:
        best_guesses = top_solution_gesses


    return best_guesses

def get_turn_solve_counts(guesses, solutions):
    avg_turns = 0
    for solution in solutions:
        avg_turns += len(solve(guesses, solutions, solution, [], [], False, False))
    return (avg_turns / len(solutions))



def print_wordle(past_guesses):
    output = ""
    for past_guess in past_guesses:
        for i in range(len(past_guess["colors"])):
            if past_guess["colors"][i] == 0:
                output += f"{Style.BRIGHT}{Back.LIGHTBLACK_EX} {list(past_guess['word'])[i].upper()} {Style.RESET_ALL}"
            elif past_guess["colors"][i] == 1:
                output += f"{Style.BRIGHT}{Back.YELLOW} {list(past_guess['word'])[i].upper()} {Style.RESET_ALL}"
            else:
                output += f"{Style.BRIGHT}{Back.GREEN} {list(past_guess['word'])[i].upper()} {Style.RESET_ALL}"
        output += "\n"
    print(Style.BRIGHT + Back.LIGHTBLACK_EX + output[:-1] + Style.RESET_ALL)

def prompt_next_guess(solutions, best_guesses, past_guesses):
    _best_guesses = best_guesses.copy()
    solutions_length = len(solutions)

    known = list(max(solutions, key = len))
    known_colors = [0] * len(known)

    for i in range(len(known)):
        known_letter = True
        for solution in solutions:
            if (i >= len(solution)) or (solution[i] != known[i]):
                known_letter = False
                break
        if not known_letter:
            known[i] = "?"
        else:
            known_colors[i] = 2

    print(f"{Style.BRIGHT}{Fore.GREEN}KNOWN LETTERS:\n {Style.RESET_ALL}", end = '')
    print_wordle([{"colors": known_colors, "word": "".join(known)}])

    print(f"\n{Style.BRIGHT}{Fore.GREEN}SOLUTIONS: {Style.RESET_ALL}{'{:,}'.format(solutions_length)}")
    if len(best_guesses) > 0:
        print(f"{Style.BRIGHT}{Fore.GREEN}BEST GUESSES: {Style.RESET_ALL}")
        overflow = len(best_guesses) - 10
        best_guesses = best_guesses[:10]
        for best_guess in best_guesses:
            if best_guess["word"] in solutions:
                print(f"  {best_guess['word']} {Fore.WHITE}(possible answer){Style.RESET_ALL}")
            else:
                print(f"  {best_guess['word']}{Style.RESET_ALL}")
        if overflow > 0:
            print(f"  +{overflow} similar guesses")
    print("")
    guess = ''.join(input(f"{Style.BRIGHT}{Fore.YELLOW}GUESS:  {Style.RESET_ALL}").split()).lower()
    color_combo = list(input(f"{Style.BRIGHT}{Fore.YELLOW}COLORS: {Style.RESET_ALL}"))

    potential_past_guesses = past_guesses.copy()
    potential_past_guesses.append({
        "colors": [int(i) for i in list(color_combo)],
        "word": guess
    })
    return potential_past_guesses

def prompt_wordle_game(guesses, solutions, past_guesses, invalid, luck):
    solutions_length = len(solutions)

    if len(past_guesses) > 0:
        print_wordle(past_guesses)

    print("")
    # alphabet = {letter: -1 for letter in list("abcdefghijklmnopqrstuvwxyz")}
    #
    # for letter in alphabet:
    #     color = 0
    #     for past_guess in past_guesses:
    #         for i in range(len(past_guess["word"])):
    #             alphabet[past_guess["word"][i]] = max(alphabet[past_guess["word"][i]], past_guess["colors"][i])
    #
    # keyboard = ""
    # for letter in alphabet.items():
    #     if letter[1] == -1:
    #         keyboard += f"{Style.BRIGHT} {letter[0].upper()} {Style.RESET_ALL}"
    #     if letter[1] == 0:
    #         keyboard += f"{Style.BRIGHT}{Back.BLACK} {letter[0].upper()} {Style.RESET_ALL}"
    #     if letter[1] == 1:
    #         keyboard += f"{Style.BRIGHT}{Back.YELLOW} {letter[0].upper()} {Style.RESET_ALL}"
    #     if letter[1] == 2:
    #         keyboard += f"{Style.BRIGHT}{Back.GREEN} {letter[0].upper()} {Style.RESET_ALL}"
    #
    # print(f"{Style.BRIGHT}{Fore.GREEN}KEYBOARD:\n {Style.RESET_ALL}{keyboard}")
    #
    # print("")

    # known = list(max(solutions, key = len))
    # known_colors = [0] * len(known)
    #
    # for i in range(len(known)):
    #     known_letter = True
    #     for solution in solutions:
    #         if (i >= len(solution)) or (solution[i] != known[i]):
    #             known_letter = False
    #             break
    #     if not known_letter:
    #         known[i] = "*"
    #     else:
    #         known_colors[i] = 2
    #
    # print(f"{Style.BRIGHT}{Fore.GREEN}KNOWN LETTERS:\n {Style.RESET_ALL}", end = '')
    # print_wordle([{"colors": known_colors, "word": "".join(known)}])
    #
    # print("")

    if invalid:
        print(f"{Style.BRIGHT}{Fore.RED}INVALID{Style.RESET_ALL}")

    print(f"{Style.BRIGHT}{Fore.GREEN}LUCK: {Style.RESET_ALL}{luck}%")
    print(f"{Style.BRIGHT}{Fore.GREEN}SOLUTIONS: {Style.RESET_ALL}{'{:,}'.format(solutions_length)}")
    guess = ''.join(input(f"{Style.BRIGHT}{Fore.GREEN}GUESS: {Style.RESET_ALL}").split()).lower()

    if guess == "?":
        return random.choice(guesses)

    if guess == "!":
        return random.choice(solutions)

    if (guess in guesses):
        return guess
    else:
        system('clear')
        return prompt_wordle_game(guesses, solutions, past_guesses, True, luck)

def solve(guesses, solutions, solution, precomputed_turns, past_guesses, display_progress, hard_mode):
    solutions = get_possible_words(solutions, past_guesses)
    if hard_mode:
        guesses = solutions
    while len(solutions) > 1:
        next_guess = get_best_next_guesses(guesses, solutions, precomputed_turns, past_guesses, False)[0]["word"]

        past_guesses.append({
            "word": next_guess,
            "colors": get_color_combo(next_guess, solution)
        })

        if solution == next_guess:
            return past_guesses

        solutions = get_possible_words(solutions, past_guesses)
        if hard_mode:
            guesses = solutions
    past_guesses.append({
        "word": solution,
        "colors": [2] * len(solution)
    })

    return past_guesses

def print_hist(turn_counts):
    turn_data = {}
    for turn_count in turn_counts:
        turn_data[turn_count] = turn_data.get(turn_count, 0) + 1
    turn_data = dict(sorted(turn_data.items()))
    maximum = max(turn_data.values())
    keys = list(turn_data.keys())

    print("")

    for i in range(len(turn_data)):
        key = keys[i]
        value = turn_data[key]
        print(Style.BRIGHT + str(key) + " " + Back.GREEN + (" " * math.ceil(value / maximum * 20)) + Style.RESET_ALL + " " + str(value) + Style.RESET_ALL)
