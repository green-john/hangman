(function entry() {
    const generate_endpoint = '/api/v1/generate_word';
    const check_endpoint = '/api/v1/check_guess';
    const score_endpoint = '/api/v1/calculate_save_score';
    const TOTAL_LIVES = 5;
    const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    const button = document.querySelector('button.cta-start-game');
    button.addEventListener('click', requestGame);

    let guess_in_progress;

    function requestGame(event) {
        axios.get(generate_endpoint).then(res => {
            startGame(event.target, res.data);
        });
    }

    function startGame(button, first_guess) {
        guess_in_progress = first_guess;
        button.style.display = 'none';
        document.querySelector('section#game').style.display = 'grid';
        console.log(guess_in_progress);
        render_game(guess_in_progress);
    }

    function render_game(guess)  {
        // Renders the game with the given guess into #game element. The #game
        // component is assumed to have 4 divs: #lives, #blanks, #letters-unused, #letters-used
        const lives = document.querySelector('#lives');
        const blanks = document.querySelector('#blanks');
        const letters_not_used = document.querySelector('.letters#unused .container-letters');
        const letters_used = document.querySelector('.letters#used .container-letters');

        render_lives(lives, guess);
        render_blanks(blanks, guess);
        render_unused_letters(letters_not_used, guess);
        render_used_letters(letters_used, guess);
    }

    function render_lives(lives_node, guess) {
        clearChildren(lives_node);
        const remaining_lives = TOTAL_LIVES - guess.wrong_guesses.length;
        for (let i=0; i<TOTAL_LIVES; i++) {
            const live = document.createElement('span');
            live.className = 'fas fa-heart ';
            live.className += (i < remaining_lives) ? 'alive' : 'dead';
            lives_node.appendChild(live);
        }
    }

    function render_blanks(blanks_node, guess) {
        clearChildren(blanks_node);
        let word = Array(guess.word_length).fill(' ');
        for (let letter in guess.correct_guesses) if (guess.correct_guesses.hasOwnProperty(letter)){
            for (let index of guess.correct_guesses[letter]) {
                console.log('index', index, 'letter', letter);
                word[index] = letter;
            }
        }

        console.log("word: ", word);
        for (let letter of word) {
            const span = document.createElement('span');
            span.className = 'blank';
            span.innerText = letter;
            blanks_node.appendChild(span);
        }
    }

    function render_unused_letters(unused_letters_node, guess) {
        clearChildren(unused_letters_node);

        const unused = set_diff(ALPHABET, get_used_letters(guess));

        for (let letter of unused) {
            const btn = document.createElement('button');
            btn.className = 'letter';
            btn.innerText = letter;
            btn.addEventListener('click', () => {
                axios.post(check_endpoint, {
                    'guess': guess_in_progress,
                    'current_char': letter
                }).then(res => {
                    console.log(res.data.next_guess);
                    guess_in_progress = res.data['next_guess'];
                    render_game(guess_in_progress);
                    if (res.data.finished) {
                        axios.post(score_endpoint, {
                            'final_guess': guess_in_progress,
                            'username': 'fake'
                        }).then(res => {
                            const score = res.data.score;
                            alert("The game has finished and your score is " + score);
                        });
                    }
                });
            });
            unused_letters_node.appendChild(btn);
        }
    }

    function render_used_letters(used_letters_node, guess) {
        clearChildren(used_letters_node);

        for (let letter of get_used_letters(guess)) {
            const span = document.createElement('span');
            span.className = 'letter';
            span.innerText = letter;
            used_letters_node.appendChild(span);
        }
    }

    function get_used_letters(guess) {
        const used_letters = [];
        for (let letter of guess.wrong_guesses) {
            used_letters.push(letter);
        }
        for (let letter in guess.correct_guesses) {
            if (guess.correct_guesses.hasOwnProperty(letter)) {
                used_letters.push(letter);
            }
        }

        return used_letters;
    }

    function set_diff(A, B) {
        // Returns all the elements present in A but not B.
        const ans = [];
        for (let elt of A) {
            if (B.indexOf(elt) === -1) {
                ans.push(elt);
            }
        }

        return ans;
    }

    function clearChildren(elt) {
        while (elt.firstChild) {
            elt.removeChild(elt.firstChild);
        }
    }
})();