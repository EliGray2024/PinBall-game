import pygame, pymunk, math, pymunk.pygame_util, random
from pymunk import Vec2d 
from Ball import*
from Hud import*
from Map import*
from Bumper import*
from Flipper import*


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

Ball.collision_type = 1
Map.collision_type = 2
Flipper.collision_type = 3
Bumper.collision_type = 4

size = (930,1000)
screen = pygame.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)
#https://www.vpforums.org/Tutorials/Sounds/SndLib1.html 
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, 400
FPS = 60
pymunk.pygame_util.positive_y_is_up = False
objects = []

ballHitBumper = space.add_collision_handler(Ball.collision_type, Bumper.collision_type)
ballHitBumper.begin = Ball.bumperHit
ballHitFlipper = space.add_collision_handler(Ball.collision_type, Flipper.collision_type)
ballHitFlipper.begin = Ball.flipperHit
ballHitMap = space.add_collision_handler(Ball.collision_type, Map.collision_type)
ballHitMap.begin = Ball.mapHit

table = Map(space)


rightFlipper = Flipper("right", (555,750), 13, space)
leftFlipper = Flipper("left", (245, 750), 13, space)

objects.append(rightFlipper)
objects.append(leftFlipper)

bumperCenters = [(250, 200), (400, 300),(550, 200)]
for center in bumperCenters:
    objects.append(Bumper(space, center))
    
points = 0

live = Hud("lives ",[0,0])
point = Hud("points ", [620,0])

def game():
    ballcountMAX = 1
    ballcount = 0 
    lives = 3
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rightFlipper.flip()
                if event.key == pygame.K_LEFT:
                    leftFlipper.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if ballcount < ballcountMAX:
                            ballcount += 1
                            if random.randint(0,1) == 0:    #left
                                x = random.randint(200, 350)
                            else:
                                x = random.randint(450, 600)
                            ball = Ball(space, [x, 350]) 
                            objects.append(ball)
                        else:
                            print("Cannot add another ball")
        
        
        for o in objects:
            o.update()
            if o.rect.top > size[1]:
                ballcount -= 1
                lives -=1
                o.drainSound.play()
                space.remove(o.body, o.shape)
                objects.remove(o)
                
        live.update(lives) 
        if lives == 0:
            pygame.quit()
        
        
        screen.fill((255,255,255))
        screen.blit(table.image, table.rect)
        screen.blit(live.image, live.rect)
        screen.blit(point.image, point.rect)
        for line in table.lines:
            pygame.draw.line(screen, ("black"), line.a, line.b, 5)
        for o in objects:
            screen.blit(o.image, o.rect)
        
        # ~ space.debug_draw(draw_options)
        
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pygame.quit()
