import unittest

from hangman.utilities import display_word, display_all_letters


class TestGetSum(unittest.TestCase):

    def test_display_word(self):
        self.assertEqual('a _ _ _ _ ', display_word('apple', 'a'))

    def test_display_all_letters(self):
        self.assertEqual('A B C', display_all_letters(['A', 'B', 'C']))




# if __name__ == '__main__':
#     unittest.main()