class Orden:
    def __init__(self, numero_orden, _archivo):
        self.archivo = _archivo
        self.estantes = self.obtener_orden(numero_orden)

    def obtener_orden(self, numero_orden):
        numeros_sin_p = []
        with open(self.archivo, 'r') as f:
            encontrada = False
            for linea in f:
                if encontrada:
                    if linea.startswith('P'):
                        numero = linea.strip()[1:]
                        numeros_sin_p.append(int(numero))
                    elif linea.startswith('Order'):
                        break
                elif linea.startswith(f'Order {numero_orden}'):
                    encontrada = True
        return numeros_sin_p