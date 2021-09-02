from constants import LIVES, WINNING_POINTS
class Player:
    def __init__(self, name):
        self.name = name
        self.rounds_won = 0
        self.letters_tried = 0
        self.lives = LIVES
        self.actual_word = []
        self.points = 0

    def get_points(self):
        #Return the actual points
        return self.points

    def win_point(self):
        #Increase the points
        self.points += 1

    def get_if_player_won(self):
        #Return if the player has 3 points
        return self.points == WINNING_POINTS

    def restart_actual_word(self):
        #Restart the actual word
        self.actual_word = []

    def add_letter(self, letter):
        #Add a letter in the actual word
        self.actual_word.append(letter)

    def pop_letter(self):
        #Pop the last letter in the actual word
        self.actual_word.pop()

    def get_actual_word(self):
        #Return an string for the actual word 
        return "".join(self.actual_word)

    def get_lives(self):
        #Return the actual lives
        return self.lives

    def restart_lives(self):
        #Restart the lives to the initial status
        self.lives = 5

    def lose_live(self):
        #Decrease the lives
        if self.lives >0:
            self.lives -= 1

    def is_alive(self):
        #Return if the player is alive
        return self.lives > 0

    def set_name(self, name):
        #Set the name of the player
        self.name = name

    def __str__(self):
        #Return the name
        return f'{self.name.upper()}'