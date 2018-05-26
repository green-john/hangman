import json
import unittest

from hangman.models import GuessInProgress, CheckOutput
from webapp import create_app

GUESS_IN_PROGRESS1 = GuessInProgress("hash", 3)


class MockGenerator:
    def generate_guess_in_progress(self):
        return GUESS_IN_PROGRESS1


class MockChecker:
    def check(self, guess_in_progress, current_guess):
        return CheckOutput(GUESS_IN_PROGRESS1, False)


class MockScorer:
    def calculate_and_save_score(self, final_guess, username):
        return 0


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test', MockGenerator(), MockChecker(), MockScorer())
        self.client = self.app.test_client()

    def test_generate_word(self):
        # Arrange
        # Act
        response = self.client.get('/api/v1/generate_word/')

        # Assert
        self.assertEqual(200, response.status_code)
        gip = GuessInProgress.from_json(response.data.decode('UTF-8'))
        self.assertEqual('hash', gip.word_hash)
        self.assertEqual(3, gip.word_length)

    def test_check_word(self):
        # Arrange
        current_char = 'a'
        data_to_send = {
            'guess': GUESS_IN_PROGRESS1.to_dict(),
            'current_char': current_char
        }
        # Act
        response = self.client.post('/api/v1/check_guess/', data=json.dumps(data_to_send),
                                    content_type='application/json')

        # Assert
        self.assertEqual(200, response.status_code)
        data_received = json.loads(response.data.decode('UTF-8'))
        self.assertIn('next_guess', data_received)
        self.assertIn('finished', data_received)

    def test_check_solution_and_save(self):
        # Arrange
        data_to_send = {
            'final_guess': GUESS_IN_PROGRESS1.to_dict(),
            'username': 'pedro'
        }

        # Act
        response = self.client.post('/api/v1/calculate_save_score/', data=json.dumps(data_to_send),
                                    content_type='application/json')

        # Assert
        self.assertEqual(200, response.status_code)
        data_received = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data_received.get('score', ''), int)
