from Recocido import Recocido as rc
import random


class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def calcular_fitness(self):
        #Ejecutar recocido simulado
        solucion_optima, camino_optimo = recocido.ejecutar_recocido(#estantes)     
        self.fitness = len(camino_optimo)


class Poblacion:
    def __init__(self, tamano_poblacion, genes, objetivo):#Inicializa la poblacion 
        self.individuos = []
        for _ in range(tamano_poblacion):
            genes_random = ''.join(random.choice(genes) for _ in range(len(objetivo)))
            individuo = Individuo(genes_random)
            self.individuos.append(individuo)
        self.objetivo = objetivo

    def evaluar_poblacion(self):#Evalua la idoneidad de cada individuo
        for individuo in self.individuos:
            individuo.calcular_fitness()

    def seleccionar_padres(self):#Seleciona 2 padres para cruzar
        padres_seleccionados = []
        total_fitness = sum(individuo.fitness for individuo in self.individuos)
        for i in range(2):  # Seleccionamos 2 padres
            r = random.uniform(0, total_fitness)
            suma = 0
            for individuo in self.individuos:
                suma += individuo.fitness
                if suma > r:
                    padres_seleccionados.append(individuo)
                    break
        return padres_seleccionados

    def cruzar(self, _padre1,_padre2):
      n = len(_padre1)
      p1 = random.randint(0, n - 1)
      p2 = random.randint(0, n - 1)
      punto_inicio = min(p1, p2)
      punto_fin = max(p1, p2)
      # Seleccionar el segmento del padre1 para copiar directamente al descendiente1
      segmento1 = _padre1[punto_inicio:punto_fin+1]
      # Seleccionar el segmento del padre2 para copiar directamente al descendiente2
      segmento2 = _padre2[punto_inicio:punto_fin+1]
      #print(segmento1)
      #print(segmento2)
      #print(len(segmento1))
      #print(1+punto_fin - punto_inicio)
      descendiente1 = []
      descendiente2 = []
      print(segmento1)
      print(segmento2)

      for i in _padre2:
        if i not in segmento1 :
          descendiente1.append(i)
      descendiente1[punto_inicio:punto_inicio] = segmento1

      for i in _padre1:
        if i not in segmento2:
          descendiente2.append(i)
      descendiente2[punto_inicio:punto_inicio] = segmento2


      #print(descendiente1)
      #print(descendiente2)
      return descendiente1, descendiente2

    def mutar(self,_individuo,_probabilidad_mutacion):
      if random.random() < _probabilidad_mutacion:
       # Seleccionar dos índices aleatorios para intercambiar
        indice1, indice2 = random.sample(range(len(_individuo)), 2)
    
        # Intercambiar los valores en los índices seleccionados
        _individuo[indice1], _individuo[indice2] = _individuo[indice2], _individuo[indice1]
    
      return _individuo
  
    def evolucionar(self, probabilidad_mutacion, genes):
        nueva_generacion = []

        self.evaluar_poblacion()

        # Elitismo: mantenemos al mejor individuo de la generación anterior
        mejor_individuo = max(self.individuos, key=lambda x: x.fitness)
        nueva_generacion.append(mejor_individuo)

        while len(nueva_generacion) < len(self.individuos):
            padre1, padre2 = self.seleccionar_padres()
            hijo1, hijo2 = self.cruzar(padre1, padre2)

            self.mutar(hijo1, probabilidad_mutacion)
            self.mutar(hijo2, probabilidad_mutacion)

            nueva_generacion.extend([hijo1, hijo2])

        self.individuos = nueva_generacion


# Ejemplo de uso
objetivo = "Hello, World!"
tamano_poblacion = 100
probabilidad_mutacion = 0.01
genes = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,!¡"

poblacion = Poblacion(tamano_poblacion, genes, objetivo)

generacion = 1
while True:
    print(f"Generación {generacion}: {poblacion.individuos[0]} (Fitness: {poblacion.individuos[0].fitness})")
    if poblacion.individuos[0].fitness == len(objetivo):
        break
    poblacion.evolucionar(probabilidad_mutacion, genes)
    generacion += 1

print("¡Objetivo alcanzado!")
