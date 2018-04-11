from unittest import TestCase

from mastermind import count_colors, evaluate_matches, Result, ai_guessing, check_guess


class TestMastermind(TestCase):

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
        count, guess = ai_guessing(solution=solution)
        print(count)
        self.assertLess(count, 13)
        self.assertTrue(check_guess(solution, guess))


if __name__ == '__main__':
    unittest.main()
