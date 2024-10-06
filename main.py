import os 
import sys
import math
import time
import pickle
from game import *
current_path = os.getcwd()
import pymunk as pm
from Characters import Bird
from level import Level
from Game_Network import game_network
from Genetic import *
import numpy as np

game = game()

population_size = 10
ai_move_interval = 250
frame_count = ai_move_interval - 2


generation = 0
game_speed = 500

use_ai = True
render_game = False

render_game = render_game or not use_ai
if not render_game:
    turn_off_rendering()
    pygame.display.iconify()

while True:

    ai_id = 0
    best_ai = 0
    ai_scores = []

    population = make_new_population(generation, population_size)
    network = population[0]

    if False:
        for network in population:
            print(network.network.layers[0].biases)
            print(network.network.layers[0].weights)
            print("")

    generation += 1

    while ai_id < population_size:

        frame_count += 1

        # Skip if offscreen to the left
        early_reset = False
        if (len(game.level.birds) > 0):
            early_reset = game.level.birds[0].body.position.x < 0
            early_reset = early_reset or game.level.birds[0].body.velocity.get_length_sqrd() < 0.1

        if early_reset:
            frame_count = ai_move_interval

        ai_launch_bird = use_ai and (frame_count % ai_move_interval == 0)
        if (ai_launch_bird):
            first_time = (game.hiscore == -9999)
            if (not first_time):
                print(str(game.level.score).ljust(5), end = ", ")

            if ai_id == 0:
                print("\nGen: ", str(generation).ljust(5), end = " ")

            if (game.level.score > game.hiscore):
                game.hiscore = game.level.score
                best_ai = ai_id

            ai_scores.append(game.level.score)
            game.restart()
            if (ai_id == population_size):
                continue
            network = population[ai_id]

            ai_id += 1

        for event in (pygame.event.get()):
            if not use_ai:
                game.process_event(event)
                game.launch_bird(False, None)

        if (ai_launch_bird):
            ai_move = network.move(np.array([980, 72, 974, 178]))
            game.launch_bird(ai_launch_bird, ai_move)

        game.draw(use_ai)
        game.update_physics()

        if render_game:
            pygame.display.flip()
            clock.tick(50 * game_speed)
            pygame.display.set_caption("Angry Birds")

    pickle.dump([population, ai_scores], open("Saved_Networks/generation" + str(generation - 1) + ".pickle", "wb"))
