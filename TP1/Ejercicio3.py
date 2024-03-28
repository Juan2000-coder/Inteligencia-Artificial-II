from Problem import Problem
from Enviroment import Enviroment
from Agent import Agent
from Game import Game
from Recocido import Recocido as rc
from Ordenes import Orden


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    orden                = Orden()
    max_estante          = max(orden.estantes)

    shelves_rows         = int(input("Indique la cantidad de filas de estanterías: "))
    min_col = max_estante//8//shelves_rows + 1
    shelves_columns = 0
    while shelves_columns < min_col:
        print(f"Debe ser un minimo de {min_col} columnas")
        shelves_columns      = int(input("Indique la cantidad de columnas de estanterías: "))
    enviroment           = Enviroment(shelves_rows, shelves_columns)

    game                 = Game(enviroment)
    game.paint_goals(orden.estantes)

    recocido = rc(1000, 0.5, 1, enviroment)
    solucion_optima, camino_optimo = recocido.ejecutar_recocido(orden.estantes)

    problema = Problem(enviroment, (0, 0), orden.estantes[-1])
    agent = Agent(problema)
    agent.path = camino_optimo

    enviroment.ocupied.append(agent.position)
    game.run_ej3(agent, solucion_optima)