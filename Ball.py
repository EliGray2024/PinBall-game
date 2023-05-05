import pygame, pymunk, math, pymunk.pygame_util
from pymunk import Vec2d 

class Ball():
    def __init__(self, space, pos, radius = 29):
        self.kind = "ball"
        self.radius = radius
        self.image = pygame.image.load("images/ball.png")
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect(center = pos)
        
        self.mass = 1*radius/30
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius, (0, 0))
        
        self.body = pymunk.Body(self.mass, self.inertia)
        self.body.position = self.rect.center
        
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        self.shape.elasticity = 0.95
        self.shape.collision_type = Ball.collision_type
        self.shape.obj = self
        
        space.add(self.body, self.shape)
        
        self.drainSound = pygame.mixer.Sound("Sounds/Drain2.wav")
        self.collisionSound = pygame.mixer.Sound("Sounds/Collision.wav")

        
    def move(self):
        self.rect.center = self.body.position.int_tuple
        
    def update(self):
        self.move()
        
    @staticmethod
    def bumperHit(arbiter, space, data):
        ball = arbiter.shapes[0].obj
        bumper = arbiter.shapes[1].obj
        if arbiter.is_first_contact:
            bumper.bump()
        return True
        
    @staticmethod
    def flipperHit(arbiter, space, data):
        ball = arbiter.shapes[0].obj
        flipper = arbiter.shapes[1].obj
        return True
        
    @staticmethod
    def mapHit(arbiter, space, data):
        ball = arbiter.shapes[0].obj
        line = arbiter.shapes[1].obj
        if arbiter.is_first_contact:
            ball.collisionSound.play()
        return True
