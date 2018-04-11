import random
import unittest
import itertools
from collections import namedtuple, defaultdict, OrderedDict

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


def ai_guess(guess_history):
    # for now, this will be random
    return "".join(random.choices(COLORS, k=4))


def check_guess(solution, guess):
    matches = evaluate_matches(solution, guess)
    return matches.exact_matches == 4


def ai_guessing(solution, num_trials=20):
    guess_history = []


    pure_colors = [c * 4 for c in COLORS]
    color_counts = OrderedDict()
    counter_of_colors = 0

    for guess_count, guess in enumerate(pure_colors, 1):

        matches = evaluate_matches(solution, guess)
        guess_history.append(guess)
        total_matches = matches.exact_matches  # all colors are the same, so only get exact matches
        if total_matches == 4:
            return guess_count

        color_counts[guess[0]] = total_matches

        counter_of_colors += total_matches
        if counter_of_colors == 4:
            break

    # do the factorial of strings
    initial_guess = sorted("".join([key * count for key, count in color_counts.items()]))
    for guess_count, guess_perm in enumerate(itertools.permutations(initial_guess), guess_count + 1):
        guess = "".join(guess_perm)
        matches = evaluate_matches(solution, guess)
        #print(matches)
        if matches.exact_matches == 4:
            return guess_count

    return False


class TestMastermind(unittest.TestCase):
    def test_count_colors(self):
        self.assertEqual(count_colors("ROYY"), dict(R=1, O=1, Y=2))

    def test_validation(self):
        self.assertRaises(ValueError, evaluate_matches, "ROYG", "ROYX")

    def test_fuzzy_and_exact_match(self):
        solution = "ROYY"
        guesses = [
            ("OGGR", Result(exact_matches=0, fuzzy_matches=2)),
            ("ROYY", Result(exact_matches=4, fuzzy_matches=0)),
            ("YGGP", Result(exact_matches=0, fuzzy_matches=1)),
            ("YYGG", Result(exact_matches=0, fuzzy_matches=2)),
            ("ROOP", Result(exact_matches=2, fuzzy_matches=0)),
            ("YOOR", Result(exact_matches=1, fuzzy_matches=2)),
        ]
        for guess, result in guesses:
            self.assertEqual(evaluate_matches(solution, guess), result)

    def test_ai(self):
        solution = "YROY"
        result = ai_guessing(solution=solution, num_trials=2 * 6 ** 4)
        self.assertTrue(bool(result))
        print(result)
        self.assertLess(result, 30)


if __name__ == "__main__":
    unittest.main()