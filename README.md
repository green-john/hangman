# Hangman
This is my implementation of the classic hangman game. The front and backend are independent
which means you can use my frontend or create a new one to play the game.

## Overview
This is a python implementation of the classical hangman game. It works by encrypting the
word being guessed and sending the encrypted string back and forth to the server to check
the different guesses and the final score of a user. This document explains the architecture
as well as the API that can be used to play the game.

## Architecture
The core logic of the application can be found in the `hangman` module. There you will find
different files, each concerning the generation, checking, scoring or encryption of words.
Each file is named according to the components it contains.

On top of this core layer, we have a web layer made with flask that we use to make our
business logic available to the world. The decision to keep api and logic separate was an
easy one because it allows for easier testability and extensibility.

## API
Note: All api endpoints are preceded by the `'api/v1'` prefix. Which for brevity would be
omitted. For example, when we refer to the `'/generate_word'` endpoint, we are actually
referring to the endpoint `'/api/v1/generate_word'`.

The system has 3 endpoints

#### `GET '/generate_word'`
This API is the beginning of the application. The user submits a request to generate
a word.

##### Input
None

##### Output

    GuessInProgress {
        word_hash: string
        word_length: int
        correct_guesses: map<char, list<int>>
        wrong_guesses: set<char>
    }

`GuessInProgress` is an object we use throughout our API to represent the status of a current guess.
`word_hash` contains a cryptographic hash of the word being guessed. This enables our hangman
backend to be stateless. `word_length` is the length of the word. `correct_guesses` maps every
letter that has correctly been guessed to the indices that such letter belongs to. `wrong_guesses`
is a set with the letters that do not appear anywhere in the word. 

#### `POST '/check_guess'`
Updates the `GuestInProgress` object and returns whether the game has finished or not.

##### Input
    
    CheckGuessInput {
        guess: GuessInProgress
        current_char: char
    }
    
##### Output

    CheckGuessOutput {
        finished: bool
        next_guess: GuessInProgress
    }

#### `POST '/calculate_save_score'`
Calculates and stores the score of the user. If the guess is not finished,
it returns a negative score. The scoring algorithm works as follows:

    score = unique_letter_count / total_attempts * 100.
    
The max score is 100. The more a person tries, the lower score they will get. 

##### Input
    
    CalculateScoreInput {
        final_guess: GuessInProgress
        username: string
    }
    
##### Output

    CalculateScoreOutput {
        score: int
    }

## Tech Stack
The backend uses python and flask. It uses a simple json file to store the
scores of the users. The frontend uses vanilla javascript and pug.

## Running and Tests
Make sure you use Python3.5+ to run the app.

First install all the requirements, better still if its on a virtual env

    pip install -r requirements.txt

To run the backend locally, do

    FLASK_APP=hangman_backend.py HANGMAN_HIGHSCORE_FILE=scores.json HANGMAN_ENV=dev flask run
    
We use the `tox` tool along with `pytest` to run our test suites. In order to
run the tests, do
    
    tox -e dev
    
## Gotchas & TODOs
- The dependencies on the backend should be injected in a better way. Right now we use
the flask config to place the dependencies there.
- The encryption algorithms take a long time to encrypt/decrypt. We should mock them
in the test in order to save time when the tests are being run.
- Alternatively, use a crypto library that allows for configuration of parameters in
order to ease them out when testing.
