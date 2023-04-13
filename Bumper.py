import pygame, pymunk, math, pymunk.pygame_util, random
from pymunk import Vec2d 

class Bumper ():
    def __init__(self, space, pos, radius =10):
        self.kind = "bumper"
        self.radius = radius
        self.pos = pos
        self.imageRest = pygame.transform.scale(pygame.image.load("images/bumper.png"), (self.radius*2, self.radius*2))
        self.imageHit = pygame.transform.scale(pygame.image.load("images/bumper-hit.png"), (int(self.radius*3), int(self.radius*3)))
        self.image = self.imageRest
        self.rect = self.image.get_rect(center = pos)
        
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.rect.center
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1.1
        self.shape.collision_type = Bumper.collision_type
        self.shape.obj = self
        
        space.add(self.body, self.shape)
        
        self.sound = pygame.mixer.Sound("Sounds/Sling2.wav")
                
        self.hitTimer = 0
        self.hitTimerMax = 3
        
        self.didHit = False
        self.value = 100
        
    def update(self):
        self.body.pos = self.pos
        self.body.velocity = 0, 0
        
        if self.hitTimer > 0:
            if self.hitTimer <= self.hitTimerMax:
                self.hitTimer += 1
                if self.didHit:
                    self.didHit = False
                    return self.value
            else:
                self.hitTimer = 0
                self.image = self.imageRest
                self.rect = self.image.get_rect(center = self.body.pos)
        return 0 

    def bump(self):
        self.sound.play()
        self.image = self.imageHit
        self.rect = self.image.get_rect(center = self.body.pos)
        self.hitTimer = 1
        self.didHit = True
        
