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

#for displaying the car
def car(x,y):
    gameDisplay.blit(carImg, (x,y)) # x,y is one parameter (a tuple)

x = (display_width * 0.45)
y = (display_height * 0.8)

#when we start we haven't crashed yet
crashed = False
while not crashed:
    
    # what key are they pressing?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # you've crashed
            crashed = True
            
    #the background color will now be white
    gameDisplay.fill(white)
    
    #put the car in the game
    car(x,y)

    pygame.display.update()
    #frame per second #how fast things move
    clock.tick(60)

pygame.quit()
quit()
