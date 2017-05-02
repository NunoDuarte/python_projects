import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

#colors definition
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

pause = True
#crash = False

#resolution
gameDisplay = pygame.display.set_mode((display_width,display_height))

#name of the display
pygame.display.set_caption('A bit Racey')

#imposes the time to everything in the game
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
car_width = 73 #we know the width of our image

# to show the game icon in the app game
pygame.display.set_icon(carImg)
    
def quitgame():
    pygame.quit()
    quit()
    
def button(msg, x,y,w,h,ic,ac, action=None):
    #msg - message
    # x, y, width, height, inactive color, active color
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
     
    # make the button interactive (if your on top of it you make it lighter
    if x + w > mouse[0] > x and y + 50 > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action() #the button will run any action I want
#             if action == 'play':
#                 game_loop()
#             elif action == 'quit':
#                 pygame.quit()
#                 quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
    #pygame.draw.rect(gameDisplay, green, (150,450,100,50))
    
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) ) # center of x and center of y oto put the text on the middle of the rect
    gameDisplay.blit(textSurf, textRect)

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+ str(count), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

#for displaying the car
def car(x,y):
    gameDisplay.blit(carImg, (x,y)) # x,y is one parameter (a tuple)
    

## functions to pause and unpause the game but keep our score.  
def unpause():
    global pause
    pause = False
    
def paused():
    
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects('Paused', largeText)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect) 
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
        # our two buttons
        button('Continue', 150,450,100,50, green, bright_green, unpause)
        button('Quit', 550,450,100,50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15) 
        
def game_intro():
    
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text_objects('A bit racey', largeText)
        textRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(textSurf, textRect)   
        
        
        # our two buttons
        button('GO!', 150,450,100,50, green, bright_green, game_loop)
        button('Quit', 550,450,100,50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15)             
    
def text_objects(text, font):
    textSurface = font.render(text, True, black) # the text, the anti-aliasing is True, and the color of the text
    
    return textSurface, textSurface.get_rect()
    
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    
    #show for 2 seconds
    time.sleep(2)
    #reset the game
    game_loop()
    
def crash():
    
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects('You Crashed', largeText)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect) 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
        # our two buttons
        button('Play Again', 150,450,100,50, green, bright_green, game_loop)
        button('Quit', 550,450,100,50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15) 

def game_loop():
    
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    x_change = 0
    
    # where do you want the object to start? You don't want to always start at the same position
    thing_startx = random.randrange(0, display_width)
    thing_starty = 0 #you want it to start on top of the image
    thing_speed = 7
    thing_width = 100
    thing_height = 100
    
    dodged = 0
     
    #when we start we haven't left the game yet (duh!!)
    gameExit = False
    while not gameExit:
        
        # what key are they pressing?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # you've left the game
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        x += x_change
 
        #the background color will now be white
        gameDisplay.fill(white)
        
        #things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed # so the object moves down at the specific speed
        # however, the object continues to move off the screen forever
        
        #put the car in the game
        car(x,y)
        
        things_dodged(dodged)
        
        if x > display_width - car_width or x < 0:
            #you've crashed
            crash()
        
        if thing_starty > display_height: #if object disappears off the screen
            thing_starty = 0 - thing_height # show up the object back on top
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            #make the game more difficult
            thing_speed += 0.1
            thing_width += 5
            
        if y < thing_starty + thing_height:
            #print('y cross over')
            
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                #print('x cross over')
                crash()
    
        pygame.display.update()
        #frame per second #how fast things move
        clock.tick(60)
        
game_intro()
        
game_loop()

pygame.quit()
quit()
