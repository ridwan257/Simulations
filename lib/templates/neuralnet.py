import numpy as np
from lib import rmath

c = rmath.c

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

def tanh(x):
    return np.tanh(x)

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

class Perceptron:
    def __init__(self, input_no) -> None:
        self.learning_rate = 0.002
        self.weights = np.random.rand(input_no + 1)
        # personal thing
        self.__activator = sigmoid
        self.output = 0
        self.__inputs = np.zeros(input_no+1)
        self.__inputs[0] = 1
        
    def set_activator(self, func):
        self.__activator = func


    def fire(self):
        z = np.dot(self.weights, self.__inputs)
        self.output = self.__activator(z)

    def think(self, inputs:list):
        self.__inputs[1:] = inputs
        self.fire()
        return self.output
    
    def train(self, inputs, label):
        self.__inputs[1:] = inputs
        z = np.dot(self.weights, self.__inputs)
        result = self.__activator(z)
        error = label - result
        delta_w = self.__inputs * (error * self.learning_rate)
        self.weights += delta_w

        # print(f'{self.__inputs=}')
        # print(f'{z=}')
        # print(f'{result=}')
        # print(f'{error=}')
        # print(f'{delta_w=}')
        # print(f'{self.weights=}')
        # print('-----------')
