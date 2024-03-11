from Astar import A_star
from Problem import Problem

class Agent:
    def __init__(self, initial:tuple, problem:Problem):
        self.position   = initial
        self.problem    = problem
        self.a_star     = A_star(self.problem)
        self.problem.enviroment.ocupied.append(initial)
        self.path       = None

    def check_move(self, position):
        return not(position in self.problem.enviroment.ocupied)

    def move(self, new_position):
        if self.check_move(new_position):
            self.position = new_position
        else:
            self.problem.start = self.position
            self.path          = self.a_star.solve()