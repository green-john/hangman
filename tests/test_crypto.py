import json
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

    def test_hash_json_serializable_deserializable(self):
        # Arrange
        word_to_encrypt = 'word'

        # Act
        encrypted = self.hasher.encrypt(word_to_encrypt)
        serialized = json.dumps(encrypted)

        # Assert
        deserialized = json.loads(serialized)
        self.assertEqual(encrypted, deserialized)
        self.assertEqual(word_to_encrypt, self.hasher.decrypt(deserialized))

