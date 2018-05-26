import unittest

from hangman import check, crypto, models
from hangman.models import CheckOutput


class CheckGuessTestCase(unittest.TestCase):
    WORD = "all"
    SECRET = "secreto"

    def setUp(self):
        self.hasher = crypto.CryptoHasher(self.SECRET)
        self.checker = check.GuessChecker(self.hasher)
        self.gip1 = models.GuessInProgress(self.hasher.encrypt(self.WORD),
                                           len(self.WORD))

    def test_check_guess_correct_guess_unfinished(self):
        # Arrange
        current_guess = 'l'

        # Act
        check_output = self.checker.check(self.gip1, current_guess)

        # Assert
        self.assertFalse(check_output.finished)
        new_gip = check_output.guess
        self.assertListEqual(new_gip.correct_guesses[current_guess], [1, 2])
        self.assertSetEqual(new_gip.wrong_guesses, set())

    def test_check_guess_wrong_guess_unfinished(self):
        # Arrange
        current_guess = 'h'

        # Act
        check_output = self.checker.check(self.gip1, current_guess)

        # Assert
        self.assertFalse(check_output.finished)
        new_gip = check_output.guess
        self.assertSetEqual(new_gip.wrong_guesses, {'h'})
        self.assertDictEqual(new_gip.correct_guesses, {})

    def test_check_guess_correct_guess_finished(self):
        # Arrange
        letters = ['a', 'l']
        indices = [[0], [1, 2]]

        # Act
        # Assert
        check_output = self.checker.check(self.gip1, letters[0])
        self.assertFalse(check_output.finished)
        new_gip = check_output.guess
        self.assertListEqual(new_gip.correct_guesses[letters[0]], indices[0])

        check_output = self.checker.check(check_output.guess, letters[1])
        self.assertTrue(check_output.finished)
        new_gip = check_output.guess
        self.assertListEqual(new_gip.correct_guesses[letters[1]], indices[1])

    def test_check_guess_wrong_guess_finished(self):
        # Arrange
        letters = ['b', 'c', 'd', 'e']
        last_guess = 'f'
        check_output = CheckOutput(self.gip1, False)

        # Act
        for guess in letters:
            check_output = self.checker.check(check_output.guess, guess)

            # Assert
            self.assertFalse(check_output.finished)

        check_output = self.checker.check(check_output.guess, last_guess)
        self.assertTrue(check_output.finished)
