from Astar      import A_star
from Problem    import Problem

class Agent:
    def __init__(self, problem: Problem):
        '''Constructor de la clase Agent'''

        # Inicializa el agente con un problema dado
        self.problem    = problem
        # Establece la posición inicial del agente
        self.position   = self.problem.start
        # Inicializa el algoritmo A* con el problema dado
        self.a_star     = A_star(self.problem)
        # Inicializa una lista vacía para almacenar el camino del agente
        self.path:list       = []

    def check_move(self, position):
        '''Método para verificar si un movimiento es válido'''

        # Retorna True si la posición no está ocupada, False de lo contrario
        return not (position in self.problem.enviroment.ocupied)

    def move(self, new_position):
        '''Método para mover al agente a una nueva posición'''

        # Encuentra el índice de la posición actual en la lista de posiciones ocupadas
        indice = self.problem.enviroment.ocupied.index(self.position)
        # Remueve la posición actual de la lista de posiciones ocupadas
        self.problem.enviroment.ocupied.pop(indice)

        if self.check_move(new_position):
            # Si el movimiento es válido, actualiza la posición del agente
            self.position = new_position
        else:
            # Si el movimiento no es válido, reinicia el problema y encuentra un nuevo camino
            self.problem.start  = self.position
            self.a_star.re_init(self.problem)
            self.path           = self.a_star.solve()
            # Actualiza la posición del agente al siguiente paso del camino
            self.position       = self.path.pop(0)
        # Agrega la nueva posición del agente a la lista de posiciones ocupadas
        self.problem.enviroment.ocupied.append(self.position)

