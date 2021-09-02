import pygame
from game import Game
import constants as c

pygame.init()
pygame.display.set_caption("Hangman The Game")


YOU_WIN_SOUND = pygame.mixer.Sound('assets/you_win.mp3')
MUSIC = 'assets/song.mp3'

            
def main():
    game = Game()
    name_word = []
    run = True
    pygame.mixer.music.set_volume(game.get_volume())
    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.play(-1)

    #Eval events and draw the window in loop

    while run:
        game.draw_window(name_word)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            game.eval_window(event,name_word)
        pygame.display.update()

        if game.get_actual_window() == c.END_WINDOW:
            game.play_win_sound(YOU_WIN_SOUND)

        if game.get_is_over():
            #Restart the game
            game = Game()
            name_word = []
            game.restart_volume()
            pygame.mixer.music.set_volume(game.get_volume())

    pygame.quit()
    pass

main()
