from classes import *

pygame.init()

# Creating root window
root = pygame.display.set_mode((1000, 600))
# root = pygame.display.set_mode((540, 630))
pygame.display.set_caption("Connect 4")

# Making class objects
pm = PlayMode()
img = Images()
fnt = TextFont()
col = Color()


play_mode = pm.load
game_mode = pm.in_game_single_player
active = True


while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

        # Mouse click Check
        if inp.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()  # Fetching mouse click location

            if (50 <= m[0] <= 80 and 190 <= m[1] <= 220) or (220 <= m[0] <= 250 and 190 <= m[1] <= 220):
                if game_mode == pm.in_game_two_player:
                    game_mode = pm.in_game_single_player
                else:
                    game_mode = pm.in_game_two_player

    # HOME SCREEN
    if play_mode == pm.load:
        root.blit(img.load, (0, 0))

        pygame.draw.rect(root, col.dark_blue, pygame.Rect(50, 250, 200, 60), 5)  # (x, y, length, breadth), thickness
        pygame.draw.rect(root, col.dark_blue, pygame.Rect(50, 330, 200, 60), 5)

        text = pygame.font.Font(fnt.joe_fin, 50).render("<", True, col.dark_blue)
        root.blit(text, [50, 180])
        text = pygame.font.Font(fnt.joe_fin, 50).render(">", True, col.dark_blue)
        root.blit(text, [225, 180])

        if game_mode == pm.in_game_single_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V AI", True, col.dark_blue)
            root.blit(text, [95, 190])

        elif game_mode == pm.in_game_two_player:
            text = pygame.font.Font(fnt.joe_fin, 40).render("P V P", True, col.dark_blue)
            root.blit(text, [95, 190])

        text = pygame.font.Font(fnt.joe_fin, 40).render("PLAY", True, col.dark_blue)
        root.blit(text, [95, 265])
        text = pygame.font.Font(fnt.joe_fin, 40).render("HELP", True, col.dark_blue)
        root.blit(text, [95, 345])

    pygame.display.update()

