import math
import random

from classes import *
from threading import Thread

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
sound = Sound()

pygame.mixer.music.load(sound.background)
pygame.mixer.music.play(-1)  # continuous bg music
pygame.mixer.music.set_volume(0.3)  # Setting background music volume
music_on = True

play_state = pm.load
game_mode = pm.in_game_single_player
active = True
user_turn = True
initial = True
t = None
done = False
lag = 0
win_lag = ess.win_lag
win_line = [[], []]
ess.winner = None
scoredict = dict()
counter = 0
scoredict["RED"] = 0
scoredict["YELLOW"] = 0
scoredict["JARVIS"] = 0
scoredict["YOU"] = 0


def reset_game():
    """Resets all game variables to initial"""

    global play_state, game_mode, active, user_turn, initial, t, done, lag, win_lag, win_line, scoredict, counter
    counter = 0
    play_state = pm.load
    active = True
    user_turn = True
    initial = True
    t = None
    done = False
    lag = 0
    win_lag = ess.win_lag
    win_line = [[], []]
    ess.winner = None
    ess.turn = 0
    ess.board = [[-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1]]
    counter = 0


def is_valid(board, c):
    """Checks if coin can be dropped in column c | There is at least one empty row in column c"""

    return board[ess.rows - 1][c] == -1


def get_all_valid(board):
    """Returns all valid columns | Columns where coin can be dropped"""

    val_locs = list()

    for c in range(ess.cols):
        if is_valid(board, c):
            val_locs.append(c)

    return val_locs


def get_empty_row(board, c):
    """For a particular column return the first empty row"""

    for r in range(ess.rows):
        if board[r][c] == -1:
            return r


def make_move(c, player, board):
    """Function to drop players coin"""

    r = get_empty_row(board, c)

    print(player, "making move at ", r, c)
    board[r][c] = player

    # for piece in board:
    #     print(piece)


def is_winner(board, player):
    """Function to check if there are 4 coins adjacent to each other | Function to check if anyone has won"""

    global win_line

    # HORIZONTAL WIN
    for i in range(ess.rows):
        for j in range(ess.cols - 3):
            if board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == player:
                win_line = ([ess.h_padding + int(j * ess.unit + ess.unit / 2), 600 - int(i * ess.unit + ess.unit / 2)],
                            [ess.h_padding + int((j + 3) * ess.unit + ess.unit / 2),
                             600 - int(i * ess.unit + ess.unit / 2)])
                return True

    # VERTICAL WIN
    for i in range(ess.rows - 3):
        for j in range(ess.cols):
            if board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][
                j] == player:
                win_line = ([ess.h_padding + int(j * ess.unit + ess.unit / 2), 600 - int(i * ess.unit + ess.unit / 2)],
                            [ess.h_padding + int(j * ess.unit + ess.unit / 2),
                             600 - int((i + 3) * ess.unit + ess.unit / 2)])

                return True

    # FORWARD DIAGONAL WIN
    for i in range(3, ess.rows):
        for j in range(ess.cols - 3):
            if board[i][j] == player and board[i - 1][j + 1] == player and board[i - 2][j + 2] == player and \
                    board[i - 3][j + 3] == player:
                win_line = ([ess.h_padding + int(j * ess.unit + ess.unit / 2), 600 - int(i * ess.unit + ess.unit / 2)],
                            [ess.h_padding + int((j + 3) * ess.unit + ess.unit / 2),
                             600 - int((i - 3) * ess.unit + ess.unit / 2)])

                return True

    # BACKWARD DIAGONAL WIN
    for i in range(ess.rows - 3):
        for j in range(ess.cols - 3):
            if board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and \
                    board[i + 3][j + 3] == player:
                win_line = ([ess.h_padding + int(j * ess.unit + ess.unit / 2), 600 - int(i * ess.unit + ess.unit / 2)],
                            [ess.h_padding + int((j + 3) * ess.unit + ess.unit / 2),
                             600 - int((i + 3) * ess.unit + ess.unit / 2)])

                return True

    return False


