from Enviroment import Space, Position

class Problem:
    def __init__(self, space:Space, start:Position, goal:Position):
        self.space = space
        self.start = start
        self.goal  = goal