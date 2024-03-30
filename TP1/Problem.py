from Enviroment import Enviroment

class Problem:
    def __init__(self, enviroment: Enviroment, start: tuple, goal_shelf):
        '''Constructor de la clase Problem, inicializa el problema con el entorno, la posición inicial y el estante objetivo.'''
        self.enviroment     = enviroment            # Establece el entorno del problema
        self.goal_shelf     = goal_shelf            # Establece el estante objetivo
        self.first_start    = start                 # Establece la posición inicial original
        '''Se tiene una posición inicial original porque en caso de colisión con otro agente, el problema
        del agente se debe modificar cambiando la posición inicial para el algoritmo A*'''
        self.start          = start                 # Establece la posición inicial actual
        if isinstance(goal_shelf, int):             # El goal_shelf viene dado como int
            self.goal       = self.enviroment.shelf2coor(goal_shelf)  # Establece el objetivo (se asume que el objetivo es el estante)
        elif isinstance(goal_shelf, tuple):         # El goal_shelf viene dado como tuple
            self.goal       = goal_shelf            # Establece el objetivo (se asume que el objetivo es el estante)
