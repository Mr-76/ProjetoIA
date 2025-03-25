import pygame
import numpy as np

pygame.init()

TILE_SIZE = 40 
WIDTH, HEIGHT = 7 * TILE_SIZE, 5 * TILE_SIZE
BLACK, WHITE ,RED= (255, 255, 255), (0, 0, 0),(255,0,0)

labyrinth = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 2, 0, 0, 0, 0, 0]
])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_labyrinth():
    screen.fill(WHITE)
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if cell == 2:  # Wall
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_labyrinth()
    clock.tick(30)

pygame.quit()
