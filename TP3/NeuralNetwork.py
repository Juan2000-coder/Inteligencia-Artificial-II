import numpy as np

'''
    Esta clase incluye la definición de la forma de la red y el tipo de funciones que se aplican en cada capa.
        Actualmente la red tiene 6 entradas, 2 capas ocultas con 2 y 3 neuronas respectivamente y 2 salidas.
        La función de activación de las capas internas es "ReLu".
            - (Se pueden cambiar las funciones de activación en la función think, modificando self.ReLu por la función deseada)
        La función de activación de la capa de salida es "softmax".
            - (Se pueden cambiar las funciones de activación en la función think, modificando self.softmax por la función deseada)

            
    Tener en cuenta que se puede modificar lo que recibe la función think, desde el main (línea 155 aprox)
        - Al modificar esto, se debe ser consistente y modificar del mismo modo a la primera capa de la red.
        - Actualmente se está recibiendo:
                -- Pos en x del dino: dino_params.x
                -- Pos en y del dino: dino_params.y
                -- Pos en x del obstaculo: obstacle_params.x 
                -- Pos en y del obstaculo: obstacle_params.y
                -- Delta de pos en x: (dino_params.x - obstacle_params.x)
                -- Delta de pos en y: (dino_params.y - obstacle_params.y)
'''


class NeuralNetwork:
    def __init__(self):

        self.red_neuronal = [6, 2, 3, 2]
            # Neuronas Entrada, Capa Oculta 1: Neuronas, ... , Capa Oculta N-1: Neuronas, Neuronas Salida        

        # Lista de matrices de peso de cada capa
        self.weights = []              # Cada matriz tiene: en filas las neuronas de la capa anterior
                                                          # en columnas las neuronas de la capa siguiente
        # Lista de vectores de bias de cada capa
        self.biases = []               # Cada vector tiene tantos elementos como neuronas en la capa

        self.initialize()

    def initialize(self):
        # ====================== INITIALIZE NETWORK WEIGTHS AND BIASES ===========================
               
        for i in range(len(self.red_neuronal) - 1):
            weight_matrix = np.random.rand(self.red_neuronal[i], self.red_neuronal[i + 1])
            bias_vector = np.random.rand(self.red_neuronal[i + 1])
            
            self.weights.append(weight_matrix)
            self.biases.append(bias_vector)

        # ========================================================================================


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def tanh(self, x):
        return np.tanh(x)

    def lineal(self, x):
        return 1*x + 0
    
    def ReLu(self, x):
        return np.maximum(0, x)
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)


    def think(self, inputs):
        # ======================== PROCESS INFORMATION SENSED TO ACT =============================
        # Propagación hacia adelante
        layer_input = inputs
        for i in range(len(self.weights) - 1):
            # Primera it: se multiplican todas las entradas x la primera matriz de W y B y se obtienen salidas
                # de la primera capa oculta. Estas luego son las entradas a la segunda capa oculta y así...
            hidden_input = np.matmul(layer_input, self.weights[i]) + self.biases[i]
            layer_output = self.ReLu(hidden_input)
            layer_input = layer_output

        output_input = np.matmul(layer_input, self.weights[-1]) + self.biases[-1]
        output = self.softmax(output_input)
        #print("Salida: ", output)
        return self.act(output)
        # ========================================================================================


    def act(self, output):
        # ======================== USE THE ACTIVATION FUNCTION TO ACT =============================
        action = np.argmax(output)
        #print("Output: ", output)
        #print("Action: ", action)
        if (action == 0):
            return "JUMP"
        elif (action == 1):
            return "DUCK"
        #elif (action == 2):
        #    return "RUN"
        # =========================================================================================