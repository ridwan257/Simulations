import numpy as np
import re

def c(*args, **argv):
    return np.array(args, **argv)

def to_string(vector, digit=3, sep=' '):
    text = np.array2string(vector, precision=digit, 
                           suppress_small=True, separator=sep)
    return text

def sigmoid(x):
    x = np.clip(x, -500, 500)
    return 1 / ( 1 + np.exp(-x) )

def dsigmoid(y):
    return y * (1 - y)

def tanh(x):
    return np.tanh(x)

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

def toBinary(data, threshold=0.5):
    return [0 if n < threshold else 1 for n in data]


class Perceptron:
    def __init__(self, input_no) -> None:
        self.total_i = input_no
        self.learning_rate = 0.5

        # self.weights = np.random.rand(input_no + 1)
        self.weights = np.random.uniform(-2, 2, input_no+1)
        
        # personal thing
        self.__activator = sigmoid
        self.output = c(0)
        self.__inputs = np.zeros(input_no+1)
        self.__inputs[0] = 1


    def summary(self, name='*'):
        print()
        print('*'*20,  name, '*'*20)
        print(f'Input Node - {self.total_i} | Output Node - {1}')
        print(f'Learning rate - {self.learning_rate}')
        print('-'*20, 'Matrix Structure', '-'*20)
        print('row -> output | column -> input')
        print('•'*20, 'Weight', '•'*20)
        print(to_string(self.weights, 4))
        print()

    def save(self, filename):
        # input_no
        # learning rate
        # self.weights
        with open(filename, 'w') as f:
            f.write(f'{self.total_i}\n')
            f.write(f'{self.learning_rate}\n')

            text = np.array2string(self.weights, separator=",")
            text = re.sub(r'\n', '', text)
            f.write(f'{text}\n')
    
    @staticmethod
    def loadFromFile(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            lines = list(map(lambda l : l.strip(), lines))
            
            i = int(lines[0])
            lr = float(lines[1])
            weights = np.array(eval(lines[2]))

        brain = Perceptron(i)
        brain.learning_rate = lr
        brain.weights = weights

        return brain

    def set_activator(self, func):
        self.__activator = func


    def fire(self):
        z = np.dot(self.weights, self.__inputs)
        self.output = c(self.__activator(z))

    def think(self, inputs:list):
        self.__inputs[1:] = inputs
        self.fire()
        return self.output
    
    def train(self, inputs, label): 
        self.__inputs[1:] = inputs
        z = np.dot(self.weights, self.__inputs)
        result = self.__activator(z)
        error = label - result
        delta_w = self.__inputs * (result * (1-result) * error * self.learning_rate)
        self.weights += delta_w

        # print(f'{self.__inputs=}')
        # print(f'{z=}')
        # print(f'{result=}')
        # print(f'{error=}')
        # print(f'{delta_w=}')
        # print(f'{self.weights=}')
        # print('-----------')


class NeuralNetwork:
    def __init__(self, input_no, hidden_no, output_no) -> None:
        self.total_i = input_no
        self.total_h = hidden_no
        self.total_o = output_no
        # self.input_weights = np.zeros((input_no+1, 1))
        self.hidden_weights = np.zeros((hidden_no, input_no+1))
        self.output_weights = np.zeros((output_no, hidden_no+1))
        self.learning_rate = 0.5

        self.__activator = sigmoid
        self.__yderivative = dsigmoid
        
        # personal thing
        self.__inputs = np.zeros(input_no+1)
        self.__inputs[0] = 1
        self.__output_input = np.zeros(hidden_no+1)
        self.__output_input[0] = 1
        
        self.output = np.zeros(output_no)

    def randomize(self):
        self.hidden_weights = np.random.uniform(-5, 5, (self.total_h, self.total_i+1))
        self.output_weights = np.random.uniform(-5, 5, (self.total_o, self.total_h+1))

    def save(self, filename):
        # input_no, hidden_no, output_no
        # learning rate
        # self.hidden_weights
        # self.output_weights
        with open(filename, 'w') as f:
            f.write(f'{self.total_i} {self.total_h} {self.total_o}\n')
            f.write(f'{self.learning_rate}\n')

            text = np.array2string(self.hidden_weights, separator=",", max_line_width=np.inf, threshold=np.inf)
            text = re.sub(r'\n', '', text)
            f.write(f'{text}\n')

            text = np.array2string(self.output_weights, separator=",", max_line_width=np.inf, threshold=np.inf)
            text = re.sub(r'\n', '', text)
            f.write(f'{text}\n')
    
    @staticmethod
    def laodFromFile(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            lines = list(map(lambda l : l.strip(), lines))
            
            i, h, o = map(lambda n : int(n), lines[0].split(' '))
            
            lr = float(lines[1])
            hidden_weights = np.array(eval(lines[2]))
            out_weights = np.array(eval(lines[3]))

        brain = NeuralNetwork(i, h, o)
        brain.learning_rate = lr
        brain.hidden_weights = hidden_weights
        brain.output_weights = out_weights

        return brain
        

    def summary(self):
        print()
        print('*'*65)
        print(f'Input Node - {self.total_i} | Hidden Node - {self.total_h} | Output Node - {self.total_o}')
        print(f'Learning rate - {self.learning_rate}')
        print('-'*20, 'Matrix Structure', '-'*20)
        print('row -> output | column -> input')
        print('•'*20, 'Hidden Layer Weight', '•'*20)
        print(to_string(self.hidden_weights, 4))
        print('•'*20, 'Output Layer Weight', '•'*20)
        print(to_string(self.output_weights, 4))
        print()

    def think(self, inputs):
        self.__inputs[1:] = inputs
       
        hidden_out = self.hidden_weights @ self.__inputs
        self.__output_input[1:] = self.__activator(hidden_out)
        output = self.output_weights @ self.__output_input
        self.output = self.__activator(output)

        return self.output
    
    def train(self, inputs, targets):
        output = self.think(inputs)
        err = np.subtract(targets, output)

        # claculating the hidden error
        weight_matrix = self.output_weights.T[1:,]
        hidden_err = weight_matrix @ err


        # calculating the dERROR to callibrate the output weight matrix
        # the error1 * result1 * (1-result1)
        # a (n,1) matrix 
        error_gradiant = err * self.__yderivative(output)
        error_gradiant_matrix = error_gradiant.reshape((self.total_o, 1))
        # converting the inputs into (1,m) matrix
        input_matrix = self.__output_input.reshape((1, self.total_h+1))
        # calculates the weight changes
        dWeights = error_gradiant_matrix @ input_matrix
        dWeights *= self.learning_rate
        # adding weight changes to callibrate previous
        self.output_weights += dWeights

        # calculating the dERROR to callibrate the hidden weight matrix
        error_gradiant = hidden_err * self.__yderivative(self.__output_input[1:])
        error_gradiant_matrix = error_gradiant.reshape((self.total_h, 1))
        input_matrix = self.__inputs.reshape((1, self.total_i+1))
        dWeights = error_gradiant_matrix @ input_matrix
        dWeights *= self.learning_rate
        self.hidden_weights += dWeights


        
class NeuralNetwork2H:
    def __init__(self, input_no, hiddenI_no, hiddenO_no, output_no) -> None:
        self.total_i = input_no
        self.total_ih = hiddenI_no
        self.total_oh = hiddenO_no
        self.total_o = output_no
        # self.input_weights = np.zeros((input_no+1, 1))
        self.hiddenI_weights = np.zeros((hiddenI_no, input_no+1))
        self.hiddenO_weights = np.zeros((hiddenO_no, hiddenI_no+1))
        self.output_weights = np.zeros((output_no, hiddenO_no+1))
        self.learning_rate = 0.5

        self.__activator = sigmoid
        self.__yderivative = dsigmoid
        
        # personal thing
        self.__inputs = np.zeros(input_no+1)
        self.__hiddenI_out = np.zeros(hiddenI_no+1)
        self.__hiddenO_out = np.zeros(hiddenO_no+1)
        self.__inputs[0] = 1
        self.__hiddenI_out[0] = 1
        self.__hiddenO_out[0] = 1
        
        self.output = np.zeros(output_no)

    def randomize(self):
        self.hiddenI_weights = np.random.uniform(0, 1, (self.total_ih, self.total_i+1))
        self.hiddenO_weights = np.random.uniform(0, 1, (self.total_oh, self.total_ih+1))
        self.output_weights = np.random.uniform(0, 1, (self.total_o, self.total_oh+1))
    
    def summary(self):
        print()
        print('*'*65)
        print(f'Input Node - {self.total_i} | Output Node - {self.total_o}')
        print(f'Hidden Node 1st Layer- {self.total_ih} | Hidden Node 2nd Layer- {self.total_oh}')
        print(f'Learning rate - {self.learning_rate}')
        print('-'*20, 'Matrix Structure', '-'*20)
        print('row -> output | column -> input')
        print('•'*18, 'Hidden 1st Layer Weight', '•'*18)
        print(to_string(self.hiddenI_weights, 4))
        print('•'*18, 'Hidden 2nd Layer Weight', '•'*18)
        print(to_string(self.hiddenO_weights, 4))
        print('•'*18, 'Output Layer Weight', '•'*18)
        print(to_string(self.output_weights, 4))
        print()

    def think(self, inputs):
        self.__inputs[1:] = inputs
       
        hidden_out = self.hiddenI_weights @ self.__inputs
        self.__hiddenI_out[1:] = self.__activator(hidden_out)

        hidden_out = self.hiddenO_weights @ self.__hiddenI_out
        self.__hiddenO_out[1:] = self.__activator(hidden_out)

        output = self.output_weights @ self.__hiddenO_out
        self.output = self.__activator(output)

        return self.output
    
    def train(self, inputs, targets):
        output = self.think(inputs)
        err = np.subtract(targets, output)

        # claculating the hiddenO error
        weight_matrix = self.output_weights.T[1:,]
        hiddenO_err = weight_matrix @ err

        # claculating the hiddenI error
        weight_matrix = self.hiddenO_weights.T[1:,]
        hiddenI_err = weight_matrix @ hiddenO_err


        # calculating the dERROR to callibrate the output weight matrix
        # the error1 * result1 * (1-result1)
        # a (n,1) matrix 
        error_gradiant = err * self.__yderivative(output)
        error_gradiant_matrix = error_gradiant.reshape((self.total_o, 1))
        # converting the inputs into (1,m) matrix
        input_matrix = self.__hiddenO_out.reshape((1, self.total_oh+1))
        # calculates the weight changes
        dWeights = error_gradiant_matrix @ input_matrix
        dWeights *= self.learning_rate
        # adding weight changes to callibrate previous
        self.output_weights += dWeights

        # calculating the dERROR to callibrate the hiddenO weight matrix
        error_gradiant = hiddenO_err * self.__yderivative(self.__hiddenO_out[1:])
        error_gradiant_matrix = error_gradiant.reshape((self.total_oh, 1))
        input_matrix = self.__hiddenI_out.reshape((1, self.total_ih+1))
        dWeights = error_gradiant_matrix @ input_matrix
        dWeights *= self.learning_rate
        self.hiddenO_weights += dWeights

        # calculating the dERROR to callibrate the hiddenI weight matrix
        error_gradiant = hiddenI_err * self.__yderivative(self.__hiddenI_out[1:])
        error_gradiant_matrix = error_gradiant.reshape((self.total_ih, 1))
        input_matrix = self.__inputs.reshape((1, self.total_i+1))
        dWeights = error_gradiant_matrix @ input_matrix
        dWeights *= self.learning_rate
        self.hiddenI_weights += dWeights














