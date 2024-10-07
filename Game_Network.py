import random
from Sequential_Network import sequential_network
import numpy as np

from Util import *

class game_network:

    def __init__(self, seed):

        np.random.seed(seed)

        num_pigs = 2
        num_pig_vars = 2 

        hidden_layer_size = 2

        num_input_neurons = num_pigs * num_pig_vars

        network = sequential_network(num_input_neurons)
        network.dense(num_input_neurons, 1, hidden_layer_size, 1, relu = False)
        #network.dense(hidden_layer_size, 1, hidden_layer_size, 1)
        #network.dense(hidden_layer_size, 1, 2, 1)

        self.network = network

    def __repr__(self):
        out = self.network.__repr__()

        # todo: don't hard code
        show_activation = True
        if show_activation:
            activations = self.move(np.array([980, 72, 974, 178]))
            out += "   ".join([str(round(a)) for a in activations])

        return out

    def move(self, level_input):        

        [screen_x, screen_y] = get_screen_size()

        x_values = level_input[::2]
        y_values = level_input[1::2]

        normalized_x = ((x_values / screen_x) - 0.5) * 2
        normalized_y = ((y_values / screen_y) - 0.5) * 2

        normalized = np.ravel(np.column_stack((normalized_x, normalized_y)))

        move = self.network.feed_forward(normalized, len(normalized), 1).activations

        # switch from -1, 1 to 0, 1
        move = (move + 1.0) / 2

        x_range = [100, 250]
        y_range = [370, 550]
        move = [x_range[0] + (move[0] * (x_range[1] - x_range[0])), y_range[0] + (move[1] * (y_range[1] - y_range[0]))]

        return move


