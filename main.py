import os 
import sys
import math
import time
import pickle
from game import *
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level
from Game_Network import *
from Genetic import *
import numpy as np

population_size = 14
ai_move_interval = 250
frame_count = 0

max_pigs = 3

start_level = 0
start_ai = 0
generation = 0
game_speed = 6

use_ai = True
play_multiple_levels = True
bail_on_failed_level = False
render_game = True

game = game(start_level)

render_game = render_game or not use_ai
if not render_game:
    pygame.display.iconify()

while True:

    ai_id = start_ai
    ai_scores = [0 for i in range(population_size)]
    game.hiscore = -9999
    game.level.number = start_level

    population = load_population(generation, population_size, max_pigs)
    network = population[ai_id]

    print("\nGen " + str(generation).ljust(5))

    while ai_id <= population_size:

        frame_count += 1

        game.update_physics()
        game.process_game_state()
        game.remove_offscreen_pigs()

        level_completed = (game.game_state != PLAY)
        ai_launch_bird = use_ai and (frame_count % ai_move_interval == 0)
        ai_completed = should_early_reset(game, ai_launch_bird) and bail_on_failed_level

        if level_completed and play_multiple_levels:
            frame_count = 0
            ai_launch_bird = True
            game.level.number += 1
            game.restart(game.level.score)

        elif level_completed:
            ai_completed = True

        if ai_completed:

            completed = "+" if level_completed else " "
            status = str(game.level.number) if play_multiple_levels else completed
            print((status + " " + str(game.level.score)).ljust(7), end = ", ")

            ai_scores[ai_id] = game.level.score

            frame_count = 0
            game.level.number = start_level
            game.restart()

            population_complete = (ai_id == population_size - 1)
            if population_complete:
                break
            else:
                ai_id += 1
                network = population[ai_id]

        for event in (pygame.event.get()):
            if not use_ai:
                game.process_event(event)
                game.launch_bird(False, None)

        if ai_launch_bird:
            pig_positions = [[pig.body.position.x, pig.body.position.y] for pig in game.level.pigs]
            ai_move = network.move(pig_positions)
            game.launch_bird(ai_launch_bird, ai_move)

        if render_game:
            game.draw(use_ai)
            pygame.display.flip()
            clock.tick(int(120 * game_speed))
            pygame.display.set_caption("Angry Birds - Gen: " + str(generation) + " AI: " + str(ai_id + 1) + " Level: " + str(game.level.number))

    
    generation += 1
    population = make_new_population(generation, population, ai_scores)
    pickle.dump(population, open("Saved_Networks/generation" + str(generation) + ".pickle", "wb"))
    ai_scores = [0 for i in range(population_size)]
