from Enviroment import Almacen
from Agent import Agent12
from Astar import A_star
from Game import Game


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment        = Almacen(shelves_rows, shelves_columns)

    game              = Game(enviroment)
    start_pos, goal_pos = game.get_checkpoints(1)
    a_star              = A_star(enviroment, start_pos.pop(0), goal_pos.pop(0))

    agent            = Agent12(a_star.start, a_star.enviroment, a_star)

    # Realizar búsqueda A*
    agent.path       = agent.a_star.solve()

    enviroment.ocupied.append(agent.position)
    game.run_ej1(agent)