import os 
import sys
import math
import time
#import pygame
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level
import numpy as np
from Util import *

pygame.init()
screen = pygame.display.set_mode((1200, 650))

PLAY = 0
PAUSED = 1
FAILED = 3
COMPLETED = 4

redbird =     pygame.image.load("estevaofon/resources/images/red-bird3.png").convert_alpha()
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
    game_state = PLAY
    bonus_score_once = True

    t1 = 0
    angle = 0
    x_mouse = 0
    y_mouse = 0
    sling_pressed = False
    sling_released = False
    mouse_pressed = False
    mouse_released = False
    mouse_distance = 0

    hiscore = -9999

    def __init__(self, start_level):
        self.level = Level()
        self.level.number = start_level
        self.level.load_level()

        self.game_state = PLAY
        self.bird_path = []
        self.counter = 0
        self.restart_counter = True

    def restart(self, start_score = 0):
        self.game_state = PLAY
        self.bonus_score_once = True
        self.bird_path = []

        pigs_to_remove = []
        birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []

        self.level.load_level()
        self.level.score = start_score

    def pigs_moving(self):
        eps = 1.0

        for pig in self.level.pigs:
            if abs(pig.body.velocity.x) > eps or abs(pig.body.velocity.y) > eps:
                return True

        return False

    def update_sling(self):
        self.mouse_distance = distance(sling_x, sling_y, self.x_mouse, self.y_mouse)

        if self.mouse_distance <= rope_length:
            self.mouse_distance += 10

        # Angle of impulse
        dy = self.y_mouse - sling_y
        dx = self.x_mouse - sling_x
        if dx == 0:
            dx = 0.00000000000001
        self.angle = math.atan((float(dy)) / dx)

    def draw_sling(self):
        v = vector((sling_x, sling_y), (self.x_mouse, self.y_mouse))
        uv = unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]
        pu = (uv1 * rope_length + sling_x, uv2 * rope_length + sling_y)
        bigger_rope = 102
        x_redbird = self.x_mouse - 20
        y_redbird = self.y_mouse - 20

        if self.mouse_distance > rope_length:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = pux, puy
            screen.blit(redbird, pul)
            pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
            pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
            screen.blit(redbird, pul)
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)

        else:
            pu3 = (uv1 * self.mouse_distance + sling_x, uv2 * self.mouse_distance + sling_y)
            pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
            screen.blit(redbird, (x_redbird, y_redbird))
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)

    def release_bird(self):

        self.sling_pressed = False
        if self.level.number_of_birds > 0:
            self.level.number_of_birds -= 1
            self.t1 = time.time() * 1000
            xo = 154
            yo = 156

            if self.mouse_distance > rope_length:
                self.mouse_distance = rope_length

            if self.x_mouse < sling_x + 5:
                bird = Bird(self.mouse_distance, self.angle, xo, yo, self.level.space)
                self.level.birds.append(bird)

            else:
                self.level.score = -1
                bird = Bird(-self.mouse_distance, self.angle, xo, yo, self.level.space)
                self.level.birds.append(bird)

            if self.level.number_of_birds == 0:
                self.t2 = time.time()


    def process_event(self, event):

        self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
        x_valid = (self.x_mouse > 0 and self.x_mouse < 450)
        y_valid = (self.y_mouse > 170 and self.y_mouse < 650)
        pygame_mouse_pressed = pygame.mouse.get_pressed()[0]
        pygame_mouse_up = (event.type == pygame.MOUSEBUTTONUP and event.button == 1)

        self.sling_released = (self.sling_pressed and pygame_mouse_up)

        self.sling_pressed = (pygame_mouse_pressed and x_valid and y_valid)

        self.mouse_released = (self.mouse_pressed and pygame_mouse_up)

        self.mouse_pressed = pygame_mouse_pressed

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Pause button
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (self.x_mouse < 60 and self.y_mouse < 155 and self.y_mouse > 90):
                self.game_state = PAUSED

    def launch_bird(self, ai_launch_bird, ai_move):

        if self.game_state != PLAY:
            return

        if ai_launch_bird:
            self.x_mouse, self.y_mouse = [float(ai_move[0]), float(ai_move[1])]

        self.update_sling()

        if (ai_launch_bird or self.sling_released):
            self.release_bird()

    def process_game_state(self):

        if self.level.score > self.hiscore:
            self.hiscore = self.level.score

        if self.level.number_of_birds <= 0 and len(self.level.pigs) > 0:
            self.game_state = FAILED

        if self.level.number_of_birds >= 0 and len(self.level.pigs) == 0:
            self.game_state = COMPLETED
            if self.bonus_score_once:
                self.level.score += ((self.level.number_of_birds - 1) * 10000)

            self.bonus_score_once = False

        if (self.mouse_released):
            if self.game_state == PAUSED:
                if self.x_mouse > 500 and self.y_mouse > 200 and self.y_mouse < 300:
                    # Resume in the paused screen
                    self.game_state = PLAY

                if self.x_mouse > 500 and self.y_mouse > 300:
                    # Restart in the paused screen
                    restart()

            if self.game_state == FAILED:
                if self.x_mouse > 500 and self.x_mouse < 620 and self.y_mouse > 450:
                    restart()

            if self.game_state == COMPLETED:
                # Build next level
                if self.x_mouse > 610 and self.y_mouse > 450:
                    self.restart()
                    self.level.number += 1
                    self.game_state = PLAY
                    self.level.load_level()
                    self.bird_path = []
                    self.bonus_score_once = True

                if self.x_mouse < 610 and self.x_mouse > 500 and self.y_mouse > 450:
                    # Restart in the level cleared screen
                    self.restart()
                    self.level.load_level()
                    self.game_state = PLAY
                    self.bird_path = []

    def draw_level_cleared(self):
        level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
        score_level_cleared = bold_font2.render(str(self.level.score), 1, WHITE)

        if self.level.number_of_birds >= 0 and len(self.level.pigs) == 0:
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(screen, BLACK, rect)
            screen.blit(level_cleared, (450, 90))
            if self.level.score >= self.level.one_star and self.level.score <= self.level.two_star:
                screen.blit(star1, (310, 190))

            if self.level.score >= self.level.two_star and self.level.score <= self.level.three_star:
                screen.blit(star1, (310, 190))
                screen.blit(star2, (500, 170))

            if self.level.score >= self.level.three_star:
                screen.blit(star1, (310, 190))
                screen.blit(star2, (500, 170))
                screen.blit(star3, (700, 200))

            screen.blit(score_level_cleared, (550, 400))
            screen.blit(replay_button, (510, 480))
            screen.blit(next_button, (620, 480))

    def draw_level_failed(self, game_state):
        failed = bold_font3.render("Level Failed", 1, WHITE)

        if self.level.number_of_birds <= 0 and time.time() - self.t2 > 5 and len(self.level.pigs) > 0:
            rect = pygame.Rect(300, 0, 600, 800)
            draw_rect(screen, BLACK, rect)
            screen.blit(failed, (450, 90))
            screen.blit(pig_happy, (380, 120))
            screen.blit(replay_button, (520, 460))

    def draw(self, use_ai):
        screen.fill((130, 200, 100))
        screen.blit(background2, (0, -50))

        # Draw first part of the sling
        rect = pygame.Rect(50, 0, 70, 220)
        screen.blit(sling_image, (138, 420), rect)

        # Draw the trail left behind
        for point in self.bird_path:
            pygame.draw.circle(screen, WHITE, point, 5, 0)

        # Draw the birds in the wait line
        if self.level.number_of_birds > 0:
            for i in range(self.level.number_of_birds - 1):
                x = 100 - (i * 35)
                screen.blit(redbird, (x, 508))

        # Draw sling behavior
        if (use_ai or self.sling_pressed) and self.level.number_of_birds > 0:
            self.draw_sling()
        else:
            if time.time() * 1000 - self.t1 > 300 and self.level.number_of_birds > 0:
                screen.blit(redbird, (130, 426))
            else:
                pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y - 8), (sling2_x, sling2_y - 7), 5)

        # Draw birds
        for bird in self.level.birds:
            p = to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            screen.blit(redbird, (x, y))
            pygame.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2)

            if self.counter >= 3 and time.time() - self.t1 < 5:
                self.bird_path.append(p)
                self.restart_counter = True
        self.counter += 1

        if self.restart_counter:
            self.counter = 0
            self.restart_counter = False

        self.level.draw_level(screen)

        # Drawing second part of the sling
        rect = pygame.Rect(0, 0, 60, 200)
        screen.blit(sling_image, (120, 420), rect)

        score_font = bold_font.render("SCORE", 1, WHITE)
        number_font = bold_font.render(str(self.level.score), 1, WHITE)
        screen.blit(score_font, (1060, 90))

        if self.level.score == 0:
            screen.blit(number_font, (1100, 130))
        else:
            screen.blit(number_font, (1060, 130))

        score_font = bold_font.render("HISCORE", 1, WHITE)
        number_font = bold_font.render(str(self.hiscore), 1, WHITE)
        screen.blit(score_font, (1060, 20))
        screen.blit(number_font, (1060, 50))

        if self.game_state == PAUSED:
            screen.blit(play_button, (500, 200))
            screen.blit(replay_button, (500, 300))

        self.draw_level_cleared()
        self.draw_level_failed(self.game_state)

        screen.blit(pause_button, (10, 90))

    def update_physics(self):
        dt = 1.0 / 50.0 / 2.
        for x in range(2):
            self.level.space.step(dt) # make two updates per frame for better stability

    def remove_offscreen_pigs(self):
        pigs_to_remove = []
        for pig in self.level.pigs:
            offscreen = (pig.body.position.x > screen_x or pig.body.position.x < 0)
            if offscreen:
                pigs_to_remove.append(pig)

        for pig in pigs_to_remove:
            self.level.space.remove(pig.shape, pig.shape.body)
            self.level.pigs.remove(pig)