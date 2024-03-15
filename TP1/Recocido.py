import math
import random
from Problem import Problem
from Astar import A_star
from Enviroment import Enviroment

class Recocido:

    def __init__(self,_enviroment:Enviroment):
        self.T = 200
        self.T_min = 0.5
        self.estado_inicial = [22 , 30, 1, 4]
        self.L = math.factorial(len(self.estado_inicial))//2
        self.entorno = _enviroment
        self.pb = Problem(self.entorno,(0,0),(1,1))
        self.estrella = A_star(self.pb)

    def esquema_enfriamiento(self, temperatura):
        return temperatura * 0.2

    # Función para generar una solución vecina (perturbación)
    def generar_vecino(self, solucion_actual):
        return random.shuffle(solucion_actual)
    def energia(self ,estado):
        self.pb.start = (0,0)
        self.pb.goal = self.entorno.shelf2coor(estado[0])
        self.estrella.re_init(self.pb)
        E = len(self.estrella.solve())
        
        for i in range(len(estado)-1):
            self.pb.start = self.entorno.shelf2coor(estado[i])
            self.pb.goal = self.entorno.shelf2coor(estado[i+1])
            self.estrella.re_init(self.pb)
            E = E + len(self.estrella.solve())

        return E
    # Algoritmo de recocido simulado
    def ejecutar_recocido(self):
        solucion_actual = self.estado_inicial  # Solución inicial aleatoria
        temperatura = self.T
        energia_actual = self.energia(solucion_actual) 

        while temperatura>self.T_min:
            for i in range(self.L):
                vecino = self.generar_vecino(solucion_actual)
                energia_vecino = self.energia(vecino)
                d_E = energia_actual-energia_vecino

                if random.random()<math.exp(d_E/temperatura):
                    solucion_actual = vecino
            temperatura = self.esquema_enfriamiento(temperatura)
        return solucion_actual

    # Parámetros del algoritmo
    #temperatura_inicial = 100
    #enfriamiento = 0.95
    #iteraciones = 1000
    #rango_perturbacion = 0.1

    # Ejecutar el algoritmo
    #mejor_solucion, valor_objetivo = self.recocido_simulado(funcion_objetivo, temperatura_inicial, enfriamiento, iteraciones, rango_perturbacion)

    #print("Mejor solución encontrada:", mejor_solucion)
    #print("Valor objetivo de la mejor solución:", valor_objetivo)
