from Enviroment import Enviroment
from Problem import Problem
from Astar import A_star

import random
import math
import copy
import csv


class Recocido:
	def __init__(self, T, T_min, L, enviroment:Enviroment, tb_alta=0.08, tb_baja=0.28, f_T=0.85):
		'''Constructor de la clase Recocido.
		Inicializa los parámetros del algoritmo de recocido simulado.'''

		self.T = T						# T (float): Temperatura inicial.
		self.T_min = T_min				# T_min (float): Temperatura mínima.
		self.L = L						# L (int): Número de iteraciones por cada temperatura.
		self.L_original = L				# L (int): Número de iteraciones por cada temperatura.
		self.enviroment = enviroment	# enviroment (Enviroment): Objeto de la clase Enviroment que representa el entorno del problema.
		self.tb_alta = tb_alta			# Tamaño de bloque a alta T (porcentaja de la longitud de la orden)
		self.tb_baja = tb_baja			# Tamaño de bloque a baja T (porcentaja de la longitud de la orden)
		self.f_T 	 = f_T				# Factor de reducción de la temperatura

	def esquema_enfriamiento(self, temperatura):
		'''Función para variar la temperatura en cada iteración.'''

		return temperatura * self.f_T

    
	def generar_vecino(self, solucion_actual, tam_bloque):
		'''Genera una solución vecina (perturbación) a partir de la solución actual.'''
		vecino = copy.deepcopy(solucion_actual)
		
		# Forma 1
		#indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
		#bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
		#random.shuffle(bloque)
		#vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
		#return vecino		

		# Forma 2
		'''indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
		bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
		random.shuffle(bloque)
		vecino[indice_inicio:indice_inicio + tam_bloque] = bloque'''
		# Forma 2
		indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
		bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
		pares = list(zip(bloque[:-1], bloque[1:]))
		bloque1 = []
		indices1 = []
		for i, par in enumerate(pares):
			if self.enviroment.are_opposed(par[0], par[1]) or self.enviroment.are_beside(par[0], par[1]):
				bloque1 += [par[0], par[1]]
				indices1 += [i, i + 1]
		bloque2  = [elemento for elemento in bloque if elemento not in bloque1]
		indices2 = [indice for indice in list(range(0, len(bloque))) if indice not in indices1]
		random.shuffle(bloque2)

		for i, indice in enumerate(indices2):
			bloque[indice] = bloque2[i]
		vecino[indice_inicio:indice_inicio + tam_bloque] = bloque
		return vecino
		
		'''if abs(bloque[0] - bloque[1]) == 2:
			while abs(bloque[0] - bloque[1]) == 2:
				indice_inicio = random.randint(0, len(vecino) - tam_bloque)        
				bloque = vecino[indice_inicio:indice_inicio + tam_bloque]
			random.shuffle(bloque)
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
	
	def energia(self, estado):
		'''Calcula la energía (o costo) de un estado del problema.'''

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
	
	def solucion_incial(self, orden:list):
		'''Obtiene una propuesta para la solución incial'''
		solucion_actual = copy.deepcopy(orden)
		solucion_propuesta = []
		dist = []

		# En el bucle se obtiene el elemento más cercano al punto de partida
		for i in solucion_actual:
			dist.append(self.enviroment.manhattan(self.enviroment.shelf2coor(i), (0, 0)))
		solucion_actual.insert(0, solucion_actual.pop(dist.index(min(dist))))

		# Se arma la solución propuesta incorporando sucesivemente el elemento más
		# cercano al último en la lista
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
	
		return solucion_propuesta

	def ejecutar_recocido(self, orden: list):
		'''Ejecuta el algoritmo de recocido simulado.'''
		solucion_actual = self.solucion_incial(orden)

		temperatura = self.T
		energia_actual, camino_actual = self.energia(solucion_actual)
		it = 0

		# Se escriben los datos en un archivo para visualizar la evolución
		with open('ejecucion_recocido.csv', 'w', newline='') as archivo_csv: 
			escritor_csv = csv.writer(archivo_csv) 
			escritor_csv.writerow(['it', 'T','e'] + ['-']*len(orden))
			while temperatura > self.T_min:
				if temperatura > 0.1: 	# Parámetros en alta temperatura
					if not (int(len(solucion_actual) * self.tb_alta) == 1):
						tam_bloque =  int(len(solucion_actual) * self.tb_alta)
					else:
						tam_bloque = 2
					self.L = round(0.1*self.L_original)
				else:					# Parámetros en baja temperatura
					tam_bloque =  int(len(solucion_actual) * self.tb_baja)
					self.L = self.L_original


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
				temperatura = self.esquema_enfriamiento(temperatura)

			escritor_csv.writerow([it, temperatura, energia_actual] + solucion_actual)
			
		return solucion_actual, camino_actual
