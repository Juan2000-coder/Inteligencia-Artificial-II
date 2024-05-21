from NeuralNetwork import NeuralNetwork
from Dinosaur import Dinosaur
import numpy as np
import random

def updateNetwork(population):
    # ===================== ESTA FUNCIÓN RECIBE UNA POBLACIÓN A LA QUE SE DEBEN APLICAR MECANISMOS DE SELECCIÓN, =================
    # ===================== CRUCE Y MUTACIÓN. LA ACTUALIZACIÓN DE LA POBLACIÓN SE APLICA EN LA MISMA VARIABLE ====================
    # Seleccionamos los dinosaurios más aptos
    fittest = select_fittest(population)
    
    # Generamos la nueva población mediante cruce y mutación
    # Incluimos a los dos mejores de la elite
    new_population = [fittest[0], fittest[1]]

    id = list(range(39))
    id.remove(fittest[0].id)
    id.remove(fittest[1].id) 


    for i in range((len(population) // 2) - 1):
        parent1 = random.choice(fittest)
        parent2 = random.choice(fittest)
        child1, child2 = evolve(parent1, parent2, id[i])
        new_population.append(child1)
        new_population.append(child2)

    # Reemplazamos la población antigua con la nueva
    for i in range(len(population) - 1):
        population[i] = new_population[i]



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

def evolve(parent1, parent2, i):
    # ================= FUNCIÓN DE CRUCE Y MUTACIÓN ==================
    # Le damos a los hijos la estructura de la red neuronal. A pesar de que tengan valores random, luego los cambiamos
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    if (R < 20 and G < 20):
        B = 255
    else:
        B = random.randint(0, 255)
    color = (R, G, B)

    child1 = Dinosaur(i, color, True)
    child2 = Dinosaur(i+1, color, True)
    
    # Realizamos el cruce y la mutación
    for i in range(len(parent1.weights_input_hidden)):
        if random.random() > 0.5:
            child1.weights_input_hidden[i] = parent1.weights_input_hidden[i]
            child2.weights_input_hidden[i] = parent2.weights_input_hidden[i]
        else:
            child1.weights_input_hidden[i] = parent2.weights_input_hidden[i]
            child2.weights_input_hidden[i] = parent1.weights_input_hidden[i]
    
    for i in range(len(parent1.weights_hidden_output)):
        if random.random() > 0.5:
            child1.weights_hidden_output[i] = parent1.weights_hidden_output[i]
            child2.weights_hidden_output[i] = parent2.weights_hidden_output[i]
        else:
            child1.weights_hidden_output[i] = parent2.weights_hidden_output[i]
            child2.weights_hidden_output[i] = parent1.weights_hidden_output[i]
    
    for i in range(len(parent1.bias_hidden)):
        if random.random() > 0.5:
            child1.bias_hidden[i] = parent1.bias_hidden[i]
            child2.bias_hidden[i] = parent2.bias_hidden[i]
        else:
            child1.bias_hidden[i] = parent2.bias_hidden[i]
            child2.bias_hidden[i] = parent1.bias_hidden[i]
    
    for i in range(len(parent1.bias_output)):
        if random.random() > 0.5:
            child1.bias_output[i] = parent1.bias_output[i]
            child2.bias_output[i] = parent2.bias_output[i]
        else:
            child1.bias_output[i] = parent2.bias_output[i]
            child2.bias_output[i] = parent1.bias_output[i]
    
    # Mutación
    mutate(child1)
    mutate(child2)
    
    return child1, child2

def mutate(child, mutation_rate=0.1):
    for i in range(len(child.weights_input_hidden)):
        if random.random() < mutation_rate:
            child.weights_input_hidden[i] += np.random.randn() * mutation_rate
    
    for i in range(len(child.weights_hidden_output)):
        if random.random() < mutation_rate:
            child.weights_hidden_output[i] += np.random.randn() * mutation_rate
    
    for i in range(len(child.bias_hidden)):
        if random.random() < mutation_rate:
            child.bias_hidden[i] += np.random.randn() * mutation_rate
    
    for i in range(len(child.bias_output)):
        if random.random() < mutation_rate:
            child.bias_output[i] += np.random.randn() * mutation_rate

    # ===============================================================