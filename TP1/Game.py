import pygame
from Agent import Agent
from Enviroment import Enviroment

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)

class Game():
    def __init__(self, enviroment:Enviroment):
        self.enviroment = enviroment
        self.cell_size  = int(40//(enviroment.number_of_shelves*0.15))
        pygame.init()
        pygame.display.set_caption("Búsqueda A*")
        self.font       = pygame.font.SysFont(None, 12)
        self.screen     = pygame.display.set_mode((enviroment.width * self.cell_size, enviroment.heigth * self.cell_size))
        self.grid()

    def grid(self):
        self.screen.fill(WHITE)
        for x in range(0, self.enviroment.width * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.enviroment.heigth * self.cell_size))
        for y in range(0, self.enviroment.heigth * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (0, y), (self.enviroment.width * self.cell_size, y))

        for i, row in enumerate(self.enviroment.data):
            for j, element in enumerate(row):
                if self.enviroment.is_shelf((i, j)):
                    pygame.draw.rect(self.screen, BLACK, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                    number_text = self.font.render(str(element), True, WHITE)
                    self.screen.blit(number_text, (j * self.cell_size + 10, i * self.cell_size + 10))

    def checkpoints(self, starts, goals):
        for start in starts:
            pygame.draw.rect(self.screen, BLUE, (start[1]*self.cell_size, start[0]*self.cell_size, self.cell_size, self.cell_size))   # Posición de inicio
        for goal in goals:
            pygame.draw.rect(self.screen, RED, (goal[1] * self.cell_size, goal[0] * self.cell_size, self.cell_size, self.cell_size))  # Posición de fin

    def run(self, agent1:Agent, agent2:Agent):
        running = True
        clock   = pygame.time.Clock()

        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 500)

        first = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == move_event:
                    if first:
                        if agent1.path:
                            pygame.draw.rect(self.screen, VIOLET, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))
                            position = agent1.path.pop(0)
                            agent1.move(position)
                            # Actualizar posición del agente
                            pygame.draw.rect(self.screen, BLUE, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))
                        first = not first
                    else:
                        if agent2.path:
                            pygame.draw.rect(self.screen, RED, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))
                            position = agent2.path.pop(0)
                            agent2.move(position)
                            # Actualizar posición del agente
                            pygame.draw.rect(self.screen, BLACK, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))
                        first = not first
                    pygame.display.flip()
            clock.tick(30)
        pygame.quit()