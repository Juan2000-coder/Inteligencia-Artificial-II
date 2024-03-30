#Debajo de esto empieza la magia
import random
from Recocido import Recocido as rc
from Ordenes import Orden
from Enviroment import Enviroment

class Individuo:
  def __init__(self, genes):
    self.genes = genes
    self.fitness = 0
    self.costo = 0

  def calcular_costo(self):
    #Ejecutar recocido simulado
    ordenes = [1,2,3,4,5]
    for numero_orden in ordenes:
      # Creación de la instancia de la clase Orden
      orden = Orden(numero_orden, "ordenes2.txt")
      max_estante = max(orden.estantes)

      # Configuración del entorno de estanterías
      shelves_rows = 2
      shelves_columns = 2
      
      enviroment = Enviroment(shelves_rows, shelves_columns, self.genes)
     # enviroment.get_enviroment(self.genes)
      # Ejecución del algoritmo de recocido simulado
 #     print_divider()
 #     print_instruction("Ejecución del algoritmo de Recocido Simulado")
      recocido = rc(100, 1e-12, 8, enviroment)
      solucion_optima, camino_optimo = recocido.ejecutar_recocido(orden.estantes)    
      self.costo =+ len(camino_optimo)
      print(self.costo)

class Poblacion:
  def __init__(self, tamano_poblacion, genes, _probabilidad_de_mutacion):#Inicializa la poblacion 
    self.individuos = []
    for _ in range(tamano_poblacion):
      genes_random = random.shuffle(genes)
      individuo = Individuo(genes_random)
      self.individuos.append(individuo)
      self.probabilidad_de_mutacion = _probabilidad_de_mutacion
      self.probabilidades = []

  def evaluar_poblacion(self):#Evalua la idoneidad de cada individuo
      for individuo in self.individuos:
        individuo.calcular_costo()
      costo_max = max([i.costo for i in self.individuos])
      sum = 0
      for individuo in self.individuos:
        print(sum)
        sum = sum + (costo_max-individuo.costo)
      for individuo in self.individuos:
        individuo.fitness = (costo_max-individuo.costo)/sum 
        
      self.probabilidades = [i.fitness for i in self.individuos]
    
  def seleccionar_padres(self):#Seleciona 2 padres para cruzar
    
    ind = self.individuos
    prob = self.probabilidades
    padre1 = random.choices(ind, weights=prob, k=1)[0]
    ind.remove(padre1)
    prob.remove(padre1.fitness)
    padre2 = random.choices(ind, weights=prob, k=1)[0]
#    print(padre1.genes)
    return padre1, padre2

  def cruzar(self, _padre1,_padre2):
#    print(_padre1)
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
    print(segmento1)
    print(segmento2)

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
    if random.random() < self.probabilidad_de_mutacion:
     # Seleccionar dos índices aleatorios para intercambiar
      indice1, indice2 = random.sample(range(len(_individuo.genes)), 2)

      # Intercambiar los valores en los índices seleccionados
      _individuo.genes[indice1], _individuo.genes[indice2] = _individuo.genes[indice2], _individuo.genes[indice1]

  def evolucionar(self):
      nueva_generacion = []

      self.evaluar_poblacion()

      # Elitismo: mantenemos al mejor individuo de la generación anterior
      mejor_individuo = max(self.individuos, key=lambda x: x.fitness)
  #    print(mejor_individuo.genes)
      nueva_generacion.append(mejor_individuo)

      while len(nueva_generacion) < len(self.individuos):
          padre1, padre2 = self.seleccionar_padres()
          hijo1, hijo2 = self.cruzar(padre1, padre2)

          hijo1 = self.mutar(hijo1)
          hijo2 = self.mutar(hijo2)

          nueva_generacion.extend([hijo1, hijo2])

      self.individuos = nueva_generacion


