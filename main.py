import os 
import sys
import math
import time
import pickle
import datetime
from game import *
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level
from Game_Network import *
from Genetic import *
import numpy as np

population_size = 20
ai_move_interval = 250
frame_count = -1

max_pigs = 4

start_level = 0
end_level = 11
start_ai = 0
generation = 0
game_speed = 1

use_ai = True
use_random_network = False
play_multiple_levels = True
bail_on_failed_level = False
render_game = False

game = game(start_level)

date = datetime.datetime.now()
run_id = str(date.year) + "_" + str(date.month) + "_" + str(date.day) + "-" + str(date.hour) + "-" + str(date.minute)
run_dir = "Saved_Networks/" + run_id + "/"

render_game = render_game or not use_ai
if not render_game:
    pygame.display.iconify()

if (len(sys.argv) > 1):
    print("Starting with population size ", sys.argv[1])
    population_size = int(sys.argv[1])

while True:

    ai_id = start_ai
    ai_scores = [0 for i in range(population_size)]
    game.hiscore = -9999
    game.level.number = start_level

    population = load_population(run_dir, generation, population_size, max_pigs)
    network = population[ai_id]
    levels_passed = 0

    print("\nGen " + str(generation).ljust(5))

    while ai_id <= population_size:

        frame_count += 1

        game.update_physics()
        game.process_game_state()
        game.remove_offscreen_pigs()

        level_completed = (game.game_state != PLAY)
        level_passed = (game.game_state == COMPLETED)
        ai_launch_bird = use_ai and (frame_count % ai_move_interval == 0)
        ai_completed = should_early_reset(game, ai_launch_bird) and bail_on_failed_level
        final_level = ai_completed or (game.level.number == end_level)

        if level_completed and play_multiple_levels and not final_level:
            frame_count = -1
            ai_launch_bird = False
            game.level.number += 1
            levels_passed += level_passed
            game.restart(game.level.score)

        elif level_completed:
            ai_completed = True

        if ai_completed:

            if play_multiple_levels:
                print(str(levels_passed) +  " ", end = "")
            else:
                print("+" if level_passed else " ", end = "")
            print(str(game.level.score).ljust(7), end = ", ")

            ai_scores[ai_id] = game.level.score

            levels_passed = 0
            frame_count = -1
            ai_launch_bird = False
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
            owner = "Random: " if use_random_network else "Generation:"
            pygame.display.set_caption("Angry Birds - " + owner + " " + str(generation) + " AI: " + str(ai_id + 1) + " Level: " + str(game.level.number))

    
    generation += 1

    if use_random_network:
        population = [game_network(generation * population_size + i, max_pigs) for i in range(population_size)] 
    else:
        population = make_new_population(generation, population, ai_scores)

    if not os.path.exists(run_dir):
        os.mkdir(run_dir)
    pickle.dump(population, open(run_dir + "generation" + str(generation) + ".pickle", "wb"))
    ai_scores = [0 for i in range(population_size)]


#Python Environments -> Open in powershell

#cd ../../../
#cd 'Users\light\source\repos\Angry Birds AI\'
#python main.py
