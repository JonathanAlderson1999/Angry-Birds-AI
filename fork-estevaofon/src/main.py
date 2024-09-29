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

global x_mouse
global y_mouse

def normalize_array(a):
    normalized = (a - np.min(a)) / (np.max(a) - np.min(a))
    return normalized

use_ai = True

ai_move_interval = 250
frame_count = ai_move_interval - 2
ai_id = 0
high_score = 0
best_ai = 0

population = pickle.load( open("Saved_Networks/generation0.pickle", "rb"))
network = population[0]

while running:

    frame_count += 1

    # Skip if offscreen to the left
    early_reset = False
    if (len(birds) > 0):
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

        restart()
        level.load_level()
        game_state = 0
        bird_path = []
        reset_score()

        network = population[ai_id]

        if (ai_id >= len(population) - 1):
            sys.exit()

        print("new network " + str(ai_id))
        ai_id += 1

    # add a fake event so the AI can play
    for event in (pygame.event.get() + [pygame.event.Event(pygame.MOUSEBUTTONDOWN)]):

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            # Toggle wall
            if wall:
                for line in static_lines1:
                    space.remove(line)
                wall = False
            else:
                for line in static_lines1:
                    space.add(line)
                wall = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            space.gravity = (0.0, -10.0)
            level.bool_space = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            space.gravity = (0.0, -700.0)
            level.bool_space = False
        if (use_ai or (pygame.mouse.get_pressed()[0] and x_mouse > 100 and
                x_mouse < 250 and y_mouse > 370 and y_mouse < 550)):
            mouse_pressed = True
        if (ai_launch_bird or (event.type == pygame.MOUSEBUTTONUP and
                event.button == 1 and mouse_pressed)):
            # Release new bird
            mouse_pressed = False
            if level.number_of_birds > 0:
                #level.number_of_birds -= 1 # unlimited for testing
                t1 = time.time()*1000
                xo = 154
                yo = 156

                if mouse_distance > rope_length:
                    mouse_distance = rope_length
                if x_mouse < sling_x+5:
                    bird = Bird(mouse_distance, angle, xo, yo, space)
                    birds.append(bird)
                else:
                    bird = Bird(-mouse_distance, angle, xo, yo, space)
                    birds.append(bird)
                if level.number_of_birds == 0:
                    t2 = time.time()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (x_mouse < 60 and y_mouse < 155 and y_mouse > 90):
                game_state = 1
            if game_state == 1:
                if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                    # Resume in the paused screen
                    game_state = 0
                if x_mouse > 500 and y_mouse > 300:
                    # Restart in the paused screen
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
            if game_state == 3:
                # Restart in the failed level screen
                if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    reset_score()
            if game_state == 4:
                # Build next level
                if x_mouse > 610 and y_mouse > 450:
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    reset_score()
                    bird_path = []
                    bonus_score_once = True
                if x_mouse < 610 and x_mouse > 500 and y_mouse > 450:
                    # Restart in the level cleared screen
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    reset_score()

    if (use_ai):
        ai_move = network.move(normalize_array(np.array([980, 72, 974, 178])))
        x_mouse, y_mouse = [float(ai_move[0]), float(ai_move[1])]
    else:
        x_mouse, y_mouse = pygame.mouse.get_pos()
    # Draw background
    screen.fill((130, 200, 100))
    debug_blit(background2, (0, -50))
    # Draw first part of the sling
    rect = pygame.Rect(50, 0, 70, 220)
    debug_blit(sling_image, (138, 420), rect)
    # Draw the trail left behind
    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)
    # Draw the birds in the wait line
    if level.number_of_birds > 0:
        for i in range(level.number_of_birds-1):
            x = 100 - (i*35)
            debug_blit(redbird, (x, 508))
    # Draw sling behavior
    if mouse_pressed and level.number_of_birds > 0:
        [mouse_distance, rope_length, angle, x_mouse, y_mouse] = sling_action(mouse_distance, rope_length, angle, x_mouse, y_mouse)
    else:
        if time.time()*1000 - t1 > 300 and level.number_of_birds > 0:
            debug_blit(redbird, (130, 426))
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y-8),
                             (sling2_x, sling2_y-7), 5)
    birds_to_remove = []
    pigs_to_remove = []
    counter += 1
    # Draw birds
    for bird in birds:
        if bird.shape.body.position.y < 0:
            birds_to_remove.append(bird)
        p = to_pygame(bird.shape.body.position)
        x, y = p
        x -= 22
        y -= 20
        debug_blit(redbird, (x, y))
        pygame.draw.circle(screen, BLUE,
                           p, int(bird.shape.radius), 2)
        if counter >= 3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter:
        counter = 0
        restart_counter = False
    # Remove birds and pigs
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    # Draw static lines
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])
    i = 0
    # Draw pigs
    for pig in pigs:
        i += 1
        # print (i,pig.life)
        pig = pig.shape
        if pig.body.position.y < 0:
            pigs_to_remove.append(pig)

        p = to_pygame(pig.body.position)
        x, y = p

        angle_degrees = math.degrees(pig.body.angle)
        img = pygame.transform.rotate(pig_image, angle_degrees)
        w,h = img.get_size()
        x -= w*0.5
        y -= h*0.5
        debug_blit(img, (x, y))
        pygame.draw.circle(screen, BLUE, p, int(pig.radius), 2)
    # Draw columns and Beams
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    # Update physics
    dt = 1.0/50.0/2.
    for x in range(2):
        space.step(dt) # make two updates per frame for better stability
    # Drawing second part of the sling
    rect = pygame.Rect(0, 0, 60, 200)
    debug_blit(sling_image, (120, 420), rect)
    # Draw score
    score_font = bold_font.render("SCORE", 1, WHITE)
    number_font = bold_font.render(str(score), 1, WHITE)
    debug_blit(score_font, (1060, 90))
    if score == 0:
        debug_blit(number_font, (1100, 130))
    else:
        debug_blit(number_font, (1060, 130))
    debug_blit(pause_button, (10, 90))
    # Pause option
    if game_state == 1:
        debug_blit(play_button, (500, 200))
        debug_blit(replay_button, (500, 300))

    [game_state, bonus_score_once, score] = draw_level_cleared(game_state, bonus_score_once, score)
    game_state = draw_level_failed(game_state)
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
