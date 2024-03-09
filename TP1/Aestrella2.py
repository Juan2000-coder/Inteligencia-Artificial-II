#grafo
from nodos import Nodos
import numpy as np
class AEstrella:
    def _init_(self,_matriz):
        self.matriz = _matriz
        self.nodos_visitados = []

    def abrir_nodo(self,_x,_y):
        # Obtenemos las dimensiones de la matriz
        filas, columnas = self.matriz.shape
        grafo = np.empty((filas, columnas))
        
        # Recorremos la matriz e imprimimos cada elemento
        for i in range(filas):
            for j in range(columnas):
                grafo[i,j] = Nodos(self.matriz[i, j],(i,j))
        
        for i in range(filas-1)[1:]:
            for j in range(columnas-1)[1:]:
                grafo[i,j].set_vecinos([grafo[i-1,j],grafo[i+1,j],grafo[i,j-1],grafo[i,j+1]])
        

        
        
           
