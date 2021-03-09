from classes import *

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
first = True


def draw_board():
    pygame.draw.rect(root, col.black, (ess.h_padding, ess.v_padding, 595, 510))
    for r in range(ess.rows):
        for c in range(ess.cols):
            pygame.draw.circle(root, col.dark_blue, (int(c * ess.unit + ess.unit / 2 + ess.h_padding), int(r * ess.unit + ess.unit / 2 + ess.v_padding)), ess.radius)


while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

        # Mouse motion
        if inp.type == pygame.MOUSEMOTION:
            if play_state == pm.in_game_two_player and ess.h_padding - 100 <= inp.pos[0] <= ess.h_padding + 595 + 100:
                pygame.draw.circle(root, col.red, (inp.pos[0], 47), ess.radius)

                pygame.display.update()

        # Mouse click Check
        if inp.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()  # Fetching mouse click location
            print(m)

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

        pygame.display.update()

    # SINGLE PAGE
    if play_state == pm.in_game_single_player:
        root.fill(col.dark_blue)

    # SINGLE PAGE
    if play_state == pm.in_game_two_player:
        root.fill(col.dark_blue)

        draw_board()

        if first:
            pygame.display.update()
            first = False

    # HELP PAGE
    if play_state == pm.info:
        root.blit(img.help, (0, 0))

        pygame.display.update()
