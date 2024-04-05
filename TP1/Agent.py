from Astar import A_star
from Enviroment import Enviroment


class Agent34:
    def __init__(self, initial_position: tuple, enviroment: Enviroment):
        self.initial_position   = initial_position
        self.position           = initial_position
        self.enviroment         = enviroment
        self.path:list          = []

    def move(self, new_position:tuple):
        '''Método para mover al agente a una nueva posición'''

        # Encuentra el índice de la posición actual en la lista de posiciones ocupadas
        indice = self.enviroment.ocupied.index(self.position)
        
        # Remueve la posición actual de la lista de posiciones ocupadas
        self.enviroment.ocupied.pop(indice)
        self.position = new_position
        self.enviroment.ocupied.append(self.position)
    

class Agent12(Agent34):
    def __init__(self, initial_position: tuple, enviroment: Enviroment, a_star: A_star):
        super().__init__(initial_position, enviroment)
        self.a_star = a_star

    def check_move(self, position):
        '''Método para verificar si un movimiento es válido'''

        # Retorna True si la posición no está ocupada, False de lo contrario
        return not (position in self.enviroment.ocupied)

    def move(self, new_position:tuple):
        '''Método para mover al agente a una nueva posición'''

        # Encuentra el índice de la posición actual en la lista de posiciones ocupadas
        indice = self.enviroment.ocupied.index(self.position)
        # Remueve la posición actual de la lista de posiciones ocupadas
        self.enviroment.ocupied.pop(indice)

        if self.check_move(new_position):
            # Si el movimiento es válido, actualiza la posición del agente
            self.position = new_position
        else:
            # Si el movimiento no es válido, reinicia el problema y encuentra un nuevo camino
            self.a_star.re_init(self.position, self.a_star.goal)
            self.path           = self.a_star.solve()
            # Actualiza la posición del agente al siguiente paso del camino
            self.position       = self.path.pop(0)
        # Agrega la nueva posición del agente a la lista de posiciones ocupadas
        self.enviroment.ocupied.append(self.position)