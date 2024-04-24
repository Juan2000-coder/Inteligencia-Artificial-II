class VariableLinguistica:
  def __init__(self, Nombre:str, TLinguisticos: dict[str, float], UDiscurso: list):
	  '''
		Constructor de la clase VariableLinguistica
		Nombre: str, nombre de la variable linguistica
		TLinguisticos: dict[str, float], diccionario de tuplas (nombre del término, funcion de pertenencia(objeto))
		'''
		self.Nombre = Nombre
    self.Tling 	= TLinguisticos
    self.Udisc 	= UDiscurso

	def es(self, Termino:str, Valor):
		'''
		"es"		: es una función que determina el grado de pertenencia de un valor a un término de la variable.
		termino	: str, nombre del término
		'''
		if Termino in self.Tling:
			return self.Tling[Termino].evaluar(Valor)