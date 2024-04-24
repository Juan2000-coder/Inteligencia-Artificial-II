from VariablesLinguisticas import VariableLinguistica
from FuncionesPertenencia import *

if __name__ == '__main__':
	#-------------------------Definir los terminos linguisticos-----------------------

	diaCompleto = [x * 0.5 for x in range(0, int(24 / 0.5) + 1)]
	
	#Terminos linguisticos de Z
	ZN = HombroDerecho(0, 50)   # Hay que ver en que valores varia (Znegativo)
	ZC = Triangular(0, 50)			# Hay que ver en qué valores varía	(Zcentro)
	ZP = HombroIzquierdo(0, 50) # Hay que ver en que valores varía	(Zpositivo)

	#Terminos linguisticos de V (ventana)
	VA	= HombroIzquierdo(50, 20) # Ventana abrir
	VC	= HombroDerecho(50, 20)		# Ventana cerrar
	VM	= Triangular(50, 20)			# Ventana medio
	
	#-----------------------Definición de variables linguísticas-----------------------
	Z = VariableLinguistica('Z', {'ZN':ZN, 'ZC':ZC, 'ZP':ZP}, [-1000, 1000]) # Ajustar los valores despues
  # Zenf
  # Zcal
  # Hora
	Hora = VariableLinguistica('HORA', {'DIA':Hombro(12, 0, 23), 'NOCHE':Hombro()}, diaCompleto)
	# Tp

	VariablesBorrosas = [Z, ZCal, ZEnf, TP, Hora] # Colocamos todas las variables en una lista
	V									= VariableLinguistica('V', {'VA':VA, 'VC':VC, 'VM':VM}, [0, 100])
	
	#--------------------------------Variables nitidas----------------------------------
	ZNitida 		= None
	ZCalNitida 	= None
	ZEnfNitida 	= None
	TPNitida	 	=	None
	HoraNitida 	= None
	VariablesNitidas	 = [Znitida, ZCalNitida, ZEnfNitida, TPNitida, HoraNitida]

	#----------------------Iteración en el paso de tiempo--------------------------------
	VectorTemperaturaAmbiente						# Serie de temperatura exterior
	VectorTiempos												# Serie de tiempos en correspondiente con la Tambiente
	while(True):
		#-------------------------------Medición------------------------
		Hora_n 			= VectorTiempos.pop()								# Hora actual
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
			Terminos = {}
			for Termino in VariableBorrosa.tling:
				Terminos[Termino] = VariableBorrosa.es(Termino, VariableNitida)
			ValoresBorrosos[VariableBorrosa.Nombre] = dict(Terminos)
				
		#--------------------Evaluar las reglas de la base de conocimiento---------------------
		# Se obtiene como resultado para cada regla, una función de pertenencia
		f1 = Then(And(ValoresBorrosos['H']['D'], ValoresBorrosos['Z']['ZP']), V.tling['VC'])
		# f2
		# f3
		# f4
		# f5
		# f6
		# f7
		# f8
		# f9
		
		# Se juntan todas las funciones de pertenencia
		f = Or(f1, f2, f3, f4, f5, f6, f7, f8, f9)

		#--------------------------------Desborrosificacion-------------------------------------
		# Se obtiene el centroide a partir de f que estará definida en un subintervalo del rango de la ventana
		# que es de 0 a 100