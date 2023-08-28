import random

word_database = ['Apple', 
                'Apricot', 
                'Avocado', 
                'Banana', 
                'Blackberry', 
                'Cherry',
                'Coconut',
                'Cucumber',
                'Durian',
                'Dragonfruit',
                'Fig',
                'Gooseberry',
                'Guava',
                'Jackfruit',
                'Plum',
                'Kiwifruit',
                'Kumquat',
                'Lemon',
                'Lime',
                'Mango',
                'Watermelon',
                'Mulberry',
                'Orange',
                'Papaya',
                'Passionfruit',
                'Peach',
                'Pear',
                'Persimmon',
                'Pineapple',
                'Pineberry',
                'Quince',
                'Raspberry',
                'Soursop',
                'Strawberry',
                'Tamarind',
                'Yuzu'
                ]


def get_random_word(word_database: list) -> str: 
    random_word = random.choice(word_database)
    upper_random_word = random_word.upper()
    return upper_random_word
    

def display_word(word: str, guessed_letters: list) -> str:
    displayed_word = ""
    for letter in word:
        if letter in guessed_letters:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "
        
    return displayed_word

def get_random_word_length(random_word: str) -> str:
    return f'The word is {len(random_word)} letters length'


def display_all_letters(unused_letters_list: list) -> str:
    joined_unused_letters_list = ' '.join(unused_letters_list)
    return joined_unused_letters_list

if __name__ == '__main__':
    pass
            
        

        



