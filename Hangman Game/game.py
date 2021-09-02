import pygame
from player import Player
import aux_functions as af
import constants as c
from random import choice
pygame.init()

#Window
WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

#Fonts
FONT = pygame.font.SysFont('Comic Sans MS', int(c.WIDTH * 0.0375))
SMALL_FONT = pygame.font.SysFont('Comic Sans MS', int(c.WIDTH * 0.025))
BIG_FONT = pygame.font.SysFont('Comic Sans MS', int(c.WIDTH * 0.0375))
BIG_FONT_2 = pygame.font.SysFont('Comic Sans MS', int(c.WIDTH * 0.0625))

#Texts
WELCOME_TEXT = FONT.render('WELCOME TO: HANGMAN GAME', False, (0, 0, 0))
PRESS_ENTER = SMALL_FONT.render('PRESS ENTER TO START', False, (0, 0, 0))
ENTER_YOUR_TRY = SMALL_FONT.render('TRY ONE LETTER OR THE WHOLE WORD(1 SHOT)', False, (0, 0, 0))
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/background.png'),(c.WIDTH,c.HEIGHT))
PERSON_INTRO = pygame.transform.scale(pygame.image.load('assets/intro_person.png'),(c.WIDTH//2,c.HEIGHT//2))
YOU_WIN_IMG = pygame.transform.scale(pygame.image.load('assets/you_win_img.png'),(c.WIDTH//2,c.HEIGHT//2))
HEART = pygame.transform.scale(pygame.image.load('assets/heart.png'),(c.WIDTH//34,c.WIDTH//34))
TROPHY = pygame.transform.scale(pygame.image.load('assets/trophy.png'),(c.WIDTH//30,c.WIDTH//30))

#Sounds
WRONG_SOUND = pygame.mixer.Sound('assets/wrong_word.wav')
POINT_SOUND = pygame.mixer.Sound('assets/point_sound.wav')
KEY_PRESSED = pygame.mixer.Sound('assets/key_press.wav')
WORD_COMPLETE = pygame.mixer.Sound('assets/word_complete.wav')
WRONG_TRY = pygame.mixer.Sound('assets/wrong_try.mp3')

class Game:
    def __init__(self):
        self.is_over = False
        self.actual_window = c.INITIAL_WINDOW
        self.player_one = None
        self.player_two = None
        self.actual_player = 1
        self.count_names = 0
        self.wrong_letters = []
        self.winning_player = None
        self.volume = 0.1
        self.win_sound_was_played = False
        self.last_word = ''

    def play_win_sound(self, sound):
        #Play the wind sound (only can be played once)
        if not self.win_sound_was_played:
            pygame.mixer.Sound.play(sound)
        self.win_sound_was_played = True
            
    def end_game(self):
        #End the actual game
        self.is_over = True

    def get_is_over(self):
        #Return if the game is over
        return self.is_over
        
    def get_volume(self):
        #Return the actual volume of the music
        return self.volume

    def get_last_word(self):
        #Return the last word
        return self.last_word
    
    def set_last_word(self, word):
        #Set the last word
        self.last_word = word

    def increase_volume(self):
        #Increase the volume of the music
        self.volume += 0.08
    
    def restart_volume(self):
        #Restart the volumen
        self.volume = 0.1

    def set_winning_player(self, player):
        #Set the player that has won
        self.winning_player = player

    def get_winning_player(self):
        #Return the player that has won
        return self.winning_player

    def restart_wrong_letters(self):
        #Restart the actual wrong letters
        self.wrong_letters = []

    def get_wrong_letters(self):
        #Get an string that represents the letters that has been tried and are wrong
        if len(self.wrong_letters) == 1:
            return self.wrong_letters[0]
        string = ', '.join(self.wrong_letters)
        return string

    def add_wrong_letter(self, letter):
        #Add one wrong letter
        self.wrong_letters.append(letter)

    def set_actual_player(self, player):
        #Set actual player
        if self.actual_player == 1:
            self.player_one = player
        else:
            self.player_two = player

    def get_player(self):
        #Get the actual player
        if self.actual_player == 1:
            return self.player_one
        else:
            return self.player_two

    def set_random_player(self):
        self.actual_player = choice([1, 2])

    def players(self):
        #Return the names of the players
        return (str(self.player_one), str(self.player_two))

    def add_count_names(self):
        #Add one count names that represent how many player have been created
        self.count_names += 1

    def get_count_names(self):
        #Get the count names
        return self.count_names

    def get_actual_player(self):
        #Return the number of the actual player
        return self.actual_player

    def get_player_one(self):
        #Get the player one
        return (self.player_one)

    def get_player_two(self):
        #Get the player two
        return (self.player_two)

    def get_name_player(self):
        #Get the name of the actual player
        if self.actual_player == 1:
            return str(self.player_one)
        else:
            return str(self.player_two)
        
    def next_player(self):
        #Set the actual player with the next
        if self.actual_player == 1:
            self.actual_player = 2
        else:
            self.actual_player = 1

    def next_window(self):
        #Set the actual window with the next
        if self.actual_window == c.INITIAL_WINDOW:
            self.actual_window = c.INSERT_NAME_WINDOW
        elif self.actual_window == c.INSERT_NAME_WINDOW:
            self.actual_window = c.BATTLE_WINDOW
        else:
            self.actual_window = c.END_WINDOW

    def get_actual_window(self):
        #Return the actual window
        return self.actual_window

    def _draw_initial_window(self):

        WIN.blit(PERSON_INTRO,(c.WIDTH//2-PERSON_INTRO.get_width()/2,c.HEIGHT//2))
        WIN.blit(WELCOME_TEXT,(c.WIDTH/4 - c.WIDTH*0.0375, c.HEIGHT/4 - c.HEIGHT*0.2))
        WIN.blit(PRESS_ENTER,(c.WIDTH/2-PRESS_ENTER.get_width()/2,c.HEIGHT/4))

    def _draw_insert_name_window(self, list):
        word = "".join(list)
        name_text = BIG_FONT.render(word.upper(), False, (0, 0, 0))

        INSERT_YOUR_NAME = BIG_FONT.render(f'INSERT YOUR NAME(PLAYER {self.get_actual_player()})', False, (0, 0, 0))
        WIN.blit(INSERT_YOUR_NAME ,(c.WIDTH/4,c.HEIGHT/4))
        WIN.blit(name_text,(c.WIDTH/2-name_text.get_width()/2, c.HEIGHT/4 + c.HEIGHT*0.2))

    def _draw_things(self,img,  x, y, n):
        dx = 0
        for _ in range(n):
            WIN.blit(img,(x + dx, y))
            dx += c.WIDTH*0.0375

    def _draw_battle_window(self, list):
        word = af.create_string_in_battle(list)
        turn_name = BIG_FONT.render(f'Turn of {str(self.get_player())}', False, (0, 0, 0))
        word_obj = BIG_FONT_2.render(word, False, (0, 0, 0))
        name_1 = FONT.render(str(self.get_player_one()), False, (0, 0, 0))
        name_2 = FONT.render(str(self.get_player_two()), False, (0, 0, 0))
        wrong_letters_obj = BIG_FONT.render(self.get_wrong_letters(), False, c.RED)
        last_word = SMALL_FONT.render(f'LAST WORD: {self.get_last_word()}', False, (0, 0, 0))

        WIN.blit(ENTER_YOUR_TRY,((c.WIDTH//2-ENTER_YOUR_TRY.get_width()/2),c.HEIGHT//2))
        WIN.blit(turn_name,((c.WIDTH//2-turn_name.get_width()/2),c.HEIGHT//9))
        WIN.blit(word_obj,((c.WIDTH//2-word_obj.get_width()/2),c.HEIGHT//4))
        WIN.blit(name_1, (c.WIDTH//6-name_1.get_width()//2, c.HEIGHT*5//6))
        WIN.blit(name_2, (c.WIDTH*5//6 - name_2.get_width(), c.HEIGHT*5//6))
        WIN.blit(last_word,((c.WIDTH//2-last_word.get_width()/2),c.HEIGHT//22))
        WIN.blit(wrong_letters_obj,((c.WIDTH//2-wrong_letters_obj.get_width()/2),c.HEIGHT//2 + c.HEIGHT*0.2))
        
        actual_word = self.get_player().get_actual_word()
        actual_word_obj = BIG_FONT.render(actual_word.upper(), False, af.try_color(word, actual_word, self.get_wrong_letters()))
        WIN.blit(actual_word_obj,((c.WIDTH//2-actual_word_obj.get_width()/2),c.HEIGHT//2 + c.HEIGHT*0.1))
        
        lives_one = self.get_player_one().get_lives()
        lives_two = self.get_player_two().get_lives()

        self._draw_things(HEART, c.WIDTH//6 - name_1.get_width()//2, (c.HEIGHT*5//6) + c.HEIGHT*0.1, lives_one)
        self._draw_things(HEART, c.WIDTH*5//6 - name_2.get_width(), (c.HEIGHT*5//6) + c.HEIGHT*0.1, lives_two)
        
        points_one = self.get_player_one().get_points()
        points_two = self.get_player_two().get_points()

        self._draw_things(TROPHY,c.WIDTH//6 - name_1.get_width()//2, (c.HEIGHT*5//6) - c.HEIGHT*0.08, points_one)
        self._draw_things(TROPHY,c.WIDTH*5//6 - name_2.get_width(), c.HEIGHT*5//6 - c.HEIGHT*0.08, points_two)
        

    def _draw_end_window(self):
        last_word = SMALL_FONT.render(f'LAST WORD: {self.get_last_word()}', False, (0, 0, 0))
        winnig_player = BIG_FONT_2.render(f'{self.get_winning_player()}!', False, (0, 0, 0))
        
        WIN.blit(YOU_WIN_IMG,(c.WIDTH//2-YOU_WIN_IMG.get_width()/2,c.HEIGHT//5))
        WIN.blit(winnig_player,(c.WIDTH/2-winnig_player.get_width()/2,c.HEIGHT*3/4))
        WIN.blit(last_word,((c.WIDTH//2-last_word.get_width()/2),c.HEIGHT//22))
    
    def draw_window(self, list):
        WIN.blit(BACKGROUND,(0,0))

        if self.get_actual_window() == c.INITIAL_WINDOW:
            self._draw_initial_window()
            return

        if self.get_actual_window() == c.INSERT_NAME_WINDOW:
            self._draw_insert_name_window(list)
            return
        
        if self.get_actual_window() == c.BATTLE_WINDOW:
            self._draw_battle_window(list)
            return

        if self.get_actual_window() == c.END_WINDOW:
            self._draw_end_window()

    def _eval_initial_window(self, event):

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            if key == 'return':
                pygame.mixer.Sound.play(KEY_PRESSED)
                self.next_window()
                return

    def _eval_insert_name_window(self, event, list):

        if event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            if key.isalpha() and len(key) == 1:
                pygame.mixer.Sound.play(KEY_PRESSED)
                list.append(key)

            if key == 'backspace' and len(list) > 0:
                pygame.mixer.Sound.play(KEY_PRESSED)
                list.pop()

            if key == 'return' and af.name_is_valid(list):
                pygame.mixer.Sound.play(KEY_PRESSED)
                self.set_actual_player(Player(''.join(list)))
                list.clear()
                self.add_count_names()
                self.next_player()
                if self.get_count_names() == 2:
                    self.set_random_player()
                    self.next_window()
                    af.random_word(c.WORDS_FILE,list)

    def _eval_battle_window(self, event, list):
        actual_player = self.get_player()
        word = af.create_string_in_battle(list)
        try_word = self.get_player().get_actual_word()

        if event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            if key.isalpha() and len(key) == 1:
                pygame.mixer.Sound.play(KEY_PRESSED)
                actual_player.add_letter(key.upper())

            if key == 'backspace' and len(actual_player.get_actual_word())>0:
                pygame.mixer.Sound.play(KEY_PRESSED)
                actual_player.pop_letter()

            if key == 'return' and af.try_is_valid(word, try_word, self.get_wrong_letters()):

                pygame.mixer.Sound.play(KEY_PRESSED)
                if len(try_word) == 1:
                    if af.handle_one_word(list, try_word):
                        pygame.mixer.Sound.play(POINT_SOUND)
                        self.get_player().restart_actual_word()
                    else:
                        pygame.mixer.Sound.play(WRONG_SOUND)
                        self.get_player().lose_live()
                        self.add_wrong_letter(try_word)
                        self.get_player().restart_actual_word()
            
                else:
                    if not af.handle_complete_word(list, try_word):
                        self.set_last_word(af.create_complete_word(list))
                        pygame.mixer.Sound.play(WRONG_TRY)
                        self.next_player()
                        self.get_player().win_point()
                        self.increase_volume()
                        pygame.mixer.music.set_volume(self.get_volume())
                        af.restart_game(self, list)

                if af.word_is_complete(list):
                    self.set_last_word(af.create_complete_word(list))
                    self.increase_volume()
                    pygame.mixer.music.set_volume(self.get_volume())
                    pygame.mixer.Sound.play(WORD_COMPLETE)
                    self.get_player().win_point()
                    af.restart_game(self, list)   
                elif len(try_word) == 1:
                    self.next_player() 
            

            if not self.get_player_one().is_alive():
                self.set_last_word(af.create_complete_word(list))
                pygame.mixer.Sound.play(WRONG_TRY)
                self.get_player_two().win_point()
                af.restart_game(self, list)
                 

            if not self.get_player_two().is_alive():
                self.set_last_word(af.create_complete_word(list))
                pygame.mixer.Sound.play(WRONG_TRY)
                self.get_player_one().win_point()
                af.restart_game(self, list)
                 
            
            if self.get_player_one().get_if_player_won():
                self.next_window()
                self.set_winning_player(self.get_player_one())
            
            if self.get_player_two().get_if_player_won():
                self.next_window()
                self.set_winning_player(self.get_player_two())
            return

    def _eval_end_window(self, event):
        if event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                if key == 'return':
                    self.end_game()


    def eval_window(self, event, list):

        if self.get_actual_window() == c.INITIAL_WINDOW:
            self._eval_initial_window(event)
            return
            
        if self.get_actual_window() == c.INSERT_NAME_WINDOW:
            self._eval_insert_name_window(event, list)
            return
            
        if self.get_actual_window() == c.BATTLE_WINDOW:
            self._eval_battle_window(event, list)
            return

        if self.get_actual_window() == c.END_WINDOW:
            self._eval_end_window(event)
            return
        
