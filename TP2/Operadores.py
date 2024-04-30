from FuncionesPertenencia import FuncionPertenencia

class Or(FuncionPertenencia):
	def __init__(self, *args):
		super().__init__()
		self.Operandos = args
    
	def Evaluar(self, *args):
		if len(args) == 1:
			val = args[0]
			parametros = [val for _ in self.Operandos]
		else:
			parametros = list(args)
		ValoresBorrosos = [Operando.Evaluar(arg) for arg, Operando in zip(parametros, self.Operandos)]
		return max(ValoresBorrosos, default = 0)
	
class And(FuncionPertenencia):
	def __init__(self, *args):
		super().__init__()
		self.Operandos = args

	def Evaluar(self, *args):
		if len(args) == 1:
			val = args[0]
			parametros = [val for _ in self.Operandos]
		else:
			parametros = list(args)
		ValoresBorrosos = [Operando.Evaluar(arg) for arg, Operando in zip(parametros, self.Operandos)]
		return min(ValoresBorrosos, default = 0)