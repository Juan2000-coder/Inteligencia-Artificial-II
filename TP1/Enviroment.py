import numpy as np

class Enviroment():
    def __init__(self):
        self.height         = None
        self.width          = None
        self.ocupied:list   = None
        self.data:np.array  = None

    def get_enviroment(self, gen:list = []):
        '''Redefinir en la clase Hijo.
        Para definir la estructura de datos del entorno.
        La unica convención es que los estantes son números enteros mayores a cero
        y los pasillos se representan con cero'''
        pass

    def neighbors(self, p: tuple):
        '''Método para obtener los vecinos de una posición dada.
        Solo devuelve casillas vecinas en un pasillo que no están ocupadas.'''
        neighbors_list = []
        for step in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            pos = tuple(x + y for x, y in zip(p, step))
            if self.is_available(pos):
                neighbors_list.append(pos)
        return neighbors_list

    def is_in(self, p: tuple):
        '''Método para verificar si una posición está dentro de los límites del entorno'''
        return (0 <= p[0] < self.height) and (0 <= p[1] < self.width)

    def is_shelf(self, p: tuple):
        '''Método para verificar si una posición contiene un estante'''
        return self.data[p] != 0

    def is_available(self, p: tuple):
        '''Método para verificar si una posición está disponible (no es un estante ni está ocupada)'''
        return self.is_in(p) and not self.is_shelf(p) and p not in self.ocupied

    def shelf2coor(self, sh):
        '''Método para convertir un número de estante en coordenadas (fila, columna)'''
        p = np.where(self.data == sh)
        return (p[0][0], p[1][0])

    def manhattan(self, p1, p2):
        '''Método para calcular la distancia Manhattan entre dos puntos'''
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Almacen(Enviroment):
    '''Esta clase es básicamente el tablero con los métodos necesarios.'''
    def __init__(self, shelves_rows: int, shelves_columns: int, gen:list = []):
        super().__init__()
        '''Constructor de la clase Enviroment.
        inicializa el entorno con el número dado de filas y columnas de estantes'''
        self.number_of_shelves  = shelves_rows * shelves_columns
        self.shelves_rows       = shelves_rows
        self.shelves_columns    = shelves_columns
        self.width              = 3 * (shelves_columns) + 1
        self.height             = 5 * (shelves_rows) + 1
        self.data               = self.get_enviroment(gen) # Genera el entorno
        self.ocupied            = []                        # Lista para almacenar las posiciones ocupadas
    
    def get_enviroment(self, gen:list = []):
        '''Método para generar el entorno del almacén.
        Llena un numpy array con 0 en los pasillos y los números en las estanterías.'''
        if not gen:
            shelf = np.arange(1, 9).reshape(4, 2)
            for j in range(self.shelves_columns):
                shift = shelf + self.shelves_rows * 8 * j

                for i in range(self.shelves_rows):
                    block = shift + 8 * i
                    block = np.hstack((np.zeros((4, 1)), block))
                    block = np.vstack((np.zeros((1, 3)), block))

                    if i == 0:
                        column = block
                    else:
                        column = np.vstack((column, block))
                column = np.vstack((column, np.zeros((1, 3))))
                if j == 0:
                    data = column
                else:
                    data = np.hstack((data, column))
            data = np.hstack((data, np.zeros((self.height, 1))))
        else:
            k = 0
            for j in range(self.shelves_columns):
                for i in range(self.shelves_rows):
                    block = np.array(gen[k*8:(k+1)*8]).reshape(4, 2)
                    block = np.hstack((np.zeros((4, 1)), block))
                    block = np.vstack((np.zeros((1, 3)), block))
                    if i == 0:
                        column = block
                    else:
                        column = np.vstack((column, block))
                    # Insertar la estantería en el entorno del almacén
                    k += 1
                column = np.vstack((column, np.zeros((1, 3))))
                if j == 0:
                    data = column
                else:
                    data = np.hstack((data, column))
            data = np.hstack((data, np.zeros((self.height, 1)))) 
        return data

    def is_invertix(self, sh):
        p = self.shelf2coor(sh)
        return (p[0] - 1) % 5 == 0 or (p[0] - 4) % 5 == 0
    
    def are_beside(self, sh1, sh2):
        '''Método para determinar si dos estántes están uno al lado del otro
        en una misma columna de una estánteria, por ejemplo 1 y 3.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return p1[1] == p2 [1] and abs(p1[0] - p2[0]) == 1
    
    def are_opposed(self, sh1, sh2):
        '''Método para determinar si dos estántes están frente a frente
        separados por un pasillo, por ejemplo 2 y 17 en una nave de 2 filas.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return p1[0] == p2 [0] and abs(p1[1] - p2[1]) == 2
    
    def are_border_opposed(self, sh1, sh2):
        '''Método para determinar si dos estántes están frente a frente
        separados por un pasillo en bordes de estanterías, por ejemplo 7 y 9
        en una nave de al menos dos filas.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return abs(p1[0] - p2 [0]) == 2 and p1[1] == p2[1] and self.is_invertix(sh1) and self.is_invertix(sh2)
    
    def are_border_beside(self, sh1, sh2):
        '''Método para determinar si dos estántes están uno al lado del 
        otro pero en el borde de la estanteria. Por ejemplo 1 y 2.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return p1[0] == p2 [0] and abs(p1[1] - p2[1]) == 1 and self.is_invertix(sh1)
    
    def are_cross_beside(self, sh1, sh2):
        '''Método para determinar si dos estántes están en filas adyacentes
        pero separados por un pasillo en columnas de estanterías enfrentadas.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return abs(p1[0] - p2 [0]) == 1 and abs(p1[1] - p2[1]) == 2
    
    def are_border_cross_beside(self, sh1, sh2):
        '''Método para determinar si dos estántes están separados por un pasillo
        entre bordes de dos estanterías y cruzados. Por ejemplo 8 y 9 en una nave
        de al menos filas.'''
        p1 = self.shelf2coor(sh1)
        p2 = self.shelf2coor(sh2)
        return abs(p1[0] - p2 [0]) == 2 and abs(p1[1] - p2[1]) == 1 and self.is_invertix(sh1) and self.is_invertix(sh2)
    
class U(Enviroment):
    def __init__(self, size:int):
        super().__init__()
        self.height = size
        self.width  = self.height
        self.data   = self.get_enviroment()
        self.ocupied = []

    def get_enviroment(self, gen: list = []):
        # Crear una matriz cuadrada llena de ceros
        data = np.zeros((self.height, self.width), dtype=int)

        # Llenar la segunda fila con unos desde la segunda columna hasta la ante-penúltima columna
        data[1, 1:-2] = 1

        # Llenar la penúltima fila con unos desde la segunda columna hasta la ante-penúltima columna
        data[-2, 1:-2] = 1

        # Llenar la columna ante-penúltima con unos entre la segunda y la penúltima fila
        data[1:-1, -3] = 1

        # Poner un 10 en la posición correspondiente a la fila del medio y la última columna
        data[self.height // 2, -1] = 10
        return data