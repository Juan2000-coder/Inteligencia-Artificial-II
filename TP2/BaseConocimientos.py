from Operadores import *
from VariablesLinguisticas import *

f1 = Then(And(Hora.tling['D'], Z.tling['ZP']), V.tling['VC'])
f2 = Then(And(Hora.tling['D'], Z.tling['ZC']), V.tling['VM'])
f3 = Then(And(Hora.tling['D'], Z.tling['ZN']), V.tling['VA'])

f4 = Then(And(Hora.tling['N'], Tp.tling['TAlta'], ZEnf.tling['ZEnfP']), V.tling['VC'])
f5 = Then(And(Hora.tling['N'], Tp.tling['TAlta'], ZEnf.tling['ZEnfC']), V.tling['VM'])
f6 = Then(And(Hora.tling['N'], Tp.tling['TAlta'], ZEnf.tling['ZEnfN']), V.tling['VA'])

f7 = Then(And(Hora.tling['N'], Tp.tling['TBaja'], ZEnf.tling['ZCalP']), V.tling['VC'])
f8 = Then(And(Hora.tling['N'], Tp.tling['TBaja'], ZEnf.tling['ZCalC']), V.tling['VM'])
f9 = Then(And(Hora.tling['N'], Tp.tling['TBaja'], ZEnf.tling['ZCalN']), V.tling['VA'])

Base	= Or(f1, f2, f3, f4, f5, f6, f7, f8, f9)
f=Or(And(Or(a,b),Or(c,d)), And(Or(e,f),Or(g,h)))
f.evaluar(1, 2, 3, 4,5,6,7,8)