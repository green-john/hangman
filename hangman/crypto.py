import base64

from simplecrypt import encrypt as _encrypt
from simplecrypt import decrypt as _decrypt


class CryptoHasher:
    """
    Utility class to encrypt and decrypt strings using the given secret.
    """

    def __init__(self, secret: str):
        """
        Creates a new `CryptoHasher` with the given `secret`
        :param secret: secret key used for encryption and decryption.
        """
        self.secret = secret

    def encrypt(self, word: str) -> str:
        """
        Encrypts `word` and encodes it using base64 encoding in order to make it
        json friendly

        :param word: word to be encrypted
        :return: encrypted word
        """
        encrypted_bytes = _encrypt(self.secret, word)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, word: str) -> str:
        """
        Decrypts `word`.

        :param word: (str) Word to be decrypted
        :return: decrypted word
        """
        word_bytes = base64.b64decode(word)
        return _decrypt(self.secret, word_bytes).decode('UTF-8')
