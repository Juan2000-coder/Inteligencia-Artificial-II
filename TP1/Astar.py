#-----------------------------IMPORTS---------------------------#
import pygame
import heapq
from rich.console import Console
from rich.panel import Panel
from Problem import Problem

#-----------------------------AGENTE---------------------------#
class Agent:
    def __init__(self, initial:tuple):
        self.position = initial

    def move(self, new_position):
        self.position = new_position


#----------------------------CLASE A_star---------------------#
class A_star:
    def __init__(self, problem:Problem):
        self.problem    = problem
        self.open_list  = [(0, self.problem.start)]
        self.parent_of  = {}
        self.g_score    = {(x, y): float('inf') for x in range(self.problem.enviroment.width) for y in range(self.problem.enviroment.heigth)}
        self.g_score[self.problem.start] = 0

    def goal_test(self, current:tuple):
        return current == self.problem.goal
    
    def get_path(self):
        path    = []
        current = self.problem.goal
        while current in self.parent_of:
            path.insert(0, current)
            current = self.parent_of[current]
        return path
    
    def solve(self):
        while self.open_list:
            current = heapq.heappop(self.open_list)[1]

            if self.goal_test(current):
                return self.get_path()

            self.expand(current)

    def expand(self, current:tuple):
        for neighbor in self.problem.enviroment.neighbors(current):
            tentative_g_score = self.g_score[current] + 1

            if tentative_g_score < self.g_score[neighbor]:
                self.parent_of[neighbor] = current
                self.g_score[neighbor]   = tentative_g_score
                f_score                  = tentative_g_score + self.problem.enviroment.manhattan(neighbor, self.problem.goal)
                heapq.heappush(self.open_list, (f_score, neighbor))

#print(estante_a_coordenadas)

#Le preguntamos al usuario el alamcen que quiere
almacen_in = int(input("Ingrese el número de estante que desea buscar: "))

# Crear una instancia de la consola
console = Console()
# Definir el contenido que deseas mostrar
contenido = f"Se buscara el almacen numero: \n[bold]{almacen_in}[/bold]"
# Crear un panel con el contenido
panel = Panel.fit(contenido, title="ALMACEN LOS MECAPIBE", border_style="green")
# Imprimir el panel
console.print(panel)

obj=estante_a_coordenadas[almacen_in]

#Si almacen_in es par
if almacen_in%2==0:
    obj=(obj[0]+1,obj[1])
if almacen_in%2==1:
    obj=(obj[0]-1,obj[1])
    
# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
cell_size = int(40//(almacen*0.15))
screen = pygame.display.set_mode((width * cell_size, heigth * cell_size))
pygame.display.set_caption("Búsqueda A* para ir de la casilla I a la F.")


# Inicialización del agente
agent = Agent()

# Bucle principal
running = True
clock = pygame.time.Clock()
'''
# Inicialización de la matriz
matrix = [[0 for _ in range(width)] for _ in range(heigth)]

# Asignar valor 1 a las posiciones de las paredes
for wall in WALLS:
    x, y = wall
    if 0 <= x < width and 0 <= y < heigth:  # Verificar si las coordenadas están dentro de los límites de la matriz
        matrix[y][x] = 1

# Imprimir la matriz
for row in matrix:
    print(row)
'''

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Dibujar rejilla
    for x in range(0, width * cell_size, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, heigth * cell_size))
    for y in range(0, heigth * cell_size, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width * cell_size, y))

    # Dibujar celdas negras (paredes)
    for wall in WALLS:
        pygame.draw.rect(screen, BLACK, (wall[0] * cell_size, wall[1] * cell_size, cell_size, cell_size))

    # Dibujar celda inicial y final
    pygame.draw.rect(screen, BLUE, (agent.position[0] * cell_size, agent.position[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, BLUE, (0, 0, cell_size, cell_size))  # Posición de inicio
    pygame.draw.rect(screen, RED, (obj[0] * cell_size, obj[1] * cell_size, cell_size, cell_size))  # Posición de fin

    # Dibujar números en los estantes
    font = pygame.font.SysFont(None, 12)
    counter = 1
    for i in range(1, width + 1, 3):
        for j in range(1, heigth + 1, 5):
            if (i, j) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, (i * cell_size + 10, j * cell_size + 10))
                counter += 1
            if (i + 1, j) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, ((i + 1) * cell_size + 10, j * cell_size + 10))
                counter += 1
            if (i, j + 1) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, (i * cell_size + 10, (j + 1) * cell_size + 10))
                counter += 1
            if (i + 1, j + 1) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, ((i + 1) * cell_size + 10, (j + 1) * cell_size + 10))
                counter += 1
            if (i, j + 2) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, (i * cell_size + 10, (j + 2) * cell_size + 10))
                counter += 1
            if (i + 1, j + 2) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, ((i + 1) * cell_size + 10, (j + 2) * cell_size + 10))
                counter += 1
            if (i, j + 3) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, (i * cell_size + 10, (j + 3) * cell_size + 10))
                counter += 1
            if (i + 1, j + 3) in WALLS:
                number_text = font.render(str(counter), True, WHITE)
                screen.blit(number_text, ((i + 1) * cell_size + 10, (j + 3) * cell_size + 10))
                counter += 1

            
    # Realizar búsqueda A*
    path = a_star(agent.position, (obj[0], obj[1]))

    # Dibujar camino
    if path:
        for position in path:
            pygame.draw.rect(screen, VIOLET, (position[0] * cell_size, position[1] * cell_size, cell_size, cell_size))

        # Actualizar posición del agente
        agent.move(path[0])

    pygame.display.flip()
    clock.tick(5)

pygame.quit()