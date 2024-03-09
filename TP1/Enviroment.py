import numpy as np

class Enviroment:
    def __init__(self, shelves_width:int, shelves_heigth:int):
        # Ancho y altura dados en número de estantes
        self.number_of_shelves  = shelves_width*shelves_heigth
        self.shelves_width      = shelves_width
        self.shelves_heigth     = shelves_heigth
        self.width              = 3*(shelves_heigth) + 1
        self.heigth             = 5*(shelves_width)  + 1
        self.data               = self.get_enviroment()
    
    def get_enviroment(self):
        shifth = np.array[]
        for i in self.shelves_width:
            for j in self.shelves_heigth:
                np.array[]
    def neighbors(self, p:tuple):

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)

    

# Crear un diccionario para mapear el número de estante a sus coordenadas
shelf_2_coordinate = {}

# Inicializar el contador de estantes
counter = 1

# Iterar sobre las posiciones en las que se dibujarán los números
for i in range(1, width + 1, 3):
    for j in range(1, heigth + 1, 5):
        # Verificar si la posición actual está en las paredes
        if (i, j) in WALLS:
            # Agregar la posición al diccionario de estantes
            estante_a_coordenadas[counter] = (i, j)
            counter += 1
        if (i + 1, j) in WALLS:
            estante_a_coordenadas[counter] = (i + 1, j)
            counter += 1
        if (i, j + 1) in WALLS:
            estante_a_coordenadas[counter] = (i, j + 1)
            counter += 1
        if (i + 1, j + 1) in WALLS:
            estante_a_coordenadas[counter] = (i + 1, j + 1)
            counter += 1
        if (i, j + 2) in WALLS:
            estante_a_coordenadas[counter] = (i, j + 2)
            counter += 1
        if (i + 1, j + 2) in WALLS:
            estante_a_coordenadas[counter] = (i + 1, j + 2)
            counter += 1
        if (i, j + 3) in WALLS:
            estante_a_coordenadas[counter] = (i, j + 3)
            counter += 1
        if (i + 1, j + 3) in WALLS:
            estante_a_coordenadas[counter] = (i + 1, j + 3)
            counter += 1