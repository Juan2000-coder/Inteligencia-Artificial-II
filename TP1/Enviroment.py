import numpy as np

class Enviroment:
    '''Esta clase es básicamente el tablero con los métodos necesarios.'''
    def __init__(self, shelves_rows: int, shelves_columns: int):
        '''Constructor de la clase Enviroment.
        inicializa el entorno con el número dado de filas y columnas de estantes'''

        self.number_of_shelves  = shelves_rows * shelves_columns
        self.shelves_rows       = shelves_rows
        self.shelves_columns    = shelves_columns
        self.width              = 3 * (shelves_columns) + 1
        self.heigth             = 5 * (shelves_rows) + 1
        self.data               = self.get_enviroment()     # Genera el entorno
        self.ocupied            = []                        # Lista para almacenar las posiciones ocupadas

    def get_enviroment(self):
        '''Método para generar el entorno del almacén.
        Llena un numpy array con 0 en los pasillos y los números en las estanterías.'''
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
        data = np.hstack((data, np.zeros((self.heigth, 1))))

        return data

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
        return (0 <= p[0] < self.heigth) and (0 <= p[1] < self.width)

    def is_shelf(self, p: tuple):
        '''Método para verificar si una posición contiene un estante'''
        return self.data[p] != 0

    def is_available(self, p: tuple):
        '''Método para verificar si una posición está disponible (no es un estante ni está ocupada)'''
        return self.is_in(p) and not self.is_shelf(p) and p not in self.ocupied

    def shelf2coor(self, shelf):
        '''Método para convertir un número de estante en coordenadas (fila, columna)'''
        return np.where(self.data == shelf)

    def manhattan(self, p1, p2):
        '''Método para calcular la distancia Manhattan entre dos puntos'''
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
