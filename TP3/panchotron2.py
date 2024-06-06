import numpy as np
from sklearn.preprocessing import MinMaxScaler
from IPython.display import clear_output
import matplotlib.pyplot as plt

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return np.where(x<=0,0,1)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    sig = sigmoid(x)
    return sig * (1 - sig)

def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1 - np.tanh(x)**2

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_deriv(x, alpha=0.01):
    return np.where(x > 0, 1, alpha)

def elu(x, alpha=1.0):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

def elu_deriv(x, alpha=1.0):
    return np.where(x > 0, 1, elu(x, alpha) + alpha)

def swish(x):
    return x * sigmoid(x)

def swish_deriv(x):
    sig = sigmoid(x)
    return swish(x) + sig * (1 - swish(x))

        

class Perceptron:

    def __init__(self, learning_rate = 0.01, n_iters = 1000, activation='relu', neuronas = 3):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.funcion_act, self.funcion_act_deriv = self.get_activation_function(activation)
        self.pesos = {'oculta': np.random.rand(1, neuronas), 'salida': np.random.rand(neuronas, 1)}
        self.bias = {'oculta': np.zeros((1, neuronas)), 'salida': np.zeros((1, 1))}
        #RED CON UNA CAPA OCULTA DE 3 NEURONAS
        #print(self.pesos)
        
        
    def get_activation_function(self, activation):
        if activation == 'relu':
            return relu, relu_deriv
        elif activation == 'sigmoid':
            return sigmoid, sigmoid_deriv
        elif activation == 'tanh':
            return tanh, tanh_deriv
        elif activation == 'leakyrelu':
            return leaky_relu, leaky_relu_deriv
        elif activation == 'swish':
            return swish, swish_deriv
        elif activation == 'elu':
            return elu, elu_deriv
        else:
            raise ValueError("Error: Elija entre relu, sigmoid, tanh, leakyrelu, swish, elu")
    
    def MSE(self, Yp, Yr , deriv = False):
        if deriv:
            return 2*(Yp-Yr)
        return np.mean((Yp-Yr)**2)


    def fit(self, X,y):
        n_samples, n_features =  X.shape            
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'r-')
        ERROR = []
    #    print(X.shape)
        for i in range(self.n_iters):

           
            for idx, x_i in enumerate(X):
              #  print(self.pesos)
              #  print(self.bias)
                
                oculta_input = np.dot(x_i, self.pesos['oculta']) + self.bias['oculta'] # Z = B1 + x_i * W1 , Z ES DE 1X3
                oculta_output = self.funcion_act(oculta_input.flatten()).reshape(1, -1) # H  = Relu(Z)

                # Capa de salida
                salida_input = np.dot(oculta_output, self.pesos['salida']) + self.bias['salida'] # Y = B2 + H * W2 , Y ES UN ESCALAR
                salida_output = self.funcion_act(salida_input) # Ŷ = Relu(Y)
               
                # Cálculo del error MSE
                error = np.mean((salida_output - y[idx])**2) # ERROR CUADRATICO MEDIO (Ypredicho - Yreal)² por algun motivo no se usa, sino que se usa la derivada mas bien
                
                # Retropropagación (Backpropagation)
                dl_dy = 2*np.mean(salida_output - y[idx]) #  2(ŷ-y)/m
                #dỳ_dH = self.funcion_act_deriv(salida_input)
                dy_dH = self.pesos['salida'].T
                dH_dz = self.funcion_act_deriv(oculta_input.flatten()).reshape(1, -1)
                dl_dw2 = dl_dy * oculta_output  #* dỳ_dH             # 2(ŷ-y)/m * H
                dl_db2 = dl_dy #* dỳ_dH                               # 2(ŷ-y)/m
                dl_dw1 = dl_dy * dy_dH *  dH_dz * x_i #* dỳ_dH       # 2(ŷ-y)/m * W2 * ReluDerivada * x_i
                dl_db1 = dl_dy * dy_dH *  dH_dz # * dỳ_dH             # 2(ŷ-y)/m * W2 * ReluDerivada
                
 #               if idx < 5 and i <= 3:
 #                   print("oculta_input:", oculta_input)
 #                   print("oculta_output:", oculta_output)
 #                   print("salida_input:", salida_input)
 #                   print("salida_output:", salida_output)
 #                   print("error:", error)
 #                   print("dl_dy", dl_dy)
 #                   print("dy_dH", dy_dH)
 #                   print("dH_dz", dH_dz)
 #                   print("dL_dw2", dl_dw2)
 #                   print("dL_db2", dl_db2)
 #                   print("dL_dw1", dl_dw1)
 #                   print("dL_db1", dl_db1)
 #                   print(self.pesos['salida'])
                   # print("xd", dy_dH *  dH_dz)
               
                
                #salida_delta = error * self.funcion_act_deriv(salida_output) # esto lo hizo chatgpt pero probablemente este mal
                
                # Actualización de los pesos y sesgos de la capa de salida
                #self.pesos['salida'] += self.lr * np.dot(oculta_output.T, salida_delta)
                #self.bias['salida'] += self.lr * np.sum(salida_delta, axis=0, keepdims=True)
                self.pesos['salida'] +=  -self.lr * dl_dw2.T
                self.bias['salida'] += -self.lr * dl_db2

                # Retropropagación a la capa oculta
               #oculta_error = np.dot(salida_delta, self.pesos['salida'].T)
               #oculta_delta = oculta_error * self.funcion_act_deriv(oculta_output)
               
                # Actualización de los pesos y sesgos de la capa oculta
                self.pesos['oculta'] += -self.lr * dl_dw1
                self.bias['oculta'] += -self.lr * dl_db1   
            
            ERROR.append(error)

            line.set_xdata(range(len(ERROR)))
            line.set_ydata(ERROR)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()    
            print(error)
            print(ERROR)
           
           
        plt.ioff()
        plt.show()   
                
    def predict(self, X):
        # Propagación hacia adelante
        # Capa oculta
        oculta_input = np.dot(X, self.pesos['oculta']) + self.bias['oculta']
        oculta_output = self.funcion_act(oculta_input)

        # Capa de salida
        salida_input = np.dot(oculta_output, self.pesos['salida']) + self.bias['salida']
        salida_output = self.funcion_act(salida_input)

        return salida_output
    
    
