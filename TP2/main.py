from VariablesLinguisticas import VariableLinguistica
from FuncionesPertenencia import *

if __name__ == '__main__':
	#-------------------------Definir los terminos linguisticos-----------------------

	diaCompleto = [x * 0.5 for x in range(0, int(24 / 0.5) + 1)]
	
	#Terminos linguisticos de Z
	ZN = HombroDerecho(0, 50)   # Hay que ver en que valores varia
	ZC = Triangular(0, 50)			# Hay que ver en qué valores varía
	ZP = HombroIzquierdo(0, 50) # Hay que ver en que valores varía

	#-----------------------Definición de variables linguísticas-----------------------
	Z = VariableLinguistica('Z', {'ZN':ZN, 'ZC':ZC, 'ZP':ZP}, [-1000, 1000]) # Ajustar los valores despues

  # Zenf
  # Zcal
  # Hora
	Hora = VariableLinguistica('HORA', {'DIA':Hombro(12, 0, 23), 'NOCHE':Hombro()}, diaCompleto)
	# Tp

	VariablesBorrosas = [Z, ZCal, ZEnf, TP, Hora] # Colocamos todas las variables en una lista

	#--------------------------------Variables nitidas----------------------------------
	ZNitida 		= None
	ZCalNitida 	= None
	ZEnfNitida 	= None
	TPNitida	 	=	None
	HoraNitida 	= None
	VariablesNitidas	 = [Znitida, ZCalNitida, ZEnfNitida, TPNitida, HoraNitida]

	#----------------------Iteración en el paso de tiempo--------------------------------
	while(True):
		VectorTemperaturaAmbiente						# Serie de temperatura exterior
		
		#-------------------------------Medición------------------------
		Hora_n 	= 																	# Hora actual
		TENitida 		= VectorTemperaturaAmbiente.pop()		# Temperatua exterior actual
		TINitida		=																		# La temperatura interior actual
		TONitida		= 25																# La temperatura objetivo actual
		
		# dia_siguiente 				= [inicio:fin]				# Una forma a ver de cómo obtener estos índices
		# cantidad_muestras		 	= len(dia_siguiente)	# Cantidad de muestras de temperatura en el dia siguiente
		
		TPNitida 		= sum(VectorTemperaturaAmbiente[dia_siguiente])/cantidad_temperaturas	# La temperatura pronostico promedio
		TEnfNitida	= 25
		TCalN				= 50
		
		ZNitida 		= (TINitida - TONitida)*(TENitida - TINitida)
		ZEnfNitida 	= (TINitida - TEnfNitida)*(TENitida - TINitida)
		ZCalNitida	= (TINitida - TCalNitida)*(TENitida - TINitida)
		
		#--------------------------Borrosificar todas las variables----------------------------
		# Evaluar todos los terminos linguisticos de todas las variables
		ValoresBorrosos = {}
		for VariableNitida, VariableBorrosa in zip(VariablesNitidas, VariablesBorrosas):
			for Termino in VariableBorrosa.tling:
				# En donde verga guardamos los valores?
				ValoresBorrosos[VariableBorrosa.Nombre][Termino] = VariableBorrosa.es(Termino, VariableNitida)
				
		#--------------------Evaluar las reglas de la base de conocimiento---------------------
		f1 = Then(And(ValoresBorrosos['H']['D'], ValoresBorrosos['Z']['ZP']), ValoresBorrosos['V']['A'])
		# Se obtiene como resultado una función de pertenencia también para cada regla