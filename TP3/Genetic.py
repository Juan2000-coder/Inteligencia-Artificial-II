import numpy as np
import pickle
import random


'''
Funcionamiento:
    - Se tiene una población con sus weights, biases y score.
    - Se selecciona al 10% mejor puntuado a partir de su score y se les llama élite.
    - Se agregan los individuos de la élite a la nueva población.
    - Se generan los individuos restantes a partir de cruces entre todos los individuos de la población anterior,
    pero ponderados según el score obtenido en la partida en que jugaron.
    - Se agregan los individuos restantes a la nueva población.

    - Por último, se reemplazan los valores de weights y biases de la población con los nuevos establecidos.
'''


def updateNetwork(population):
    # ============= ESTA FUNCIÓN RECIBE UNA POBLACIÓN A LA QUE SE DEBEN APLICAR MECANISMOS DE SELECCIÓN, ==============
    # =============== CRUCE Y MUTACIÓN. LA ACTUALIZACIÓN DE LA POBLACIÓN SE APLICA EN LA MISMA VARIABLE ===============
    # Ordenamos a la población en función de su score
    fittest = select_fittest(population)

    # Determinamos el número de individuos en la élite (10% de la población) y aseguramos que sea un número par
    elite_count = max(1, len(population) // 10)  # Al menos un individuo en la élite
    if elite_count % 2 != 0:
        elite_count += 1

    # Generamos la nueva población, incluyendo a los individuos de la élite
    elite = fittest[:elite_count]
    new_population_data = [(ind.weights, ind.biases) for ind in elite]


    # Se asigna probabilidad a cada individuo de la población en función de su score. La probabilidad de selección
    # de cada individuo es la representación proporcional de su puntaje respecto al puntaje total de la población.
    scores = np.array([ind.score for ind in population])
    probabilities = scores / scores.sum()


    # Generar hijos por cruces aleatorios entre todos los individuos
    while len(new_population_data) < len(population):

        parent1 = select_parent(population, probabilities)
        parent2 = select_parent(population, probabilities)
        
        # Asegurarse de que los padres no sean el mismo individuo
        while parent1 == parent2:
            parent2 = select_parent(population, probabilities)
        
        # Crear dos hijos
        child1_weights, child1_biases, child2_weights, child2_biases = evolve(parent1, parent2)
        new_population_data.append((child1_weights, child1_biases))
        if len(new_population_data) < len(population):
            new_population_data.append((child2_weights, child2_biases))

    # Reemplazar la población antigua con la nueva
    for i in range(len(population)):
        population[i].weights, population[i].biases = new_population_data[i]


    # Guardar el modelo de la red neuronal
    save_population_data(population, population[0].model_name)
    # =================================================================================================================


def select_parent(population, probabilities):
    # Función para seleccionar un individuo basado en la probabilidad
    probabilities /= probabilities.sum()  # Normalizar probabilidades para asegurar que sumen exactamente 1
    return np.random.choice(population, p=probabilities)


def select_fittest(population):
    # ===================== FUNCIÓN DE SELECCIÓN =====================
    # Ordenamos la población por puntaje de mayor a menor
    fittest = sorted(population, key=lambda x: x.score, reverse=True)
    
    return fittest
    # ================================================================

def evolve(parent1, parent2):
    # ======================= FUNCIÓN DE CRUCE =======================
    child1_weights = [np.copy(w) for w in parent1.weights]
    child1_biases = [np.copy(b) for b in parent1.biases]
    child2_weights = [np.copy(w) for w in parent2.weights]
    child2_biases = [np.copy(b) for b in parent2.biases]

    # Cruce
    for i in range(len(parent1.weights)):
        for j in range(len(parent1.weights[i][0])):
            if random.random() > 0.5:
                child1_weights[i][:, j] = parent1.weights[i][:, j]
                child1_biases[i][j] = parent1.biases[i][j]
                
                child2_weights[i][:, j] = parent2.weights[i][:, j]
                child2_biases[i][j] = parent2.biases[i][j]
            else:
                child1_weights[i][:, j] = parent2.weights[i][:, j]
                child1_biases[i][j] = parent2.biases[i][j]
                
                child2_weights[i][:, j] = parent1.weights[i][:, j]
                child2_biases[i][j] = parent1.biases[i][j]

    # Mutación
    mutate(child1_weights, child1_biases)
    mutate(child2_weights, child2_biases)
    
    return child1_weights, child1_biases, child2_weights, child2_biases
    # ================================================================


def mutate(weights, biases, mutation_rate=0.3):
    # ===================== FUNCIÓN DE MUTACIÓN ======================
    # Mutar pesos
    for layer_weights in weights:
        for neuron_weights in layer_weights:
            for i in range(len(neuron_weights)):
                if random.random() < mutation_rate:
                    neuron_weights[i] += np.random.randn() * mutation_rate
    
    # Mutar biases
    for neuron_bias in biases:
        for i in range(len(neuron_bias)):
            if random.random() < mutation_rate:
                neuron_bias[i] += np.random.randn() * mutation_rate

    # ================================================================





def save_population_data(population, file_path):
    population_data = {}

    for i, individual in enumerate(population):
        individual_data = {
            "weights": individual.weights,
            "biases": individual.biases
        }
        population_data[f"individual_{i}"] = individual_data

    with open(file_path, "wb") as file:
        pickle.dump(population_data, file)
