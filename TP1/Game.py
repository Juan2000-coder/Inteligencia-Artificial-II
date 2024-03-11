import pygame
from Astar import Agent
from Problem import Problem

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)

class Game():
    def __init__(self, problem1:Problem, problem2:Problem):
        self.problem1   = problem1
        self.problem2   = problem2
        self.cell_size  = int(40//(self.problem1.enviroment.number_of_shelves*0.15))
        pygame.init()
        pygame.display.set_caption("Búsqueda A*")
        self.font       = pygame.font.SysFont(None, 12)
        self.screen     = pygame.display.set_mode((self.problem1.enviroment.width * self.cell_size, self.problem1.enviroment.heigth * self.cell_size))
        self.grid()
        

    def grid(self):
        self.screen.fill(WHITE)
        for x in range(0, self.problem1.enviroment.width * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.problem1.enviroment.heigth * self.cell_size))
        for y in range(0, self.problem1.enviroment.heigth * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (0, y), (self.problem1.enviroment.width * self.cell_size, y))

        for i, row in enumerate(self.problem1.enviroment.data):
            for j, element in enumerate(row):
                if self.problem1.enviroment.is_shelf((i, j)):
                    pygame.draw.rect(self.screen, BLACK, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                    number_text = self.font.render(str(element), True, WHITE)
                    self.screen.blit(number_text, (j * self.cell_size + 10, i * self.cell_size + 10))

        pygame.draw.rect(self.screen, BLUE, (self.problem1.start[1]*self.cell_size, self.problem1.start[0]*self.cell_size, self.cell_size, self.cell_size))   # Posición de inicio
        pygame.draw.rect(self.screen, RED, (self.problem1.goal[1] * self.cell_size, self.problem1.goal[0] * self.cell_size, self.cell_size, self.cell_size))  # Posición de fin

        pygame.draw.rect(self.screen, BLUE, (self.problem2.start[1]*self.cell_size, self.problem2.start[0]*self.cell_size, self.cell_size, self.cell_size))   # Posición de inicio
        pygame.draw.rect(self.screen, RED, (self.problem2.goal[1] * self.cell_size, self.problem2.goal[0] * self.cell_size, self.cell_size, self.cell_size))  # Posición de fin

    def run(self, path1:list, path2:list, agent1:Agent, agent2:Agent):
        running = True
        clock   = pygame.time.Clock()

        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 1000)

        first = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == move_event:
                    if first:
                        if path1:
                            position = path1.pop(0)
                            pygame.draw.rect(self.screen, VIOLET, (position[1] * self.cell_size, position[0] * self.cell_size, self.cell_size, self.cell_size))
                            # Actualizar posición del agente
                            agent1.move(position)
                            #pygame.draw.rect(screen, BLUE, (agent.position[1] * cell_size, agent.position[0] * cell_size, cell_size, cell_size))
                        first = not first
                    else:
                        if path2:
                            position = path2.pop(0)
                            pygame.draw.rect(self.screen, VIOLET, (position[1] * self.cell_size, position[0] * self.cell_size, self.cell_size, self.cell_size))
                            # Actualizar posición del agente
                            agent2.move(position)
                            #pygame.draw.rect(screen, BLUE, (agent.position[1] * cell_size, agent.position[0] * cell_size, cell_size, cell_size))
                        first = not first
                    pygame.display.flip()
            clock.tick(30)
        pygame.quit()