import copy

from hangman import utils
from hangman.config import MAX_ATTEMPTS
from hangman.crypto import CryptoHasher
from hangman.models import GuessInProgress, CheckOutput


class GuessChecker:
    """
    Checks and returns a new a `GuessInProgress` in order to advance the turn
    of the player.
    """

    def __init__(self, hasher: CryptoHasher):
        """
        Creates a new `GuessChecker` using the given hasher.
        :param hasher: hasher to be used
        """
        self.hasher = hasher

    def check(self, guess_in_progress: GuessInProgress, current_guess: str) -> CheckOutput:
        """
        Checks the current guess with respect to the progress so far. Returns a new
        updated `GuessInProgress`. If the `current_guess` is in the word, it is
        added to the `correct_guesses` in the new `guess_in_progress`. Otherwise,
        it's added to the `wrong_guesses` list.

        :param guess_in_progress: progress so far
        :param current_guess: the current character the user is guessing
        :return: updated `GuessInProgress`
        """
        raw_word = self.hasher.decrypt(guess_in_progress.word_hash)
        unique_char_count = len(set(list(raw_word)))
        new_gip = copy.deepcopy(guess_in_progress)
        if current_guess in raw_word:
            indices = utils.find_all(current_guess, raw_word)
            new_gip.correct_guesses[current_guess] = indices
        else:
            new_gip.wrong_guesses.add(current_guess)

        finished = len(new_gip.wrong_guesses) >= MAX_ATTEMPTS
        if not finished:
            finished = len(new_gip.correct_guesses) >= unique_char_count

        return CheckOutput(new_gip, finished)
