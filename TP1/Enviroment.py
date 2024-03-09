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
        shelf = np.arange(1, 9).reshape(4, 2)
        for j in range(self.shelves_width):
            shift = shelf + self.shelves_heigth*8*j

            for i in range(self.shelves_heigth):
                block = shift + 8*i
                block = np.hstack((np.zeros((4, 1)), block))
                block = np.vstack((np.zeros((1, 3)), block))

                if i == 0:
                    column = block
                else:
                    np.vstack((column, block))

            if j == 0:
                data = column
            else:
                np.hstack((data, column))

        return data
    
    def neighbors(self, p:tuple):
        neighbors_list = []
        for step in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            pos = p + step
            if self.is_in(pos):
                if not self.is_shelf(pos):
                    neighbors_list.append(pos)
        return neighbors_list
    
    def is_in(self, p:tuple):
        return (0 <= p[0] < self.heigth) and (0 <= p[1] < self.width)

    def is_shelf(self, p:tuple):
        return self.data[p] != 0
    
    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

#-------------------------COLORES--------------------------#
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
VIOLET = (255, 0, 200)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)