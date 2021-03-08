import pygame


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


class TextFont(object):
    def __init__(self):
        # Loading required font files
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"


class Color(object):
    def __init__(self):
        self.yellow = (255, 238, 46)