import pygame
import numpy as np
import random
import time

pygame.init()

TILE_SIZE = 40 
WIDTH, HEIGHT = 15 * TILE_SIZE, 15 * TILE_SIZE
BLACK, WHITE, RED, BLUE, GREEN = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)

labyrinth = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

time_limit = 10
generation_limit = 3
best_path = None
generation_count = 0

def find_exit():
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == 2:
                return x, y
    return None

goal_x, goal_y = find_exit()


class Agente:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []
        self.visited = set()
        self.found_exit = False

    def mover(self):
        if self.found_exit:
            return

        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            if 0 <= novo_x < labyrinth.shape[1] and 0 <= novo_y < labyrinth.shape[0]:
                if labyrinth[novo_y, novo_x] == 1 and (novo_x, novo_y) not in self.visited:
                    self.visited.add((novo_x, novo_y))
                    self.path.append((self.x, self.y))
                    self.x, self.y = novo_x, novo_y
                    return
                elif labyrinth[novo_y, novo_x] == 2:
                    self.found_exit = True
                    self.path.append((self.x, self.y))
                    return

def replay_best_path():
    if best_path:
        for position in best_path:
            screen.fill(WHITE)
            for y, row in enumerate(labyrinth):
                for x, cell in enumerate(row):
                    if cell == 1:
                        pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif cell == 2:
                        pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.circle(screen, GREEN, (position[0] * TILE_SIZE + TILE_SIZE // 2, position[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)
            pygame.display.flip()
            clock.tick(5)

def reset_generation():
    global agents, generation_count, best_path
    generation_count += 1
    print(f"Geração: {generation_count}")
    if generation_count > generation_limit:
        print("Melhor caminho encontrado:", best_path)
        replay_best_path()
        return False
    agents = [Agente(1, 1) for _ in range(10)]
    return True

def genetic_algorithm(agents):
    global best_path
    paths = [agent.path for agent in agents if agent.found_exit]
    if paths:
        best_candidate = min(paths, key=len)
        if best_path is None or len(best_candidate) < len(best_path):
            best_path = best_candidate
#apth agente,ter uma dict de pesso para cada posicao, metade com agente 1 metade para outro agente, tenta encontrar  agentes  compaatives meio + range de 30 20 ou 10 % testar, 
#caso nao encontre um certo numero, pega um resto de agentes e addiciona uma mutacao...


agents = [Agente(1, 1) for _ in range(10)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for agent in agents:
        agent.mover()
    
    if any(agent.found_exit for agent in agents):
        genetic_algorithm(agents)
        running = reset_generation()
    
    screen.fill(WHITE)
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 2:
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    for agent in agents:
        if not agent.found_exit:
            pygame.draw.circle(screen, BLUE, (agent.x * TILE_SIZE + TILE_SIZE // 2, agent.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

