import heapq
from Problem import Problem

#----------------------------CLASE A_star---------------------#
class A_star:
    def __init__(self, problem:Problem):
        self.problem    = problem
        self.settings()
    
    def settings(self):
        self.open_list  = [(0, self.problem.start)]
        self.parent_of  = {}
        self.g_score    = {(x, y): float('inf') for x in range(self.problem.enviroment.heigth) for y in range(self.problem.enviroment.width)}
        self.g_score[self.problem.start] = 0

    def re_init(self, problem:Problem):
        self.problem       = problem
        self.settings()

    def goal_test(self, current:tuple):
        return current == self.problem.goal
    
    def get_path(self):
        path    = []
        current = self.problem.goal
        while current in self.parent_of:
            path.insert(0, current)
            current = self.parent_of[current]
        return path
    
    def solve(self):
        while self.open_list:
            current = heapq.heappop(self.open_list)[1]

            if self.goal_test(current):
                path = self.get_path()
                if self.problem.goal_shelf is not None:
                    if self.problem.enviroment.is_vertix(self.problem.goal):
                        if self.problem.enviroment.is_neighbor(path[-2], self.problem.goal_shelf):
                            path.pop()
                        else:
                            path.append(self.problem.enviroment.neighbors(self.problem.goal_shelf).pop())
                        self.problem.goal = path[-1]
                return path
            self.expand(current)

    def expand(self, current:tuple):
        neighbors = self.problem.enviroment.neighbors(current)
        for neighbor in neighbors:
            tentative_g_score = self.g_score[current] + 1

            if tentative_g_score < self.g_score[neighbor]:
                self.parent_of[neighbor] = current
                self.g_score[neighbor]   = tentative_g_score
                f_score                  = tentative_g_score + self.problem.enviroment.manhattan(neighbor, self.problem.goal)
                heapq.heappush(self.open_list, (f_score, neighbor))