import numpy as np

class Enviroment:
    def __init__(self, data:np.array):
        self.enviroment  = data
        self.width       = data.shape[0]
        self.heigth      = data.shape[1]
    
    def neighbors(self, p:tuple):

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])




almacen = 8
# Tamaño del tablero
width  = 3*(almacen//2) + 1
heigth = 5*(almacen//2) + 1

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VIOLET = (255, 0, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Definir las celdas de la pared
WALLS = {(1,1)}  # Paredes en las posiciones de los números

for i in range(1, (width+ 1), 3):
    for j in range(1, (heigth+1), 5):
        WALLS.add((i,j))
        WALLS.add((i,j+1))
        WALLS.add((i,j+2))
        WALLS.add((i,j+3))
        WALLS.add((i+1,j))
        WALLS.add((i+1,j+1))
        WALLS.add((i+1,j+2))
        WALLS.add((i+1,j+3))
    

# Crear un diccionario para mapear el número de estante a sus coordenadas
estante_a_coordenadas = {}