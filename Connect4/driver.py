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
active = True


while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

    # HOME SCREEN
    if play_mode == pm.load:
        root.blit(img.load, (0, 0))

        text = pygame.font.Font(fnt.joe_fin, 50).render("Single Player", True, col.yellow)
        root.blit(text, [20, 140])
        text = pygame.font.Font(fnt.joe_fin, 50).render("Two Player", True, col.yellow)
        root.blit(text, [20, 200])
        text = pygame.font.Font(fnt.joe_fin, 50).render("Help", True, col.yellow)
        root.blit(text, [20, 260])

    pygame.display.update()

