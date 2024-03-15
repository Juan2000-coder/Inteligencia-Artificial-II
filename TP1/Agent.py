from Astar import A_star
from Problem import Problem

class Agent:
    def __init__(self, problem:Problem):
        self.problem    = problem
        self.position   = self.problem.start
        self.a_star     = A_star(self.problem)
        self.path       = []

    def check_move(self, position):
        return not(position in self.problem.enviroment.ocupied)

    def move(self, new_position):
        indice = self.problem.enviroment.ocupied.index(self.position)
        self.problem.enviroment.ocupied.pop(indice)

        if self.check_move(new_position):
            self.position = new_position
        else:
            self.problem.start = self.position
            self.a_star.re_init(self.problem)
            self.path          = self.a_star.solve()
            self.position      = self.path.pop(0)

        self.problem.enviroment.ocupied.append(self.position)