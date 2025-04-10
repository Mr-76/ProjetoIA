import pygame
import numpy as np
import random
import time

pygame.init()

TILE_SIZE = 40 
WIDTH, HEIGHT = 15 * TILE_SIZE, 15 * TILE_SIZE
BLACK, WHITE, RED, BLUE, GREEN = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)

class Path:
    """
    toda vez que um agente passa por um caminho
    um tile pode ter uma propriedade ou nao,
    gerar aleatoriamente pistas,
    de forma que pistas especificas sao passadas de geracao em geracao
    agente escolhe entre pista e nao pista e pista desconhecida,
        claro que pista conhecida quer dizer uma boa escolha....
        pista eh um string random,, pode se repetir, lugares parecidos
    """
    def __init__(self, pista):
        self.pista = pista 


path1 = Path("1")
path2 = Path("2")
path3 = Path("3")

labyrinth = [
    [0, path1, path2, path3, 2, 0],
]

#labyrinth = np.array([
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
#    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#])

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
        """
        Can only move if its not a wall,and its not a visited place.
        New generation keeps track of good places where the did pass before
        """
        if self.found_exit:
            return

        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            print(novo_x)
            print(novo_y)
            if 0 <= novo_x < (len(labyrinth[0])) and 0 <= novo_y < len(labyrinth):
                print("can move")
                if type(labyrinth[novo_y][novo_x]) == Path and (novo_x, novo_y) not in self.visited:
                    print("its moving now")
                    self.visited.add((novo_x, novo_y))
                    self.path.append((self.x, self.y))
                    self.x, self.y = novo_x, novo_y
                    return
                elif labyrinth[novo_y][novo_x] == 2:
                    print("Found exit")
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

#invertido agente
agents = [Agente(1,0)]

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
            if type(cell) == Path :
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 2:
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    for agent in agents:
        if not agent.found_exit:
            pygame.draw.circle(screen, BLUE, (agent.x * TILE_SIZE + TILE_SIZE // 2, agent.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)
    
    time.sleep(1)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

