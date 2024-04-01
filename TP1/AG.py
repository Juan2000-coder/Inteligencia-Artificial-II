from Recocido import Recocido as rc
from Ordenes import Orden
from Enviroment import Enviroment

import random


class Individuo:
    '''Clase que representa un individuo de la población.
    Cada individuo es una solución al problema que se desea resolver.'''
    def __init__(self, genes):
        self.genes = genes      # Genes que representan la solución
        self.fitness = 0        # Idoneidad de la solución
        self.costo = 0          # Costo de la solución

    def calcular_costo(self):
        '''Calcula el costo de la solución representada por el individuo.'''
        ordenes = [1,2,3,4,5]
        costo = 0
        for numero_orden in ordenes:
            # Creación de la instancia de la clase Orden
            orden = Orden(numero_orden, "ordenes2.txt")
            max_estante = max(orden.estantes)

            # Configuración del entorno de estanterías
            shelves_rows = 2
            shelves_columns = 2
            
            enviroment = Enviroment(shelves_rows, shelves_columns, self.genes)
            #enviroment.get_enviroment(self.genes)
            # Ejecución del algoritmo de recocido simulado
            #print_divider()
            #print_instruction("Ejecución del algoritmo de Recocido Simulado")
            recocido = rc(100, 1e-12, 8, enviroment)
            solucion_optima, camino_optimo = recocido.ejecutar_recocido(orden.estantes)    
            costo = costo + len(camino_optimo)
        
        
        self.costo = costo
      

class Poblacion:
    '''Clase que representa una población de individuos.
    Una población es un conjunto de soluciones al problema que se desea resolver.'''
    def __init__(self, tam_poblacion, genes, _prob_mutacion): 
        self.individuos = []
        for _ in range(tam_poblacion):
            lista_permutable = genes[:]                     # Copia de la lista de genes
            random.shuffle(lista_permutable)                # Mezcla aleatoria de los genes
            individuo = Individuo(lista_permutable)         # Creación de un nuevo individuo
            self.individuos.append(individuo)               # Agregar el individuo a la población
            self.prob_mutacion = _prob_mutacion             # Probabilidad de mutación
            self.probabilidades = []                        # Probabilidades de selección de los individuos
      

    def evaluar_poblacion(self):
        '''Evalúa la idoneidad de la poblacion de individuos.'''
        for individuo in self.individuos:
            individuo.calcular_costo()
        costo_max = max([i.costo for i in self.individuos])
        
        suma = 0
        
        for individuo in self.individuos:
            suma = suma + (costo_max-individuo.costo)
        
        for individuo in self.individuos:
            individuo.fitness = (costo_max-individuo.costo)/suma 
          
        self.probabilidades = [i.fitness for i in self.individuos]
        print("Probabilidades")
        print(self.probabilidades)
      

    def seleccionar_padres(self):
        '''Selecciona dos padres de la población actual,
        teniendo en cuenta la probabilidad de selección de cada individuo.'''
        ind = self.individuos
        prob = self.probabilidades
        
        padre1 = random.choices(ind, weights=prob, k=1)[0]
        ind.remove(padre1)
        prob.remove(padre1.fitness)
        padre2 = random.choices(ind, weights=prob, k=1)[0]
        
        return padre1, padre2

    def cruzar(self, _padre1,_padre2):
        '''Cruza dos individuos para producir dos descendientes.'''
        n = len(_padre1.genes)
        p1 = random.randint(0, n - 1)
        p2 = random.randint(0, n - 1)
        punto_inicio = min(p1, p2)
        punto_fin = max(p1, p2)
        # Seleccionar el segmento del padre1 para copiar directamente al descendiente1
        segmento1 = _padre1.genes[punto_inicio:punto_fin+1]
        # Seleccionar el segmento del padre2 para copiar directamente al descendiente2
        segmento2 = _padre2.genes[punto_inicio:punto_fin+1]
        #print(segmento1)
        #print(segmento2)
        #print(len(segmento1))
        #print(1+punto_fin - punto_inicio)
        descendiente1 = []
        descendiente2 = []
        

        for i in _padre2.genes:
            if i not in segmento1 :
                descendiente1.append(i)
        descendiente1[punto_inicio:punto_inicio] = segmento1

        for i in _padre1.genes:
            if i not in segmento2:
                descendiente2.append(i)
        descendiente2[punto_inicio:punto_inicio] = segmento2
        hijo1 = Individuo(descendiente1)
        hijo2 = Individuo(descendiente2)
        #print(descendiente1)
        #print(descendiente2)
        return hijo1, hijo2

    def mutar(self,_individuo):
        '''Muta un individuo, en fución de su probabilidad de mutación.'''
        if random.random() < self.prob_mutacion:
        # Seleccionar dos índices aleatorios para intercambiar
          indice1, indice2 = random.sample(range(len(_individuo.genes)), 2)

        # Intercambiar los valores en los índices seleccionados
        _individuo.genes[indice1], _individuo.genes[indice2] = _individuo.genes[indice2], _individuo.genes[indice1]

        return _individuo


    def evolucionar(self):
        '''Ejecuta una generación de una nueva población.'''
        nueva_generacion = []
        
        self.evaluar_poblacion()
        self.imprimir_poblacion()
        # Elitismo: mantenemos al mejor individuo de la generación anterior
        mejor_individuo = max(self.individuos, key=lambda x: x.fitness)
        #print(mejor_individuo.genes)
        nueva_generacion.append(mejor_individuo)

        while len(nueva_generacion) < (len(self.individuos) - 1):   # -1 porque el elitismo ya agrega un individuo a nueva_generacion
            padre1, padre2 = self.seleccionar_padres()
            hijo1, hijo2 = self.cruzar(padre1, padre2)
            
            _hijo1 = self.mutar(hijo1)
            _hijo2 = self.mutar(hijo2)
            
            
            #nueva_generacion.extend([hijo1, hijo2])
            nueva_generacion.append(_hijo1)
            nueva_generacion.append(_hijo2)
            
        self.individuos = nueva_generacion
    
    
    def imprimir_poblacion(self):
        '''Imprime la población actual.'''
        for i in self.individuos:
            print("Individuo", i.genes)
            print("Fitness", i.fitness)
        print("tamano", len(self.individuos))


