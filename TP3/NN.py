import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.display import clear_output
import random

def random_indices_selection(vec1, vec2, n):
    if n > len(vec1) or n > len(vec2):
        raise ValueError("n debe ser menor o igual a la longitud de los vectores")

    # Seleccionar índices aleatorios únicos
    indices = random.sample(range(len(vec1)), n)

    # Crear nuevos vectores con los valores seleccionados
    selected_values_vec1 = [vec1[i] for i in indices]
    selected_values_vec2 = [vec2[i] for i in indices]

    # Crear nuevos vectores sin los valores seleccionados
    remaining_vec1 = [vec1[i] for i in range(len(vec1)) if i not in indices]
    remaining_vec2 = [vec2[i] for i in range(len(vec2)) if i not in indices]

    return selected_values_vec1, selected_values_vec2, remaining_vec1, remaining_vec2

def normalizar_datos(datos):
    # Convertimos los datos a un arreglo de NumPy
    datos = np.array(datos, dtype=float)
    
    # Encontramos el valor mínimo y máximo de los datos
    min_val = np.min(datos)
    max_val = np.max(datos)
    
    # Aplicamos la fórmula de normalización
    datos_normalizados = (datos - min_val) / (max_val - min_val)
    
    return datos_normalizados
def sigmoid(x, deriv = False):
	R = 1/(1+np.e**(-x))
	if deriv:
		return R*(1-R)
	else:
		return R
def tanh(x, deriv = False):
	R = (np.e**x-np.e**(-x))/(np.e**x+np.e**(-x))
	if deriv:
		return (1 - R**2)
	return R
def ReLu(x, deriv = False):
	if deriv:
		x[x<=0] = 0
		x[x>0] = 1
		return x
	return np.maximum(x, 0)

def leaky_ReLU(x, alpha=0.01, deriv=False):
	if deriv:
		x[x<=0] = alpha
		x[x>0] = 1
		return x
	return np.where(x<=0, alpha*x,x)
   

def identidad(x, deriv=False):
	
	if deriv:
		x[x<=0] = 1
		x[x>0] = 1
		return x  # Derivada de la función identidad es siempre 1
	return x

def MSE(Yp, Yr , deriv = False):
	if deriv:
		return 2*(Yp-Yr)
	return np.mean((Yp-Yr)**2)

class Layer:
	def __init__(self, con, neuron):
		'''
		    con:    el numero de conexiones de la capa con la anterior (numero de salidas de la capa anterior)
			neuron: el numero de neuronas en la capa
		'''
		self.b = np.random.rand(1, neuron) * 2 - 1 #Genera una matriz de 1 x neuron, con valores entre [-1,1)
		self.w = np.random.rand(con, neuron) * 2 - 1
class NeuralNetwork:
	def __init__(self, top = [], act_fun = []):
		'''
		    top:     la topologia de la red [entradas, neuron(capa1), neuron(capa2), ..., salidas (neuron ultima capa)]
			act_fun: función de activación
		'''
		self.top = top
		self.act_fun = act_fun
		self.model = self.define_model()

	def define_model(self):
		'''
		Define la red neuronal como una lista de capas de neuronas.
		'''
		NeuralNetwork = []
		
		
		for i in range(len(self.top)-1): # Crea las capas
			'''El numero de conexiones de una capa es el numero de neuronas de la
			capa anterior'''
			NeuralNetwork.append(Layer(self.top[i], self.top[i+1]))
		return NeuralNetwork

	def predict(self, X = []):
		'''
		    Función que a partir de las entradas obtiene la salida de la red neuronal.
		    X: Es una matriz que tiene como filas las entradas para cada ejemplo
		'''
		out = X

		for i in range(len(self.model)): # Recorre las capas del modelo aplicando la función de activación
			z = self.act_fun[i](out @ self.model[i].w + self.model[i].b) # Aplica la función de activación de la capa.
			out = z # Actualiza el valor de out como las entradas para la siguiente capa.
		return out
	def fit(self, X = [], Y = [], X_t= [], Y_t= [],epochs = 100, learning_rate = 0.5):
		
		plt.ion()
		fig, ax = plt.subplots()
		line, = ax.plot([], [],label='Error de validacion',color='red')
		line_t, = ax.plot([], [],label='Error de test',color='blue')
		error = []
		error_t = []
		print(X)
		
		print(X)
		for k in range(epochs):
			'''
			    out: Una lista de tuplas que tienen como primer elemento
    			los z (suma ponderada por los pesos de las neuronas de las entradas a la capa mas los bias)
	    		y como segundo elemento las salidas de la capa
			'''
			
			out = [(None, X)]

			for i in range(len(self.model)): # Recorre las capas calculando los z y a(salidas)
				z = out[-1][1] @ self.model[i].w + self.model[i].b
				a = self.act_fun[i](z, deriv = False)
				out.append((z,a))
			print(MSE(a, Y))

			deltas = []

			for i in reversed(range(len(self.model))):
				z = out[i + 1][0]
				a = out[i + 1][1]

				if i == len(self.model) - 1:
					deltas.insert(0, MSE(a, Y, deriv = True) * self.act_fun[i](a, deriv = True))
				else:
					deltas.insert(0, deltas[0] @ _W.T * self.act_fun[i](a, deriv = True))
				_W = self.model[i].w
				
				self.model[i].b = self.model[i].b - np.mean(deltas[0], axis = 0, keepdims = True) * learning_rate
				self.model[i].w = self.model[i].w - out[i][1].T @ deltas[0] * learning_rate
			print(k)
			#if k>1000:
			#	 learning_rate = 0.5*learning_rate
			
			error.append(MSE(out[-1][1],Y,))
			error_t.append(MSE(self.predict(X_t),Y_t))


			line.set_xdata(range(len(error)))
			line.set_ydata(error)
			line_t.set_xdata(range(len(error_t)))
			line_t.set_ydata(error_t)
			ax.relim()
			ax.autoscale_view()
			fig.canvas.draw()
			fig.canvas.flush_events()
			#time.sleep(0.001)  
		plt.ioff()
		plt.show()
		print('NeuralNetwork Successfully Trained')

