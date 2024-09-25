import random
from Sequential_Network import sequential_network
import numpy as np

def crossover_layer(x, y, mutation):

    num_weights = len(x.weights)
    num_biasese = len(x.biases)

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_weights)

    for w in range(num_weights):
        if (rand[b] > 0.5):
           temp = x.weights[w]
           x.weights[w] = y.weights[w]
           y.weights[w] = temp

        x.weights[w] += mutations[w]
        y.weights[w] += mutations[w + num_biasese]

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_biasese)

    for b in range(num_biasese):
        if (rand[b] > 0.5):
           temp = x.biases[b]
           x.biases[b] = y.biases[b]
           y.biases[b] = temp

        x.biases[b] += mutations[b]
        y.biases[b] += mutations[b + num_biasese]

def crossover(a, b, mutation):

    for i in range(len(a.layers)):

        crossover_layer(a.layers[i], b.layers[i], mutation)

class game_network:

    def __init__(self, seed):

        np.random.seed(seed)

        num_pigs = 2
        num_pig_vars = 2 

        hidden_layer_size = 2

        network = sequential_network()
        network.dense(num_pigs * num_pig_vars, 1, hidden_layer_size, 1)
        #network.dense(hidden_layer_size, 1, hidden_layer_size, 1)
        #network.dense(hidden_layer_size, 1, 2, 1)

        self.network = network

    def move(self, level_input):        

        input = np.array(level_input)
        move = self.network.feed_forward(input, len(input), 1).activations

        x_range = [100, 250]
        y_range = [370, 550]
        move = [x_range[0] + (move[0] * (x_range[1] - x_range[0])), y_range[0] + (move[1] * (y_range[1] - y_range[0]))]

        return move


