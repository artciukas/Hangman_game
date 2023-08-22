import random


# from database_crud import get_all_words


word_database = ['table', 'watermelon', 'lemon', 'apple']
unused_letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
guessed_letters = []
lives = 7

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

# def print_hangman_picture(lives: int) -> str:
#     if lives == 7:
#         return lives_visual_dict[7]
#     elif lives == 6:
#         return lives_visual_dict[6]
#     elif lives == 5:
#         return lives_visual_dict[5]
#     elif lives == 4:
#         return lives_visual_dict[4]
#     elif lives == 3:
#         return lives_visual_dict[3]
#     elif lives == 2:
#         return lives_visual_dict[2]
#     elif lives == 1:
#         return lives_visual_dict[1]
#     elif lives == 0:
#         return lives_visual_dict[0]





if __name__ == '__main__':

    print('!!!=-Welcome to hangman game-=!!!')
    random_word = get_random_word(word_database)
    print(f'Answer: {random_word}')
    while lives > 0:
        print(f'Word are: {display_word(random_word, guessed_letters)}')
        print(get_random_word_length(random_word))
        print(f'{print_hangman_picture(lives)}')
        print("******************************************")
        print('Available letters:')
        print(display_all_letters(unused_letters_list))
        print("******************************************")
        user_guess = input('Please enter a letter: ').upper()
        if user_guess in guessed_letters:
            print('Letter was already used!!!')
            print("############################")
        elif user_guess.isalpha() and len(user_guess) == 1:
            guessed_letters.append(user_guess)

            if user_guess in random_word:
                print('Correct. This letter is in the word')
                unused_letters_list.remove(user_guess)
                print("############################")
            else:
                lives -= 1
                print('This letter does not exist in the word')
                print("############################")
            
        else:
            print('Please enter single letter!')
            print("############################")

        if "_" not in display_word(random_word, guessed_letters):
            print("\nCongratulations! You guessed the word:", random_word)
            break
    else:
        print(f'{print_hangman_picture(lives)}')
        print(f'GAME OVER. The word was {random_word}')
            
        

        



