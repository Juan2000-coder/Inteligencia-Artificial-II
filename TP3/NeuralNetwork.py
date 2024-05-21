import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.initialize()

    def initialize(self):
        # ====================== INITIALIZE NETWORK WEIGTHS AND BIASES ===========================

        self.weights_input_hidden = np.random.rand(4, 2)  # 4 entradas, 2 neuronas en la capa ocultas  W1[4x2]
        self.bias_hidden = np.random.rand(2)              # 2 bias para las neuronas ocultas           B1[1x2]
        self.weights_hidden_output = np.random.rand(2, 3) # 2 neurona en la capa oculta, 3 salidas     W2[2x3]
        self.bias_output = np.random.rand(3)              # 2 bias para las neuronas de salida         B2[1x3]
        '''                                                 
                                                            X  -->     
                                                            X  -->  X  -->  X
                                                               -->     -->  X
                                                            X  -->  X  -->  X
                                                            X  -->     
        '''
        # ========================================================================================


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    '''def sigmoid_derivative(x):
        sig = sigmoid(x)
        return sig * (1 - sig)'''

    def tanh(self, x):
        return np.tanh(x)

    '''def tanh_derivative(self, x):
        return 1 - np.tanh(x) ** 2'''

    def lineal(self, x):
        return 1*x + 0

    '''def lineal_derivative(self, x):
        return 1'''


    def think(self, inputs):
        # ======================== PROCESS INFORMATION SENSED TO ACT =============================
        # Propagación hacia adelante
        hidden_input = np.matmul(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden_output = self.tanh(hidden_input)
        
        output_input = np.matmul(hidden_output, self.weights_hidden_output) + self.bias_output
        output = self.lineal(output_input)
        
        return self.act(output)
        # ========================================================================================


    def act(self, output):
        # ======================== USE THE ACTIVATION FUNCTION TO ACT =============================
        action = np.argmax(output)
        if (action >= 0.75):
            return "JUMP"
        elif (action <= -0.75):
            return "DUCK"
        else:
            return "RUN"
        # =========================================================================================