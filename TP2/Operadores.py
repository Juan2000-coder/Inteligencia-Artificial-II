from FuncionesPertenencia import FuncionPertenencia

class Or(FuncionPertenencia):
	def __init__(self, *args):
		super().__init__()
		self.Operandos = args
		
	def Evaluar(self, *args):
		ValoresBorrosos = [Operando.Evaluar(arg) for arg, Operando in zip(args, self.Operandos)]
		return max(ValoresBorrosos, default = 0)
		
class And(FuncionPertenencia):
	def __init__(self, *args):
		super().__init__()
		self.Operandos = args

	def Evaluar(self, *args):
		ValoresBorrosos = [Operando.Evaluar(arg) for arg, Operando in zip(args, self.Operandos)]
		return min(ValoresBorrosos, default = 0)
		
class Not(FuncionPertenencia):
	def __init__(self, Operando):
		super().__init__()
		self.Operando = Operando

	def Evaluar(self, Valor):
		return 1 - self.Operando.evaluar(Valor)
		
class Then(FuncionPertenencia):
	def __init__(self, Antecedente, Consecuente):
		super().__init__()
		self.Antecedente = Antecedente
		self.Consecuente = Consecuente
		self.f					 = Or(Not(self.Antecedente), self.Consecuente)

	def Evaluar(self, ValorAntecedente, ValorConsecuente):
		return f.Evaluar(ValorAntecedente, ValorConsecuente)