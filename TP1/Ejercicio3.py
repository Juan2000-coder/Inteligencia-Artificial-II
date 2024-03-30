from Recocido import Recocido as rc
from Enviroment import Enviroment
from Problem import Problem
from Ordenes import Orden
from Agent import Agent
from Game import Game

import pandas as pd
import matplotlib.pyplot as plt


# Función para imprimir una línea divisoria
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
    print_divider()

    # Modo de ejecución: Estadístico o Juego
    flag_mode = input("¿Desea ingresar en el modo Estadístico (E) o en el modo de Juego (J)? (E/J): ")
    while flag_mode != "E" and flag_mode != "J":
        flag_mode = input("Por favor, ingrese una opción válida (E/J): ")

    # Número de orden
    numero_orden = int(input("Introduzca el número de la orden [1-100]: "))
    while numero_orden < 1 or numero_orden > 100:
        numero_orden = int(input("Por favor, ingrese un número de orden válido: "))

    # Creación de la instancia de la clase Orden
    orden = Orden(numero_orden)
    max_estante = max(orden.estantes)

    # Configuración del entorno de estanterías
    print_divider()
    print_instruction("CONFIGURACIÓN DEL ENTORNO DE ESTANTERÍAS")
    shelves_rows = int(input("Indique la cantidad de filas de estanterías: "))
    min_col = max_estante // 8 // shelves_rows + 1
    shelves_columns = 0
    while shelves_columns < min_col:
        print_instruction(f"Debe haber como mínimo {min_col} columnas.")
        shelves_columns = int(input("Indique la cantidad de columnas de estanterías: "))
    enviroment = Enviroment(shelves_rows, shelves_columns)

    # Ejecución del algoritmo de recocido simulado
    print_divider()
    print_instruction("Ejecución del algoritmo de Recocido Simulado")
    recocido = rc(100, 1e-12, 8, enviroment)
    solucion_optima, camino_optimo = recocido.ejecutar_recocido(orden.estantes)

    # Configuración del problema y el agente
    problema = Problem(enviroment, (0, 0), orden.estantes[-1])
    agent = Agent(problema)
    agent.path = camino_optimo
    enviroment.ocupied.append(agent.position)

    # Ejecución del juego o visualización de estadísticas
    print_divider()
    if flag_mode == "J":
        print_instruction("Inicio del juego...")
        game = Game(enviroment)
        game.paint_goals(orden.estantes)
        game.run_ej3(agent, solucion_optima)
    elif flag_mode == "E":
        print_instruction("Visualización de estadísticas...")
        # Lee el archivo CSV
        df = pd.read_csv('ejecucion_recocido.csv')
        plt.scatter(df['it'], df['e'])
        plt.grid(True)
        plt.xlabel('Iteración')
        plt.ylabel('Valor de Energía')
        plt.title('Gráfico de dispersión de la energía contra las iteraciones')
        plt.show()

    print_success("Programa finalizado. ¡Hasta luego!")
