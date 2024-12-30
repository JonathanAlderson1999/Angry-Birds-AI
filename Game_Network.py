import random
from Sequential_Network import sequential_network
import numpy as np

from Util import *
from game import *

class game_network:

    def __init__(self, seed, max_pigs):

        np.random.seed(seed)

        self.max_pigs = max_pigs
        self.num_pig_vars = 2 

        hidden_layer_size = 2

        num_input_neurons = self.max_pigs * self.num_pig_vars

        network = sequential_network(num_input_neurons)
        network.dense(num_input_neurons, 1, hidden_layer_size, 1, relu = False)
        #network.dense(hidden_layer_size, 1, hidden_layer_size, 1)
        #network.dense(hidden_layer_size, 1, 2, 1)

        self.network = network

    def __repr__(self):
        out = self.network.__repr__()

        # todo: don't hard code
        #show_activation = False
        #if show_activation:
        #    activations = self.move(np.array([980, 72, 974, 178]))
        #    out += "   ".join([str(round(a)) for a in activations])

        return out

    def move(self, pig_positions):        

        [screen_x, screen_y] = screen.get_size()

        padded_pig_positions = np.concatenate((np.array(pig_positions).flatten(), np.zeros((self.max_pigs - len(pig_positions)) * self.num_pig_vars)))

        x_values = padded_pig_positions[::2]
        y_values = padded_pig_positions[1::2]

        normalized_x = ((x_values / screen_x) - 0.5) * 2
        normalized_y = ((y_values / screen_y) - 0.5) * 2

        normalized = np.ravel(np.column_stack((normalized_x, normalized_y)))

        move = self.network.feed_forward(normalized, len(normalized), 1).activations

        # switch from -1, 1 to 0, 1
        move = (move + 1.0) / 2

        x_range = [40, 100]
        y_range = [400, 500]

        move = [x_range[0] + (move[0] * (x_range[1] - x_range[0])), y_range[0] + (move[1] * (y_range[1] - y_range[0]))]

        return move

def should_early_reset(game, ai_launch_bird):

    first_bird_launched = (len(game.level.birds) > 0)
    if not first_bird_launched:
        return False

    completed_level = (game.game_state == COMPLETED)
    offscreen = (game.level.birds[0].body.position.x < 0)
    not_moving = (game.level.birds[-1].body.velocity.x < 2)
    not_scored = (game.level.birds[-1].score == 0)
    
    if completed_level or offscreen or (not_moving and not_scored):
        return True

    pig_score = 5000
    destoryed_pig = (game.level.birds[-1].score >= pig_score)
    if ai_launch_bird and not destoryed_pig:
        return True

    return False
