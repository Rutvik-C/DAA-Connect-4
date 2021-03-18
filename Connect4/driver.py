import math
import random

from classes import *
from threading import Thread
import time

pygame.init()

# Creating root window
root = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Connect 4")

# Making class objects
ess = Essentials()
pm = PlayMode()
img = Images()
fnt = TextFont()
col = Color()

play_state = pm.load
game_mode = pm.in_game_single_player
active = True
user_turn = True
initial = True
t = None
done = False
lag = 0
win_lag = 0


def is_valid(c):
    return ess.board[ess.rows - 1][c] == -1


def make_move(c, player):
    r = 0
    for r in range(ess.rows):
        if ess.board[r][c] == -1:
            break

    print("put at r =", r, "c =", c)
    ess.board[r][c] = player

    for i in ess.board:
        print(i)


def is_winner(player):

    # HORIZONTAL WIN
    for i in range(ess.rows):
        for j in range(ess.cols - 3):
            if ess.board[i][j] == player and ess.board[i][j + 1] == player and ess.board[i][j + 2] == player and ess.board[i][j + 3] == player:
                return True

    # VERTICAL WIN
    for i in range(ess.rows - 3):
        for j in range(ess.cols):
            if ess.board[i][j] == player and ess.board[i + 1][j] == player and ess.board[i + 2][j] == player and ess.board[i + 3][j] == player:
                return True

    # FORWARD DIAGONAL WIN
    for i in range(3, ess.rows):
        for j in range(ess.cols - 3):
            if ess.board[i][j] == player and ess.board[i - 1][j + 1] == player and ess.board[i - 2][j + 2] == player and ess.board[i - 3][j + 3] == player:
                return True

    # BACKWARD DIAGONAL WIN
    for i in range(ess.rows - 3):
        for j in range(ess.cols - 3):
            if ess.board[i][j] == player and ess.board[i + 1][j + 1] == player and ess.board[i + 2][j + 2] == player and ess.board[i + 3][j + 3] == player:
                return True

    return False


def AI_logic():
    global done

    c = random.randint(0, ess.cols - 1)
    if is_valid(c):
        make_move(c, ess.turn)

    draw_board()

    done = True


def play_AI():
    global user_turn, t, done, initial, play_state

    if initial:
        initial, done = False, False
        t = Thread(target=AI_logic)
        t.start()

    if done:

        if is_winner(ess.turn):
            ess.winner = ess.turn
            play_state = pm.win

        ess.turn = (ess.turn + 1) % 2
        user_turn = True


def draw_board():
    pygame.draw.rect(root, col.black, (ess.h_padding, ess.v_padding, 595, 510))
    for r in range(ess.rows):
        for c in range(ess.cols):
            pygame.draw.circle(root, col.dark_blue, (int(c * ess.unit + ess.unit / 2 + ess.h_padding), int(r * ess.unit + ess.unit / 2 + ess.v_padding)), ess.radius)

    for r in range(ess.rows):
        for c in range(ess.cols):
            if ess.board[r][c] == 0:
                pygame.draw.circle(root, col.red, (ess.h_padding + int(c * ess.unit + ess.unit / 2), 600 - int(r * ess.unit + ess.unit / 2)), ess.radius)

            elif ess.board[r][c] == 1:
                pygame.draw.circle(root, col.yellow, (ess.h_padding + int(c * ess.unit + ess.unit / 2), 600 - int(r * ess.unit + ess.unit / 2)), ess.radius)


while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

        # Mouse motion
        if inp.type == pygame.MOUSEMOTION:
            if play_state in (pm.in_game_two_player, pm.in_game_single_player) and ess.h_padding - 100 <= inp.pos[0] <= ess.h_padding + 595 + 100:
                if 100 <= inp.pos[0] <= 500:
                    pygame.draw.circle(root, col.red, (300, 47), ess.radius)
                # pygame.display.update()

        # Mouse click Check
        if inp.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()  # Fetching mouse click location
            # print(m)

            if play_state == pm.in_game_two_player:  # TWO PLAYER MODE
                column = int(math.floor((m[0] - ess.h_padding) / ess.unit))
                print("col:", column)
                if 0 <= column <= 6 and is_valid(column):
                    print("Valid")
                    make_move(column, ess.turn)

                    ess.turn = (ess.turn + 1) % 2

            if play_state == pm.in_game_single_player:  # SINGLE PLAYER MODE
                column = int(math.floor((m[0] - ess.h_padding) / ess.unit))
                print("col:", column)
                if 0 <= column <= 6 and is_valid(column) and user_turn:
                    print("Valid")
                    make_move(column, ess.turn)

                    if is_winner(ess.turn):
                        ess.winner = ess.turn
                        play_state = pm.win

                    ess.turn = (ess.turn + 1) % 2
                    user_turn = False
                    initial = True

            if (20 <= m[0] <= 45 and 155 <= m[1] <= 190) or (200 <= m[0] <= 230 and 155 <= m[1] <= 190):
                if game_mode == pm.in_game_two_player:
                    game_mode = pm.in_game_single_player
                else:
                    game_mode = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 200 <= m[1] <= 280:  # play button
                if game_mode == pm.in_game_single_player:
                    play_state = pm.in_game_single_player
                else:
                    play_state = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 340 <= m[1] <= 410:  # help button
                play_state = pm.info

    # HOME SCREEN
    if play_state == pm.load:
        root.blit(img.load, (0, 0))

        text = pygame.font.Font(fnt.joe_fin, 50).render("<", True, col.red)
        root.blit(text, [20, 150])
        text = pygame.font.Font(fnt.joe_fin, 50).render(">", True, col.red)
        root.blit(text, [200, 150])

        if game_mode == pm.in_game_single_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V AI", True, col.red)
            root.blit(text, [65, 160])

        elif game_mode == pm.in_game_two_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V P", True, col.red)
            root.blit(text, [65, 160])

    # SINGLE PAGE
    if play_state == pm.in_game_single_player:
        root.fill(col.dark_blue)

        draw_board()

        if ess.turn == 0:
            pygame.draw.circle(root, col.red, (100, 100), ess.radius // 2)
            user_turn = True
            lag = 0

        elif ess.turn == 1:
            pygame.draw.circle(root, col.white, (100, 100), ess.radius // 2)
            if lag == ess.lag:
                play_AI()

            else:
                lag += 1

    # 2 PLAYER PAGE
    if play_state == pm.in_game_two_player:
        root.fill(col.dark_blue)

        draw_board()

        if ess.turn == 0:
            pygame.draw.circle(root, col.red, (100, 100), ess.radius // 2)

        elif ess.turn == 1:
            pygame.draw.circle(root, col.yellow, (100, 100), ess.radius // 2)

    # HELP PAGE
    if play_state == pm.info:
        root.blit(img.help, (0, 0))

    if play_state == pm.win:
        if win_lag == ess.win_lag:
            root.fill(col.yellow)

        else:
            win_lag += 1
            draw_board()
            print(ess.winner, "HAS WON!")

    pygame.display.update()
