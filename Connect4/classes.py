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
        self.win_lag = 1500

        self.winner = "Bot"
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
        self.background = pygame.image.load("./images/background.png")
        self.mute = pygame.image.load("./images/mute.png")
        self.unmute = pygame.image.load("./images/unmute.png")
        self.win = pygame.image.load("./images/win.png")
        self.back = pygame.image.load("./images/back.png")
        self.home = pygame.image.load("./images/home.png")
        self.red_arrow = pygame.image.load("./images/red_arrow.png")
        self.yellow_arrow = pygame.image.load("./images/yellow_arrow.png")


class TextFont(object):
    def __init__(self):
        # Loading required font files
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"


class Color(object):
    def __init__(self):
        self.yellow = (255, 238, 46)
        self.bg_blue = (69, 187, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
