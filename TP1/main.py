import pygame
from Problem import Problem
from Enviroment import Enviroment
from Astar import A_star, Agent

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)

#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))
    start_row         = int(input("Ingrese la fila de partida: "))
    start_column      = int(input("Ingrese la columna de partida: "))
    start             = (start_row, start_column)
    shelf_goal        = int(input("Ingrese el número de estante que desea buscar: "))

    enviroment        = Enviroment(shelves_rows, shelves_columns)
    goal              = enviroment.get_goalcell(start, shelf_goal)

    problem           = Problem(enviroment, start, goal)
    a_star            = A_star(problem)
    agent             = Agent(start)

    # Realizar búsqueda A*
    path = a_star.solve()
    
    pygame.init()
    cell_size = int(40//(enviroment.number_of_shelves*0.15))
    screen = pygame.display.set_mode((enviroment.width * cell_size, enviroment.heigth * cell_size))
    pygame.display.set_caption("Búsqueda A*")

    # Bucle principal
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # Dibujar rejilla
        for x in range(0, enviroment.width * cell_size, cell_size):
            pygame.draw.line(screen, BLACK, (x, 0), (x, enviroment.heigth * cell_size))
        for y in range(0, enviroment.heigth * cell_size, cell_size):
            pygame.draw.line(screen, BLACK, (0, y), (enviroment.width * cell_size, y))

        # Dibujar celdas negras (paredes)
        # Dibujar números en los estantes
        font = pygame.font.SysFont(None, 12)

        for i, row in enumerate(enviroment.data):
            for j, element in enumerate(row):
                if enviroment.is_shelf((i, j)):
                    pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size))
                    number_text = font.render(str(element), True, WHITE)
                    screen.blit(number_text, (j * cell_size + 10, i * cell_size + 10))

        # Dibujar celda inicial y final
        pygame.draw.rect(screen, BLUE, (agent.position[1] * cell_size, agent.position[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, BLUE, (start[1]*cell_size, start[0]*cell_size, cell_size, cell_size))  # Posición de inicio
        pygame.draw.rect(screen, RED, (goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size))  # Posición de fin

        # Dibujar camino
        if path:
            for position in path:
                pygame.draw.rect(screen, VIOLET, (position[1] * cell_size, position[0] * cell_size, cell_size, cell_size))
                # Actualizar posición del agente
                agent.move(position)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()