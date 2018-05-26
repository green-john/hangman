import random
from typing import Sequence

from hangman.crypto import CryptoHasher
from hangman.models import GuessInProgress


class GuessGenerator:
    """
    Generates a word to be guessed playing hangman. Uses the CryptHasher to
    encrypt the generated words.
    """

    def __init__(self, crypto_hasher: CryptoHasher, vocab: Sequence[str]):
        """
        Creates a `WordGenerator` with the given vocabulary and crypto_hasher
        :param crypto_hasher: Used to encrypt the generated word
        :param vocab: Vocabulary to be used for the word generator
        """
        self.hasher = crypto_hasher
        self.vocabulary = vocab

    def generate_guess_in_progress(self) -> GuessInProgress:
        """
        Selects a random word at random from the vocab and returns a GuessInProgress
        corresponding to turn 0 (i.e. No one has played yet).
        :return: GuessInProgress with the chosen word corresponding to turn 0.
        """
        word = self.vocabulary[random.randint(0, len(self.vocabulary) - 1)]
        word_length = len(word)
        word_encrypted = self.hasher.encrypt(word)

        return GuessInProgress(word_encrypted, word_length)
