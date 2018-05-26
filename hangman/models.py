import json
from typing import Mapping, List, Set


class GuessInProgress:
    """
    Stores information related to a guess that is currently in
    progress by the user.
    """

    def __init__(self, word_hash: str, word_length: int,
                 correct_guesses: Mapping[str, List[int]] = None,
                 wrong_guesses: Set[int] = None):
        """
        Creates a new GuessInProgress with the given `word_hash` and `word_length`.
        The set and dictionary for the wrong and correct letters are initialized empty
        if None is given.

        :param word_hash: encrypted hash of the word
        :param word_length: length of the word
        :param correct_guesses: maps each correct character to the indices where such
                                character can be found.
        :param wrong_guesses: each wrong guess the user has made.
        """
        self.word_hash = word_hash
        self.word_length = word_length
        self.correct_guesses = correct_guesses or dict()
        self.wrong_guesses = wrong_guesses or set()

    def to_dict(self) -> dict:
        """
        :return: dictionary with the info of the object
        """
        return {
            'word_hash': self.word_hash,
            'word_length': self.word_length,
            'correct_guesses': self.correct_guesses,
            'wrong_guesses': list(self.wrong_guesses),
        }

    def to_json(self) -> str:
        """
        :return: the json representation of the current object
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, _dict) -> 'GuessInProgress':
        """
        Creates an instance of the `cls` using `_dict`.
        TODO: validate fields
        :param _dict:
        :return:
        """
        word_hash = _dict.get('word_hash')
        word_length = _dict.get('word_length')
        correct_guesses = _dict.get('correct_guesses')
        wrong_guesses = set(_dict.get('wrong_guesses'))

        return cls(word_hash, word_length, correct_guesses, wrong_guesses)

    @classmethod
    def from_json(cls, _json) -> 'GuessInProgress':
        """
        Creates an instance of `cls`. Uses `_json` string.
        TODO: validate

        :param _json: raw json string
        :return: instance of `cls` with the given data
        """
        return cls.from_dict(json.loads(_json))


class CheckOutput:
    """
    Check output class used to return results from the check method
    """

    def __init__(self, guess: GuessInProgress, finished: bool):
        """
        Creates a new CheckOutput with the given params
        """
        self.guess = guess
        self.finished = finished

    def to_dict(self) -> dict:
        return {
            'next_guess': self.guess.to_dict(),
            'finished': self.finished
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

