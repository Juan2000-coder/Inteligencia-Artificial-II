import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from panchotron2 import Perceptron
import math

# Función cuadrática centrada en 0
def funcion_cuadratica(x):
    return x**2

# Funcion Seno
def funcion_seno(x):
    return np.sin(x)

# Generar datos
np.random.seed(0)
X = np.linspace(-3, 3, 500).reshape(-1, 1)
y = funcion_cuadratica(X) + np.random.normal(scale=0.8, size=X.shape)  # Modificar scale para dar más o menos desviación estándar a los valores (valores más dispersos)

# Normalizar datos
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y)

# Dividir los datos en conjuntos de entrenamiento, validación y prueba
X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Parámetros a probar
learning_rates = [0.001, 0.01, 0.1]
activation_functions = ['relu', 'sigmoid', 'tanh', 'leakyrelu', 'swish', 'elu']
neurons_options = [2, 3, 4, 5]

# Variables para almacenar los mejores parámetros
best_lr = learning_rates[0]
best_activation = activation_functions[0]
best_neurons = neurons_options[0]
best_val_error = float('inf')
results_df = pd.DataFrame(columns=['Learning rate:','Activation', 'Neurons', 'Validation Error'])



# Búsqueda de la mejor combinación de parámetros COMENTAR SI NO SE QUIERE HACER VALIDACION
'''for lr in learning_rates:
    for activation in activation_functions:
        for neurons in neurons_options:
            perceptron = Perceptron(learning_rate=lr, n_iters=50, activation=activation, neuronas=neurons)
            perceptron.fit(X_train, y_train)
            
            # Evaluar el error en el conjunto de validación
            val_predictions = perceptron.predict(X_val)
            val_error = np.mean((val_predictions - y_val)**2)
            
            print(f'Learning rate: {lr}, Activation: {activation}, Neurons: {neurons}, Validation Error: {val_error}')
            results_df = results_df.append({'Learning rate': lr, 'Activation': activation, 'Neurons': neurons, 'Validation Error': val_error}, ignore_index=True)
            
            if val_error < best_val_error:
                best_val_error = val_error
                best_lr = lr
                best_activation = activation
                best_neurons = neurons

print(f'Mejor combinación - Learning rate: {best_lr}, Activation: {best_activation}, Neurons: {best_neurons} con un error de validación: {best_val_error}')

# Guardar los resultados en un archivo Excel
results_df.to_excel('resultados_perceptron.xlsx', index=False)'''



# Entrenar el modelo final con la mejor combinación de parámetros utilizando los conjuntos de entrenamiento y validación combinados
X_train_val = np.vstack((X_train, X_val))
y_train_val = np.vstack((y_train, y_val))

#perceptron = Perceptron(learning_rate=best_lr, n_iters=50, activation=best_activation, neuronas=best_neurons) # COMENTAR SI NO SE HIZO UNA VALIDACION. LOS PARAMETROS DE AQUI SALEN DE VALIDACION
perceptron = Perceptron(learning_rate=0.01, n_iters=100, activation='relu', neuronas=3)
perceptron.fit(X_train_val, y_train_val)

# Predicciones en el conjunto de prueba
X_test_ordenado = sorted(X_test)
predicciones_test = perceptron.predict(X_test_ordenado)

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Datos de Prueba')
plt.plot(X_test_ordenado, predicciones_test, color='red', linewidth=2, label='Predicciones')
plt.xlabel('X (Normalizado)')
plt.ylabel('y')
plt.title('Aproximación de la Función Cuadrática por el Perceptrón (Conjunto de Prueba)')
plt.legend()
plt.grid(True)
plt.show()
