import os

from hangman.crypto import CryptoHasher
from hangman.check import GuessChecker
from hangman.score import GuessScorer
from hangman.gen import GuessGenerator
from webapp import create_app

VOCAB = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
HANGMAN_SECRET = 'this is the most hidden secret'

# All this dependencies should be injected using a DI library
# or at least a better method
# TODO: use a DI library for this
hasher = CryptoHasher(HANGMAN_SECRET)
generator = GuessGenerator(hasher, VOCAB)
checker = GuessChecker(hasher)


app = create_app(os.environ.get('HANGMAN_ENV', 'dev'), generator, checker, GuessScorer)
