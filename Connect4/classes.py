import pygame


class Essentials(object):
    def __init__(self):
        self.board = [[-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]]
        self.unit = 85
        self.rows = 6
        self.cols = 7
        self.radius = int(self.unit / 2 - 5)
        self.h_padding = 202
        self.v_padding = 90

        self.lag = 0
        self.win_lag = 2000

        self.winner = None
        self.turn = 0


class PlayMode(object):
    def __init__(self):
        # Declaring various playing modes
        self.load = "LOAD PAGE"
        self.in_game_single_player = "SINGLE PLAYER"
        self.in_game_two_player = "TWO PLAYER"
        self.info = "INFO PAGE"
        self.win = "WINNER"


class Images(object):
    def __init__(self):
        # Loading all image files
        self.load = pygame.image.load("./images/connect4.png")
        self.help = pygame.image.load("./images/help.png")


class TextFont(object):
    def __init__(self):
        # Loading required font files
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"


class Color(object):
    def __init__(self):
        self.yellow = (255, 238, 46)
        self.dark_blue = (6, 28, 105)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
