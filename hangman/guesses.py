import copy
import random

from hangman.crypto import  CryptoHasher
from hangman.models import GuessInProgress, CheckOutput
from hangman.config import MAX_ATTEMPTS


class WordGenerator:
    """
    Generates a word to be guessed playing hangman. Uses the CryptHasher to
    encrypt the generated words.
    """

    def __init__(self, crypto_hasher: CryptoHasher, vocab: list):
        """
        Creates a `WordGenerator` with the given vocabulary and crypto_hasher
        :param crypto_hasher: Used to encrypt the generated word
        :param vocab: Vocabulary to be used for the word generator
        """
        self.hasher = crypto_hasher
        self.vocabulary = vocab

    def generate_guess_in_progress(self):
        """
        Selects a random word at random from the vocab and returns a GuessInProgress
        corresponding to turn 0 (i.e. No one has played yet).
        :return: GuessInProgress with the chosen word corresponding to turn 0.
        """
        word = self.vocabulary[random.randint(0, len(self.vocabulary) - 1)]
        word_length = len(word)
        word_encrypted = self.hasher.encrypt(word)

        return GuessInProgress(word_encrypted, word_length)


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

    def check(self, guess_in_progress: GuessInProgress, current_guess: str):
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
            indices = find_all(current_guess, raw_word)
            new_gip.correct_guesses[current_guess] = indices
        else:
            new_gip.wrong_guesses.add(current_guess)

        finished = len(new_gip.wrong_guesses) >= MAX_ATTEMPTS
        if not finished:
            finished = len(new_gip.correct_guesses) >= unique_char_count

        return CheckOutput(new_gip, finished)


def find_all(sub: str, a_str: str):
    """
    Finds all the occurrences of `sub` in `a_str`. returns a list
    containing all of them. This should be moved somewhere else.
    TODO: Move to a more appropriate module
    """
    indices = []
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            break
        indices.append(start)
        start += len(sub)  # use start += 1 to find overlapping matches

    return indices
