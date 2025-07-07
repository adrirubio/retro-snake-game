# snake-game.py
import pygame, sys
from pygame.math import Vector2
from random import randint

grid_top  = 100
cell_size = 20
max_cols = 800 // cell_size
max_rows = (600 - grid_top) // cell_size

# Class for fruit
class fruit:
    def __init__(self):
        self.x = randint(0, max_cols - 1)
        self.y = randint(0, max_rows - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        px = self.pos.x * cell_size
        py = grid_top + self.pos.y * cell_size
        fruit_rect = pygame.Rect(px, py, cell_size, cell_size)
        pygame.draw.rect(screen, pygame.Color("firebrick"), fruit_rect)

# Class for snake
class snake:
    def __init__(self):
        self.body = [Vector2(3, 11), Vector2(4, 11), Vector2(5, 11), Vector2(6, 11)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            px = block.x * cell_size
            py = grid_top + block.y * cell_size
            snake_rect = pygame.Rect(px, py, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color("green"), snake_rect)

    def move_snake(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        self.body.pop()

pygame.init()
pygame.mixer.init()

# Move
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 150)

# Start game sound effect
startup_sound = pygame.mixer.Sound('game-start.mp3')
startup_sound.play()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retro Snake Game")

# Scan set up
scan = pygame.Surface((800, 600), flags=pygame.SRCALPHA)
for y in range(0, 600, 2):
    pygame.draw.line(scan, (0, 0, 0, 40), (0, y), (800, y))

title_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
title_color = pygame.Color("goldenrod")
border_color = (80, 200, 80)

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

fruit = fruit()
snake = snake()

# Game loop
running = True
while running:
    clock.tick(60)
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.direction = Vector2(0, 1)

    screen.fill((15, 56, 15))

    # Color background
    play_rect = pygame.Rect(0, grid_top, 800, 600 - grid_top)
    screen.fill((24, 90, 0), play_rect)

    # Border
    pygame.draw.rect(screen, border_color, play_rect, width=2)

    # Flicker
    if not flicker_done:
        if frame_count % flicker_interval == 0:
            show_text = not show_text
        if frame_count >= flicker_duration:
            flicker_done = True
            show_text = True

        if show_text:
            # Show label
            title_text = title_font.render("Retro Snake Game", True, title_color)
            title_rect = title_text.get_rect(center=(800 // 2, 50))
            screen.blit(title_text, title_rect)

    else:
        # Animate typing effect
        if not done:
            if count < speed * len(message):
                count += 1
            else:
                done = True

        snip = title_font.render(message[0:count // speed], True, title_color)
        snip_rect = snip.get_rect(center=(800 // 2, 50))
        screen.blit(snip, snip_rect)

    fruit.draw_fruit()
    snake.draw_snake()

    screen.blit(scan, (0, 0))
    pygame.display.update()

pygame.quit()
sys.exit()
