from Enviroment import Enviroment

class Problem:
    def __init__(self, enviroment: Enviroment, start:tuple, goal_shelf:tuple):
        self.enviroment  = enviroment 
        self.goal_shelf  = goal_shelf
        self.first_start = start
        self.start       = start
        self.goal        = goal_shelf