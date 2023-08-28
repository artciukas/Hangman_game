import unittest

from hangman.utilities import display_word, display_all_letters, get_random_word_length, get_random_word, word_database


class TestUtilities(unittest.TestCase):

    def test_display_word(self):
        self.assertEqual('a _ _ _ _ ', display_word('apple', 'a'))
        self.assertEqual('_ _ w _ ', display_word('kiwi', 'w'))

    def test_display_all_letters(self):
        self.assertEqual('A B C', display_all_letters(['A', 'B', 'C']))
        self.assertEqual('X W Z', display_all_letters(['X', 'W', 'Z']))

    def test_get_random_word_length(self):
        self.assertEqual("The word is 5 letters length", get_random_word_length('apple'))
        self.assertEqual("The word is 4 letters length", get_random_word_length('kiwi'))

    def test_get_random_word(self):
        random_word = get_random_word(word_database)
        self.assertIn(random_word.capitalize(), word_database)




# if __name__ == '__main__':
#     unittest.main()