import unittest
from bagels_with_words import BagelsWithWords

class BagelsWordsTestCase(unittest.TestCase):
    """Tests for 'bagels_with_words.py'."""

    def test_guess_repeating_letters(self):
        """Will a guess with repeating letters work as expected?"""
        secretword = 'taint'
        guess = 'twtat'
        clues = BagelsWithWords(5, 10).get_clues(guess, secretword)
        self.assertEqual(clues, 'Fermi Bruno Bruno Pico Fermi')
    
    def test_bagels(self):
        """Will no matching letters result in Bagels?"""
        secretword = 'taint'
        guess = 'muser'
        clues = BagelsWithWords(5, 10).get_clues(guess, secretword)
        self.assertEqual(clues, 'Bagels')
    
    def test_get_secret_word(self):
        """Will the api call result in a secret word?"""
        secretword = BagelsWithWords(5, 10).get_secret_word()
        self.assertIsNotNone(secretword)

    def test_check_if_guess_exists_false(self):
        """Is 'twtat' recognized as a non-word?"""
        guess = 'twtat'
        check = BagelsWithWords(5, 10)._check_if_guess_exists(guess)
        self.assertEqual(check, False)

    def test_check_if_guess_exists_true(self):
        """Is 'taint' recognized as a word?"""
        guess = 'taint'
        check = BagelsWithWords(5, 10)._check_if_guess_exists(guess)
        self.assertEqual(check, True)

if __name__ == '__main__':
    unittest.main()