def get_partial_array_analysis(array, player):
    """Check the pattern in given array"""
    score = 0
    other_player = (player + 1) % 2

    # SCORING
    if array.count(player) == 4:  # Winning move
        score += 10 ** 9

    elif array.count(player) == 3 and array.count(-1) == 1:  # Made 3 in adjacent
        score += 10

    elif array.count(player) == 2 and array.count(-1) == 2:  # Made 2 in adjacent
        score += 5

    # BLOCKING
    if array.count(other_player) == 3 and array.count(-1) == 1:  # Opponent 3 in adjacent
        score -= 100

    return score


def analyse_board(board, player):
    """Check various patterns in the board"""
    score = 0

    # CENTER COLUMN ADVANTAGE
    center_col = list()
    for ro in board:
        center_col.append(ro[ess.cols // 2])
    score += center_col.count(player) * 6

    # HORIZONTAL ANALYSIS
    for ro in board:
        for c in range(ess.cols - 3):
            partial_row = ro[c: c + 4]

            score += get_partial_array_analysis(partial_row, player)

    # VERTICAL ANALYSIS
    for c in range(ess.cols):
        co = list()
        for ro in board:
            co.append(ro[c])

        for r in range(ess.rows - 3):
            partial_col = co[r: r + 4]

            score += get_partial_array_analysis(partial_col, player)

    # BACKWARD DIAGONAL
    for r in range(ess.rows - 3):
        for c in range(ess.cols - 3):
            partial_b_diag = [board[r + x][c + x] for x in range(4)]

            score += get_partial_array_analysis(partial_b_diag, player)

    # FORWARD DIAGONAL
    for r in range(ess.rows - 3):
        for c in range(ess.cols - 3):
            partial_f_diag = [board[r + 3 - x][c + x] for x in range(4)]

            score += get_partial_array_analysis(partial_f_diag, player)

    return score


def minimax(board, depth, alpha, beta, maximising_player):
    """Implementation of minimax algorithm | Bot is maximising, User is minimising"""
    print("==========IN MINIMAX", depth, maximising_player, "==========")
    # for i in board[:: -1]:
    #     print(i)

    if depth == 0 or is_winner(board, 0) or is_winner(board, 1) or len(
            get_all_valid(board)) == 0:  # depth is 0 or we are at terminal node
        print("Terminal")

        if is_winner(board, 0) or is_winner(board, 1) or len(get_all_valid(board)) == 0:
            if is_winner(board, 1):  # Winning move, Max priority
                return None, 10 ** 9

            elif is_winner(board, 0):  # Losing move, Min priority
                return None, -10 ** 9

            else:  # No more valid location, Game draw
                return None, 0

        else:
            print("Returns:", analyse_board(board, 1))
            return None, analyse_board(board, 1)

    valid_cols = get_all_valid(board)

    if maximising_player:
        value = -math.inf
        best_col = random.choice(valid_cols)
        for c in valid_cols:
            alt_board = list()
            for r in board:
                alt_board.append(r.copy())

            make_move(c, 1, alt_board)  # maximise bot

            x = minimax(alt_board, depth - 1, alpha, beta, False)[1]
            if x > value:
                value = x
                best_col = c

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_cols)
        for c in valid_cols:
            alt_board = list()
            for r in board:
                alt_board.append(r.copy())

            make_move(c, 0, alt_board)  # minimise player

            x = minimax(alt_board, depth - 1, alpha, beta, True)[1]
            if x < value:
                value = x
                best_col = c

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value


def AI_logic():
    """Implementation of minimax algorithm | Decide where the bot will play"""

    global done

    print("***************************************AI***************************************")
    c = minimax(ess.board, 3, -math.inf, math.inf, True)[0]
    make_move(c, ess.turn, ess.board)
    print("***************************************AI***************************************")

    if music_on:
        sound.coin_drop.play()

    draw_board()

    done = True


def play_AI():
    """Thread implementation to avoid 'Not Responding' state"""

    global user_turn, t, done, initial, play_state, win_lag

    if initial:
        initial, done = False, False
        t = Thread(target=AI_logic)
        t.start()

    if done:

        if is_winner(ess.board, ess.turn):
            ess.winner = "JARVIS"
            win_lag = 0
            play_state = pm.win

        ess.turn = (ess.turn + 1) % 2
        user_turn = True


def draw_board():
    """Convert the matrix into GUI"""

    pygame.draw.rect(root, col.black, (ess.h_padding, ess.v_padding, 595, 510))
    for r in range(ess.rows):
        for c in range(ess.cols):
            pygame.draw.circle(root, col.bg_blue, (
                int(c * ess.unit + ess.unit / 2 + ess.h_padding), int(r * ess.unit + ess.unit / 2 + ess.v_padding)),
                               ess.radius)

    for r in range(ess.rows):
        for c in range(ess.cols):
            if ess.board[r][c] == 0:
                pygame.draw.circle(root, col.red, (
                    ess.h_padding + int(c * ess.unit + ess.unit / 2), 600 - int(r * ess.unit + ess.unit / 2)),
                                   ess.radius)

            elif ess.board[r][c] == 1:
                pygame.draw.circle(root, col.yellow, (
                    ess.h_padding + int(c * ess.unit + ess.unit / 2), 600 - int(r * ess.unit + ess.unit / 2)),
                                   ess.radius)


# MAIN
while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

        # Mouse click Check
        if inp.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()  # Fetching mouse click location
            # print("MOUSE PTR", m)

            if 5 <= m[0] <= 50 and 5 <= m[1] <= 50:  # Back Button
                if music_on:
                    sound.click.play()

                if play_state == pm.info:
                    play_state = pm.load

                elif play_state == pm.in_game_two_player or play_state == pm.in_game_single_player:
                    reset_game()
                    play_state = pm.load

            if play_state == pm.in_game_two_player:  # TWO PLAYER MODE
                column = int(math.floor((m[0] - ess.h_padding) / ess.unit))
                print("col:", column)
                if 0 <= column <= 6 and is_valid(ess.board, column):
                    # print("Valid")
                    make_move(column, ess.turn, ess.board)

                    if music_on:
                        sound.coin_drop.play()

                    if is_winner(ess.board, ess.turn):
                        play_state = pm.win
                        win_lag = 0
                        if ess.turn == 0:
                            ess.winner = "Red"
                        else:
                            ess.winner = "Yellow"

                    ess.turn = (ess.turn + 1) % 2

            if play_state == pm.in_game_single_player:  # SINGLE PLAYER MODE
                column = int(math.floor((m[0] - ess.h_padding) / ess.unit))
                print("col:", column)
                if 0 <= column <= 6 and is_valid(ess.board, column) and user_turn:
                    # print("Valid")
                    make_move(column, ess.turn, ess.board)

                    if music_on:
                        sound.coin_drop.play()

                    if is_winner(ess.board, ess.turn):
                        ess.winner = "You"
                        play_state = pm.win

                    ess.turn = (ess.turn + 1) % 2
                    user_turn = False
                    initial = True

            if (20 <= m[0] <= 45 and 155 <= m[1] <= 190) or (
                    200 <= m[0] <= 230 and 155 <= m[1] <= 190) and play_state == pm.load:
                if music_on:
                    sound.click.play()
                
                if game_mode == pm.in_game_two_player:
                    game_mode = pm.in_game_single_player
                else:
                    game_mode = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 200 <= m[1] <= 280 and play_state == pm.load:  # play button
                if music_on:
                    sound.click.play()

                if game_mode == pm.in_game_single_player:
                    play_state = pm.in_game_single_player
                else:
                    play_state = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 340 <= m[1] <= 410 and play_state == pm.load:  # help button
                if music_on:
                    sound.click.play()
                play_state = pm.info

            if 948 <= m[0] <= 980 and 10 <= m[1] <= 42 and play_state != pm.win:  # mute unmute
                if music_on:
                    sound.click.play()

                if music_on:
                    music_on = False
                    pygame.mixer.music.pause()

                else:
                    music_on = True
                    pygame.mixer.music.unpause()

            if 90 <= m[0] <= 210 and 150 <= m[1] <= 270 and play_state == pm.win:
                if music_on:
                    sound.click.play()

                reset_game()
                play_state = pm.load

    # HOME SCREEN
    if play_state == pm.load:
        root.blit(img.load, (0, 0))

        text = pygame.font.Font(fnt.joe_fin, 50).render("<", True, col.red)
        root.blit(text, [20, 150])
        text = pygame.font.Font(fnt.joe_fin, 50).render(">", True, col.red)
        root.blit(text, [200, 150])

        if music_on:
            root.blit(img.unmute, (948, 10))
        else:
            root.blit(img.mute, (948, 10))

        if game_mode == pm.in_game_single_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V AI", True, col.red)
            root.blit(text, [65, 160])

        elif game_mode == pm.in_game_two_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V P", True, col.red)
            root.blit(text, [65, 160])

    # SINGLE PAGE
    if play_state == pm.in_game_single_player:
        root.blit(img.background, (0, 0))
        root.blit(img.back, (10, 10))

        root.blit(img.player_1, (50, 100))
        root.blit(img.player_2, (825, 100))
        text = pygame.font.Font(fnt.joe_fin, 30).render("YOU", True, col.red)
        root.blit(text, [77, 240])
        text = pygame.font.Font(fnt.joe_fin, 30).render("JARVIS", True, col.yellow)
        root.blit(text, [837, 240])

        text = pygame.font.Font(fnt.joe_fin, 50).render(str(scoredict["YOU"]), True, col.black)
        root.blit(text, [430, 40])
        text = pygame.font.Font(fnt.joe_fin, 50).render("_", True, col.black)
        root.blit(text, [485, 30])
        text = pygame.font.Font(fnt.joe_fin, 50).render(str(scoredict["JARVIS"]), True, col.black)
        root.blit(text, [540, 40])

        if music_on:
            root.blit(img.unmute, (948, 10))
        else:
            root.blit(img.mute, (948, 10))

        draw_board()

        # All positions filled
        if len(get_all_valid(ess.board)) == 0:
            play_state = pm.win

        if ess.turn == 0:
            root.blit(img.dash, (80, 245))

            user_turn = True
            lag = 0

        elif ess.turn == 1:
            root.blit(img.dash, (855, 245))

            if lag == ess.lag:
                play_AI()

            else:
                lag += 1

    # 2 PLAYER PAGE
    if play_state == pm.in_game_two_player:
        root.blit(img.background, (0, 0))
        root.blit(img.back, (10, 10))

        root.blit(img.player_1, (50, 100))
        root.blit(img.player_2, (825, 100))
        text = pygame.font.Font(fnt.joe_fin, 30).render("RED", True, col.red)
        root.blit(text, [80, 240])
        text = pygame.font.Font(fnt.joe_fin, 30).render("YELLOW", True, col.yellow)
        root.blit(text, [825, 240])

        text = pygame.font.Font(fnt.joe_fin, 50).render(str(scoredict["RED"]), True, col.black)
        root.blit(text, [430, 40])
        text = pygame.font.Font(fnt.joe_fin, 50).render("_", True, col.black)
        root.blit(text, [485, 30])
        text = pygame.font.Font(fnt.joe_fin, 50).render(str(scoredict["YELLOW"]), True, col.black)
        root.blit(text, [540, 40])

        if music_on:
            root.blit(img.unmute, (948, 10))
        else:
            root.blit(img.mute, (948, 10))

        draw_board()

        # All positions filled
        if len(get_all_valid(ess.board)) == 0:
            play_state = pm.win

        bias = 230
        valid = get_all_valid(ess.board)
        if ess.turn == 0:
            root.blit(img.dash, (80, 245))

        elif ess.turn == 1:
            root.blit(img.dash, (855, 245))

    # HELP PAGE
    if play_state == pm.info:
        root.blit(img.help, (0, 0))
        root.blit(img.back, (10, 10))

        if music_on:
            root.blit(img.unmute, (948, 10))
        else:
            root.blit(img.mute, (948, 10))

    if play_state == pm.win:
        if win_lag == ess.win_lag:

            root.blit(img.win, (0, 0))

            if ess.winner is not None:

                if music_on:
                    sound.victory.play()

                text = ess.winner
                if counter == 0:
                    scoredict[ess.winner.upper()] += 1
                    print("TEST", scoredict[ess.winner.upper()])
                    counter = 1
                if text == "You":
                    text += " win!"
                else:
                    text += " wins!"

            else:
                text = "Draw!"

            text = pygame.font.Font(fnt.pacifico, 50).render(text, True, col.black)
            root.blit(text, [50, 50])
            root.blit(img.home, [90, 150])

        else:
            win_lag += 1

            draw_board()
            if win_line != [None, None]:
                pygame.draw.line(root, col.white, win_line[0], win_line[1], 8)

    pygame.display.update()
