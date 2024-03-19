def obtener_numeros_sin_letra_p(archivo):
  numeros_sin_p = []
  with open(archivo, 'r') as f:
      for linea in f:
          if linea.startswith('P'):
              numero = linea.strip()[1:]  # Eliminar la letra 'P' del principio
              numeros_sin_p.append(int(numero))
  return numeros_sin_p

# Ejemplo de uso:
archivo = 'tu_archivo.txt'
numeros_sin_p = obtener_numeros_sin_letra_p(archivo)
print(numeros_sin_p)