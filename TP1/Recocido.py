import math
import random
from Problem import Problem
from Astar import A_star
from Enviroment import Enviroment
import copy
import csv

class Recocido:
	def __init__(self, T, T_min, L, enviroment:Enviroment):
		self.T = T
		self.T_min = T_min
		self.L = L
		self.L_original = L
		self.enviroment = enviroment


    # Funcion variación de la temperatura
	def esquema_enfriamiento(self, temperatura):
		#return (self.T - 0.001 * round((math.exp(iteracion/2)), 2))
		#return (self.T - 2*iteracion)
		return temperatura * 0.82

    # Función para generar una solución vecina (perturbación)
	def generar_vecino(self, solucion_actual:list, tam_bloque):
		vecino = copy.deepcopy(solucion_actual)
		
		# Forma 1
		indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
		bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
		random.shuffle(bloque)
		vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
		# Forma 2
		'''indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
		bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
		if abs(bloque[0] - bloque[1]) == 2:
			while abs(bloque[0] - bloque[1]) == 2:
				indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
				bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
			vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
			return vecino	
		elif abs(bloque[0] - bloque[1]) == 1:			
			if random.random() > 0.85:
				random.shuffle(bloque)
				vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
			return vecino
		else:
			random.shuffle(bloque)
			vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
			return vecino'''
		return vecino
	
	def energia(self, estado):
		path:list = []
		start_pos = (0, 0)
		# Calculo del camino completo de ida
		for i, goal in enumerate(estado):
				if i == 0:
					# Problema inicial desde la posición de inicio al primer objetivo
						problem  = Problem(self.enviroment, start_pos, self.enviroment.shelf2coor(goal))
						a_star   = A_star(problem)
				else:
					# Redefine el problema por cada objetivo
						a_star.problem.start = path[-1]
						a_star.problem.goal  = self.enviroment.shelf2coor(goal)
						a_star.re_init(a_star.problem)
				# Actualiza el camino
				path       += a_star.solve()
		
		#-------APPENDEA EL CAMINO DE VUELTA-----------#
		a_star.problem.start = path[-1]
		a_star.problem.goal  = start_pos
		a_star.problem.goal_shelf = None
		a_star.re_init(a_star.problem)
		path       	+= a_star.solve()
		#----------------------------------------------#
		return len(path), path
	

    # Algoritmo de recocido simulado
	def ejecutar_recocido(self, solucion_inicial: list):
		solucion_actual = copy.deepcopy(solucion_inicial)
		solucion_propuesta = []
		dist = []

		for i in solucion_actual:
			dist.append(self.enviroment.manhattan(self.enviroment.shelf2coor(i), (0, 0)))
		solucion_actual.insert(0, solucion_actual.pop(dist.index(min(dist))))

		l = len(solucion_actual)
		for k in range(l):
			dist = []

			if k == 0:
				solucion_propuesta = [solucion_actual.pop(0)]
			else:
				for j in solucion_actual:
					i = solucion_propuesta[-1]
					dist.append(self.enviroment.manhattan(self.enviroment.shelf2coor(i), self.enviroment.shelf2coor(j)))
				
				solucion_propuesta.append(solucion_actual.pop(dist.index(min(dist))))
	
		solucion_actual = solucion_propuesta
		temperatura = self.T
		energia_actual, camino_actual = self.energia(solucion_actual)
		it = 0

		with open('ejecucion_recocido.csv', 'w', newline='') as archivo_csv: 
			escritor_csv = csv.writer(archivo_csv) 
			escritor_csv.writerow(['it', 'T','e'] + ['-']*25)
			while temperatura > self.T_min:

				if temperatura > 0.1:
					if not (int(len(solucion_actual) * 0.08) == 1):
						tam_bloque =  int(len(solucion_actual) * 0.08)
					else:
						tam_bloque = 2
					self.L = round(0.1*self.L_original)
				else:
					tam_bloque =  int(len(solucion_actual) * 0.28)
					self.L = self.L_original
				if not self.L > 0:
					self.L = 1
				if not tam_bloque >= 2:
					tam_bloque = 2
				#self.L = self.L_original
	
				for _ in range(round(self.L)):
					escritor_csv.writerow([it, temperatura, energia_actual] + solucion_actual)
					vecino = self.generar_vecino(solucion_actual, tam_bloque)
					energia_vecino, camino_vecino = self.energia(vecino)
					d_E = energia_actual - energia_vecino
					
					if d_E > 0 or (random.random() < math.exp(d_E / temperatura)):
						solucion_actual = vecino
						camino_actual = camino_vecino
						energia_actual  = energia_vecino
						
				it += 1
				temperatura = self.esquema_enfriamiento(temperatura)

			escritor_csv.writerow([it, temperatura, energia_actual] + solucion_actual)
			
		return solucion_actual, camino_actual
