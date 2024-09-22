import random
from Sequential_Network import sequential_network
import numpy as np

class game_network:

    def __init__(self):

        num_pigs = 2
        num_pig_vars = 2 

        hidden_layer_size = 25

        network = sequential_network()
        network.dense(num_pigs * num_pig_vars, 1, hidden_layer_size, 1)
        network.dense(hidden_layer_size, 1, hidden_layer_size, 1)
        network.dense(hidden_layer_size, 1, 2, 1)

        self.network = network

    def move(self, level_input):        

        input = np.array(level_input)
        move = self.network.feed_forward(input, len(input), 1).activations
        return move