def main():
	
    # Número de puntos a generar
	num_puntos = 1000
	
    # Generar valores de x
	x = np.linspace(0, 10, num_puntos)

    # Calcular valores de y para la parte positiva de la parábola y = x^2
	#y = np.sin(x)+1#**2
	y = x**2

    # Añadir algo de ruido a los puntos para hacer la nube más realista
	#ruido = np.random.normal(0, 10, num_puntos)
	ruido = np.random.normal(0, 10, y.shape)
	#ruido = np.random.normal(0, 0.2, y.shape)
	y_ruidoso = y + ruido
	n = round(0.2*1000)
	x_t, y_ruidoso_t,x, y_ruidoso = random_indices_selection(x,y_ruidoso, n)
	
	x_t = np.array(x_t)
	y_ruidoso_t = np.array(y_ruidoso_t)
	x = np.array(x)
	y_ruidoso = np.array(y_ruidoso)

    # Filtrar para solo tener la parte positiva
	x_positivos = normalizar_datos(np.array(x[y_ruidoso >= 0]).reshape(-1, 1))
	y_positivos = normalizar_datos(np.array(y_ruidoso[y_ruidoso >= 0]).reshape(-1, 1))

	x_positivos_t = normalizar_datos(np.array(x_t[y_ruidoso_t >= 0]).reshape(-1, 1))
	y_positivos_t = normalizar_datos(np.array(y_ruidoso_t[y_ruidoso_t >= 0]).reshape(-1, 1))
	
  
	
	 
	NN = NeuralNetwork(top = [1, 30,20,10, 1], act_fun = [leaky_ReLU,leaky_ReLU,leaky_ReLU,sigmoid])
	#NN = NeuralNetwork(top = [1, 150,50,10, 1], act_fun = [leaky_ReLU,leaky_ReLU,leaky_ReLU,sigmoid])
	
	NN.fit(X = x_positivos, Y = y_positivos,X_t = x_positivos_t, Y_t = y_positivos_t, epochs = 700, learning_rate = 0.0005)
	#NN.fit(X = x_positivos, Y = y_positivos,X_t = x_positivos_t, Y_t = y_positivos_t, epochs = 1000, learning_rate = 0.00005)

	#x_test = random_points(n = 5000)
	#y_test = brain_xor.predict(x_test)
	yy = []
	xx = []
	for i in range(len(x_positivos)):
		yy.append(NN.predict(x_positivos[i])[0][0])
		xx.append(x_positivos[i][0])
		
	#print(x_positivos)
	# Graficar
	plt.scatter(x_positivos, y_positivos,color='blue', alpha=0.5, s=10)
	plt.scatter(xx, yy,color='red', alpha=0.5, s=10)
	plt.title('Nube de puntos con forma de parábola positiva centrada en 0')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.grid(True)
	plt.show()
	#print(brain_xor.predict([0,0,0,1]))
	#plt.scatter(x_test[:, 0], x_test[:, 1], c = y_test, s = 25, cmap = 'GnBu')
	#plt.show()
	


if __name__ == '__main__':
	main()
