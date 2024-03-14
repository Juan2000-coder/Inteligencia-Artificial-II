import math
import random

# Función objetivo de ejemplo (puede ser cualquier función que desees optimizar)
def funcion_objetivo(x):
    return x**2

# Función de enfriamiento
def esquema_enfriamiento(temperatura, enfriamiento):
    return temperatura * enfriamiento

# Función para generar una solución vecina (perturbación)
def generar_vecino(solucion_actual, rango_perturbacion):
    return solucion_actual + random.uniform(-rango_perturbacion, rango_perturbacion)

# Algoritmo de recocido simulado
def recocido_simulado(funcion_objetivo, temperatura_inicial, enfriamiento, iteraciones, rango_perturbacion):
    solucion_actual = random.uniform(-10, 10)  # Solución inicial aleatoria
    mejor_solucion = solucion_actual
    temperatura = temperatura_inicial

    for i in range(iteraciones):
        vecino = generar_vecino(solucion_actual, rango_perturbacion)
        diferencia = funcion_objetivo(vecino) - funcion_objetivo(solucion_actual)

        # Si el vecino es mejor, aceptarlo siempre
        if diferencia < 0:
            solucion_actual = vecino
            if funcion_objetivo(vecino) < funcion_objetivo(mejor_solucion):
                mejor_solucion = vecino
        # Si el vecino es peor, aceptarlo con cierta probabilidad
        else:
            probabilidad_aceptacion = math.exp(-diferencia / temperatura)
            if random.random() < probabilidad_aceptacion:
                solucion_actual = vecino

        # Actualizar la temperatura
        temperatura = esquema_enfriamiento(temperatura, enfriamiento)

    return mejor_solucion, funcion_objetivo(mejor_solucion)

# Parámetros del algoritmo
temperatura_inicial = 100
enfriamiento = 0.95
iteraciones = 1000
rango_perturbacion = 0.1

# Ejecutar el algoritmo
mejor_solucion, valor_objetivo = recocido_simulado(funcion_objetivo, temperatura_inicial, enfriamiento, iteraciones, rango_perturbacion)

print("Mejor solución encontrada:", mejor_solucion)
print("Valor objetivo de la mejor solución:", valor_objetivo)
