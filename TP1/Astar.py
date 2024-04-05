import heapq                 # Importa el módulo heapq para el manejo de colas
from Enviroment import Enviroment


class A_star():
    def __init__(self, enviroment:Enviroment, start:tuple, goal):
        '''Constructor de la clase A_star'''
        self.enviroment = enviroment
        self.start                  = start
        self.goal, self.goal_shelf  = self.set_goal(goal)
        self.settings()  # Llama al método settings para configurar la búsqueda A*

    def set_goal(self, goal):
        if isinstance(goal, int):       # El objetivo es un estante
            goal_shelf = goal
            goal       = self.enviroment.shelf2coor(goal)
        elif isinstance(goal, tuple):   # El objetivo no es un estante
            if self.enviroment.is_shelf(goal):
                goal_shelf = int(self.enviroment.data[goal])
            else:
                goal_shelf = None
        return goal, goal_shelf
        
    def settings(self):
        '''Método para configurar la búsqueda A*.
        Setea la lista abierta y los costos de camino de las casillas.'''

        self.open_list = [(self.enviroment.manhattan(self.start, self.goal), self.start)]  # Lista abierta inicial con el nodo de inicio y su costo estimado
        self.parent_of = {}                         # Diccionario para almacenar los padres de cada nodo

        self.g_score    = {(x, y): float('inf') for x in range(self.enviroment.height) for y in range(self.enviroment.width)}
        # Inicializa los valores de g_score a infinito para cada posición posible

        self.g_score[self.start] = 0        # Establece el valor de g_score para el nodo inicial en 0

    def re_init(self, start:tuple, goal):
        '''Método para reinicializar la búsqueda A* con un nuevo problema'''
        self.start                   = start
        self.goal, self.goal_shelf   = self.set_goal(goal)
        self.settings()                             # Llama al método settings para reconfigurar la búsqueda A*

    def goal_test(self, current: tuple):
        '''Método para verificar si el nodo actual es el nodo objetivo'''
        if self.goal_shelf is None: # El objetivo no es un estante. Por ejemplo en el camino de retorno
            return current == self.goal
        else:                       # El objetivo sí es un estante. Por ejemplo en el camino directo
            return self.enviroment.manhattan(current, self.goal) == 1

    def get_path(self, current: tuple):
        '''Método para reconstruir el camino desde el nodo actual hasta el nodo inicial'''
        path    = []                            # Inicializa la lista de camino
        current = current                       # Establece el nodo actual como el inicio del camino
        while current in self.parent_of:        # Itera hasta llegar al nodo inicial (que no tiene padre)
            path.insert(0, current)             # Agrega el nodo actual al principio del camino
            current = self.parent_of[current]   # Actualiza el nodo actual al padre del nodo actual
        return path                             # Retorna el camino construido

    def solve(self)->list:
        '''Método para realizar la búsqueda A*'''
        while self.open_list:                           # Itera mientras la lista abierta no esté vacía
            current = heapq.heappop(self.open_list)[1]  # Extrae el nodo con el menor costo estimado de la lista abierta
            if self.goal_test(current):                 # Verifica si el nodo actual es el nodo objetivo
                path = self.get_path(current)           # Reconstruye el camino
                return path                             # Retorna el camino
            self.expand(current)                        # Expande el nodo actual

    def expand(self, current: tuple):
        '''Método para expandir el nodo actual y actualizar los valores de los nodos vecinos'''
        neighbors = self.enviroment.neighbors(current)  # Obtiene los vecinos del nodo actual
        for neighbor in neighbors:                              # Itera sobre los vecinos del nodo actual
            tentative_g_score = self.g_score[current] + 1       # Calcula el puntaje g tentativo para el vecino

            if tentative_g_score < self.g_score[neighbor]:      # Comprueba si el puntaje g tentativo es menor que el puntaje g actual del vecino
                self.parent_of[neighbor] = current              # Actualiza el padre del vecino
                self.g_score[neighbor] = tentative_g_score      # Actualiza el puntaje g del vecino
                f_score = tentative_g_score + self.enviroment.manhattan(neighbor, self.goal) # Función de evaluación
                heapq.heappush(self.open_list, (f_score, neighbor)) # Agrega el vecino a la lista abierta con su puntaje f estimado