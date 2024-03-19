import math
import random
from Problem import Problem
from Astar import A_star
from Enviroment import Enviroment
import copy

class Recocido:
	def __init__(self, T, T_min, L, enviroment:Enviroment):
		self.T = T
		self.T_min = T_min
		self.L = L     #math.factorial(len(self.estado_inicial)) // 2
		self.enviroment = enviroment

    # Funcion variación de la temperatura
	def esquema_enfriamiento(self, temperatura):
		return temperatura * 0.2
	
    # Función para generar una solución vecina (perturbación)
	def generar_vecino(self, solucion_actual):
		vecino = copy.deepcopy(solucion_actual)
		random.shuffle(vecino)
		return vecino
	
	def energia(self, estado):
		path:list = []
		start_pos = (0, 0)
		# Calculo del camino completo de ida
		for i, goal in enumerate(estado):
				if i == 0:
					# Problema inicial desde la posición de inicio al primer objetivo
						#problem  = Problem(self.enviroment, start_pos, self.enviroment.shelf2coor(goal))
						problem  = Problem(self.enviroment, start_pos, goal)
						a_star   = A_star(problem)
				else:
					# Redefine el problema por cada objetivo
						a_star.problem.start = path[-1]
						#a_star.problem.goal  = self.enviroment.shelf2coor(goal)
						a_star.problem.goal  = goal
						a_star.re_init(a_star.problem)
				# Actualiza el camino
				path       += a_star.solve()
		
		#-------APPENDEA EL CAMINO DE VUELTA-----------#
		a_star.problem.start = path[-1]
		a_star.problem.goal  = start_pos
		a_star.re_init(a_star.problem)
		path       	+= a_star.solve()
		#----------------------------------------------#
		return len(path), path
	
    # Algoritmo de recocido simulado
	def ejecutar_recocido(self, solucion_inicial: list):
		solucion_actual = solucion_inicial
		temperatura = self.T
		energia_actual, camino_actual = self.energia(solucion_actual)

		while temperatura > self.T_min:
			for i in range(self.L):
				vecino = self.generar_vecino(solucion_actual)
				energia_vecino, camino_vecino = self.energia(vecino)
				d_E = energia_actual - energia_vecino
				
				if d_E > 0:
					solucion_actual = vecino
					camino_actual = camino_vecino
					energia_actual  = energia_vecino
				elif random.random() < math.exp(d_E / temperatura):
					solucion_actual = vecino
					camino_actual 	= camino_vecino
					energia_actual 	= energia_vecino
			temperatura = self.esquema_enfriamiento(temperatura)
		return solucion_actual, camino_actual

  # Parámetros del algoritmo
  #temperatura_inicial = 100
  #enfriamiento = 0.95
  #iteraciones = 1000
  #rango_perturbacion = 0.1

  # Ejecutar el algoritmo
  #mejor_solucion, valor_objetivo = self.recocido_simulado(funcion_objetivo, temperatura_inicial, enfriamiento, iteraciones, rango_perturbacion)

  #print("Mejor solución encontrada:", mejor_solucion)
  #print("Valor objetivo de la mejor solución:", valor_objetivo)
