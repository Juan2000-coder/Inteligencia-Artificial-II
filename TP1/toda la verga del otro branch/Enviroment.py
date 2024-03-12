import numpy as np

class Enviroment:
    def __init__(self, shelves_rows:int, shelves_columns:int):
        # Ancho y altura dados en número de estantes
        self.number_of_shelves  = shelves_rows*shelves_columns
        self.shelves_rows       = shelves_rows
        self.shelves_columns    = shelves_columns
        self.width              = 3*(shelves_columns) + 1
        self.heigth             = 5*(shelves_rows)    + 1
        self.data               = self.get_enviroment()
        self.ocupied            = []
    
    def get_enviroment(self):
        shelf = np.arange(1, 9).reshape(4, 2)
        for j in range(self.shelves_columns):
            shift = shelf + self.shelves_rows*8*j

            for i in range(self.shelves_rows):
                block = shift + 8*i
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
    
    def neighbors(self, p:tuple):
        neighbors_list = []
        for step in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            pos = tuple(x + y for x, y in zip(p, step))
            if self.is_available(pos):
                neighbors_list.append(pos)
        return neighbors_list
    
    def is_in(self, p:tuple):
        return (0 <= p[0] < self.heigth) and (0 <= p[1] < self.width)

    def is_shelf(self, p:tuple):
        return self.data[p] != 0
    
    def is_available(self, p:tuple):
        return self.is_in(p) and not self.is_shelf(p) and p not in self.ocupied
    
    def get_goalcell(self, start:tuple, shelf_goal:int):
        coordinate       = np.where(self.data == shelf_goal)
        shelf_neighbors  = self.neighbors((coordinate[0][0], coordinate[1][0]))

        min = None
        for neighbor in shelf_neighbors:
            dist = self.manhattan(start, neighbor)
            if min is None or dist < min:
                min     = dist
                nearest = neighbor
        return nearest
    
    def get_goalcell2(self, start:tuple, coordinate:tuple):
        shelf_neighbors  = self.neighbors((coordinate[0], coordinate[1]))

        min = None
        for neighbor in shelf_neighbors:
            dist = self.manhattan(start, neighbor)
            if min is None or dist < min:
                min     = dist
                nearest = neighbor
        return nearest
    

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])