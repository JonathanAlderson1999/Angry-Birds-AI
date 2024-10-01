import os 
import sys
import math
import time
import pygame
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1200, 650))
rect = 

star1 =           stars.subsurface(pygame.Rect(0,   0,    200, 200)).copy()
star2 =           stars.subsurface(pygame.Rect(204, 0,    200, 200)).copy()
star3 =           stars.subsurface(pygame.Rect(426, 0,    200, 200)).copy()
pause_button =  buttons.subsurface(pygame.Rect(164, 10,   60,  60 )).copy()
replay_button = buttons.subsurface(pygame.Rect(24,  4,    100, 100)).copy()
next_button =   buttons.subsurface(pygame.Rect(142, 365,  130, 100)).copy()
cropped =   full_sprite.subsurface(pygame.Rect(181, 1050, 50,  50 )).copy()

clock = pygame.time.Clock()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()

redbird =     pygame.image.load("C:\\Users\\light\\source\\repos\\Angry Birds AI\\fork-estevaofon\\resources\\images\\red-bird3.png").convert_alpha()
background2 = pygame.image.load("fork-estevaofon/resources/images/background3.png").convert_alpha()
sling_image = pygame.image.load("fork-estevaofon/resources/images/sling-3.png").convert_alpha()
full_sprite = pygame.image.load("fork-estevaofon/resources/images/full-sprite.png").convert_alpha()
buttons =     pygame.image.load("fork-estevaofon/resources/images/selected-buttons.png").convert_alpha()
pig_happy =   pygame.image.load("fork-estevaofon/resources/images/pig_failed.png").convert_alpha()
stars =       pygame.image.load("fork-estevaofon/resources/images/stars-edited.png").convert_alpha()

pig_image =   pygame.transform.scale(cropped, (30, 30))

bold_font =  pygame.font.SysFont("arial", 30, bold = True)
bold_font2 = pygame.font.SysFont("arial", 40, bold = True)
bold_font3 = pygame.font.SysFont("arial", 50, bold = True)


running = True
# the base of the physics
space = pm.Space()
space.gravity = (0.0, -700.0)

poly_points = []
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_length = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0
game_state = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
wall = False

# Static floor
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_body)
for line in static_lines:
    space.add(line)

space.add_collision_handler(0, 1).post_solve=post_solve_bird_pig
space.add_collision_handler(0, 2).post_solve=post_solve_bird_wood
space.add_collision_handler(1, 2).post_solve=post_solve_pig_wood
level = Level(pigs, columns, beams, space)
level.number = 0
level.load_level()








def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)
    
def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


