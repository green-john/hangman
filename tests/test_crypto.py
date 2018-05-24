import unittest

from hangman.crypto import CryptoHasher

SECRET_PASSWORD = "VerysEcret"


class HashingTestCase(unittest.TestCase):

    def setUp(self):
        self.hasher = CryptoHasher(SECRET_PASSWORD)

    def test_encrypt_word(self):
        # Arrange
        word_to_encrypt = "GUSANO"

        # Act
        encrypted = self.hasher.encrypt(word_to_encrypt)

        # Assert
        self.assertEqual(self.hasher.decrypt(encrypted), word_to_encrypt)
