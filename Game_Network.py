import random
from Sequential_Network import sequential_network
import numpy as np

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


