from VariablesLinguisticas 	import *
from FuncionesPertenencia  	import *
from Operadores 			import *
import matplotlib.pyplot as plt
import math
from modelo import *


def CalcularCentroide(dx = 0.5):    
	PesoTotal 		= 0
	PesoPonderado 	= 0
	for i in range(1 + int(100/dx)):
		PesoPonderado 	+= (InferenciaDifusa.Evaluar(i*dx) * i*dx)
		PesoTotal 		+= (InferenciaDifusa.Evaluar(i*dx))
	return PesoPonderado/PesoTotal

def EvolucionTe(Dia, HoraNitida, MediaLarga = 25, RangoLargo = 30, RangoCorto = 5, PeriodoLargo = 24, PeriodoCorto = 6):
	return RangoLargo*math.sin((2*math.pi/PeriodoLargo)*(HoraNitida + Dia*24)) + RangoCorto*math.sin((2*math.pi/PeriodoCorto)*(HoraNitida + Dia*24))+ MediaLarga

def CalcularTp(Dia, Hora):
	if Hora < 8:
		return np.mean([EvolucionTe(Dia, HoraPronostico) for HoraPronostico in np.arange(8, 20.5, 0.5)])
	else:
		return np.mean([EvolucionTe(Dia + 1, HoraPronostico) for HoraPronostico in np.arange(8, 20.5, 0.5)])


if __name__ == '__main__':
	#--------------------------------Variables nitidas----------------------------------
	TenfNitida				= 10
	TcalNitida				= 50
	ToNitida				= 25							# La temperatura objetivo
	ZNitida 				= None
	ZcalNitida 				= None
	ZenfNitida 				= None
	TpNitida	 			= None
	HoraNitida 				= 0
	TiNitida				= 10					# La temperatura interior inicial
	TiNitidaVabierta 		= TiNitida
	TiNitidaVcerrada 		= TiNitida
	Vp 						= 50
	Tau 					= 24*3600*1/5
	Dt					    = 3600/2
	Dia						= 0
	LimiteDias				= 14
	Hab						= Habitacion(Tau)

	ListaTiNitida 				= []
	ListaTeNitida				= []
	ListaTiNitidaVabierta 		= []
	ListaTiNitidaVcerrada		= []
	ListaVp						= []
	VectorTiempos				= []

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	while(Dia < LimiteDias):

		#---------------------------------------MEDICIÓN---------------------------------------
		TeNitida 	= EvolucionTe(Dia, HoraNitida, MediaLarga = -5, RangoLargo=10, RangoCorto=2, PeriodoCorto=4)

		VectorTiempos.append(HoraNitida + Dia*24)
		ListaTiNitida.append(TiNitida)
		ListaTiNitidaVabierta.append(TiNitidaVabierta)
		ListaTiNitidaVcerrada.append(TiNitidaVcerrada)
		ListaTeNitida.append(TeNitida)

		ZNitida 	= (TiNitida - ToNitida)*(TeNitida - TiNitida)
		ZenfNitida 	= (TiNitida - TenfNitida)*(TeNitida - TiNitida)
		ZcalNitida	= (TiNitida - TcalNitida)*(TeNitida - TiNitida)
		TpNitida	= CalcularTp(HoraNitida, Dia)

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
		Vp 				= CalcularCentroide() #Ventana Porcentaje
		if Vp > 50:
			Vp = 100
		else:
			Vp = 0
		
		ListaVp.append(Vp)
		# Euler
		'''TauInstantaneo 	= Tau*(1 + 0.1*(100 - Vp)/100)
		TiNitida 		= Dt*(TeNitida - TiNitida)/TauInstantaneo + TiNitida
		TiNitidaSinCorreccion += Dt*(TeNitida - TiNitida)/Tau'''

		#RK
		TiNitida 				= Hab.runge_kutta_4(HoraNitida, TiNitida, Dt, TeNitida, Vp)
		TiNitidaVabierta 		= Hab.runge_kutta_4(HoraNitida, TiNitida, Dt, TeNitida, 0)
		TiNitidaVcerrada		= Hab.runge_kutta_4(HoraNitida, TiNitida, Dt, TeNitida, 100)

		if HoraNitida == 23.5:
			HoraNitida  = 0
			Dia		+=1
		else:
			HoraNitida		+= 0.5						# Hora actual

	fig, ax1 = plt.subplots()
	# Plotear la segunda gráfica
	plt.grid(True)
	plt.plot(VectorTiempos, ListaTiNitida, label='T. Interior')
	plt.plot(VectorTiempos, ListaTiNitidaVabierta, label='T. Interior V abieta', color ='cyan')
	plt.plot(VectorTiempos, ListaTiNitidaVcerrada, label='T. Interior V cerrada', color ='yellow')
	plt.plot(VectorTiempos, ListaVp, label='Ventana', color = 'g')
	plt.plot(VectorTiempos, ListaTeNitida , label='T. Exterior')

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
	plt.grid(True)
	plt.plot(VectorTiempos, [Tic-TiVa for Tic, TiVa in zip(ListaTiNitida, ListaTiNitidaVabierta)], label='Diferencia Vcorregida - Vabieta', color='red')
	plt.plot(VectorTiempos, [Tic-TiVc for Tic, TiVc in zip(ListaTiNitida, ListaTiNitidaVcerrada)], label='Diferencia Vcorregida - Vcerrada', color='green')
	plt.plot(VectorTiempos, [TiVa-TiVc for TiVa, TiVc in zip(ListaTiNitidaVabierta, ListaTiNitidaVcerrada)], label='Diferencia Vabierta - Vcerrada', color='blue')
	plt.legend()
	plt.title('Comparación de la correccion/No corrección')
	plt.xlabel('Tiempo (h)')
	plt.ylabel('Temperatura (°C)')
	plt.show()

	plt.show()
	#print(lista_vp)
	plt.grid(True)
	plt.plot(VectorTiempos, [Tic-ToNitida for Tic in ListaTiNitida], label='Diferencia Vcorregida - Vobjetivo', color='red')
	plt.plot(VectorTiempos, [TiVc-ToNitida for TiVc in ListaTiNitidaVcerrada], label='Diferencia Vcerrada - Vobjetivo', color='green')
	plt.plot(VectorTiempos, [TiVa-ToNitida for TiVa in ListaTiNitidaVabierta], label='Diferencia Vabierta - Vobjetivo', color='blue')
	plt.legend()
	plt.title('Comparación de la correccion/No corrección')
	plt.xlabel('Tiempo (h)')
	plt.ylabel('Temperatura (°C)')
	plt.show()