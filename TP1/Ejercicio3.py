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

    game                 = Game(enviroment)
    start_pos, goals_pos = game.get_checkpoints_list() 

    recocido = rc(200, 0.5, 50, enviroment)
    solucion_optima, camino_optimo = recocido.ejecutar_recocido(goals_pos)

    problema = Problem(enviroment, (0, 0), goals_pos[-1])
    agent = Agent(problema)
    agent.path = camino_optimo

    enviroment.ocupied.append(agent.position)
    game.run_ej3(agent, solucion_optima)