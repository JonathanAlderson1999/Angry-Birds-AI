import math
#import pygame
import pymunk as pm
from Characters import Pig
from Util import *

pygame.init()
screen = pygame.display.set_mode((1200, 650))


full_sprite = pygame.image.load("estevaofon/resources/images/full-sprite.png").convert_alpha()
cropped =   full_sprite.subsurface(pygame.Rect(181, 1050, 50,  50 )).copy()
pig_image = pygame.transform.scale(cropped, (30, 30))


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)

class Level():

    pigs = []
    birds = []
    balls = []
    polys = []
    beams = []
    columns = []

    score = 0

    def __init__(self):
        self.score = 0
        self.number = 0
        self.number_of_birds = 4
        # lower limit
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        self.bool_space = False

        self.setup_space()

    def post_solve_bird_pig(self, arbiter, space, _):
        surface = screen
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        p = to_pygame(bird_body.position)
        p2 = to_pygame(pig_body.position)
        r = 30
        debug_draw_circle(surface, BLACK, p, r, 4)
        debug_draw_circle(surface, RED, p2, r, 4)

        pigs_to_remove = []
        for pig in self.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                pigs_to_remove.append(pig)
                self.score += 10000

        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def post_solve_bird_wood(self, arbiter, space, _):
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in self.columns:
                if b == column.shape:
                    poly_to_remove.append(column)

            for beam in self.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)

            for poly in poly_to_remove:
                if poly in self.columns:
                    self.columns.remove(poly)

                if poly in self.beams:
                    self.beams.remove(poly)

            space.remove(b, b.body)
            self.score += 5000

    def post_solve_pig_wood(self, arbiter, space, _):
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    self.score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def setup_space(self):
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)

        static_body = pm.Body(body_type = pm.Body.STATIC)
        self.static_lines =  [pm.Segment(static_body, (0.0, 060.0),    (1200.0, 60.0),  0.0)]
        static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]

        for line in self.static_lines:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3

        for line in static_lines1:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3

        self.space.add(static_body)

        for line in self.static_lines:
            self.space.add(line)

        self.space.add_collision_handler(0, 1).post_solve=self.post_solve_bird_pig
        self.space.add_collision_handler(0, 2).post_solve=self.post_solve_bird_wood
        self.space.add_collision_handler(1, 2).post_solve=self.post_solve_pig_wood

    def open_flat(self, x, y, n):
        """Create a open flat struture"""
        y0 = y
        for i in range(n):
            y = y0+100+i*100
            p = (x, y)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+60, y)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+30, y+50)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def closed_flat(self, x, y, n):
        """Create a closed flat struture"""
        y0 = y
        for i in range(n):
            y = y0+100+i*125
            p = (x+1, y+22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+60, y+22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+30, y+70)
            self.beams.append(Polygon(p, 85, 20, self.space))
            p = (x+30, y-30)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def horizontal_pile(self, x, y, n):
        """Create a horizontal pile"""
        y += 70
        for i in range(n):
            p = (x, y + i * 20)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def vertical_pile(self, x, y, n):
        """Create a vertical pile"""
        y += 10
        for i in range(n):
            p = (x, y + 85 + i * 85)
            self.columns.append(Polygon(p, 20, 85, self.space))

    def build_0(self):
        """level 0"""
        pig1 = Pig(980, 100, self.space)
        pig2 = Pig(985, 182, self.space)
        self.pigs.append(pig1)
        self.pigs.append(pig2)
        p = (950, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 150)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (950, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 240)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4

        if self.bool_space:
            self.number_of_birds = 8

        self.one_star =   30000
        self.two_star =   40000
        self.three_star = 60000

    def build_1(self):
        """level 1"""
        pig = Pig(1000, 100, self.space)
        self.pigs.append(pig)
        p = (900, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1050, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1105, 210)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_2(self):
        """level 2"""
        pig1 = Pig(880, 180, self.space)
        self.pigs.append(pig1)
        pig2 = Pig(1000, 230, self.space)
        self.pigs.append(pig2)
        p = (880, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (880, 150)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1000, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1000, 180)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1000, 210)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_3(self):
        """level 3"""
        pig = Pig(950, 320, self.space)
        pig.life = 25
        self.pigs.append(pig)
        pig = Pig(885, 225, self.space)
        pig.life = 25
        self.pigs.append(pig)
        pig = Pig(1005, 225, self.space)
        pig.life = 25
        self.pigs.append(pig)
        p = (1100, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1070, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1040, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (920, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (950, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1010, 180)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (860, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (800, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (830, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (890, 180)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (860, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (920, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1040, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (890, 280)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1010, 280)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (950, 300)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (920, 350)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 350)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (950, 400)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_4(self):
        """level 4"""
        pig = Pig(900, 300, self.space)
        self.pigs.append(pig)
        pig = Pig(1000, 500, self.space)
        self.pigs.append(pig)
        pig = Pig(1100, 400, self.space)
        self.pigs.append(pig)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_5(self):
        """level 5"""
        pig = Pig(900, 70, self.space)
        self.pigs.append(pig)
        pig = Pig(1000, 152, self.space)
        self.pigs.append(pig)
        for i in range(9):
            p = (800, 70+i*21)
            self.beams.append(Polygon(p, 85, 20, self.space))
        for i in range(4):
            p = (1000, 70+i*21)
            self.beams.append(Polygon(p, 85, 20, self.space))
        p = (970, 176)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1026, 176)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1000, 230)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_6(self):
        """level 6"""
        pig = Pig(920, 533, self.space)
        pig.life = 40
        self.pigs.append(pig)
        pig = Pig(820, 533, self.space)
        self.pigs.append(pig)
        pig = Pig(720, 633, self.space)
        self.pigs.append(pig)
        self.closed_flat(895, 423, 1)
        self.vertical_pile(900, 0, 5)
        self.vertical_pile(926, 0, 5)
        self.vertical_pile(950, 0, 5)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_7(self):
        """level 7"""
        pig = Pig(978, 180, self.space)
        pig.life = 30
        self.pigs.append(pig)
        pig = Pig(978, 280, self.space)
        pig.life = 30
        self.pigs.append(pig)
        pig = Pig(978, 80, self.space)
        pig.life = 30
        self.pigs.append(pig)
        self.open_flat(950, 0, 3)
        self.vertical_pile(850, 0, 3)
        self.vertical_pile(830, 0, 3)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_8(self):
        """level 8"""
        pig = Pig(1000, 180, self.space)
        pig.life = 30
        self.pigs.append(pig)
        pig = Pig(1078, 280, self.space)
        pig.life = 30
        self.pigs.append(pig)
        pig = Pig(900, 80, self.space)
        pig.life = 30
        self.pigs.append(pig)
        self.open_flat(1050, 0, 3)
        self.open_flat(963, 0, 2)
        self.open_flat(880, 0, 1)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_9(self):
        """level 9"""
        pig = Pig(1000, 180, self.space)
        pig.life = 20
        self.pigs.append(pig)
        pig = Pig(900, 180, self.space)
        pig.life = 20
        self.pigs.append(pig)
        self.open_flat(1050, 0, 3)
        self.open_flat(963, 0, 2)
        self.open_flat(880, 0, 2)
        self.open_flat(790, 0, 3)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_10(self):
        """level 10"""
        pig = Pig(960, 250, self.space)
        pig.life = 20
        self.pigs.append(pig)
        pig = Pig(820, 160, self.space)
        self.pigs.append(pig)
        pig = Pig(1100, 160, self.space)
        self.pigs.append(pig)
        self.vertical_pile(900, 0, 3)
        self.vertical_pile(930, 0, 3)
        self.vertical_pile(1000, 0, 3)
        self.vertical_pile(1030, 0, 3)
        self.horizontal_pile(970, 250, 2)
        self.horizontal_pile(820, 0, 4)
        self.horizontal_pile(1100, 0, 4)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_11(self):
        """level 11"""
        pig = Pig(820, 177, self.space)
        self.pigs.append(pig)
        pig = Pig(960, 150, self.space)
        self.pigs.append(pig)
        pig = Pig(1100, 130, self.space)
        self.pigs.append(pig)
        pig = Pig(890, 270, self.space)
        pig.life = 30
        self.pigs.append(pig)
        self.horizontal_pile(800, 0, 5)
        self.horizontal_pile(950, 0, 3)
        self.horizontal_pile(1100, 0, 2)
        self.vertical_pile(745, 0, 2)
        self.vertical_pile(855, 0, 2)
        self.vertical_pile(900, 0, 2)
        self.vertical_pile(1000, 0, 2)
        p = (875, 230)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def load_level(self):
        self.score = 0
        pigs_to_remove = []
        for pig in self.pigs:
            pigs_to_remove.append(pig)

        for pig in pigs_to_remove:
            self.space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

        birds_to_remove = []
        for bird in self.birds:
            birds_to_remove.append(bird)

        for bird in birds_to_remove:
            self.space.remove(bird.shape, bird.shape.body)
            self.birds.remove(bird)

        columns_to_remove = []
        for column in self.columns:
            columns_to_remove.append(column)

        for column in columns_to_remove:
            self.space.remove(column.shape, column.shape.body)
            self.columns.remove(column)

        beams_to_remove = []
        for beam in self.beams:
            beams_to_remove.append(beam)

        for beam in beams_to_remove:
            self.space.remove(beam.shape, beam.shape.body)
            self.beams.remove(beam)

        try:
            build_name = "build_" + str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_" + str(self.number)
            getattr(self, build_name)()

    def draw_level(self, screen):
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            debug_draw_line(screen, (150, 150, 150), False, [p1, p2])

        i = 0
        for pig in self.pigs:
            i += 1
            pig = pig.shape
            if pig.body.position.y < 0:
                pigs_to_remove.append(pig)

            p = to_pygame(pig.body.position)
            x, y = p

            angle_degrees = math.degrees(pig.body.angle)
            img = pygame.transform.rotate(pig_image, angle_degrees)
            w,h = img.get_size()
            x -= w * 0.5
            y -= h * 0.5
            debug_blit(img, (x, y))
            debug_draw_circle(screen, BLUE, p, int(pig.radius), 2)

        for column in self.columns:
            column.draw_poly('columns', screen)

        for beam in self.beams:
            beam.draw_poly('beams', screen)