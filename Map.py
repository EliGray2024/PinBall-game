import pygame, pymunk, math, pymunk.pygame_util, random
from pymunk import Vec2d 

class Map():
    def __init__ (self, space):
        self.image = pygame.image.load("images/Map.png")
        self.rect = self.image.get_rect()
        Arc1x = 814
        Arc1y = 120
        Arc2x = 772
        Arc2y = 168
        
        self.lineSegments =[ 
            #box
            [(65, 665), (218, 708)],
            [(735, 665), (582, 708)],
            [(735, 665), (735, 140)],
            [(815, 65), (65, 65)],
            [(65, 65), (65, 665)],
            #left pinch
            [(140, 600), (235, 630)],
            [(140, 600), (145, 500)],
            #right pinch
            [(660, 600), (565, 630)],
            [(660, 600), (655, 500)],
            #Launcher
            [(735, 140), (775, 140)],
            [(869, 121), (869, 935)],
            [(869, 935), (800, 935)],
            [(800, 935), (800, 166)],
            #launcher Arc 1
            [(55+Arc1x,0+Arc1y), (51+Arc1x, -10+Arc1y)],
            [(51+Arc1x, -10+Arc1y), (47+Arc1x,-20+Arc1y)],
            [(47+Arc1x,-20+Arc1y), (42+Arc1x,-30+Arc1y)],
            [(42+Arc1x,-30+Arc1y), (30+Arc1x,-42+Arc1y)],
            [(30+Arc1x,-42+Arc1y), (20+Arc1x,-47+Arc1y)],
            [(20+Arc1x,-47+Arc1y), (10+Arc1x, -51+Arc1y)],
            [(10+Arc1x, -51+Arc1y), (0+Arc1x,-55+Arc1y)],
            #Launcher Arc 2
            [(28+Arc2x,0+Arc2y), (27+Arc2x,-7+Arc2y)],
            [(27+Arc2x,-7+Arc2y), (23+Arc2x, -16+Arc2y)],
            [(23+Arc2x, -16+Arc2y), (16+Arc2x,-23+Arc2y)],
            [(16+Arc2x,-23+Arc2y), (16+Arc2x, -23+Arc2y)],
            [(16+Arc2x, -23+Arc2y), (7+Arc2x,-27+Arc2y)],
            [(7+Arc2x,-27+Arc2y), (0+Arc2x,-28+Arc2y)],
        ]
        
        self.lines  = []
        
        for segment in self.lineSegments:
            line = pymunk.Segment(space.static_body, segment[0], segment[1], 5)
            line.elasticity = .95
            line.collision_type = Map.collision_type
            line.obj = self
            line.friction = 10
            line.group = 1
            self.lines += [line]
        
        space.add(*self.lines)
    
    
