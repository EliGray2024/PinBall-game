import pygame, pymunk, math, pymunk.pygame_util, random
from pymunk import Vec2d 

class Map():
    def __init__ (self, space):
        self.image = pygame.image.load("images/Map.png")
        self.rect = self.image.get_rect()
        
        self.lineSegments =[ 
            #box
            [(65, 665), (218, 708)],
            [(735, 665), (582, 708)],
            [(735, 665), (735, 130)],
            [(815, 65), (65, 65)],
            [(65, 65), (65, 665)],
            #left pinch
            [(140, 600), (235, 630)],
            [(140, 600), (145, 500)],
            #right pinch
            [(660, 600), (565, 630)],
            [(660, 600), (655, 500)],
            #Launcher
            [(735, 130), (775, 130)],
            [(869, 121), (869, 935)],
            [(869, 935), (800, 935)],
            [(800, 935), (800, 156)],
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
    
    
