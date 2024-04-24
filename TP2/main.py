from VariablesLinguisticas import *
from FuncionesPertenencia  import *

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
	VariablesNitidas	= [Znitida, ZCalNitida, ZEnfNitida, TPNitida, HoraNitida]

	#----------------------ITERACIÓN EN EL TIEMPO--------------------------------------------
	VectorTemperaturaAmbiente						# Serie de temperatura exterior
	VectorTiempos												# Serie de tiempos en correspondiente con la Tambiente
	
	while(True):
		#---------------------------------------MEDICIÓN---------------------------------------
		HoraNitida	= VectorTiempos.pop()								# Hora actual
		TENitida 		= VectorTemperaturaAmbiente.pop()		# Temperatua exterior actual
		TINitida		=																		# La temperatura interior actual
		ZNitida 		= (TINitida - TONitida)*(TENitida - TINitida)
		ZEnfNitida 	= (TINitida - TEnfNitida)*(TENitida - TINitida)
		ZCalNitida	= (TINitida - TCalNitida)*(TENitida - TINitida)

		# dia_siguiente 				= [inicio:fin]				# Una forma a ver de cómo obtener estos índices
		# cantidad_muestras		 	= len(dia_siguiente)	# Cantidad de muestras de temperatura en el dia siguiente
		TPNitida 		= sum(VectorTemperaturaAmbiente[dia_siguiente])/cantidad_muestras	# La temperatura pronostico promedio
		
		'''#--------------------------------------BORROSIFICAR LAS VARIABLES-------------------------------------------
		# Evaluar todos los terminos linguisticos de todas las variables
		ValoresBorrosos = {}
		for VariableNitida, VariableBorrosa in zip(VariablesNitidas, VariablesBorrosas):
			Terminos = {}
			for Termino in VariableBorrosa.tling:
				Terminos[Termino] = VariableBorrosa.es(Termino, VariableNitida)
			ValoresBorrosos[VariableBorrosa.Nombre] = dict(Terminos)'''
				
		#-------------------------------------EVALUAR LAS REGLAS DE LA BASE--------------------------------------------
		# Se obtiene una funcion de pertenencia como evaluación de cada función
		# Es mejor definir las operaciones and, or, then como funciones de pertenencia de multiples variables.
		
		# De esta manera, las funciones f1, f2, f3, ... quedan definidas como funciones de pertenencia de multiples
		# variables que se dan a las funciones de pertenencia en el orden de las variables.
		
		f1 = Then(And(ValoresBorrosos['H']['D'], ValoresBorrosos['Z']['ZP']), V.tling['VC'])
		f2 = Then(And(ValoresBorrosos['H']['D'], ValoresBorrosos['Z']['ZC']), V.tling['VM'])
		f3 = Then(And(ValoresBorrosos['H']['D'], ValoresBorrosos['Z']['ZN']), V.tling['VA'])
		
		f4 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TAlta'], ValoresBorrosos['ZEnf']['ZEnfP']), V.tling['VC'])
		f5 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TAlta'], ValoresBorrosos['ZEnf']['ZEnfC']), V.tling['VM'])
		f6 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TAlta'], ValoresBorrosos['ZEnf']['ZEnfN']), V.tling['VA'])
							
		f7 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TBaja'], ValoresBorrosos['ZCal']['ZCalP']), V.tling['VC'])
		f8 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TBaja'], ValoresBorrosos['ZCal']['ZCalC']), V.tling['VM'])
		f9 = Then(And(ValoresBorrosos['H']['N'], ValoresBorrosos['Tp']['TBaja'], ValoresBorrosos['ZCal']['ZCalN']), V.tling['VA'])
		
		# Se juntan todas las funciones de pertenencia
		f = Or(f1, f2, f3, f4, f5, f6, f7, f8, f9)

		#--------------------------------DESBORROSIFICACIÓN-------------------------------------
		# Se obtiene el centroide a partir de f que estará definida en un subintervalo del rango de la ventana
		# que es de 0 a 100
		