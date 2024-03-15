from Problem import Problem
from Enviroment import Enviroment
from Agent import Agent
from Game import Game
from Recocido import Recocido as rc
from Astar import A_star


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows         = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns      = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment           = Enviroment(shelves_rows, shelves_columns)

    game1                = Game(enviroment)
    start_pos, goals_pos = game1.get_checkpoints_list()


    """
    start = start_pos.pop()

    recocido = rc(enviroment)
    mejor_solucion = recocido.ejecutar_recocido()
    print(mejor_solucion)
    """

    for i in range(len(goals_pos)):
        problem1          = Problem(enviroment, start_pos[0], goals_pos[i])
        agent1            = Agent(problem1)
        agent1.path       = agent1.a_star.solve()
        enviroment.ocupied.append(agent1.position)
        print("start_pos: ", start_pos)
        print("goal_pos: ", goals_pos)
        print(f"Trayecto {i+1}: ", agent1.path)
        start_pos[0] = goals_pos[i]
        
        #game1.run_ej3(agent1)