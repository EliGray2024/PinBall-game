import pygame, pymunk, math, pymunk.pygame_util, random, sys
from pymunk import Vec2d 
from Ball import*
from Hud import*
# ~ from Hub import*
from Map import*
from Bumper import*
from Flipper import*
#spoon
from Launcher import*

from Button import Button


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

Ball.collision_type = 1
Map.collision_type = 2
Flipper.collision_type = 3
Bumper.collision_type = 4

#spoon
Launcher.collision_type = 5

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
    
#spoon
launcher = Launcher(space, [834, 600])
objects.append(launcher)

live = Hud("lives ",[0,0])
point = Hud("points ", [620,0])


def game():
    ballcountMAX = 1
    ballcount = 0 
    lives = 3
    points = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rightFlipper.flip()
                if event.key == pygame.K_ESCAPE:
                    paused()
                if event.key == pygame.K_LEFT:
                    leftFlipper.flip()
                if event.key == pygame.K_SPACE:
                    launcher.go()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if ballcount < ballcountMAX:
                            ballcount += 1
                            # ~ if random.randint(0,1) == 0:    
                                # ~ x = random.randint(200, 350)
                            # ~ else:
                                # ~ x = random.randint(450, 600)
                            ball = Ball(space, [834, 350]) 
                            objects.append(ball)
                        else:
                            print("Cannot add another ball")
                
                
                

             
        for o in objects:
            if o.kind == "bumper":
                points += o.update()
            else:
                o.update()
            if o.rect.top > size[1]:
                ballcount -= 1
                lives -=1
                o.drainSound.play()
                space.remove(o.body, o.shape)
                objects.remove(o)
                
        live.update(lives) 
        point.update(points) 
        if lives == 0:
            menu_state = "end"
        screen.fill((255,255,255))
        screen.blit(table.image, table.rect)
        screen.blit(live.image, live.rect)
        screen.blit(point.image, point.rect)
        for line in table.lines:
            pygame.draw.line(screen, ("black"), line.a, line.b, 5)
        for o in objects:
            screen.blit(o.image, o.rect)
        
        #space.debug_draw(draw_options)
        
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

def main_menu():
    BG = pygame.image.load("images/Background.png")

    MENU_TEXT = pygame.font.Font("images/font.ttf", 100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(465, 100))

    PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(465, 250), 
                        text_input="PLAY", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(465, 400), 
                        text_input="OPTIONS", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 550), 
                        text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
    screen.blit(BG, (0, 0))
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                    button.changeColor(event.pos)
                    button.update(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(event.pos):
                    game()
                if OPTIONS_BUTTON.checkForInput(event.pos):
                    options()
                if QUIT_BUTTON.checkForInput(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
        

def paused():
    
    TextSurf = pygame.font.Font("images/font.ttf", 115).render("Paused", True, "#b68f40")
    TextRect = TextSurf.get_rect(center=(465, 100))

    screen.blit(TextSurf, TextRect)
    

    while paused:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(465, 250), 
                        text_input="Continue", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 550), 
                        text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")

        pygame.display.update()
        clock.tick(15) 
         
main_menu()



pygame.quit()
