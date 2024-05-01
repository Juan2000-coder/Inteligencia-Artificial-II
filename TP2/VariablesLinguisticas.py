from FuncionesPertenencia import *
import matplotlib.pyplot as plt
from Operadores import *
import matplotlib.pyplot as plt
import numpy as np

class VariableLinguistica:
	def __init__(self, Nombre:str, TLinguisticos: dict, limites: tuple):
		'''
		Constructor de la clase VariableLinguistica
		
		Nombre: 				str, nombre de la variable linguistica
		TLinguisticos:  dict[str, float], diccionario de tuplas (nombre del término, funcion de pertenencia(objeto))
		'''
		self.Nombre  = Nombre
		self.Tling 	 = TLinguisticos
		self.limites = limites

	def es(self, Termino:str, Valor):
		'''
		"es"		: es una función que determina el grado de pertenencia de un valor a un término de la variable.
		termino	: str, nombre del término
		'''
		if Termino in self.Tling:
			return self.Tling[Termino].Evaluar(Valor)

#--------------------------DEFINICIÓN DE TÉRMINOS Y VARIABLES LINGUÍSTICAS DEL PROBLEMA--------------------------
#-------------------------------------------DEFINICIÓN DE TÉRMINOS-----------------------------------------------
#Terminos linguisticos de Z
ZN = HombroDerecho(0, 10)   # Hay que ver en que valores varia (Znegativo)
ZC = Triangular(0, 5)		# Hay que ver en qué valores varía	(Zcentro)
ZP = HombroIzquierdo(0, 10) # Hay que ver en que valores varía	(Zpositivo)

#Terminos linguisticos de V (ventana)
VA	= HombroIzquierdo(50, 30)   # Ventana abrir
VC	= HombroDerecho(50, 30)		# Ventana cerrar
VM	= Triangular(50, 10)		# Ventana medio

#Terminos linguisticos de Zcal
ZcalN = HombroDerecho(0, 50)   	# Hay que ver en que valores varia (Znegativo)
ZcalC = Triangular(0, 50)		# Hay que ver en qué valores varía	(Zcentro)
ZcalP = HombroIzquierdo(0, 50)  # Hay que ver en que valores varía	(Zpositivo)

#Terminos linguisticos de Zenf
ZenfN = HombroDerecho(0, 50)   	# Hay que ver en que valores varia (Znegativo)
ZenfC = Triangular(0, 50)		# Hay que ver en qué valores varía	(Zcentro)
ZenfP = HombroIzquierdo(0, 50)  # Hay que ver en que valores varía	(Zpositivo)

#Terminos linguisticos de Tp (Temperatura pronóstico)
Talta = HombroIzquierdo(15, 10)  	# Temperatura pronóstico alta
Tbaja = HombroDerecho(20, 10)		# Temperatura pronóstico baja

#Terminos linguisticos de Hora (Hora del día)
Dia 	= And(HombroIzquierdo(7, 2), HombroDerecho(21, 2))  	# En horas.
Noche 	= Or(HombroDerecho(9, 2), HombroIzquierdo(19, 2))	# Temperatura pronóstico baja

#--------------------------DEFINICIÓN DE LAS VARIABLES LINGUISTICAS-------------------------------------
Z 		= VariableLinguistica('Z', {'ZN':ZN, 'ZC':ZC, 'ZP':ZP}, [-1000, 1000]) 	# Ajustar los valores despues
Zcal  	= VariableLinguistica('ZCal', {'ZCalN':ZcalN, 'ZCalC':ZcalC,'ZCalP':ZcalP}, [-1000, 1000]) # Ajustar 
Zenf  	= VariableLinguistica('ZEnf', {'ZEnfN':ZenfN, 'ZEnfC':ZenfC,'ZEnfP':ZenfP}, [-1000, 1000]) # Ajustar
Tp 		= VariableLinguistica('Tp', {'TAlta':Talta, 'TBaja':Tbaja}, [-15, 45])
Hora	= VariableLinguistica('Hora', {'Dia':Dia, 'Noche':Noche}, [0, 24])
V		= VariableLinguistica('V', {'VA':VA, 'VC':VC, 'VM':VM}, [0, 100])

InferenciaDifusa 	= Or(VA, VC, VM)

VariablesBorrosas 	= [Z, Zcal, Zenf, Tp, Hora]

colores 			= ['red', 'green', 'blue']


'''for variable in VariablesBorrosas:
	universo = np.linspace(variable.limites[0], variable.limites[1], 2001)
	graphs = [[] for _ in variable.Tling]
	
	for valor in universo:
		for i, termino in enumerate(variable.Tling):
			graphs[i].append(variable.es(termino, valor))

	color = 0
	for graph, nombre in zip(graphs, variable.Tling.keys()):
		plt.plot(universo, graph, label = nombre, color=colores[color])
		color += 1
	plt.legend()
	plt.title(variable.Nombre)
	plt.show()
'''