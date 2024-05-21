import numpy as np

# Función de activación Sigmoid y su derivada
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Función de pérdida cuadrática media y su derivada
def mse_loss(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def mse_loss_derivative(y_true, y_pred):
    return y_pred - y_true

# Inicialización de pesos y sesgos
def initialize_parameters(n_x, n_h, n_y):
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    return W1, b1, W2, b2

# Propagación hacia adelante
def forward_propagation(X, W1, b1, W2, b2):
    Z1 = np.dot(W1, X) + b1
    A1 = sigmoid(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = Z2  # Sin activación para la capa de salida en regresión
    return Z1, A1, Z2, A2

# Propagación hacia atrás
def backward_propagation(X, Y, Z1, A1, A2, W2):
    m = X.shape[1]
    dZ2 = mse_loss_derivative(Y, A2)
    dW2 = (1 / m) * np.dot(dZ2, A1.T)
    db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = dA1 * sigmoid_derivative(A1)
    dW1 = (1 / m) * np.dot(dZ1, X.T)
    db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)
    return dW1, db1, dW2, db2

# Actualización de parámetros
def update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate):
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2
    return W1, b1, W2, b2

# Entrenamiento de la red neuronal
def train_neural_network(X, Y, n_h, num_iterations, learning_rate):
    n_x = X.shape[0]
    n_y = Y.shape[0]
    W1, b1, W2, b2 = initialize_parameters(n_x, n_h, n_y)
    
    for i in range(num_iterations):
        Z1, A1, Z2, A2 = forward_propagation(X, W1, b1, W2, b2)
        dW1, db1, dW2, db2 = backward_propagation(X, Y, Z1, A1, A2, W2)
        W1, b1, W2, b2 = update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate)
        
        if i % 1000 == 0:
            loss = mse_loss(Y, A2)
            print(f"Iteración {i}, Pérdida: {loss}")
    
    return W1, b1, W2, b2

# Prueba de la red neuronal
def predict(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_propagation(X, W1, b1, W2, b2)
    return A2

# Datos de entrenamiento (ejemplo sencillo)
X_train = np.random.rand(2, 500)  # 2 características, 500 ejemplos
Y_train = np.sum(X_train, axis=0, keepdims=True)  # La salida es la suma de las dos características

# Entrenamiento del modelo
n_h = 5  # Número de neuronas en la capa oculta
num_iterations = 10000
learning_rate = 0.01
W1, b1, W2, b2 = train_neural_network(X_train, Y_train, n_h, num_iterations, learning_rate)

# Predicción
X_test = np.random.rand(2, 10)
Y_pred = predict(X_test, W1, b1, W2, b2)
print("Predicciones:", Y_pred)
