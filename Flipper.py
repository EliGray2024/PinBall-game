import pygame, pymunk, math, pymunk.pygame_util, random
from pymunk import Vec2d 

class Flipper():
    def __init__ (self, side, pos, angle, space):
        fp = [[0, 7], [-7, 20], [0, 33], # Tip
              [130, 40] , [142, 35], [148, 20], [142, 5], [130, 0]]
        for f in fp:
            f[0]-=120
            f[1]-=20
        self.mass = 100
        self.moment = pymunk.moment_for_poly(self.mass, fp)
        self.group = 1
        self.elasticity = 0.4
    
        self.body = pymunk.Body(self.mass, self.moment)
        
        if side == "right":
            self.baseImage = pygame.image.load("images/rightFlipper.png")
            self.image = self.baseImage
            self.rect = self.image.get_rect(center = pos)
            self.body.position = self.rect.center
            self.shape = pymunk.Poly(self.body, fp)
            self.rotation = -1
        else: 
            self.baseImage = pygame.image.load("images/leftFlipper.png")
            self.image = self.baseImage
            self.rect = self.image.get_rect(center = pos)
            self.body.position = self.rect.center
            self.shape = pymunk.Poly(self.body, [(-x, y) for x, y in fp])
            self.rotation = 1
        space.add(self.body, self.shape)

        self.joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.joint_body.position = self.body.position
        self.joint = pymunk.PinJoint(self.body, self.joint_body, (0, 0), (0, 0))

        self.spring = pymunk.DampedRotarySpring(
            self.body, self.joint_body, 0.225*self.rotation, 70000000, 2500000
        )
        space.add(self.joint, self.spring)
    
        self.sound = pygame.mixer.Sound("Sounds/Flipperup9.wav")
        
    def update(self):
        self.body.pos = self.rect.center
        self.body.velocity = 0, 0
        angle = -math.degrees(self.body.angle)
        self.rotate(angle)
        
    def flip(self):
        self.sound.play()
        self.body.apply_impulse_at_local_point(
            Vec2d.unit() * 60000*self.rotation, (-100, 0)
        )
        
    def rotate(self, angle):
        rot_image = pygame.transform.rotate(self.baseImage, angle)
        rot_rect = self.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.image = rot_image.subsurface(rot_rect).copy() 