class game:

    score = 0
    game_state = 0
    bonus_score_once = 0

    def restart():

        game_state = 0
        game_state = 0
        bird_path = []

        pigs_to_remove = []
        birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []
        for pig in pigs:
            pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)
        for bird in birds:
            birds_to_remove.append(bird)
        for bird in birds_to_remove:
            space.remove(bird.shape, bird.shape.body)
            birds.remove(bird)
        for column in columns:
            columns_to_remove.append(column)
        for column in columns_to_remove:
            space.remove(column.shape, column.shape.body)
            columns.remove(column)
        for beam in beams:
            beams_to_remove.append(beam)
        for beam in beams_to_remove:
            space.remove(beam.shape, beam.shape.body)
            beams.remove(beam)

        level.load_level()

    def sling_action():
        """Set up sling behavior"""
        # Fixing bird to the sling rope
        v = vector((sling_x, sling_y), (x_mouse, y_mouse))
        uv = unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]
        mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
        pu = (uv1*rope_length+sling_x, uv2*rope_length+sling_y)
        bigger_rope = 102
        x_redbird = x_mouse - 20
        y_redbird = y_mouse - 20

        if mouse_distance > rope_length:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = pux, puy
            debug_blit(redbird, pul)
            pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
            pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
            debug_blit(redbird, pul)
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)

        else:
            mouse_distance += 10
            pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
            pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
            debug_blit(redbird, (x_redbird, y_redbird))
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)

        # Angle of impulse
        dy = y_mouse - sling_y
        dx = x_mouse - sling_x
        if dx == 0:
            dx = 0.00000000000001
        angle = math.atan((float(dy))/dx)


    def release_bird():
        mouse_pressed = False
        if level.number_of_birds > 0:
            #level.number_of_birds -= 1 # unlimited for testing
            t1 = time.time() * 1000
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

    def process_event(event, use_ai, ai_launch_bird, ai_move):
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        x_valid = (x_mouse > 100 and x_mouse < 250)
        y_valid = (y_mouse > 370 and y_mouse < 550)
        if (use_ai or (pygame.mouse.get_pressed()[0] and x_valid and y_valid)):
            mouse_pressed = True

        if (ai_launch_bird or (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_pressed)):
            release_bird()

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

            if game_state == 3:
                # Restart in the failed level screen
                if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                    restart()

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

    def post_solve_bird_pig(arbiter, space, _):
        surface=screen
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        p = to_pygame(bird_body.position)
        p2 = to_pygame(pig_body.position)
        r = 30
        pygame.draw.circle(surface, BLACK, p, r, 4)
        pygame.draw.circle(surface, RED, p2, r, 4)

        pigs_to_remove = []
        for pig in pigs:
            if pig_body == pig.body:
                pig.life -= 20
                pigs_to_remove.append(pig)
                global score
                score += 10000
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)

    def post_solve_bird_wood(arbiter, space, _):
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in columns:
                if b == column.shape:
                    poly_to_remove.append(column)

            for beam in beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)

            for poly in poly_to_remove:
                if poly in columns:
                    columns.remove(poly)

                if poly in beams:
                    beams.remove(poly)

            space.remove(b, b.body)
            score += 5000

    def post_solve_pig_wood(arbiter, space, _):
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    global score
                    score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)

    def draw_level_cleared(game_state, bonus_score_once, score):
        """Draw level cleared"""
        level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
        score_level_cleared = bold_font2.render(str(score), 1, WHITE)

        if level.number_of_birds >= 0 and len(pigs) == 0:
            if bonus_score_once:
                score += (level.number_of_birds-1) * 10000

            bonus_score_once = False
            game_state = 4
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(screen, BLACK, rect)
            debug_blit(level_cleared, (450, 90))
            if score >= level.one_star and score <= level.two_star:
                debug_blit(star1, (310, 190))

            if score >= level.two_star and score <= level.three_star:
                debug_blit(star1, (310, 190))
                debug_blit(star2, (500, 170))

            if score >= level.three_star:
                debug_blit(star1, (310, 190))
                debug_blit(star2, (500, 170))
                debug_blit(star3, (700, 200))

            debug_blit(score_level_cleared, (550, 400))
            debug_blit(replay_button, (510, 480))
            debug_blit(next_button, (620, 480))

    def draw_level_failed(game_state):
        failed = bold_font3.render("Level Failed", 1, WHITE)

        if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) > 0:
            game_state = 3
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(screen, BLACK, rect)
            debug_blit(failed, (450, 90))
            debug_blit(pig_happy, (380, 120))
            debug_blit(replay_button, (520, 460))

    def draw():
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
            sling_action()
        else:
            if time.time() * 1000 - t1 > 300 and level.number_of_birds > 0:
                debug_blit(redbird, (130, 426))
            else:
                pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y - 8), (sling2_x, sling2_y - 7), 5)

        # Draw birds
        birds_to_remove = []
        pigs_to_remove = []
        for bird in birds:
            if bird.shape.body.position.y < 0:
                birds_to_remove.append(bird)
            p = to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            debug_blit(redbird, (x, y))
            pygame.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2)

            if counter >= 3 and time.time() - t1 < 5:
                bird_path.append(p)
                restart_counter = True

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

        # Pause option
        if game_state == 1:
            debug_blit(play_button, (500, 200))
            debug_blit(replay_button, (500, 300))

        debug_blit(pause_button, (10, 90))

    def update_physics():
        dt = 1.0 / 50.0 / 2.
        for x in range(2):
            space.step(dt) # make two updates per frame for better stability


    def debug_blit(image, pos, rect = None):
        # todo: faster way of rendering for testing
        screen.blit(image, pos, rect)