import pygame
import uuid
import random
import time

pygame.init()

TILE_SIZE = 40
WIDTH, HEIGHT = 15 * TILE_SIZE, 16 * TILE_SIZE
BLACK, WHITE, RED, BLUE, GREEN = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)

class Path:
    def __init__(self, pista):
        self.pista = pista

def caminho_unico(caminho):
    visto = set()
    unico = []
    for pos in caminho:
        if pos not in visto:
            visto.add(pos)
            unico.append(pos)
    return unico


def gerar_labirinto(entrada, linhas=15, colunas=15):
    labirinto = [[0 for _ in range(colunas)] for _ in range(linhas)]

    def escavar(x, y):
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas and labirinto[nx][ny] == 0:
                labirinto[nx][ny] = 1
                labirinto[x + dx // 2][y + dy // 2] = 1
                escavar(nx, ny)

    # Ajusta entrada para dentro dos limites
    ex, ey = entrada
    if ex % 2 == 0:
        ex = max(1, ex - 1)
    if ey % 2 == 0:
        ey = max(1, ey - 1)

    entrada = (ex, ey)

    # Define saída em canto oposto
    saida = (linhas - 2, colunas - 1)

    # Começa escavação a partir da posição do agente (entrada)
    labirinto[ex][ey] = 1
    escavar(ex, ey)

    # Marca entrada e saída
    labirinto[entrada[0]][entrada[1]] = 2
    labirinto[saida[0]][saida[1]] = 3

    return labirinto, entrada

original_labyrinth,entrada = gerar_labirinto((1,7))

print(original_labyrinth)

#gera o novo labirinto com objetos path
labyrinth = []
for y, row in enumerate(original_labyrinth):
    new_row = []
    for x, cell in enumerate(row):
        if cell == 1:
            unique_name = str(uuid.uuid4())
            new_row.append(Path(unique_name))
        else:
            new_row.append(cell)
    labyrinth.append(new_row)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def find_exit():
    for y, row in enumerate(original_labyrinth):
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
        self.found_exit = False
        self.frequencias = {}

    def mover(self):
        if self.found_exit:
            return

        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(direcoes)  # Diversificação

        candidatos = []
        saida_vista = None

        for dx, dy in direcoes:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(labyrinth[0]) and 0 <= ny < len(labyrinth):
                target = labyrinth[ny][nx]
                if target == 2:
                    saida_vista = (nx, ny)
                    break
                if isinstance(target, Path):
                    freq = self.frequencias.get((nx, ny), 0)
                    if freq < 5:
                        candidatos.append(((nx, ny), freq))

        if saida_vista:
            self.path.append((self.x, self.y))
            self.x, self.y = saida_vista
            self.found_exit = True
            return

        if not candidatos:
            return

        candidatos.sort(key=lambda x: x[1])
        if random.random() < 0.2:  # chance de "mutação" no movimento
            escolha = random.choice(candidatos)
        else:
            escolha = candidatos[0]

        (nx, ny), freq = escolha
        self.frequencias[(nx, ny)] = freq + 1
        self.path.append((self.x, self.y))
        self.x, self.y = nx, ny

def replay_best_path():
    global best_path
    best_path = caminho_unico(best_path)
    if best_path:
        for pos in best_path:
            screen.fill(WHITE)
            for y, row in enumerate(labyrinth):
                for x, cell in enumerate(row):
                    if isinstance(cell, Path):
                        pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif cell == 2:
                        pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.circle(screen, GREEN, (pos[0] * TILE_SIZE + TILE_SIZE // 2, pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)
            pygame.display.flip()
            clock.tick(10)

def reset_generation():
    global agents, generation_count, best_path
    generation_count += 1
    print(f"Geração: {generation_count}")
    if generation_count > generation_limit:
        print("Melhor caminho encontrado:", best_path)
        replay_best_path()
        return False
    agents = [Agente(1, 1) for _ in range(n_agents)]
    return True

def genetic_algorithm(agents):
    global best_path
    paths = [agent.path for agent in agents if agent.found_exit]
    if paths:
        best_candidate = min(paths, key=len)
        if best_path is None or len(best_candidate) < len(best_path):
            best_path = best_candidate

# Parâmetros
n_agents = 20
time_limit = 5
generation_limit = 10
best_path = None
generation_count = 0
agents = [Agente(*entrada) for _ in range(n_agents)]

# Loop principal
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
            if isinstance(cell, Path):
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 2:
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for agent in agents:
        if not agent.found_exit:
            pygame.draw.circle(screen, BLUE, (agent.x * TILE_SIZE + TILE_SIZE // 2, agent.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)

    pygame.display.flip()
    clock.tick(15)
    time.sleep(0.01)

pygame.quit()

