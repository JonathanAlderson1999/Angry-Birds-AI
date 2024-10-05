import os 
import sys
import math
import time
#import pygame
current_path = os.getcwd()
import pymunk as pm
from Characters import Bird
from level import Level
import numpy as np
from Util import *

pygame.init()
screen = pygame.display.set_mode((1200, 650))

redbird =     pygame.image.load("C:\\Users\\light\\source\\repos\\Angry Birds AI\\estevaofon\\resources\\images\\red-bird3.png").convert_alpha()
background2 = pygame.image.load("estevaofon/resources/images/background3.png").convert_alpha()
sling_image = pygame.image.load("estevaofon/resources/images/sling-3.png").convert_alpha()
buttons =     pygame.image.load("estevaofon/resources/images/selected-buttons.png").convert_alpha()
pig_happy =   pygame.image.load("estevaofon/resources/images/pig_failed.png").convert_alpha()
stars =       pygame.image.load("estevaofon/resources/images/stars-edited.png").convert_alpha()

star1 =           stars.subsurface(pygame.Rect(0,   0,    200, 200)).copy()
star2 =           stars.subsurface(pygame.Rect(204, 0,    200, 200)).copy()
star3 =           stars.subsurface(pygame.Rect(426, 0,    200, 200)).copy()
pause_button =  buttons.subsurface(pygame.Rect(164, 10,   60,  60 )).copy()
replay_button = buttons.subsurface(pygame.Rect(24,  4,    100, 100)).copy()
next_button =   buttons.subsurface(pygame.Rect(142, 365,  130, 100)).copy()
play_button =   buttons.subsurface(pygame.Rect(18,  212,  100, 100)).copy()

bold_font =  pygame.font.SysFont("arial", 30, bold = True)
bold_font2 = pygame.font.SysFont("arial", 40, bold = True)
bold_font3 = pygame.font.SysFont("arial", 50, bold = True)

sling_x,  sling_y  = 135, 450
sling2_x, sling2_y = 160, 450
rope_length = 90

clock = pygame.time.Clock()

running = True
restart_counter = False
wall = False

