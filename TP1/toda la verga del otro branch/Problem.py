from Enviroment import Enviroment

class Problem:
    def __init__(self, enviroment: Enviroment, start:tuple, goal:tuple):
        self.start      = start
        self.goal       = goal
        self.enviroment = enviroment 