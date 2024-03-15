from Problem import Problem
from Enviroment import Enviroment
from Agent import Agent
from Game import Game


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment        = Enviroment(shelves_rows, shelves_columns)

    game1               = Game(enviroment)
    start_pos, goal_pos = game1.get_checkpoints()

    problem1          = Problem(enviroment, start_pos[0], goal_pos[0])
    problem2          = Problem(enviroment, start_pos[1], goal_pos[1])

    agent1            = Agent(problem1)
    agent2            = Agent(problem2)

    # Realizar búsqueda A*
    agent1.path       = agent1.a_star.solve()
    agent2.path       = agent2.a_star.solve()

    enviroment.ocupied.append(agent1.position)
    enviroment.ocupied.append(agent2.position)
    game1.run(agent1, agent2)