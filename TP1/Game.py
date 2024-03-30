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
    def __init__(self, enviroment: Enviroment):
        self.enviroment     = enviroment    # El tablero de juego
        self.cell_size      = int(40 // (enviroment.number_of_shelves * 0.15))  # Calcula el tamaño de la celda en función del número de estantes
        pygame.init()                       # Inicializa pygame
        pygame.display.set_caption("Búsqueda A*")           # Establece el título de la ventana
        self.font           = pygame.font.SysFont(None, 12) # Establece la fuente de texto
        self.screen         = pygame.display.set_mode((enviroment.width * self.cell_size, enviroment.height * self.cell_size))  # Crea la pantalla del juego con el tamaño calculado
        self.grid()                                         # Dibuja la cuadrícula del juego

    def grid(self):
        '''Método para dibujar la cuadrícula del juego'''
        self.screen.fill(WHITE)  # Rellena la pantalla con color blanco
        for x in range(0, self.enviroment.width * self.cell_size, self.cell_size):
            # Dibuja líneas verticales para representar las columnas de la cuadrícula
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.enviroment.height * self.cell_size))
        for y in range(0, self.enviroment.height * self.cell_size, self.cell_size):
            # Dibuja líneas horizontales para representar las filas de la cuadrícula
            pygame.draw.line(self.screen, BLACK, (0, y), (self.enviroment.width * self.cell_size, y))

        for i, row in enumerate(self.enviroment.data):
            for j, element in enumerate(row):
                if self.enviroment.is_shelf((i, j)):
                    # Si la posición contiene un estante, dibuja un rectángulo negro en la celda correspondiente
                    pygame.draw.rect(self.screen, BLACK, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                    number_text = self.font.render(str(element), True, WHITE)
                    # Dibuja el número del estante en la celda
                    self.screen.blit(number_text, (j * self.cell_size + 10, i * self.cell_size + 10))
        pygame.display.flip()  # Actualiza la pantalla del juego

    def run(self, agent1: Agent, agent2: Agent):
        '''Sumulación del recorrido de los montacargas'''
        running = True
        clock   = pygame.time.Clock()

        move_event  = pygame.USEREVENT + 1       # Evento de movimiento de cada montacargas
        pygame.time.set_timer(move_event, 200)  # Configura un temporizador para controlar el movimiento de los agentes

        first       = True   # Variable para controlar el turno de los agentes
        reversed1   = False  # Variable para controlar si se ha invertido el camino del agente 1 (va de regreso)
        reversed2   = False  # Variable para controlar si se ha invertido el camino del agente 2 (va de regreso)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Se cierra la ventana
                    running = False
                elif event.type == move_event:  # Es un turno de movimiento
                    if first:                   # Si es el turno del agente 1
                        if agent1.path:         # El agente 1 tiene un camino por recorrer 
                            # Dibuja el agente 1 en su posición actual antes de moverlo
                            pygame.draw.rect(self.screen, VIOLET, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))

                            # Mueve al agente 1 a la siguiente posición en su camino
                            position = agent1.path.pop(0)
                            agent1.move(position)
                            
                            # Dibuja al agente 1 en su nueva posición después de moverlo
                            pygame.draw.rect(self.screen, BLUE, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))

                        elif not reversed1: # Si el agente 1 ha llegado al final de su camino y no se ha invertido su camino
                            reversed1                 = True     # Ya no se invertira el camino otra vez
                            agent1.problem.goal_shelf = None     # En el regreso no se busca un estante
                            agent1.problem.start      = agent1.position             # El inicio es en la posición actual
                            agent1.problem.goal       = agent1.problem.first_start  # El final es en la posición inicial original
                            agent1.a_star.re_init(agent1.problem)                   # Reinicia el algoritmo
                            agent1.path = agent1.a_star.solve()                     # Calcula la ruta de regreso
                        first = not first   # Cambia al turno del agente 2
                    else:                   # Si es el turno del agente 2
                        if agent2.path:     # Si el agente 2 tiene un camino por recorrer
                            # Dibuja el agente 2 en su posición actual antes de moverlo
                            pygame.draw.rect(self.screen, YELLOW, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))

                            # Mueve al agente 2 a la siguiente posición en su camino
                            position = agent2.path.pop(0)
                            agent2.move(position)
                            
                            # Dibuja al agente 2 en su nueva posición después de moverlo
                            pygame.draw.rect(self.screen, GREEN, (agent2.position[1] * self.cell_size, agent2.position[0] * self.cell_size, self.cell_size, self.cell_size))

                        elif not reversed2: # Si el agente 2 ha llegado al final de su camino y no se ha invertido su camino
                            reversed2                   = True      # Ya no se invertira el camino otra vez
                            agent2.problem.goal_shelf   = None      # En el regreso no se busca un estante
                            agent2.problem.start        = agent2.position            # El inicio es en la posición actual
                            agent2.problem.goal         = agent2.problem.first_start # El final es en la posición inicial original
                            agent2.a_star.re_init(agent2.problem)                    # Reinicia el algoritmo
                            agent2.path                 = agent2.a_star.solve()      # Calcula la ruta de regreso
                        first = not first  # Cambia al turno del agente 1
                    pygame.display.flip()  # Actualiza la pantalla del juego
            clock.tick(30)  # Controla la velocidad del bucle
        pygame.quit()       # Cierra pygame y sale del juego

    ###-----------DIBUJAR LOS ESTANTES CUANDO VIENEN DADOS COMO LISTA--------###
    def paint_goals(self, lista):
        for shelf in lista:
            coord = self.enviroment.shelf2coor(shelf)
            pygame.draw.rect(self.screen, RED, (coord[1] * self.cell_size, coord[0] * self.cell_size, self.cell_size, self.cell_size))
            pygame.display.flip()

        
    def get_checkpoints(self):
        '''Método para obtener las posiciones de inicio y llegada seleccionadas por el usuario'''
        running = True
        clock   = pygame.time.Clock()   # Para control de tiempos

        start_positions     = []    # Lista para almacenar las posiciones de inicio seleccionadas
        goal_positions      = []    # Lista para almacenar las posiciones de llegada seleccionadas
        full                = False # Bandera para indicar si se han seleccionado todas las posiciones necesarias

        while running and (not full):  # Ciclo principal para interactuar con el usuario y seleccionar las posiciones
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # El usuario cierra la ventana
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:     # El usuario presiona el click derecho del mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtiene la posición del mouse
                    cell_x, cell_y = mouse_x // self.cell_size, mouse_y // self.cell_size   # Coordenadas x,y de la celda
                    # Las posiciones en el np.array se usan con los indices invertidos.

                    if len(start_positions) < 2:               # Solo permite dos posiciones de inicio
                        if not self.enviroment.is_shelf((cell_y, cell_x)):  # Verifica que la celda no sea un estante
                            if len(start_positions) == 0:
                                start_positions.append((cell_y, cell_x))
                                pygame.draw.rect(self.screen, BLUE, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                                # Dibuja un rectángulo azul en la celda para indicar la posición de inicio
                            else:
                                start_positions.append((cell_y, cell_x))
                                pygame.draw.rect(self.screen, GREEN, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                                # Dibuja un rectángulo verde en la celda para indicar la segunda posición de inicio

                    elif len(goal_positions) < 2:               # Solo permite dos posiciones de llegada
                        if self.enviroment.is_shelf((cell_y, cell_x)):  # Verifica que la celda sí sea un estante
                            goal_positions.append((cell_y, cell_x))
                            pygame.draw.rect(self.screen, RED, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                            # Dibuja un rectángulo rojo en la celda para indicar la posición de llegada
                    else:
                        full = True             # Se han seleccionado todas las posiciones necesarias
                    pygame.display.flip()       # Actualiza la pantalla del juego
            clock.tick(30)                      # Controla la velocidad del bucle
        return start_positions, goal_positions  # Retorna las posiciones de inicio y llegada seleccionadas
    




##############################AGREGADO VALENTIN EJ3############################################
    def run_ej3(self, agent1: Agent, solucion_optima:list):
            '''Sumulación del recorrido del montacargas'''
            running = True
            clock   = pygame.time.Clock()

            move_event  = pygame.USEREVENT + 1       # Evento de movimiento del montacargas
            pygame.time.set_timer(move_event, 200)  # Configura un temporizador para controlar el movimiento del agente

            check = False
            goal = solucion_optima.pop(0)
            i = 1

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:   # Se cierra la ventana
                        running = False
                    elif event.type == move_event:  # Es un turno de movimiento
                        if agent1.path:
                            # Dibuja el agente 1 en su posición actual antes de moverlo
                            pygame.draw.rect(self.screen, VIOLET, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))
                            # Mueve al agente 1 a la siguiente posición en su camino
                            position = agent1.path.pop(0)
                            #neighbors = agent1.problem.enviroment.neighbors(goal))
                            goal_coords = agent1.problem.enviroment.shelf2coor(goal)
                            neighbors = agent1.problem.enviroment.neighbors(goal_coords)

                            if position in neighbors:
                                number_text = self.font.render(str(i), True, BLACK)
                                # Dibuja el número del estante en la celda
                                pygame.draw.rect(self.screen, GREEN, (goal_coords[1] * self.cell_size, goal_coords[0] * self.cell_size, self.cell_size, self.cell_size))
                                self.screen.blit(number_text, (goal_coords[1]* self.cell_size + 10, goal_coords[0] * self.cell_size + 10))
                                if solucion_optima:
                                    goal = solucion_optima.pop(0)
                                    i += 1
                                    #neighbors = agent1.problem.enviroment.neighbors(goal)
                                    goal_coords = agent1.problem.enviroment.shelf2coor(goal)
                                    neighbors = agent1.problem.enviroment.neighbors(goal_coords)
                                    if position in neighbors:
                                        number_text = self.font.render(str(i), True, BLACK)
                                        pygame.draw.rect(self.screen, GREEN, (goal_coords[1] * self.cell_size, goal_coords[0] * self.cell_size, self.cell_size, self.cell_size))
                                        self.screen.blit(number_text, (goal_coords[1]* self.cell_size + 10, goal_coords[0] * self.cell_size + 10))
                                        if solucion_optima:
                                            goal = solucion_optima.pop(0)
                                            i += 1
                                pygame.time.set_timer(move_event, 800)
                                check = True
                            elif check:
                                pygame.time.set_timer(move_event, 200)
                            agent1.move(position)                    
                            # Dibuja al agente 1 en su nueva posición después de moverlo
                            pygame.draw.rect(self.screen, BLUE, (agent1.position[1] * self.cell_size, agent1.position[0] * self.cell_size, self.cell_size, self.cell_size))

                            pygame.display.flip()  # Actualiza la pantalla del juego
                clock.tick(30)  # Controla la velocidad del bucle
            pygame.quit()       # Cierra pygame y sale del juego


    def get_checkpoints_list(self):
        '''Método para obtener la posicion de inicio y las de las distintas llegadas seleccionadas por el usuario'''
        running = True
        clock   = pygame.time.Clock()   # Para control de tiempos

        start_position       = []    # Lista para almacenar la posicion de inicio seleccionada
        goals_positions      = []    # Lista para almacenar las posiciones de llegadas seleccionadas
        full                 = False # Bandera para indicar si se han seleccionado todas las posiciones necesarias

        while running and (not full):  # Ciclo principal para interactuar con el usuario y seleccionar las posiciones
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # El usuario cierra la ventana
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:     # El usuario presiona el click derecho del mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtiene la posición del mouse
                    cell_x, cell_y = mouse_x // self.cell_size, mouse_y // self.cell_size   # Coordenadas x,y de la celda
                    # Las posiciones en el np.array se usan con los indices invertidos.

                    if len(start_position) < 1:               # Solo permite una posiciones de inicio
                        if not self.enviroment.is_shelf((cell_y, cell_x)):  # Verifica que la celda no sea un estante
                            start_position.append((cell_y, cell_x))
                            pygame.draw.rect(self.screen, BLUE, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                            # Dibuja un rectángulo azul en la celda para indicar la posición de inicio
                    elif self.enviroment.is_shelf((cell_y, cell_x)):  # Verifica que la celda sí sea un estante
                        goals_positions.append((cell_y, cell_x))
                        pygame.draw.rect(self.screen, RED, (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size))
                        # Dibuja un rectángulo rojo en la celda para indicar la posición de llegada
                elif event.type == pygame.KEYDOWN:  # El usuario presiona una tecla
                    if event.key == pygame.K_RETURN: # El usuario presiona la tecla "Enter"
                        full = True             # Se han seleccionado todas las posiciones necesarias
                pygame.display.flip()       # Actualiza la pantalla del juego
            clock.tick(30)                      # Controla la velocidad del bucle
        return start_position, goals_positions  # Retorna la posicion de inicio y las de llegada seleccionadas

##############################AGREGADO VALENTIN EJ3############################################    
