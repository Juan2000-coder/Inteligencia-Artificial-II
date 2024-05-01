from VariablesLinguisticas 	import *
from FuncionesPertenencia  	import *
from Operadores 			import *
import matplotlib.pyplot as plt

def calcular_centroide(dx = 0.5):    
	pesoTotal 		= 0
	pesoPonderado 	= 0
	for i in range(1 + int(100/dx)):
		pesoPonderado 	+= (InferenciaDifusa.Evaluar(i*dx) * i*dx)
		pesoTotal 		+= (InferenciaDifusa.Evaluar(i*dx))
	return pesoPonderado/pesoTotal

if __name__ == '__main__':
	#--------------------------------Variables nitidas----------------------------------
	TenfNitida				= 25
	TcalNitida				= 50
	ToNitida				= 10							# La temperatura objetivo
	ZNitida 				= None
	ZcalNitida 				= None
	ZenfNitida 				= None
	TpNitida	 			= None
	HoraNitida 				= None
	lista_TiNitida 			= []
	lista_Vp				= []
	Vp = calcular_centroide()
	tau 					= 24*3600*1/5
	dt					    = 3600/2

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	
	# Datos del 15 de febrero de 2024 en mendoza
	#VectorTemperaturaAmbiente = [29, 28.5, 28, 27.5, 27, 26.5, 26, 25, 24, 23.5, 23, 22.5, 22, 22, 22, 21, 20, 19.5, 19, 19, 19, 19, 19, 20, 21, 22, 23, 24, 25, 25.5, 26, 27, 28, 29.5, 31, 32, 33, 33.5, 34, 34.5, 35, 35, 35, 35, 35, 34.5, 34, 33.5, 33.5]
	
	VectorPorEncima25 		   = [29, 28.5, 28, 27.5, 27, 26.5, 26, 26.1, 26.2, 26.3, 26.4, 26.5, 26.6, 26.7, 26.8, 26.9, 27, 27.1, 27.2, 27.3, 27.4, 27.5, 27.6, 27.7, 27.8, 27.9, 28, 28.1, 28.2, 28.3, 28.4, 28.5, 28.6, 28.7, 28.8, 28.9, 29, 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 30, 30.1, 30.2]
	VectorTemperaturaAmbiente  = VectorPorEncima25	

	#VectorPorDebajo25 		   = [24, 23.5, 23, 22.5, 22, 21.5, 21, 20, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5, 4, 3, 2.5, 2, 1.5, 1, 0, -1, -2, -3, -4, -6, -7, -9, -10, -11, -12]
	#VectorTemperaturaAmbiente = VectorPorDebajo25
	
	VectorTiempos = np.arange(0, 24.5, 0.5)


	TiNitida		= 10					# La temperatura interior inicial
	inicio_dia = int(len(VectorTemperaturaAmbiente)/3)
	final_dia  = int(len(VectorTemperaturaAmbiente)*5/6)

	Tp_dia = VectorTemperaturaAmbiente[inicio_dia:final_dia]
	TpNitida		= sum(Tp_dia)/len(Tp_dia)	# La temperatura pronosticada inicial


	i = 0
	while(i in range(len(VectorTemperaturaAmbiente))):

		'''		if contador % 10 == 0:
			
        # Si el contador es un múltiplo de 10, aumentar j en 1
			j += 1
			
        # Reiniciar el contador
			contador = 0
		'''
	
		#---------------------------------------MEDICIÓN---------------------------------------
		lista_TiNitida.append(TiNitida)
		lista_Vp.append(Vp)
		HoraNitida	= VectorTiempos[i]							# Hora actual
		TeNitida 	= VectorTemperaturaAmbiente[i]				# Temperatua exterior actual
		ZNitida 	= (TiNitida - ToNitida)*(TeNitida - TiNitida)
		ZenfNitida 	= (TiNitida - TenfNitida)*(TeNitida - TiNitida)
		ZcalNitida	= (TiNitida - TcalNitida)*(TeNitida - TiNitida)

		VariablesNitidas		= [ZNitida, ZcalNitida, ZenfNitida, TpNitida, HoraNitida]

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
		corte2 = min(ValB['Hora']['Dia'], ValB['Z']['ZC'])
		corte3 = min(ValB['Hora']['Dia'], ValB['Z']['ZN'])

		# Falta agregar el término de Tpredicha, se debe calcular el mínimo entre los tres
		corte4 = min(ValB['Hora']['Noche'], ValB['Tp']['TAlta'], ValB['ZEnf']['ZEnfP'])
		corte5 = min(ValB['Hora']['Noche'], ValB['Tp']['TAlta'], ValB['ZEnf']['ZEnfC'])
		corte6 = min(ValB['Hora']['Noche'], ValB['Tp']['TAlta'], ValB['ZEnf']['ZEnfN'])

		corte7 = min(ValB['Hora']['Noche'], ValB['Tp']['TBaja'], ValB['ZCal']['ZCalP'])
		corte8 = min(ValB['Hora']['Noche'], ValB['Tp']['TBaja'], ValB['ZCal']['ZCalC'])
		corte9 = min(ValB['Hora']['Noche'], ValB['Tp']['TBaja'], ValB['ZCal']['ZCalN'])

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

		Vp 				= calcular_centroide() #Ventana Porcentaje
		tau_instantaneo = tau*(1 + 0.1*(100 - Vp)/100)
		TiNitida 		= dt*(TeNitida - TiNitida)/tau_instantaneo + TiNitida
		i += 1



	fig, ax1 = plt.subplots()
	# Plotear la segunda gráfica
	plt.plot(VectorTiempos, lista_TiNitida, label='T. Interior')
	plt.plot(VectorTiempos, lista_Vp, label='Ventana', color = 'g')
	plt.plot(VectorTiempos, VectorTemperaturaAmbiente , label='T. Exterior')

	# Añadir etiquetas y título
	plt.xlabel('Tiempo (h)')
	plt.ylabel('Temperatura (°C)')
	plt.title('Gráficas superpuestas')

	# Añadir una leyenda
	plt.legend()

	
	#Plotear los porcentajes de apertura de la ventana
	ax2 = ax1.twinx()

	
	
	# Mostrar el gráfico
	plt.show()
	#print(lista_vp)
      