import pygame, pymunk, math, pymunk.pygame_util, random, sys
from pymunk import Vec2d 
from Ball import*
from Hud import*
from Map import*
from Bumper import*
from Flipper import*
from Launcher import*
from Button import Button
from pygame import mixer



pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

Ball.collision_type = 1
Map.collision_type = 2
Flipper.collision_type = 3
Bumper.collision_type = 4

Launcher.collision_type = 5

mixer.music.load("Sounds/background.ogg")
mixer.music.play(-1)



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
    
launcher = Launcher(space, [834, 600])
objects.append(launcher)

live = Hud("lives ",[0,0])
point = Hud("points ", [670,0])

points = 0
lives = 3
ballcountMAX = 1
ballcount = 0

view = "main menu" 
viewChanged = True;

while True:
    if view == "main menu" and viewChanged:
        BG = pygame.image.load("images/Background.png")

        MENU_TEXT = pygame.font.Font("images/font.ttf", 100).render("PINBALL", True, "#d7fcd4")
        MENU_RECT = MENU_TEXT.get_rect(center=(465, 100))
    
        
        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(465, 250), 
                            text_input="PLAY", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(465, 400), 
                            text_input="OPTIONS", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        CREDITS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(465, 550), 
                            text_input="CREDITS", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 700), 
                            text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        screen.blit(BG, (0, 0))
        
        points = 0
        lives = 3
        ballcount = 0
        viewChanged = False
    while view == "main menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for button in [PLAY_BUTTON, OPTIONS_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
                    button.changeColor(event.pos)
                    button.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(event.pos):
                    view = "game"
                    
                    for o in objects:
                        if o.kind == "ball":
                            space.remove(o.body, o.shape)
                            objects.remove(o)
                            print("kill ball")
                        ballcount = 0
                        
                    viewChanged = True
                if CREDITS_BUTTON.checkForInput(event.pos):
                    view = "credit"
                    viewChanged = True
                if OPTIONS_BUTTON.checkForInput(event.pos):
                    view = "options"
                    viewChanged = True
                if QUIT_BUTTON.checkForInput(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
    
    if view == "game" and viewChanged:
        viewChanged = False
    while view == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rightFlipper.flip()
                if event.key == pygame.K_ESCAPE:
                    view = "paused"
                    viewChanged = True
                if event.key == pygame.K_LEFT:
                    leftFlipper.flip()
                if event.key == pygame.K_SPACE:
                    launcher.go()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if ballcount < ballcountMAX:
                            ballcount += 1
                            x = 834
                            ball = Ball(space, [x, 350]) 
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
            view = "loss"
            viewChanged = True
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
    if view == "options" and viewChanged:
        BG = pygame.image.load("images/Background.png")

        MENU_TEXT = pygame.font.Font("images/font.ttf", 100).render("OPTIONS", True, "#d7fcd4")
        MENU_RECT = MENU_TEXT.get_rect(center=(465, 100))
        
        DESC_TEXT = pygame.font.Font("images/font.ttf", 20).render("", True, "#d7fcd4")
        DESC_RECT = DESC_TEXT.get_rect(center=(465, 300))
       
    
        
        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(465, 600), 
                            text_input="BACK", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 750), 
                            text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        screen.blit(BG, (0, 0))
        
        viewChanged = False
        
    while view == "options":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    for button in [PLAY_BUTTON, QUIT_BUTTON]:
                        button.changeColor(event.pos)
                        button.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(event.pos):
                        view = "main menu"
                        viewChanged = True
                    if QUIT_BUTTON.checkForInput(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        view = "main menu"
                        viewChanged = True
                        
            screen.blit(MENU_TEXT, MENU_RECT)
            screen.blit(DESC_TEXT, DESC_RECT)
            pygame.display.update()
         
    if view == "credit" and viewChanged:
        BG = pygame.image.load("images/Background.png")

        MENU_TEXT = pygame.font.Font("images/font.ttf", 100).render("CREDITS", True, "#d7fcd4")
        MENU_RECT = MENU_TEXT.get_rect(center=(465, 100))
        
        DESC_TEXT = pygame.font.Font("images/font.ttf", 20).render("By: Eli Gray " "And " "Christopher Spooner", True, "#d7fcd4")
        DESC_RECT = DESC_TEXT.get_rect(center=(465, 300))
       
        DESC_TEXT2 = pygame.font.Font("images/font.ttf", 20).render("Music By: KYOTO", True, "#d7fcd4")
        DESC_RECT2 = DESC_TEXT2.get_rect(center=(465, 350))
    
        
        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(465, 600), 
                            text_input="BACK", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 750), 
                            text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        screen.blit(BG, (0, 0))
        
        viewChanged = False
        
    while view == "credit":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    for button in [PLAY_BUTTON, QUIT_BUTTON]:
                        button.changeColor(event.pos)
                        button.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(event.pos):
                        view = "main menu"
                        viewChanged = True
                    if QUIT_BUTTON.checkForInput(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        view = "main menu"
                        viewChanged = True
                        
            screen.blit(MENU_TEXT, MENU_RECT)
            screen.blit(DESC_TEXT, DESC_RECT)
            screen.blit(DESC_TEXT2, DESC_RECT2)
            pygame.display.update()
         
    if view == "paused" and viewChanged:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TextSurf = pygame.font.Font("images/font.ttf", 115).render("Paused", True, "#d7fcd4")
        TextRect = TextSurf.get_rect(center=(465, 100))

        screen.blit(TextSurf, TextRect)
        
        PLAY_BUTTON = Button(image=pygame.image.load("images/Continue Rect.png"), pos=(465, 250), 
                        text_input="CONTINUE", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Continue Rect.png"), pos=(465, 400), 
                            text_input="MAIN MENU", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 550), 
                        text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        
        viewChanged = False
    while view == "paused":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        view = "game"
                        viewChanged = True
            if event.type == pygame.MOUSEMOTION:
                for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                    button.changeColor(event.pos)
                    button.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(event.pos):
                    view = "game"
                    viewChanged = True
                if OPTIONS_BUTTON.checkForInput(event.pos):
                    view = "main menu"
                    viewChanged = True
                if QUIT_BUTTON.checkForInput(event.pos):
                    pygame.quit()
                    sys.exit()

        clock.tick(15) 
        pygame.display.update()

    if view == "loss" and viewChanged:
        BG = pygame.image.load("images/Background2.png")

        MENU_TEXT = pygame.font.Font("images/font.ttf", 100).render("You Lose", True, "#d7fcd4")
        MENU_RECT = MENU_TEXT.get_rect(center=(465, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/PlayAgain Rect.png"), pos=(465, 250), 
                            text_input="PLAY AGAIN", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Continue Rect.png"), pos=(465, 400), 
                            text_input="MAIN MENU", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(465, 550), 
                            text_input="QUIT", font=pygame.font.Font("images/font.ttf", 75), base_color="#d7fcd4", hovering_color="White", screen = screen)
        screen.blit(BG, (0, 0))
        
        viewChanged = False
    
    while view == "loss":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                        button.changeColor(event.pos)
                        button.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(event.pos):
                        view = "game"
                        viewChanged = True
                    if OPTIONS_BUTTON.checkForInput(event.pos):
                        view = "main menu"
                        viewChanged = True
                    if QUIT_BUTTON.checkForInput(event.pos):
                        pygame.quit()
                        sys.exit()
            
            screen.blit(MENU_TEXT, MENU_RECT)
            pygame.display.update()
                
         



pygame.quit()
