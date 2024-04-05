from AG import Poblacion
from Game import Game
from Agent import Agent34

def print_divider():
    print("=" * 100)

# Función para imprimir una instrucción con formato
def print_instruction(instruction):
    print(f"ℹ️ {instruction}")

# Función para imprimir un mensaje de éxito
def print_success(message):
    print(f"✅ {message}")

# Función para imprimir un mensaje de error
def print_error(message):
    print(f"❌ Error: {message}")

#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    print_divider()
    print("BIENVENIDO AL PROGRAMA DE GESTIÓN DEL DEPOSITO")
    print("Optimizacion con algoritmo genetico")
    print_divider()

# Ejemplo de uso
    tam_poblacion = 10
    prob_mutacion = 0.01
    num_generaciones = 10
    genes = [i+1 for i in range(32)]
    estanterias = [2, 2]
    par_recocido = [1e-11, 1e-12, 3, 0.6, 0.6, 0.8]
    poblacion = Poblacion(tam_poblacion, genes, prob_mutacion, *estanterias, *par_recocido)
  
    generacion = 1
    flag = True
    while flag:
        print(f"Generación {generacion}:")
        
        print("-" * 100)
        if generacion >= num_generaciones:
            flag = False
        poblacion.evolucionar()
        
        generacion += 1
    mejor_individuo = max(poblacion.individuos, key=lambda x: x.fitness)
    poblacion.enviroment.data = poblacion.enviroment.get_enviroment(mejor_individuo.genes)
    
    print("¡Objetivo alcanzado!")
    juego = Game(poblacion.enviroment)
    agent = Agent34((0,0), poblacion.enviroment)
    poblacion.enviroment.ocupied.append(agent.position)
    juego.run_ej4(agent, mejor_individuo)

