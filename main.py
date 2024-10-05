import os 
import sys
import math
import time
import pygame
import pickle
from game import *
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level
from Game_Network import game_network
import numpy as np

def normalize_array(a):
    normalized = (a - np.min(a)) / (np.max(a) - np.min(a))
    return normalized

use_ai = True

ai_move_interval = 250
frame_count = ai_move_interval - 2
ai_id = 0
high_score = 0
best_ai = 0

population = pickle.load( open("Saved_Networks/generation1.pickle", "rb"))
network = population[0]

game = game()

while running:

    frame_count += 1

    # Skip if offscreen to the left
    early_reset = False
    if (len(game.level.birds) > 0):
        early_reset = birds[0].body.position.x < 0
        early_reset = early_reset or birds[0].body.velocity.get_length_sqrd() < 0.1

    if early_reset:
        frame_count = ai_move_interval

    ai_launch_bird = use_ai and (frame_count % ai_move_interval == 0)
    if (ai_launch_bird):
        score = get_score()
        print(score, end = ", ")
        if (score > high_score):
            high_score = score
            best_ai = ai_id

        game.restart()
        network = population[ai_id]

        ai_id += 1

    ai_move = network.move(normalize_array(np.array([980, 72, 974, 178])))

    # add a fake event so the AI can play
    for event in (pygame.event.get() + [pygame.event.Event(pygame.MOUSEBUTTONDOWN)]):
        game.process_event(event, use_ai, ai_launch_bird, ai_move)

    game.draw()

    counter += 1

    if restart_counter:
        counter = 0
        restart_counter = False

    game.udpate_physics()

    game.draw_level_cleared()
    game.draw_level_failed(game_state)
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
