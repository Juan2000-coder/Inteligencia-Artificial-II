from Problem import Problem
from Enviroment import Enviroment
from Agent import Agent
from Game import Game
from Recocido import Recocido as rc
from Astar import A_star


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment        = Enviroment(shelves_rows, shelves_columns)

    game1               = Game(enviroment)
    start_pos, _        = game1.get_checkpoints(True)

    start = start_pos.pop()


    #print(start1, goal1, start2, goal2)

    #print(goal1, goal2)
 
    recocido = rc(enviroment)
    mejor_solucion = recocido.ejecuctar_recocido()
    print(mejor_solucion)
    

