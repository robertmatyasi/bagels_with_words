import requests, json

class BagelsWithWords:
    """
    A deductive logic game where you must guess a word based on clues.
    Based on Bagels, by Al Sweigart. Inspired by Wordle. Powered by Wordnik.
    Tags: short, game, puzzle
    """
    def __init__(self, word_length, max_guesses):
        self.word_length = word_length
        self.max_guesses = max_guesses
        # This program requires a Wordnik api key.
        # Get one here: https://developer.wordnik.com
        filename = 'config.json'
        with open(filename) as f:
            self.config = json.load(f)
        self.api_key = self.config["wordnik"]["api_key"]

    def run_game(self):
        """Main loop for the game."""
        self.intro()
        while True:     # Main game loop.
            # This stores the secret number the player needs to guess:
            secret_word = self.get_secret_word()
            print('\nI have thought up a word.')
            print(f'You have {self.max_guesses} guesses to get.\n')
            # Initiate loop for guesses.
            self.guess_loop(secret_word)
            # Ask the player if they want to play again.
            print('Do you want to play again? (yes or no)')
            if not input('> ').lower().startswith('y'):
                break       
        print('Thanks for playing!')

    def intro(self):
        print(f'''\nBagels with Words, a deductive logic game.
        
Based on Bagels, by Al Sweigart. Inspired by Wordle. Powered by Wordnik.

I am thinking of a {self.word_length}-letter word.
Lower case. Not a plural. Try to guess what it is.
Here are some clues:

    When I say:   That means:
    Pico          Letter is correct but in the wrong position.
    Fermi         Letter is correct and in the right position.
    Bruno         Letter is not in the secret word.
    Bagels        No letter is correct.

For example, if the secret word was "rumba" and your guess was "raspy", 
the clues would be "Fermi Pico Bruno Bruno Bruno".''')

    def get_secret_word(self):
        """Look up a secret word with the specified length with Wordnik."""
        url = 'https://api.wordnik.com/v4/words.json/randomWord?' \
        'hasDictionaryDef=true' \
        '&includePartOfSpeech=noun%2C%20adjective%2C%20verb' \
        '%2C%20verb-intransitive%2C%20verb-transitive%2C%20adverb' \
        '%2C%20pronoun%2C%20preposition%2C%20past-participle' \
        '&excludePartOfSpeech=family-name%2C%20given-name%2C%20noun-plural' \
        '%2C%20noun-posessive%2C%20proper-noun%2C%20proper-noun-plural' \
        '%2C%20proper-noun-posessive' \
        '&minCorpusCount=10000&maxCorpusCount=-1' \
        '&minDictionaryCount=20&maxDictionaryCount=-1' \
        f'&minLength={self.word_length}&maxLength={self.word_length}' \
        f'&api_key={self.api_key}'

        while True:
            r = requests.get(url)
            if r.status_code == 200:
                response_dict = r.json()
                word = response_dict['word'].lower()
                return word

    def guess_loop(self, secret_word):
        """
        Ask user for guesses. Enumerates guesses.
        Compare guesses to secret word.
        """
        num_guesses = 1
        while num_guesses <= self.max_guesses:
            guess = ''
            # Keep looping until they enter a valid guess:
            while len(guess) != self.word_length or check != True:
                print(f'Guess #{num_guesses}: ')
                guess = input('> ')
                check = self._check_if_guess_exists(guess)
                if len(guess) != self.word_length:
                    print(f"Remember: {self.word_length}-letter word.")
                elif not check:
                    print("I don't recognize this word.")    

            clues = self.get_clues(guess, secret_word)
            print(clues)
            num_guesses += 1

            if guess == secret_word:
                break # They're correct, so break out of this loop.
            if num_guesses > self.max_guesses:
                print('You ran out of guesses.')
                print(f'The answer was {secret_word}.')

    def _check_if_guess_exists(self, guess):
        """
        Use the Wordnik api for checking whether a word exists in its
        dictionaries.
        """
        url = f'https://api.wordnik.com/v4/word.json/{guess}/definitions?' \
        'limit=200&includeRelated=false&' \
        'sourceDictionaries=ahd-5%2Ccentury%2Cwiktionary%2Cwebster%2Cwordnet&' \
        f'useCanonical=false&includeTags=false&api_key={self.api_key}'

        while True:
            r = requests.get(url)
            if r.status_code == 200:
                return True
            elif r.status_code == 404:
                return False

    def _get_frequency(self, word):
        """Take a word and return a dictionary with letters as the key and 
        their frequency as the value."""
        freq = {}
        for keys in word:
            freq[keys] = freq.get(keys, 0) + 1
        return freq

    def get_clues(self, guess, secret_word):
        """Return a string with the pico, fermi, bagels clues for a guess
        and secret word pair."""

        letter_frequency = self._get_frequency(secret_word)
        clues = ["", "", "", "", ""]

        # Correct guess.
        if guess == secret_word:
            return 'You got it!'
        # Check for all correct letters in the correct place.
        for i in range(self.word_length):
            if guess[i] == secret_word[i]:
                clues[i] = 'Fermi'
                letter_frequency[guess[i]] -= 1
        # Check the rest of the letters.
        for i in range(self.word_length):
            if clues[i] == "":
                try:
                    # A correct letter is in the incorrect place.
                    if letter_frequency[guess[i]] > 0:
                        clues[i] = 'Pico'
                        letter_frequency[guess[i]] -= 1
                    # Duplicates of correct letters already found.
                    else:
                        clues[i] = 'Bruno'
                # Incorrect letter.
                except:
                    clues[i] = 'Bruno'
        # There are no correct letters at all.  
        if all(i == "Bruno" for i in clues):
            return 'Bagels'
        else:
            # Make a single string from the list of string clues.
            return ' '.join(clues)

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    bw = BagelsWithWords(5, 10) # Five letters. Ten guesses.
    bw.run_game()