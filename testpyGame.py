import pygame

pygame.init()

display_width = 800
display_height = 600

#colors definition
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


#resolution
gameDisplay = pygame.display.set_mode((display_width,display_height))

#name of the display
pygame.display.set_caption('A bit Racey')

#imposes the time to everything in the game
clock = pygame.time.Clock()


carImg = pygame.image.load('racecar.png')
car_width = 73 #we know the width of our image

#for displaying the car
def car(x,y):
    gameDisplay.blit(carImg, (x,y)) # x,y is one parameter (a tuple)

def game_loop():
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    x_change = 0
    
    #when we start we haven't left the game yet (duh!!)
    gameExit = False
    while not gameExit:
        
        # what key are they pressing?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # you've left the game
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        x += x_change
                    
                
                
        #the background color will now be white
        gameDisplay.fill(white)
        
        #put the car in the game
        car(x,y)
        
        if x > display_width - car_width or x < 0:
            #you've crashed
            gameExit = True
        
    
        pygame.display.update()
        #frame per second #how fast things move
        clock.tick(60)
        
game_loop()

pygame.quit()
quit()
