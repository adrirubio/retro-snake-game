# snake-game.py
import pygame, sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retro Snake Game")

title_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
main_color = pygame.Color("goldenrod")

# Animate text set up
message = "Retro Snake Game"
count = 0
speed = 3
done = False

# Flicker set up
flicker_duration = 20
flicker_interval = 1
show_text = True
frame_count = 0
flicker_done = False

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((15, 56, 15))

    # Flicker
    if not flicker_done:
        if frame_count % flicker_interval == 0:
            show_text = not show_text
        if frame_count >= flicker_duration:
            flicker_done = True
            show_text = True

        if show_text:
            # Show label
            title_text = title_font.render("Retro Snake Game", True, main_color)
            title_rect = title_text.get_rect(center=(800 // 2, 50))
            screen.blit(title_text, title_rect)

    else:
        # Animate typing effect
        if not done:
            if count < speed * len(message):
                count += 1
            else:
                done = True

        snip = title_font.render(message[0:count // speed], True, main_color)
        snip_rect = snip.get_rect(center=(800 // 2, 50))
        screen.blit(snip, snip_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
