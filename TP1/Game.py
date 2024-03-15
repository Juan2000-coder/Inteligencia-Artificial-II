import pygame
from Agent import Agent
from Enviroment import Enviroment

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)

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
        pygame.display.flip()


    def run(self, agent1:Agent, agent2:Agent):
        running = True
        clock   = pygame.time.Clock()

        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 200)

        first     = True
        reversed1 = False
        reversed2 = False
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
                        elif not reversed1:
                            reversed1 = True
                            agent1.problem.goal_shelf = None
                            agent1.problem.start = agent1.position
                            agent1.problem.goal  = agent1.problem.first_start
                            agent1.a_star.re_init(agent1.problem)
                            agent1.path = agent1.a_star.solve()
                        first = not first
                    else:
                        if agent2.path:
                            pygame.draw.rect(self.screen, YELLOW, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))
                            position = agent2.path.pop(0)
                            agent2.move(position)
                            # Actualizar posición del agente
                            pygame.draw.rect(self.screen, GREEN, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))
                        elif not reversed2:
                            reversed2 = True
                            agent2.problem.goal_shelf = None
                            agent2.problem.start = agent2.position
                            agent2.problem.goal  = agent2.problem.first_start
                            agent2.a_star.re_init(agent2.problem)
                            agent2.path = agent2.a_star.solve()
                        first = not first
                    pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def get_checkpoints(self):
        running = True
        clock   = pygame.time.Clock()

        start_positions = []
        goal_positions = []
        full = False

        while running and (not full):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cell_x, cell_y = mouse_x // self.cell_size, mouse_y // self.cell_size
                    if len(start_positions) < 2:  # Solo permitir dos posiciones de inicio
                        if not self.enviroment.is_shelf((cell_y, cell_x)):
                            if len(start_positions) == 0:
                                start_positions.append((cell_y, cell_x))
                                pygame.draw.rect(self.screen, BLUE, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                            else:
                                start_positions.append((cell_y, cell_x))
                                pygame.draw.rect(self.screen, GREEN, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                    elif len(goal_positions) < 2:  # Solo permitir dos posiciones de llegada
                        if self.enviroment.is_shelf((cell_y, cell_x)):
                            goal_positions.append((cell_y, cell_x))
                            pygame.draw.rect(self.screen, RED, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                    else:
                        full = True
                    pygame.display.flip()
            clock.tick(30)
        return start_positions, goal_positions
    


#############################VALENTIN AGREGADO#############################
    def get_checkpoints_list(self):
        running = True
        clock   = pygame.time.Clock()

        start_position = []
        goals_positions = []        # Cambio de nombre para que sea más descriptivo
        full = False

        while running and (not full):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cell_x, cell_y = mouse_x // self.cell_size, mouse_y // self.cell_size
                    if len(start_position) < 1:  # Solo permitir una posicion de inicio
                        if not self.enviroment.is_shelf((cell_y, cell_x)):
                            start_position.append((cell_y, cell_x))
                            pygame.draw.rect(self.screen, BLUE, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                    elif self.enviroment.is_shelf((cell_y, cell_x)):
                        goals_positions.append((cell_y, cell_x))
                        pygame.draw.rect(self.screen, RED, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:    # Al presiona la tecla "Enter", se detiene el bucle
                        full = True
                pygame.display.flip()
            clock.tick(30)
        return start_position, goals_positions
    

    def run_ej3(self, agent1:Agent):
        running = True
        clock   = pygame.time.Clock()

        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 200)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == move_event:
                    if agent1.path:
                        pygame.draw.rect(self.screen, VIOLET, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))
                        position = agent1.path.pop(0)
                        agent1.move(position)
                        # Actualizar posición del agente
                        pygame.draw.rect(self.screen, BLUE, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))
                    pygame.display.flip()
            clock.tick(30)
        pygame.quit()
    
#############################################################################