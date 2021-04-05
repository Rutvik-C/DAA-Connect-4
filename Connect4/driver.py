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

play_state = pm.load
game_mode = pm.in_game_single_player
active = True
user_turn = True
initial = True
t = None
done = False
lag = 0
win_lag = 0
win_line = [[], []]


def reset_game():
    """Resets all game variables to initial"""

    global play_state, game_mode, active, user_turn, initial, t, done, lag, win_lag, win_line

    play_state = pm.load
    active = True
    user_turn = True
    initial = True
    t = None
    done = False
    lag = 0
    win_lag = 0
    win_line = [[], []]
    ess.turn = 0
    ess.board = [[-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1]]


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

    for piece in board:
        print(piece)


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
            if board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == player:
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
        score += 100

    elif array.count(player) == 3 and array.count(-1) == 1:  # Made 3 in adjacent
        score += 10

    elif array.count(player) == 2 and array.count(-1) == 2:  # Made 2 in adjacent
        score += 5

    # BLOCKING
    if array.count(other_player) == 3 and array.count(-1) == 1:  # Opponent 3 in adjacent
        score -= 70

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
    print("========================IN MINIMAX", depth, maximising_player, "====================================")
    for i in board[:: -1]:
        print(i)

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


# def get_best_move():
#     """Traverse through all possibilities and select the best move"""
#
#     valid_locs = get_all_valid(ess.board)
#
#     max_score = -math.inf
#     max_score_from_col = random.choice(valid_locs)
#
#     print("===============CHECKING POSSIBILITIES===============")
#
#     for c in valid_locs:
#         alt_board = list()
#         for r in ess.board:
#             alt_board.append(r.copy())
#
#         make_move(c, ess.turn, alt_board)
#
#         score = analyse_board(alt_board, ess.turn)
#         if score > max_score:
#             max_score = score
#             max_score_from_col = c
#
#     print("===============max:", max_score, "from: col", max_score_from_col, "===============")
#
#     print("Max score =", max_score, ":: From col", max_score_from_col)
#     return max_score_from_col


def AI_logic():
    """Implementation of minimax algorithm | Decide where the bot will play"""

    global done

    # c = get_best_move()
    c = minimax(ess.board, 3, -math.inf, math.inf, True)[0]
    make_move(c, ess.turn, ess.board)

    draw_board()

    done = True


def play_AI():
    """Thread implementation to avoid 'Not Responding' state"""

    global user_turn, t, done, initial, play_state

    if initial:
        initial, done = False, False
        t = Thread(target=AI_logic)
        t.start()

    if done:

        if is_winner(ess.board, ess.turn):
            ess.winner = "Bot"
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
            # print(m)

            if 5 <= m[0] <= 50 and 5 <= m[1] <= 50:  # Back Button
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

                    if is_winner(ess.board, ess.turn):
                        play_state = pm.win
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

                    if is_winner(ess.board, ess.turn):
                        ess.winner = "You"
                        play_state = pm.win

                    ess.turn = (ess.turn + 1) % 2
                    user_turn = False
                    initial = True

            if (20 <= m[0] <= 45 and 155 <= m[1] <= 190) or (
                    200 <= m[0] <= 230 and 155 <= m[1] <= 190) and play_state == pm.load:
                if game_mode == pm.in_game_two_player:
                    game_mode = pm.in_game_single_player
                else:
                    game_mode = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 200 <= m[1] <= 280 and play_state == pm.load:  # play button
                if game_mode == pm.in_game_single_player:
                    play_state = pm.in_game_single_player
                else:
                    play_state = pm.in_game_two_player

            if 25 <= m[0] <= 220 and 340 <= m[1] <= 410 and play_state == pm.load:  # help button
                play_state = pm.info

            if 90 <= m[0] <= 210 and 150 <= m[1] <= 270 and play_state == pm.win:
                reset_game()
                play_state = pm.load

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
        root.blit(img.background, (0, 0))
        root.blit(img.back, (10, 10))

        draw_board()

        if ess.turn == 0:
            bias = 230
            valid = get_all_valid(ess.board)
            for pos in range(7):
                if pos in valid:
                    root.blit(img.red_arrow, [bias + pos * 85, 20])

            user_turn = True
            lag = 0

        elif ess.turn == 1:
            text = pygame.font.Font(fnt.pacifico, 40).render("Thinking...", True, col.black)
            root.blit(text, [420, 10])

            if lag == ess.lag:
                play_AI()

            else:
                lag += 1

    # 2 PLAYER PAGE
    if play_state == pm.in_game_two_player:
        root.blit(img.background, (0, 0))
        root.blit(img.back, (10, 10))

        draw_board()

        bias = 230
        valid = get_all_valid(ess.board)
        if ess.turn == 0:
            for pos in range(7):
                if pos in valid:
                    root.blit(img.red_arrow, [bias + pos * 85, 20])

        elif ess.turn == 1:
            for pos in range(7):
                if pos in valid:
                    root.blit(img.yellow_arrow, [bias + pos * 85, 20])

    # HELP PAGE
    if play_state == pm.info:
        root.blit(img.help, (0, 0))
        root.blit(img.back, (10, 10))

    if play_state == pm.win:
        if win_lag == ess.win_lag:

            root.blit(img.win, (0, 0))

            text = ess.winner
            if text == "You":
                text += " win!"
            else:
                text += " wins!"

            text = pygame.font.Font(fnt.pacifico, 50).render(text, True, col.red)
            root.blit(text, [50, 50])
            root.blit(img.home, [90, 150])

        else:
            win_lag += 1

            draw_board()
            if win_line != [None, None]:
                pygame.draw.line(root, col.white, win_line[0], win_line[1], 8)

    pygame.display.update()
