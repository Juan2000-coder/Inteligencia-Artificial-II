from AG import Poblacion
def print_divider():
    print("=" * 100)

# Función para imprimir una instrucción con formato
def print_instruction(instruction):
    print(f"ℹ️ {instruction}")

# Función para imprimir un mensaje de éxito
def print_success(message):
    print(f"✅ {message}")

# Función para imprimir un mensaje de error
def print_error(message):
    print(f"❌ Error: {message}")

#---------------------------MAIN---------------------------#
if __name__ == '__main__':
    print_divider()
    print("BIENVENIDO AL PROGRAMA DE GESTIÓN DEL DEPOSITO")
    print("Optimizacion con algoritmo genetico")
    print_divider()

# Ejemplo de uso
  
    tam_poblacion = 6
    prob_mutacion = 0.5
    genes = [i+1 for i in range(32)]
  
    poblacion = Poblacion(tam_poblacion, genes, prob_mutacion)
  
    generacion = 1
    cont = 0
    while True:
        print(f"Generación {generacion}:")
        
        print("-" * 100)
        if cont >= 100 :
            break
        poblacion.evolucionar()
        
        generacion += 1
        cont =+ 1
    
    print("¡Objetivo alcanzado!")
  
