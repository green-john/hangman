import unittest

from hangman import gen, crypto


class GenerateWordTestCase(unittest.TestCase):
    VOCAB = ["A", "B", "C"]

    def test_generate_word_success(self):
        # Arrange
        hasher = crypto.CryptoHasher("SECRET")
        word_gen = gen.GuessGenerator(hasher, self.VOCAB)

        # Act
        guess_in_progress = word_gen.generate_guess_in_progress()

        # Assert
        self.assertTrue(0 <= guess_in_progress.word_length <= 1)
        decrypted = word_gen.hasher.decrypt(guess_in_progress.word_hash)
        self.assertIn(decrypted, self.VOCAB)
