import numpy as np
def sigmoid(x):
    sigm = 1. / (1. + np.exp(-x))
    return sigm

def sigmoid_derivative(x):
    return sigmoid(x) * (1. - sigmoid(x))

class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1],4) 
        self.weights2   = np.random.rand(4,1)                 
        self.y          = y
        self.output     = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def test(self, x_test):
        self.layer1 = sigmoid(np.dot(x_test, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))
        print(self.output) 

X=np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
Y=np.array([[0],[1],[1],[0]])

nn=NeuralNetwork(X,Y)
for i in range(1500):
    nn.feedforward()
    nn.backprop()

X_test=np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
nn.test(X_test)
