# Hangman

This is my implementation of the classic hangman game. You can play [here]() with the simple
UI I made, or you can connect to the backend [here]() and write your own beautiful frontend.

## Overview

This hangman project is a pretty fun one because the front and backend are completely
independent. This means you can use your own frontend with the backend in order to have
your own personal hangman.

## Description
TODO

## Architecture
TODO

## API

Note: All api endpoints are preceded by the `'api/v1'` prefix. Which for brevity would be
omitted. For example, when we refer to the `'/generate_word'` endpoint, we are actually
referring to the endpoint `'/api/v1/generate_word'`.

We have designed the system with a simple API with 3 endpoints:

#### `GET '/generate_word'`
This API is the beginning of the application. The user submits a request
to generate the word.

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
scores of the users. The frontend uses vanilla javascript.

## Running and Tests
To run the backend locally, do

    FLASK_APP=hangman_backend.py HANGMAN_HIGHSCORE_FILE=scores.json HANGMAN_ENV=dev flask run
    
We use the `tox` tool along with `pytest` to run our test suites. In order to
run the tests, do
    
    tox -e dev
    
