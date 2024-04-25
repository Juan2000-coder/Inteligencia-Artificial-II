from VariablesLinguisticas 	import *
from FuncionesPertenencia  	import *
from Operadores 			import *

if __name__ == '__main__':
	#--------------------------------Variables nitidas----------------------------------
	TenfNitida				= 25
	TcalNitida				= 50
	ToNitida				= 25																# La temperatura objetivo
	ZNitida 				= None
	ZcalNitida 				= None
	ZenfNitida 				= None
	TpNitida	 			= None
	HoraNitida 				= None
	VariablesNitidas		= [ZNitida, ZcalNitida, ZenfNitida, TpNitida, HoraNitida]

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	# Datos del 15 de febrero de 2024 en mendoza
	VectorTemperaturaAmbiente = [29, 28, 27, 26, 24, 23, 22, 22, 20, 19, 19, 19, 21, 23, 25, 26, 28, 31, 33, 34, 35, 35, 35, 34]						# Serie de temperatura exterior
	VectorTiempos 			  = list(range(24))											# Serie de tiempos en correspondiente con la Tambiente
	
	while(True):
		#---------------------------------------MEDICIÓN---------------------------------------
		HoraNitida	= VectorTiempos.pop()					# Hora actual
		TeNitida 	= VectorTemperaturaAmbiente.pop()		# Temperatua exterior actual
		TiNitida	= 1# La temperatura interior actual se obtiene por integración del modelo termico
		ZNitida 	= (TiNitida - ToNitida)*(TeNitida - TiNitida)
		ZenfNitida 	= (TiNitida - TenfNitida)*(TeNitida - TiNitida)
		ZcalNitida	= (TiNitida - TcalNitida)*(TeNitida - TiNitida)

		# dia_siguiente 			= [inicio:fin]				# Una forma a ver de cómo obtener estos índices
		# cantidad_muestras		 	= len(dia_siguiente)	# Cantidad de muestras de temperatura en el dia siguiente
		TpNitida 		= sum(VectorTemperaturaAmbiente[dia_siguiente])/cantidad_muestras #Temperatura pronostico

		#-----------------------------------BORROSIFICAR--------------------------------------
		# diccionario de valores borrosos con claves los nombres de las variables y los valores son  un diccionario por cada variable
  		# que tiene por clave los nombres de los terminos y por valores las evaluaciones de las funciones de pertenencia
		ValB = {}
		for VarNitida, VarBorrosa, in zip(VariablesNitidas, VariablesBorrosas):
			valores = {}
			for termino in VarBorrosa.Tling:
				valores[termino] = VarBorrosa.es(termino, VarNitida)
			ValB[VarBorrosa.nombre] = dict(valores)


  		#-------------------------------EVALUACIÓN DE LAS REGLAS------------------------------
		corte1 = min(ValB['Hora']['D'], ValB['Z']['ZP'])
		# Unir todas las funciones que
		#---------------------------------DESBORROSIFICACIÓN----------------------------------
		
		# Se obtiene el centroide a partir de f que estará definida en un subintervalo del rango de la ventana
		# que es de 0 a 100
		