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

    game                = Game(enviroment)
    start_pos, goals_pos = game.get_checkpoints_list()


    """
    start = start_pos.pop()

    recocido = rc(enviroment)
    mejor_solucion = recocido.ejecutar_recocido()
    print(mejor_solucion)
    """
    for i, goal in enumerate(goals_pos):
        if i == 0:
            problem = Problem(enviroment, start_pos[0], goal)
            agent   = Agent(problem)
        else: 
            agent.problem.start = agent.path[-1]
            agent.problem.goal  = goal
            agent.a_star.re_init(agent.problem)
        agent.path       += agent.a_star.solve()
        #enviroment.ocupied.append(agent.position)
        '''print("start_pos: ", start_pos)
        print("goal_pos: " , goals_pos)
        print(f"Trayecto {i+1}: ", agent.path)'''
        
        costo_trayecto = len(agent.path)
        print(f"Costo actual: ", costo_trayecto)
        #start_pos[0] = goals_pos[i]

    enviroment.ocupied.append(agent.position)
    # Chequear para que funque bien
    game.run_ej3(agent)