def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)

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
    game_state = 0
    bonus_score_once = 0

    t1 = 0
    angle = 0
    x_mouse = 0
    y_mouse = 0
    mouse_pressed = False
    released_mouse = False
    mouse_distance = 0

    def __init__(self):
        self.level = Level()
        self.level.number = 0
        self.level.load_level()

        self.game_state = 0
        self.bird_path = []
        self.counter = 0
        self.restart_counter = True

    def restart(self):
        self.game_state = 0
        self.game_state = 0
        self.bird_path = []

        pigs_to_remove = []
        birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []

        self.level.load_level()

    def sling_action(self):
        v = vector((sling_x, sling_y), (self.x_mouse, self.y_mouse))
        uv = unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]
        self.mouse_distance = distance(sling_x, sling_y, self.x_mouse, self.y_mouse)
        pu = (uv1 * rope_length + sling_x, uv2 * rope_length + sling_y)
        bigger_rope = 102
        x_redbird = self.x_mouse - 20
        y_redbird = self.y_mouse - 20

        if self.mouse_distance > rope_length:
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
            self.mouse_distance += 10
            pu3 = (uv1 * self.mouse_distance + sling_x, uv2 * self.mouse_distance + sling_y)
            pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
            debug_blit(redbird, (x_redbird, y_redbird))
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)

        # Angle of impulse
        dy = self.y_mouse - sling_y
        dx = self.x_mouse - sling_x
        if dx == 0:
            dx = 0.00000000000001
        self.angle = math.atan((float(dy)) / dx)

    def release_bird(self):
        self.mouse_pressed = False
        if self.level.number_of_birds > 0:
            #level.number_of_birds -= 1 # unlimited for testing
            self.t1 = time.time() * 1000
            xo = 154
            yo = 156

            if self.mouse_distance > rope_length:
                self.mouse_distance = rope_length

            if self.x_mouse < sling_x + 5:
                bird = Bird(self.mouse_distance, self.angle, xo, yo, self.level.space)
                self.level.birds.append(bird)

            else:
                bird = Bird(-self.mouse_distance, self.angle, xo, yo, self.level.space)
                self.level.birds.append(bird)

            if self.level.number_of_birds == 0:
                self.t2 = time.time()


    def process_event(self, event):
        self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
        x_valid = (self.x_mouse > 100 and self.x_mouse < 250)
        y_valid = (self.y_mouse > 370 and self.y_mouse < 550)
        if (pygame.mouse.get_pressed()[0] and x_valid and y_valid):
            self.mouse_pressed = True

        if self.mouse_pressed and (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            self.released_mouse = True
        else:
            self.released_mouse = False

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Pause button
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (self.x_mouse < 60 and self.y_mouse < 155 and self.y_mouse > 90):
                self.game_state = 1

    def launch_bird(self, ai_launch_bird, ai_move):

        if ai_launch_bird:
                self.x_mouse, self.y_mouse = [float(ai_move[0]), float(ai_move[1])]

        if (ai_launch_bird or self.released_mouse):
            self.release_bird()
            print("AI Move: ", str(self.x_mouse), " ", str(self.y_mouse))

            if self.game_state == 1:
                if self.x_mouse > 500 and self.y_mouse > 200 and self.y_mouse < 300:
                    # Resume in the paused screen
                    self.game_state = 0

                if self.x_mouse > 500 and self.y_mouse > 300:
                    # Restart in the paused screen
                    restart()

            if self.game_state == 3:
                # Restart in the failed level screen
                if self.x_mouse > 500 and self.x_mouse < 620 and self.y_mouse > 450:
                    restart()

            if self.game_state == 4:
                # Build next level
                if self.x_mouse > 610 and self.y_mouse > 450:
                    restart()
                    self.level.number += 1
                    self.game_state = 0
                    self.level.load_level()
                    reset_score()
                    self.bird_path = []
                    self.bonus_score_once = True

                if self.x_mouse < 610 and self.x_mouse > 500 and self.y_mouse > 450:
                    # Restart in the level cleared screen
                    restart()
                    self.level.load_level()
                    self.game_state = 0
                    self.bird_path = []
                    reset_score()

    def draw_level_cleared(self):
        level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
        score_level_cleared = bold_font2.render(str(self.level.score), 1, WHITE)

        if self.level.number_of_birds >= 0 and len(self.level.pigs) == 0:
            if self.bonus_score_once:
                self.level.score += (self.level.number_of_birds - 1) * 10000

            self.bonus_score_once = False
            self.game_state = 4
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(screen, BLACK, rect)
            debug_blit(level_cleared, (450, 90))
            if self.level.score >= self.level.one_star and self.level.score <= self.level.two_star:
                debug_blit(star1, (310, 190))

            if self.level.score >= self.level.two_star and self.level.score <= self.level.three_star:
                debug_blit(star1, (310, 190))
                debug_blit(star2, (500, 170))

            if self.level.score >= self.level.three_star:
                debug_blit(star1, (310, 190))
                debug_blit(star2, (500, 170))
                debug_blit(star3, (700, 200))

            debug_blit(score_level_cleared, (550, 400))
            debug_blit(replay_button, (510, 480))
            debug_blit(next_button, (620, 480))

    def draw_level_failed(self, game_state):
        failed = bold_font3.render("Level Failed", 1, WHITE)

        if self.level.number_of_birds <= 0 and time.time() - self.t2 > 5 and len(self.level.pigs) > 0:
            self.game_state = 3
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(screen, BLACK, rect)
            debug_blit(failed, (450, 90))
            debug_blit(pig_happy, (380, 120))
            debug_blit(replay_button, (520, 460))

    def draw(self, use_ai):
        screen.fill((130, 200, 100))
        debug_blit(background2, (0, -50))

        # Draw first part of the sling
        rect = pygame.Rect(50, 0, 70, 220)
        debug_blit(sling_image, (138, 420), rect)

        # Draw the trail left behind
        for point in self.bird_path:
            pygame.draw.circle(screen, WHITE, point, 5, 0)

        # Draw the birds in the wait line
        if self.level.number_of_birds > 0:
            for i in range(self.level.number_of_birds - 1):
                x = 100 - (i * 35)
                debug_blit(redbird, (x, 508))

        # Draw sling behavior
        if (use_ai or self.mouse_pressed) and self.level.number_of_birds > 0:
            self.sling_action()
        else:
            if time.time() * 1000 - self.t1 > 300 and self.level.number_of_birds > 0:
                debug_blit(redbird, (130, 426))
            else:
                pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y - 8), (sling2_x, sling2_y - 7), 5)

        # Draw birds
        birds_to_remove = []
        pigs_to_remove = []
        for bird in self.level.birds:
            if bird.shape.body.position.y < 0:
                birds_to_remove.append(bird)
            p = to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            debug_blit(redbird, (x, y))
            pygame.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2)

            if self.counter >= 3 and time.time() - self.t1 < 5:
                self.bird_path.append(p)
                self.restart_counter = True
        self.counter += 1

        if self.restart_counter:
            self.counter = 0
            self.restart_counter = False

        # Remove birds and pigs
        for bird in birds_to_remove:
            self.level.space.remove(bird.shape, bird.shape.body)
            self.level.birds.remove(bird)
        for pig in pigs_to_remove:
            self.level.space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)

        self.level.draw_level(screen)

        # Drawing second part of the sling
        rect = pygame.Rect(0, 0, 60, 200)
        debug_blit(sling_image, (120, 420), rect)

        # Draw self.score
        score_font = bold_font.render("SCORE", 1, WHITE)
        number_font = bold_font.render(str(self.level.score), 1, WHITE)
        debug_blit(score_font, (1060, 90))

        if self.level.score == 0:
            debug_blit(number_font, (1100, 130))
        else:
            debug_blit(number_font, (1060, 130))

        # Pause option
        if self.game_state == 1:
            debug_blit(play_button, (500, 200))
            debug_blit(replay_button, (500, 300))

        self.draw_level_cleared()
        self.draw_level_failed(self.game_state)

        debug_blit(pause_button, (10, 90))

    def update_physics(self):
        dt = 1.0 / 50.0 / 2.
        for x in range(2):
            self.level.space.step(dt) # make two updates per frame for better stability