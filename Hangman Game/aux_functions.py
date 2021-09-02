from random import choice
import constants as c

def replace_accents(name_word):
    #Replace the vocals with accent
    dic_vocals = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    for i, letter in enumerate(name_word):
        name_word[i] = dic_vocals.get(letter, letter)

def random_word(archivo, name_word):
    #Return a random word from the diccionary in a tuple (Letter, A boolean that represent if has been guess)
    n = choice(range(56329))
    i = 0
    with open(archivo, encoding = 'UTF8') as f:
        for line in f:
            line = "".join(list(filter(lambda letter: letter.isalpha(), list(line))))
            if n == i:
                for letter in line.upper():
                    name_word.append(letter)
                replace_accents(name_word)
                original = name_word[:]
                for i, element in enumerate(original):
                    name_word[i] = [element, False]
                n = choice(range(len(name_word)))
                new_letter = name_word[n][0]
                name_word[n][1] = True
                for i, element in enumerate(original):
                    if name_word[i][0] == new_letter:
                        name_word[i][1] = True
                return name_word
            i += 1
        return name_word
                
def create_string_in_battle(list):
    #Return an string with a '_' in the place where the are the letters that has not been guess
    string = ''
    for element, bool in list:
        if bool:
            string += element
        else:
            string += '_ '
    return string

def create_complete_word(list):
    #Return the complete word
    string = ''
    for element, _ in list:
        string += element
    return string

def try_is_valid(word, try_word, wrong_letters):
    #Receive the complete word, the try and the letters that have been tried and are wrongs
    #Return if the try is valid

    if try_word in word:
        return False

    if try_word in wrong_letters:
        return False

    if len(try_word) == 1:
        return True

    try_word = list(try_word)
    word = list(filter(lambda letter: letter != ' ', word))

    if len(try_word) != len(word):
        return False

    for i, letter in enumerate(word):
        if letter != '_':
            if letter != try_word[i]:
                return False
    return True

def handle_one_word(list, try_letter):
    #Return the if one word is okey or if it is a mistake

    c = False
    for i, tuple in enumerate(list):
        letter, bool = tuple
        if try_letter == letter:
            if not bool:
                c = True
            list[i][1] = True
    if c:
        return True
    return False

def handle_complete_word(word_list, try_letter):
    #Return if the try (complete word) is okey or if it is wrong

    try_letter = list(try_letter)
    for i, tuple in enumerate(word_list):
        letter, _ = tuple
        if letter != try_letter[i]:
            return False
    for i, tuple in enumerate(word_list):
        letter, _ = tuple
        word_list[i][1] = True
    return True

def word_is_complete(list):
    #Return if the word has been totally guess
    for _, bool in list:
        if not bool:
            return False
    return True

def restart_game(game, list):
    #Restart the actual state of the two players

    game.restart_wrong_letters()
    game.get_player_one().restart_lives()
    game.get_player_two().restart_lives()
    game.get_player_one().restart_actual_word()
    game.get_player_two().restart_actual_word()
    game.next_player()
    list.clear()
    random_word(c.WORDS_FILE, list)

def name_is_valid(list):
    #Return if the name is valid

    if len(list) < 2 or len(list) > 9:
        return False
    if list[0] == ' ':
        list.pop(0)
    if all(map(lambda letter: letter == ' ',list)):
        return False
    contador = 0
    for letter in list:
        if letter == ' ':
            contador += 1
    return contador < 2

def try_color(word, actual_word, wrong_letters):
    #return the color green if the word is valid or the color red if it is not
    if try_is_valid(word, actual_word, wrong_letters):
        return c.GREEN
    else:
        return c.RED