from simplecrypt import encrypt as _encrypt
from simplecrypt import decrypt as _decrypt


class CryptoHasher:
    """
    Utility class used to encrypt and decrypt strings using the given message.
    """

    def __init__(self, secret):
        """
        Creates a new `CryptoHasher` with the given secre
        :param secret: (str) secret key used for encryption and decryption.
        """
        self.secret = secret

    def encrypt(self, word):
        """
        Encrypts `word`.

        :param word: (str) word to be encrypted
        :return: encrypted word
        """
        return _encrypt(self.secret, word)

    def decrypt(self, word):
        """
        Decrypts `word`.

        :param word: (str) Word to be decrypted
        :return: decrypted word
        """
        return _decrypt(self.secret, word).decode('UTF-8')
