import pygame, pymunk, math, pymunk.pygame_util
from pymunk import Vec2d 

class Launcher():
    def __init__(self, space, pos):
        self.kind = "launcher"
    
        self.elasticity = 0.4
        
        fp = [[-30, 10], [30, 10], [30, -10] , [-30, -10]]
        
        self.mass = 30 #??
        self.moment = pymunk.moment_for_poly(self.mass, fp)
        self.body = pymunk.Body(self.mass, self.moment)
        
        self.image = pygame.image.load("images/launcher.png")
        self.rect = self.image.get_rect(center = pos)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly(self.body, fp)
        
        space.add(self.body, self.shape)
        
        #---spring---
        self.joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.joint_body.position = self.body.position
        self.joint = pymunk.GrooveJoint(self.body, self.joint_body, (0, -200), (0, 0), (0,0))
        self.joint.collide_bodies = False
        
        # ~ self.spring = pymunk.DampedSpring(
            # ~ self.body, self.joint_body, (0,-200), (0,0), -100,  70000000, 2500000
        # ~ )
        # ~ self.spring.collide_bodies = False
        
        space.add(self.joint)#, self.spring)
        
    
    def update(self):
        self.body.pos = self.rect.center
        self.rect.center = self.body.position.int_tuple
        
    def go(self):
        self.body.apply_impulse_at_local_point(
            Vec2d.unit() * -60000, (0, 0)
        )
        

