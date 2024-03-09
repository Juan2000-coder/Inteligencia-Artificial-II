import pygame
import heapq
import time

# Tamaño del tablero
# Se define el tamaño del tablero. En este caso de 17x16
WIDTH = 17
HEIGHT = 16

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VIOLET = (255, 0, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Definir las celdas de la pared
WALLS = {(11, 3), (10, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
         (9, 11), (9, 12), (9, 13), (9, 14), (10, 14), (11, 14), (12, 14)}
    
# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH * 40, HEIGHT * 40)) # Crea la ventana con el tamaño adecuado.
pygame.display.set_caption("Búsqueda A* para ir de la casilla I a la F.") # Genera titulo de la ventana

#Se crea un objeto Agent al principio y luego se llama al método move para actualizar la posición del 
# agente a medida que avanza a lo largo del camino encontrado por el algoritmo de búsqueda A*.

# Clase para representar al agente inicialmente en I (4,4)
class Agent:
    # Define el constructor de la clase Agent. 
    # El constructor es un método especial que se llama automáticamente cuando se crea un objeto de esta clase. 
    # El parámetro self hace referencia al propio objeto. 
    def __init__(self):
        self.position = (4,4) #El agente tendra su posicion inicial en I (4,4)
        
    def move(self, new_position):    # Actualiza el atributo position del agente con la nueva posición especificada. 
        self.position = new_position

# La distancia de Manhattan se utiliza como función heurística h(n) en el algoritmo A* para problemas de búsqueda en cuadrículas, 
# como el tablero que tenemos en este ejemplo. Es una heurística admisible y consistente para problemas en cuadrículas. 
# Otro ejemplo de Heuristica Euclidiana: es la distancia en línea recta entre dos puntos.

# Función para calcular la distancia de Manhattan
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Un algoritmo de búsqueda A* "A estrella" es un algoritmo de búsqueda heurística utilizado para 
# encontrar el camino más corto desde un nodo inicial hasta un nodo objetivo en un grafo ponderado. 
# Combina la búsqueda por amplitud (o por profundidad) con una función heurística 
# que guía la búsqueda hacia el objetivo de manera eficiente. 

# Algoritmo de búsqueda A*
def a_star(start, goal):        #Se define la función a_star que toma dos argumentos: start (la posición inicial) y goal (la posición objetivo).
    open_list = [(0, start)]    #Se crea una lista abierta (open_list) que se utilizará para almacenar los nodos que se deben explorar.
    came_from = {}              #Se crea un diccionario came_from que se utilizará para almacenar los nodos que se visitan durante la ejecución del algoritmo A*.
    #g_score se utilizará para almacenar las puntuaciones g (costos reales) de cada celda en el tablero.
    g_score = {(x, y): float('inf') for x in range(WIDTH) for y in range(HEIGHT)}
    # Representan las coordenadas de las celdas en el tablero, y los valores son inicializados con el valor de costo infinito (float('inf')). 
    # Esto prepara el diccionario g_score para almacenar los costos reales de las celdas a medida que se exploran durante la ejecución del algoritmo A*.
    g_score[start] = 0

    # Bucle principal: explorar nodos mientras hay elementos en la open_list
    while open_list:
        # Extraer el nodo con la puntuación más baja de open_list y obtener su posición
        current = heapq.heappop(open_list)[1]  # Extraemos la posición (coordenadas) del nodo actual
        
        #heapq: Este es un módulo de la biblioteca estándar de Python que proporciona funciones para trabajar con estructuras de datos de colas de prioridad 
        # (heap queues).Se utiliza heapq para manejar la open_list como una cola de prioridad.

        # Verificar si se ha llegado al objetivo
        if current == goal:
            path = []
            # Reconstruir el camino desde el objetivo hasta el inicio
            while current in came_from:
                path.insert(0, current)         # Agregar la posición actual al inicio de la lista de camino
                current = came_from[current]    # Cambiar a la posición anterior en el camino
            return path  # Devolver el camino óptimo encontrado

        # Explorar los vecinos de la celda actual en las direcciones arriba, abajo, izquierda y derecha
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            # Calcular la posición del vecino
            neighbor = (current[0] + dx, current[1] + dy)

            # Verificar si el vecino está dentro de los límites del tablero y no es una celda de pared
            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and neighbor not in WALLS:
                # Calcular la puntuación tentativa g_score para el vecino
                tentative_g_score = g_score[current] + 1

                # Si la puntuación tentativa es menor que la puntuación actual g_score del vecino
                if tentative_g_score < g_score[neighbor]:
                    # Actualizar came_from con el nodo actual como padre del vecino
                    came_from[neighbor] = current

                    # Actualizar g_score con la puntuación tentativa
                    g_score[neighbor] = tentative_g_score

                    # Calcular la puntuación f(n) y agregar el vecino a open_list
                    f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor)) #Se agrega n nuevo elemento a la cola de prioridad open_list. 



# Inicialización del agente
agent = Agent()

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Dibujar celdas negras
    for wall in WALLS:
        pygame.draw.rect(screen, BLACK, (wall[0] * 40, wall[1] * 40, 40, 40))

    # Dibujar celda inicial y final
    pygame.draw.rect(screen, BLUE, (agent.position[0] * 40, agent.position[1] * 40, 40, 40))
    pygame.draw.rect(screen, BLUE, (4 * 40, 4 * 40, 40, 40))
    pygame.draw.rect(screen, RED, (11 * 40, 12 * 40, 40, 40))

    # Realizar búsqueda A*
    path = a_star(agent.position, (11, 12))

    # Dibujar camino
    if path:
        for position in path:
            pygame.draw.rect(screen, VIOLET, (position[0] * 40, position[1] * 40, 40, 40))

        # Actualizar posición del agente
        agent.move(path[0])

    pygame.display.flip()
    # Se limitan los cuadros por segundo para evitar el crasheo.
    clock.tick(15)  # Limitar a 15 cuadros por segundo

pygame.quit()
