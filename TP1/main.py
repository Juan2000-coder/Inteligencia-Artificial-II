from Problem import Problem
from Enviroment import Enviroment
from Astar import A_star, Agent
from Game import Game

#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    start_row1        = int(input("Ingrese la fila de partida: "))
    start_column1     = int(input("Ingrese la columna de partida: "))

    start_row2        = int(input("Ingrese la fila de partida: "))
    start_column2     = int(input("Ingrese la columna de partida: "))

    start1            = (start_row1, start_column1)
    start2            = (start_row2, start_column2)

    shelf_goal1       = int(input("Ingrese el número de estante que desea buscar: "))
    shelf_goal2       = int(input("Ingrese el número de estante que desea buscar: "))


    enviroment        = Enviroment(shelves_rows, shelves_columns)
    goal1             = enviroment.get_goalcell(start1, shelf_goal1)
    goal2             = enviroment.get_goalcell(start2, shelf_goal2)

    problem1          = Problem(enviroment, start1, goal1)
    problem2          = Problem(enviroment, start2, goal2)
    a_star1            = A_star(problem1)
    a_star2            = A_star(problem2)

    agent1             = Agent(start1)
    agent2             = Agent(start2)

    # Realizar búsqueda A*
    path1              = a_star1.solve()
    path2              = a_star2.solve()

    game              = Game(problem1, problem2)
    game.run(path1, path2, agent1, agent2)