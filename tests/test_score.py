import os
import json
import unittest

from hangman import models, score
from hangman.config import HIGHSCORE_FILE


class ScorerTestCase(unittest.TestCase):
    def test_score_finished_guess_zero_points(self):
        # Arrange
        username = "ffkl"
        gip1 = models.GuessInProgress('', 3, {}, {'a', 'b', 'c', 'd', 'e'})

        # Act
        final_score = score.GuessScorer.calculate_and_save_score(gip1, username)

        # Assert
        self.assertEqual(0, final_score)
        with open(HIGHSCORE_FILE) as f:
            scores_dict = json.load(f)
            self.assertEqual(0, scores_dict[username])

        # cleanup
        os.remove(HIGHSCORE_FILE)

    def test_score_finished_guess_100_points(self):
        # Arrange
        username = "ffkl"
        gip1 = models.GuessInProgress('', 3, {'a': [0], 'l': [1, 2]}, set())
        # Act
        final_score = score.GuessScorer.calculate_and_save_score(gip1, username)

        # Assert
        self.assertEqual(100, final_score)
        with open(HIGHSCORE_FILE) as f:
            scores_dict = json.load(f)
            self.assertEqual(100, scores_dict[username])

        # cleanup
        os.remove(HIGHSCORE_FILE)

    def test_score_finished_guess_50_points(self):
        # Arrange
        username = "ffkl"
        gip1 = models.GuessInProgress('', 2, {'a': [0], 'b': [1]},
                                       {'d', 'e'})
        # Act
        final_score = score.GuessScorer.calculate_and_save_score(gip1, username)

        # Assert
        self.assertEqual(50, final_score)
        with open(HIGHSCORE_FILE) as f:
            scores_dict = json.load(f)
            self.assertEqual(50, scores_dict[username])

        # cleanup
        os.remove(HIGHSCORE_FILE)
