import random
from Sequential_Network import sequential_network
import numpy as np

from Util import *
from game import *


x_moves = []
y_moves = []
min_x = 0
max_x = 0
min_y = 0
max_y = 0

class game_network:

    def __init__(self, seed, max_pigs):

        np.random.seed(seed)

        self.max_pigs = max_pigs
        self.num_pig_vars = 3 

        num_input_neurons = self.max_pigs * self.num_pig_vars

        network = sequential_network(num_input_neurons)

        hidden_layer_size = 10

        network.dense(num_input_neurons, 1, hidden_layer_size, 1)

        network.dense(hidden_layer_size, 1, hidden_layer_size, 1)

        network.dense(hidden_layer_size, 1, hidden_layer_size, 1)

        network.dense(hidden_layer_size, 1, 2, 1)

        self.network = network

    def __repr__(self):
        out = self.network.__repr__()
        return out

    def move(self, pig_positions, pig_obstacles):        

        global min_x, max_x, min_y, max_y

        [screen_x, screen_y] = screen.get_size()

        padded_pig_positions = np.concatenate((np.array(pig_positions).flatten(), np.zeros((self.max_pigs - len(pig_positions)) * 2)))

        max_obstables = 5
        padded_pig_obstacles = pig_obstacles + [-max_obstables] * (self.max_pigs - len(pig_obstacles))

        x_values = padded_pig_positions[::2]
        y_values = padded_pig_positions[1::2]

        normalized_x = ((x_values / screen_x) - 0.5) * 2
        normalized_y = ((y_values / screen_y) - 0.5) * 2
        normalised_padded_pig_obstacles = [obstacle_count / max_obstables for obstacle_count in padded_pig_obstacles]

        normalized = np.ravel(np.column_stack((normalized_x, normalized_y, np.array(normalised_padded_pig_obstacles))))

        move = self.network.feed_forward(normalized, len(normalized), 1).activations
        
        #print("move: " +  str(move))
        x_moves.append(move[0])
        y_moves.append(move[1])
        min_x = min(move[0], min_x)
        max_x = max(move[0], max_x)
        
        min_y = min(move[1], min_y)
        max_y = max(move[1], max_y)

        #print(sum(x_moves) / len(x_moves))
        print(min_x, max_x)
        print(min_y, max_y)

        #print(sum(y_moves) / len(y_moves))


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

    offscreen = (game.level.birds[0].body.position.x < 0)
    not_moving = (game.level.birds[-1].body.velocity.x < 2)
    not_scored = (game.level.birds[-1].score == 0)
    
    if offscreen or (not_moving and not_scored):
        return True

    pig_score = 700
    destoryed_pig = (game.level.birds[-1].score >= pig_score)
    if ai_launch_bird and not destoryed_pig:
        return True

    return False
