import os
import json

from hangman.guesses import GuessInProgress
from hangman.config import MAX_ATTEMPTS, HIGHSCORE_FILE


class GuessScorer:
    """
    Scores the last guess from the user.
    """

    @staticmethod
    def calculate_and_save_score(last_guess: GuessInProgress, username: str):
        """
        Scores the last guess that the user made. If it is not the last guess
        returns a negative score. See readme for how to calculate the score.

        :param last_guess: the last_guess made by the user
        :param username: name of the user
        :return: score from 1 to 100.
        """
        score = -1
        if len(last_guess.wrong_guesses) < MAX_ATTEMPTS:
            total_known = sum(len(x) for x in last_guess.correct_guesses.values())

            if total_known == last_guess.word_length:
                score = len(last_guess.correct_guesses) / \
                        (len(last_guess.correct_guesses) + len(last_guess.wrong_guesses))
        else:
            score = 0

        if not os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'w') as f:
                f.write('{}')

        score = int(score * 100)
        GuessScorer._update_file(HIGHSCORE_FILE, username, score)

        return score

    @staticmethod
    def _update_file(file_name: str, username: str, score: int):
        with open(file_name) as f:
            json_dict = json.load(f)

        json_dict[username] = score

        with open(file_name, 'w') as f:
            json.dump(json_dict, f)
