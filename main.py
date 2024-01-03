import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Define shapes (tetrominos)
tetrominos = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 1], [1, 0, 0]],  # L-shape
    [[1, 1, 1], [0, 0, 1]],  # J-shape
    [[1, 1], [1, 1]],  # O-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 1, 0], [0, 1, 1]]  # S-shape
]

# Game variables
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = random.choice(tetrominos)
piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
piece_y = 0
score = 0
game_over = False

clock = pygame.time.Clock()

# Functions
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

# def draw_piece():
#     for y, row in enumerate(current_piece):
#         for x, val in enumerate(row):
#             if val:
#                 pygame.draw.rect(screen, RED, ((piece_x + x) * BLOCK_SIZE, (piece_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
def draw_piece():
    for y, row in enumerate(current_piece):
        for x, val in enumerate(row):
            if val:
                if 0 <= piece_x + x < GRID_WIDTH and 0 <= piece_y + y < GRID_HEIGHT:
                    pygame.draw.rect(screen, RED, ((piece_x + x) * BLOCK_SIZE, (piece_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def check_collision():
    for y, row in enumerate(current_piece):
        for x, val in enumerate(row):
            if val:
                if piece_y + y >= GRID_HEIGHT or piece_x + x < 0 or piece_x + x >= GRID_WIDTH or grid[piece_y + y][piece_x + x]:
                    return True
    return False

# def merge_piece():
#     for y, row in enumerate(current_piece):
#         for x, val in enumerate(row):
#             if val:
#                 grid[piece_y + y][piece_x + x] = 1

# def clear_rows():
#     global score
#     full_rows = []
#     for i, row in enumerate(grid):
#         if all(row):
#             full_rows.append(i)
#     for row_index in full_rows:
#         del grid[row_index]
#         grid.insert(0, [0 for _ in range(GRID_WIDTH)])
#         score += 10 * len(full_rows)

def merge_piece():
    for y, row in enumerate(current_piece):
        for x, val in enumerate(row):
            if val:
                if 0 <= piece_y + y < GRID_HEIGHT and 0 <= piece_x + x < GRID_WIDTH:
                    grid[piece_y + y][piece_x + x] = 1

def clear_rows():
    global score
    full_rows = []
    for i, row in enumerate(grid):
        if all(row):
            full_rows.append(i)
    for row_index in full_rows:
        del grid[row_index]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    score += 10 * len(full_rows)


def draw_score():
    font = pygame.font.SysFont('Arial', 25)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    font = pygame.font.SysFont('Arial', 40)
    game_over_text = font.render('Game Over', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_piece()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            piece_x -= 1
            if check_collision():
                piece_x += 1
        if keys[pygame.K_RIGHT]:
            piece_x += 1
            if check_collision():
                piece_x -= 1
        if keys[pygame.K_DOWN]:
            piece_y += 1
            if check_collision():
                piece_y -= 1
        if keys[pygame.K_SPACE]:
            while not check_collision():
                piece_y += 1
            piece_y -= 1

        if not check_collision():
            piece_y += 1
        else:
            merge_piece()
            clear_rows()
            current_piece = random.choice(tetrominos)
            piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
            piece_y = 0
            if check_collision():
                game_over = True

    draw_score()
    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(10)  # Adjust speed here

pygame.quit()
