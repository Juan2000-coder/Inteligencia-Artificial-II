class FuncionPertenencia:
	'''Clase para definir las funciones de pertenencia que
	vamos a utilizar, osea, triangulares, hombros, etc'''
	
	def __init__(self, ValorCaracteristico = None, Ancho = None):
		'''Constructor de la clase FuncionPertenencia
			ValorCaracteristico: 	float, por ejemplo el centro en la triangular o un extremo en los hombros.
			Ancho: 					 			float, ancho de la pendiente del hombro o del triangulo.
		'''
		
		self.ValorCaracteristico = ValorCaracteristico
		self.Ancho							 = Ancho
		
	def Evaluar(self, *args):
		'''
		Método para evaluar el grado de pertenencia de un 'valor'
		Devuelve un número entre 0 y 1.
		
		Se sobreescribe en cada subclase dado que es distinto para una función triangular
		que para una función hombro.
		'''
		pass
		
'''A continuación se definen sub-clases para las funciones de pertenencia típicas'''
class HombroIzquierdo(FuncionPertenencia):
	'''Función de Pertenencia HombroIzquierdo (pendiente positiva)'''
	def __init__(self, ValorCaracteristico, Ancho):
		super().__init__(ValorCaracteristico, Ancho)
		self.Pendiente = 1/(self.Ancho)		# Pendiente del hombro
		
	def Evaluar(self, Valor, corte = 1):
		if Valor > (self.ValorCaracteristico + self.Ancho):	# Al lado derecho del hombro
			return min(1, corte)
		elif Valor < self.ValorCaracteristico:							# Al lado izquiero del hombro
			return min(0, corte)
		else:																								# En el hombro
			return min(self.Pendiente*(Valor - self.ValorCaracteristico), corte)

class HombroDerecho(FuncionPertenencia):
	'''Función de Pertenencia HombroDerecho (pendiente negativa)'''
	def __init__(self, ValorCaracteristico, Ancho):
		super().__init__(ValorCaracteristico, Ancho)
		self.Pendiente = -1/(self.Ancho) 		# Pendiente del hombro

	def Evaluar(self, Valor, corte = 1):
		if Valor > self.ValorCaracteristico:													# Al lado derecho del hombro
			return min(0, corte)
		elif Valor < (self.ValorCaracteristico - self.Ancho): 				# Al lado izquiero del hombro
			return min(1, corte)
		else:
			return min(1 + self.Pendiente*(Valor - self.ValorCaracteristico), corte) # En el hombro

class Triangular(FuncionPertenencia):
	'''Función de Pertenencia para la Triangular'''
	def __init__(self, ValorCaracteristico, Ancho):
		super().__init__(ValorCaracteristico, Ancho)
		self.PendienteP = 2/(self.Ancho)			# Pendiente flanco derecho
		self.PendienteN = -2/(self.Ancho)			# Pendiente flanco izquierdo
		self.Inferior		= self.ValorCaracteristico - self.Ancho/2 	# Límite inferior triangulo
		self.Superior		= self.ValorCaracteristico + self.Ancho/2		# Límite superior triangulo
		
	def Evaluar(self, Valor, corte = 1):
		if Valor > self.Superior:							# A la derecha del triangulo
			return min(0, corte)
		elif Valor < self.Inferior:						# A la izquierda del triangulo
			return min(0, corte)
		elif self.ValorCaracteristico > Valor > self.Inferior:	# En el flanco izquierdo del triangulo
			return min(self.PendienteP*(Valor - self.Inferior), corte)
		elif self.ValorCaracteristico < Valor < self.Superior:	# En el flanco derecho del triangulo
			return min(self.PendienteN*(Valor - self.ValorCaracteristico), corte)