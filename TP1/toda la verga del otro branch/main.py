from Problem import Problem
from Enviroment import Enviroment
from Agent import Agent
from Game import Game


#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    shelves_rows      = int(input("Indique la cantidad de filas de estanterías: "))
    shelves_columns   = int(input("Indique la cantidad de columnas de estanterías: "))

    enviroment        = Enviroment(shelves_rows, shelves_columns)

    game1             = Game(enviroment)
    start_pos, goal_pos = game1.run2()
    start1 = (start_pos[0][1], start_pos[0][0])
    start2 = (start_pos[1][1], start_pos[1][0])

    goal1 = (goal_pos[0][1], goal_pos[0][0])
    goal2 = (goal_pos[1][1], goal_pos[1][0])

    #print(start1, goal1, start2, goal2)

    #start_row1        = int(input("Ingrese la fila de partida: "))
    #start_column1     = int(input("Ingrese la columna de partida: "))

    #start_row2        = int(input("Ingrese la fila de partida: "))
    #start_column2     = int(input("Ingrese la columna de partida: "))

    #start1            = (start_row1, start_column1)
    #start2            = (start_row2, start_column2)

    #print(start1, start2)

    #shelf_goal1       = int(input("Ingrese el número de estante que desea buscar: "))
    #shelf_goal2       = int(input("Ingrese el número de estante que desea buscar: "))


    #enviroment        = Enviroment(shelves_rows, shelves_columns)
    #goal1             = enviroment.get_goalcell(start1, shelf_goal1)
    #goal2             = enviroment.get_goalcell(start2, shelf_goal2)

    goal1             = enviroment.get_goalcell2(start1, goal1)
    goal2             = enviroment.get_goalcell2(start2, goal2)

    #print(goal1, goal2)

    problem1          = Problem(enviroment, start1, goal1)
    problem2          = Problem(enviroment, start2, goal2)

    agent1            = Agent(start1, problem1)
    agent2            = Agent(start2, problem2)

    # Realizar búsqueda A*
    agent1.path       = agent1.a_star.solve()
    agent2.path       = agent2.a_star.solve()

    enviroment.ocupied.append(agent1.position)
    enviroment.ocupied.append(agent2.position)
    
    game              = Game(enviroment)
    game.run(agent1, agent2)