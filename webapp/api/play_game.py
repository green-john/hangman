import http

from flask import current_app, request, abort, jsonify

from webapp.api import bp
from hangman.models import GuessInProgress

GENERATE_WORD_ENDPOINT = '/generate_word/'
CHECK_GUESS_ENDPOINT = '/check_guess/'
CALCULATE_SCORE_ENDPOINT = '/calculate_save_score/'

# Getting the dependencies from the config is very ugly. Next version
# will use a DI injector for fetching dependencies.
# TODO: Change the way of handling dependencies
DEPENDENCIES = 'DEP'


@bp.route(GENERATE_WORD_ENDPOINT, methods=['GET'])
def generate_word():
    generator = current_app.config[DEPENDENCIES]['generator']
    guess = generator.generate_guess_in_progress()

    return guess.to_json()


@bp.route(CHECK_GUESS_ENDPOINT, methods=['POST'])
def check_guess():
    checker = current_app.config[DEPENDENCIES]['checker']
    data_sent = request.get_json()
    current_guess_dict = data_sent.get('guess', '')
    current_char = data_sent.get('current_char', '')
    if not current_guess_dict or not current_char:
        abort(http.HTTPStatus.BAD_REQUEST)
        return

    current_guess = GuessInProgress.from_dict(current_guess_dict)
    check_output = checker.check(current_guess, current_char)

    return check_output.to_json()


@bp.route(CALCULATE_SCORE_ENDPOINT, methods=['POST'])
def score_and_save():
    scorer = current_app.config[DEPENDENCIES]['scorer']
    data_sent = request.get_json()
    final_guess_dict = data_sent.get('final_guess', '')
    username = data_sent.get('username', '')
    if not final_guess_dict or not username:
        abort(http.HTTPStatus.BAD_REQUEST)
        return

    final_guess = GuessInProgress.from_dict(final_guess_dict)
    score = scorer.calculate_and_save_score(final_guess, username)

    return jsonify({
        'score': score
    })
