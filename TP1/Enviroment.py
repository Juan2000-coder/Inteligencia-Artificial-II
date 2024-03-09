import math
class Position:
    def __init__(self, coordinate:tuple):
        # De esta manera se aceptan no solo de 2 elementos
        self.coordinate = coordinate

class Space:
    def __init__(self, data):
        #data: probablemente sea un np.array
        self.data  = data

    def is_wall(self, position:Position):
        # Debe indicar si la coordenada indicada es una pared
        # Específico del problema
        pass

    def neighbours(self, position:Position):
        # Debe indicar las coordenadas de los vecinos 
        # Específico del problema
        pass

    def manhattan(self, A:Position, B:Position):
        return sum(abs(xB - xA) for xA, xB in zip(A.coordinate, B.coordinate))

    def euclidean(self, A:Position, B:Position):
        return math.sqrt(sum((xA - xB) ** 2 for xA, xB in zip(A, B)))