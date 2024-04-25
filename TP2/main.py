from VariablesLinguisticas 	import *
from FuncionesPertenencia  	import *
from Operadores 						import *

if __name__ == '__main__':
	#--------------------------------Variables nitidas----------------------------------
	TEnfNitida	= 25
	TCalNitida	= 50
	TONitida		= 25																# La temperatura objetivo
	ZNitida 					= None
	ZCalNitida 				= None
	ZEnfNitida 				= None
	TPNitida	 				=	None
	HoraNitida 				= None
	VariablesNitidas	= [ZNitida, ZCalNitida, ZEnfNitida, TPNitida, HoraNitida]

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	VectorTemperaturaAmbiente						# Serie de temperatura exterior
	VectorTiempos												# Serie de tiempos en correspondiente con la Tambiente
	
	while(True):
		#---------------------------------------MEDICIÓN---------------------------------------
		HoraNitida	= VectorTiempos.pop()								# Hora actual
		TENitida 		= VectorTemperaturaAmbiente.pop()		# Temperatua exterior actual
		TINitida		=	# La temperatura interior actual se obtiene por integración del modelo termico
		ZNitida 		= (TINitida - TONitida)*(TENitida - TINitida)
		ZEnfNitida 	= (TINitida - TEnfNitida)*(TENitida - TINitida)
		ZCalNitida	= (TINitida - TCalNitida)*(TENitida - TINitida)

		# dia_siguiente 				= [inicio:fin]				# Una forma a ver de cómo obtener estos índices
		# cantidad_muestras		 	= len(dia_siguiente)	# Cantidad de muestras de temperatura en el dia siguiente
		TPNitida 		= sum(VectorTemperaturaAmbiente[dia_siguiente])/cantidad_muestras #Temperatura pronostico

    
		#-------------------------------EVALUACIÓN DE LAS REGLAS------------------------------
		Base.Evaluar()
		#---------------------------------DESBORROSIFICACIÓN----------------------------------

		# Se obtiene el centroide a partir de f que estará definida en un subintervalo del rango de la ventana
		# que es de 0 a 100
		