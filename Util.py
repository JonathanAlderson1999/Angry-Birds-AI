import pymunk as pm
from pymunk import Vec2d
import math
    
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

RED =   (255, 0,   0)
BLUE =  (0,   0,   255)
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((1200, 650))

render = True
def turn_off_rendering():
    global render
    render = False

def debug_blit(image, pos, rect = None):
    if render:
        screen.blit(image, pos, rect)

def debug_draw_rect(screen, colour, rect):
    if render:
        pygame.draw.rect(screen, colour, rect)

def debug_draw_line(screen, colour, p1, p2, width = 1):
    if render:
        pygame.draw.line(screen, colour, p1, p2, width)

def debug_draw_circle(screen, colour, center, radius, width):
    if render:
        pygame.draw.circle(screen, colour, center, radius, width)

class Polygon():
    def __init__(self, pos, length, height, space, mass=5.0):
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape
        wood = pygame.image.load("estevaofon/resources/images/wood.png").convert_alpha()
        wood2 = pygame.image.load("estevaofon/resources/images/wood2.png").convert_alpha()
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = wood.subsurface(rect).copy()
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = wood2.subsurface(rect).copy()

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+600)

    def draw_poly(self, element, screen):
        """Draw beams and columns"""

        if not render:
            return

        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        color = (255, 0, 0)
        debug_draw_line(screen, color, False, ps)

        if element == 'beams':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.beam_image, angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            debug_blit(rotated_logo_img, (np.x, np.y))

        if element == 'columns':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image, angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            debug_blit(rotated_logo_img, (np.x, np.y))
