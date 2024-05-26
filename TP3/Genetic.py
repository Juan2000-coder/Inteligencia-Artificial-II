import numpy as np
import pickle
import random


'''
Actualemnte esto está funcionando de la siguiente manera:
    Se tiene una población con sus weights, biases y score.
    Se selecciona al 10% mejor puntuado a partir de su score y se les llama élite.
    Se agregan los individuos de la élite a la nueva población.
    Se generan hijos a partir de cruces entre los individuos de la élite (50% de la población restante).
    Se agregan los hijos de la elite a la nueva población.
    Se generan los hijos restantes a partir de cruces random en la población (elite + no elite).
    Se agregan los hijos restantes a la nueva población.

    Por último, se reemplazan los valores de weights y biases de la población con los encontrados para la nueva.

    
    De modo que si se tenía una población de 100 individuos:
        - 10 nuevos individuos serán los 10 mejores de la élite.
        - 45 nuevos individuos serán hijos de la élite con la elite.  (en realidad 46, se crean de a dos los hijos)
        - 45 nuevos individuos serán hijos de cruces random entre los individuos de la población. (44 en realidad)
'''


def updateNetwork(population):
    # ===================== ESTA FUNCIÓN RECIBE UNA POBLACIÓN A LA QUE SE DEBEN APLICAR MECANISMOS DE SELECCIÓN, =================
    # ===================== CRUCE Y MUTACIÓN. LA ACTUALIZACIÓN DE LA POBLACIÓN SE APLICA EN LA MISMA VARIABLE ====================
    # Ordenamos a la población en función de su score
    fittest = select_fittest(population)

    # Determinamos el número de individuos en la élite (10% de la población) y aseguramos que sea un número par
    elite_count = max(1, len(population) // 10)  # Al menos un individuo en la élite
    if elite_count % 2 != 0:
        elite_count -= 1  # Nos aseguramos de que sea par, por la forma en que se crean los hijos

    # Número de individuos no pertenecientes a la élite que necesitamos generar
    non_elite_count = len(population) - elite_count
    
    # Número de individuos generados por cruces de la élite con la elite (50% de non_elite_count)
    elite_cross_count = non_elite_count // 2

    # Generamos la nueva población, incluyendo a los individuos de la élite
    elite = fittest[:elite_count]
    new_population_data = [(ind.weights, ind.biases) for ind in elite]

    # Generar hijos a partir de padres: elite con elite
    while len(new_population_data) < elite_count + elite_cross_count:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)
        
        # Asegurarse de que los padres no sean el mismo individuo
        while parent1 == parent2:
            parent2 = random.choice(elite)
        
        # Crear dos hijos
        child1_weights, child1_biases, child2_weights, child2_biases = evolve(parent1, parent2)
        new_population_data.append((child1_weights, child1_biases))
        if len(new_population_data) < len(population):
            new_population_data.append((child2_weights, child2_biases))

    # Generar hijos por cruces aleatorios entre todos los individuos
    while len(new_population_data) < len(population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        
        # Asegurarse de que los padres no sean el mismo individuo
        while parent1 == parent2:
            parent2 = random.choice(population)
        
        # Crear dos hijos
        child1_weights, child1_biases, child2_weights, child2_biases = evolve(parent1, parent2)
        new_population_data.append((child1_weights, child1_biases))
        if len(new_population_data) < len(population):
            new_population_data.append((child2_weights, child2_biases))

    # Reemplazar la población antigua con la nueva
    for i in range(len(population)):
        population[i].weights, population[i].biases = new_population_data[i]


    # Guardar el modelo de la red neuronal
    save_population_data(population, population[0].nombre_modelo)

    # =============================================================================================================================

def select_fittest(population):
    # ===================== FUNCIÓN DE SELECCIÓN =====================
    # Ordenamos la población por puntaje de mayor a menor
    sorted_population = sorted(population, key=lambda x: x.score, reverse=True)
    
    # Seleccionamos los 50% más aptos
    fittest_count = len(sorted_population) // 2
    fittest = sorted_population[:fittest_count]
    
    return fittest
    # ================================================================

def evolve(parent1, parent2):
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


def mutate(weights, biases, mutation_rate=0.3):
    # ===================== FUNCIÓN DE MUTACIÓN =====================
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

    # ===============================================================







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