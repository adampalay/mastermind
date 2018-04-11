import random
# import unittest
import itertools
from collections import namedtuple, defaultdict, OrderedDict

import matplotlib.pyplot as plt

# 6 possible colors
COLORS = "ROYGBP"
Result = namedtuple("Result", ["exact_matches", "fuzzy_matches"])
random.seed(1)


def evaluate_matches(solution, guess):
    validate_input(solution)
    validate_input(guess)

    num_total_matches = 0
    count_solution = count_colors(solution)
    for color, num_color in count_colors(guess).items():
        num_total_matches += min(num_color, count_solution[color])

    num_exact_matches = 0
    for color_guess, color_solution in zip(guess, solution):
        if color_guess == color_solution:
            num_exact_matches += 1

    return Result(exact_matches=num_exact_matches, fuzzy_matches=num_total_matches - num_exact_matches)


def validate_input(color_string):
    if not isinstance(color_string, str):
        raise ValueError("Should be string")

    if len(color_string) != 4:
        raise ValueError("Should be of length 4")

    if not (set(color_string) <= set(COLORS)):
        raise ValueError("String contains an invalid color")


def count_colors(color_string):
    color_count = defaultdict(int)
    for c in color_string:
        color_count[c] += 1

    return color_count


def check_guess(solution, guess):
    matches = evaluate_matches(solution, guess)
    return matches.exact_matches == 4


def ai_guessing(solution):

    pure_colors = [c * 4 for c in COLORS]  # RRRR
    color_counts = OrderedDict()
    counter_of_colors = 0

    for guess_count, guess in enumerate(pure_colors[:-1], 1):

        matches = evaluate_matches(solution, guess)
        total_matches = matches.exact_matches  # all colors are the same, so only get exact matches
        if total_matches == 4:
            return guess_count, guess

        if total_matches > 0:
            color_counts[guess[0]] = total_matches

        counter_of_colors += total_matches
        if counter_of_colors == 4:
            break

    if counter_of_colors < 4:
        color_counts[pure_colors[-1][0]] = 4 - sum(color_counts.values())

    # check positions using placeholders

    placeholder = sorted(set(COLORS) - set(color_counts.keys()))[0]

    our_solution = [placeholder for _ in range(4)]

    number_existing_matches = 0
    search_colors = list(color_counts.keys())
    last_color = search_colors.pop()
    for color in search_colors:
        matches_for_color = color_counts[color]
        matches_found_for_color = 0
        for i in range(3):
            if our_solution[i] != placeholder:
                continue
            our_solution[i] = color
            guess = "".join(our_solution)
            matches = evaluate_matches(solution, guess)
            guess_count += 1
            if matches.exact_matches > number_existing_matches:  # should be
                our_solution[i] = color
                number_existing_matches += 1
                matches_found_for_color += 1
            else:
                our_solution[i] = placeholder

            if matches_found_for_color == matches_for_color:
                break

        if matches_found_for_color < matches_for_color:
            our_solution[3] = color
            number_existing_matches += 1

    our_solution = "".join([(x if x != placeholder else last_color) for x in our_solution])

    return guess_count + 1, our_solution


if __name__ == "__main__":
    distribution = []
    for permutation in itertools.permutations(COLORS * 4, r=4):
        solution = "".join(permutation)
        count, guess = ai_guessing(solution)
        assert (check_guess(solution, guess))
        distribution.append(count)

    winners = sum([int(x <= 10) for x in distribution])
    print("{:.2f}% winners".format(100 * winners / len(distribution)))

    plt.hist(distribution)
    plt.show()
