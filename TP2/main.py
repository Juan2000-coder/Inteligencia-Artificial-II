#Comentario random<-Panchardo
from VariablesLinguisticas 	import *
from FuncionesPertenencia  	import *
from Operadores 			import *
import matplotlib.pyplot as plt

def calcular_centroide():    
  dx = 0.5
  pesoTotal = 0
  pesoPonderado = 0
  for i in range(200):
    pesoPonderado = pesoPonderado + (InferenciaDifusa.Evaluar(i*dx) *i*dx)
    pesoTotal = pesoTotal + (InferenciaDifusa.Evaluar(i*dx))
  return pesoPonderado/pesoTotal
  #print ("El X centroide es: ", Xcen)

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
	lista_TiNitida =[]
	tau = 24*3600*1/5
	dt=1
  

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	# Datos del 15 de febrero de 2024 en mendoza
	VectorTemperaturaAmbiente = [29, 28, 27, 26, 24, 23, 22, 22, 20, 19, 19, 19, 21, 23, 25, 26, 28, 31, 33, 34, 35, 35, 35, 34]						# Serie de temperatura exterior
	VectorTiempos 			  = list(range(24))											# Serie de tiempos en correspondiente con la Tambiente
	TiNitida	= 10# La temperatura interior actual se obtiene por integración del modelo termico
	
	pepe = 0
	while(pepe in range(24)):
		#---------------------------------------MEDICIÓN---------------------------------------
		HoraNitida	= VectorTiempos.pop()					# Hora actual
		TeNitida 	= VectorTemperaturaAmbiente.pop()		# Temperatua exterior actual
		ZNitida 	= (TiNitida - ToNitida)*(TeNitida - TiNitida)
		ZenfNitida 	= (TiNitida - TenfNitida)*(TeNitida - TiNitida)
		ZcalNitida	= (TiNitida - TcalNitida)*(TeNitida - TiNitida)

		# dia_siguiente 			= [inicio:fin]				# Una forma a ver de cómo obtener estos índices
		# cantidad_muestras		 	= len(dia_siguiente)	# Cantidad de muestras de temperatura en el dia siguiente
		#TpNitida 		= sum(VectorTemperaturaAmbiente[dia_siguiente])/cantidad_muestras #Temperatura pronostico

		#-----------------------------------BORROSIFICAR--------------------------------------
		# diccionario de valores borrosos con claves los nombres de las variables y los valores son  un diccionario por cada variable
  		# que tiene por clave los nombres de los terminos y por valores las evaluaciones de las funciones de pertenencia
		ValB = {}
		for VarNitida, VarBorrosa, in zip(VariablesNitidas, VariablesBorrosas):
			valores = {}
			for termino in VarBorrosa.Tling:
				valores[termino] = VarBorrosa.es(termino, VarNitida)
			ValB[VarBorrosa.Nombre] = dict(valores)


  		#-------------------------------EVALUACIÓN DE LAS REGLAS------------------------------
    #Calculo de los antecedentes de cada regla de la base de conocimientos
		#de aca deberia salir un corteVA, corteVC, corteVM
		corte1 = min(ValB['Hora']['Dia'], ValB['Z']['ZP'])
		corte2 = min(ValB['Hora']['Dia'], ValB['Z']['ZN'])
		corte3 = min(ValB['Hora']['Dia'], ValB['Z']['ZC'])

		# Falta agregar el término de Tpredicha, se debe calcular el mínimo entre los tres
		corte4 = min(ValB['Hora']['Noche'], ValB['ZEnf']['ZenfP'])
		corte5 = min(ValB['Hora']['Noche'], ValB['ZEnf']['ZenfN'])
		corte6 = min(ValB['Hora']['Noche'], ValB['ZEnf']['ZenfC'])

		corte7 = min(ValB['Hora']['Noche'], ValB['ZCal']['ZenfP'])
		corte8 = min(ValB['Hora']['Noche'], ValB['ZCal']['ZenfN'])
		corte9 = min(ValB['Hora']['Noche'], ValB['ZCal']['ZenfC'])

		corteVC = max(corte1, corte4, corte7)
		corteVM	= max(corte2, corte5, corte8)
		corteVA = max(corte3, corte6, corte9)

		# CORTAR EN SI
		VA.corte = corteVA
		VC.corte = corteVC
		VM.corte = corteVM
		
		#---------------------------------DESBORROSIFICACIÓN----------------------------------

		# Se obtiene el centroide a partir de f que estará definida en un subintervalo del rango de la ventana
    	#Centroide en X - Indica que tanto se abre la ventana entre 0 y 100.

		lista_TiNitida.append(TiNitida)
		Vp = calcular_centroide() #Ventana Porcentaje
		tau_instantaneo = tau*(1+0.1*(100-Vp)/100)
		TiNitida = tau_instantaneo*dt*(TeNitida-TiNitida)+TiNitida
	
		pepe = pepe + 1
    
	plt.plot(VectorTiempos,VectorTemperaturaAmbiente , label='T. Exterior')

	# Plotear la segunda gráfica
	plt.plot(VectorTiempos, lista_TiNitida, label='T. Interior')

	# Añadir etiquetas y título
	plt.xlabel('Tiempo (h)')
	plt.ylabel('Temperatura (°C)')
	plt.title('Gráficas superpuestas')

	# Añadir una leyenda
	plt.legend()

	# Mostrar el gráfico
	plt.show()
      
      
    
      