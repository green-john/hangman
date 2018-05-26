from typing import Type

from flask import Flask

from hangman.score import GuessScorer
from hangman.gen import GuessGenerator
from hangman.check import GuessChecker
from webapp.config import config

API_PREFIX = '/api/v1'
DEPENDENCIES = 'DEP'


def create_app(config_name: str, guess_gen: GuessGenerator,
               guess_check: GuessChecker, guess_score: Type[GuessScorer]):
    """
    Creates the application with the specified configuration that uses
    the given guess generator, checker and scorer.
    These dependencies are passed as parameters in order to make the
    webapp easier to test.

    :param config_name: name of the configuration to use.
    :param guess_gen: guess generator
    :param guess_check: guess checker
    :param guess_score: guess scorer
    :return: application initialized
    """
    static_url = config[config_name].STATIC_URL_PATH
    static_folder = config[config_name].STATIC_FOLDER
    app = Flask(__name__, static_url_path=static_url, static_folder=static_folder)
    app.config.from_object(config[config_name])
    app.url_map.strict_slashes = False

    from webapp.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix=API_PREFIX)

    dependencies = {
        'generator': guess_gen,
        'checker': guess_check,
        'scorer': guess_score
    }

    # Uses the config to store the dependencies for now.
    # this is very very very ugly and should be handled by a
    # dependency injection library.
    # TODO: do DI with a library

    app.config[DEPENDENCIES] = dependencies

    return app
