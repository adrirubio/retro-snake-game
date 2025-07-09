# snake-game.py
import pygame, sys
from pygame.math import Vector2
from random import randint

grid_top  = 100
cell_size = 20
max_cols = 800 // cell_size
max_rows = (600 - grid_top) // cell_size

# Class for apple
class Apple:
    def __init__(self):
        self.x = randint(0, max_cols - 1)
        self.y = randint(0, max_rows - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_apple(self):
        offset = (cell_size - apple_size) // 2
        px = self.pos.x * cell_size + offset
        py = grid_top + self.pos.y * cell_size + offset
        screen.blit(apple_img, (px, py))

# Class for snake
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 11), Vector2(5, 11), Vector2(4, 11), Vector2(3, 11)]
        self.direction = Vector2(1, 0)
        self.grow = False

    def draw_snake(self):
        for block in self.body:
            px = block.x * cell_size
            py = grid_top + block.y * cell_size
            snake_rect = pygame.Rect(px, py, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color("green"), snake_rect)

    def move_snake(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

# Class for game logic
class Logic:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()

    def apple_pickup(self):
        if self.snake.body[0] == self.apple.pos:
            self.snake.grow = True
            coin_sound.play()
            self.apple = Apple()

    def check_collisions(self):
        head = self.snake.body[0]
        if head.x < 0 or head.x >= max_cols or head.y < 0 or head.y >= max_rows:
            return True

        if head in self.snake.body[1:]:
            return True

        return False

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retro Snake Game")

# Start game sound effect
startup_sound = pygame.mixer.Sound('assets/game-start.mp3')
startup_sound.play()

# Coin sound effect
coin_sound = pygame.mixer.Sound("assets/coin.mp3")

# Apple imgage
apple_size = int(cell_size * 3.5)
apple_img = pygame.image.load("assets/apple.png").convert_alpha()
apple_img = pygame.transform.smoothscale(apple_img, (apple_size, apple_size))

# Snake sheet
sheet = pygame.image.load("assets/snake_sheet.png").convert_alpha()
tile = sheet.get_width() // 3
tiles = [[None]*3 for _ in range(3)]

for r in range(3):
    for c in range(3):
        rect = pygame.Rect(c*tile, r*tile, tile, tile)
        tiles[r][c] = sheet.subsurface(rect)

tiles = [[pygame.transform.smoothscale(tile, (cell_size, cell_size))
          for tile in row]
         for row in tiles]

head_up = tiles[0][0]
corner_tl = tiles[0][1]
corner_tr = tiles[0][2]
corner_bl = tiles[1][1]
corner_br = tiles[1][2]
tail_up = tiles[2][1]
body_straight = tiles[2][2]

# Lookup tables
HEAD = {
    Vector2(0, -1): head_up,
    Vector2(1, 0): pygame.transform.rotate(head_up, -90), # right
    Vector2(0, 1): pygame.transform.flip(head_up, False, True), # down
    Vector2(-1, 0): pygame.transform.rotate(head_up, 90) # left
}

TAIL = {
    Vector2(0, -1): tail_up,
    Vector2(1, 0): pygame.transform.rotate(tail_up, -90), # right
    Vector2(0, 1): pygame.transform.flip(tail_up, False, False),# down
    Vector2(-1, 0): pygame.transform.rotate(tail_up, 90) # left
}

CORNERS = {
    ((-1,0), (0,-1)): corner_tl, ((0,-1), (-1,0)): corner_tl,
    ((1,0), (0,-1)): corner_tr, ((-1,0), (0,1)): corner_tr,
    ((-1,0), (0,1)): corner_bl, ((0,1), (-1,0)): corner_bl,
    ((1,0), (0,1)): corner_br, ((0,1), (1,0)): corner_br
}

# Move
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 150)

# Scan set up
scan = pygame.Surface((800, 600), flags=pygame.SRCALPHA)
for y in range(0, 600, 2):
    pygame.draw.line(scan, (0, 0, 0, 40), (0, y), (800, y))

title_font = pygame.font.Font("retro-font/PressStart2P-Regular.ttf", 40)
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

# Class
logic = Logic()

# Game loop
running = True
while running:
    clock.tick(60)
    frame_count += 1
    collision = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            logic.snake.move_snake()
            logic.apple_pickup()
            collision = logic.check_collisions()
            if collision:
                collision = True
                running = False
                break
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                if logic.snake.direction.y != 1:
                    logic.snake.direction = Vector2(0, -1)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if logic.snake.direction.y != -1:
                    logic.snake.direction = Vector2(0, 1)

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if logic.snake.direction.x != 1:
                    logic.snake.direction = Vector2(-1, 0)

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if logic.snake.direction.x != -1:
                    logic.snake.direction = Vector2(1, 0)

    if collision:
        continue

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

    logic.apple.draw_apple()
    logic.snake.draw_snake()

    screen.blit(scan, (0, 0))
    pygame.display.update()

pygame.quit()
sys.exit()
