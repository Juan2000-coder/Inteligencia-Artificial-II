from Enviroment import Almacen
from Agent import Agent12
from Game import Game
from Astar import A_star


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment        = Almacen(shelves_rows, shelves_columns)

    game                = Game(enviroment)
    start_pos, goal_pos = game.get_checkpoints(2)

    a_star1           = A_star(enviroment, start_pos[0], goal_pos[0])
    a_star2           = A_star(enviroment, start_pos[1], goal_pos[1])

    agent1            = Agent12(a_star1.start, enviroment, a_star1)
    agent2            = Agent12(a_star2.start, enviroment, a_star2)

    # Realizar búsqueda A*
    agent1.path       = agent1.a_star.solve()
    agent2.path       = agent2.a_star.solve()

    enviroment.ocupied.append(agent1.position)
    enviroment.ocupied.append(agent2.position)
    game.run_ej2(agent1, agent2)