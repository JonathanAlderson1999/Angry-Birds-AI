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
from Game_Network import game_network
from Genetic import *
import numpy as np

population_size = 15
ai_move_interval = 250
frame_count = ai_move_interval - 2

max_pigs = 3
score_reset_threshold = 5000

start_level = 0#8
start_ai = 0
generation = 0
game_speed = 100

use_ai = True
render_game = True

game = game(start_level)

render_game = render_game or not use_ai
if not render_game:
    pygame.display.iconify()

while True:

    ai_id = -1 + start_ai
    best_ai = 0
    ai_scores = [0 for i in range(population_size)]
    game.hiscore = -9999
    game.update_sling()
    game.update_physics()

    population = load_population(generation, population_size, max_pigs)

    while ai_id <= population_size:

        frame_count += 1

        game.update_sling()
        game.update_physics()
        game.process_game_state()

        # Skip if offscreen to the left
        early_reset = False
        if (len(game.level.birds) > 0):
            completed_level = (game.game_state == COMPLETED)
            offscreen = (game.level.birds[0].body.position.x < 0)
            not_moving = (game.level.birds[-1].body.velocity.x < 2)
            not_scored = (game.level.birds[-1].score == 0)
            early_reset = (completed_level or offscreen or (not_moving and not_scored))

        if early_reset:
            frame_count = ai_move_interval
            #print("Early Reset")

        ai_launch_bird = use_ai and (frame_count % ai_move_interval == 0)
        if (ai_launch_bird):

            first_time = (game.hiscore == -9999)
            scored_enough = (len(game.level.birds) > 0) and (game.level.birds[-1].score >= score_reset_threshold)
            has_remaining_birds = (game.level.number_of_birds > 0)
            completed_level = (game.game_state != PLAY)
            continue_playing = (scored_enough and has_remaining_birds and not completed_level)

            if completed_level:
                ai_launch_bird = False

            #if (len(game.level.birds) > 0):
               # print("Bird Score: ", game.level.birds[-1].score)

            if not first_time and not continue_playing:
                print(str(game.level.score).ljust(5), end = ", ")

            if ai_id == -1:
                print("\nGen " + str(generation).ljust(5))

            if game.level.score > game.hiscore:
                game.hiscore = game.level.score
                best_ai = ai_id

            if not continue_playing:
                population_complete = (ai_id == population_size - 1)
                if population_complete:
                    break
                else:
                    ai_scores[ai_id] = game.level.score

                ai_id += 1
                game.restart()
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
            clock.tick(int(60 * game_speed))
            pygame.display.set_caption("Angry Birds - Gen: " + str(generation) + " AI: " + str(ai_id + 1))

    
    generation += 1
    pickle.dump(make_new_population(population, ai_scores), open("Saved_Networks/generation" + str(generation) + ".pickle", "wb"))
