import unittest

from hangman.utilities import display_word, display_all_letters


class TestUtilities(unittest.TestCase):

    def test_display_word(self):
        self.assertEqual('a _ _ _ _ ', display_word('apple', 'a'))
        self.assertEqual('_ _ w _ ', display_word('kiwi', 'w'))

    def test_display_all_letters(self):
        self.assertEqual('A B C', display_all_letters(['A', 'B', 'C']))
        self.assertEqual('X W Z', display_all_letters(['X', 'W', 'Z']))




# if __name__ == '__main__':
#     unittest.main()