from FuncionesPertenencia import FuncionPertenencia

class Or(FuncionPertenencia):
	def __init__(self, *args):
		super().__init__()
		self.Operandos = args
    
	def Evaluar(self, *args):
		ValoresBorrosos = [Operando.Evaluar(arg) for arg, Operando in zip(args, self.Operandos)]
		return max(ValoresBorrosos, default = 0)