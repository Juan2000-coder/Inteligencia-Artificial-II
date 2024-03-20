class Orden:
  def __init__(self):
     self.archivo    = 'ordenes.txt'
     self.estantes   = self.obtener_orden()

  def obtener_orden(self):
    numeros_sin_p = []
    with open(self.archivo, 'r') as f:
        for linea in f:
            if linea.startswith('P'):
                numero = linea.strip()[1:]  # Eliminar la letra 'P' del principio
                numeros_sin_p.append(int(numero))
    return numeros_sin_p
  
# Ejemplo de uso:
'''archivo = 'ordenes.txt'
numeros_sin_p = obtener_numeros_sin_letra_p(archivo)
print(numeros_sin_p)'''