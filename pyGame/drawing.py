import pygame


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800,600))
gameDisplay.fill(black)

pixAr = pygame.PixelArray(gameDisplay)
pixAr[10][20] = green # change color of pixel

# draw a line
pygame.draw.line(gameDisplay, blue, (100,200), (300,450), 5)

#draw a rectangle
pygame.draw.rect(gameDisplay, red, (400,400,50,25))

#draw a circle
pygame.draw.circle(gameDisplay, white, (150,150), 75)

gameExit = False
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            quit()
            
    pygame.display.update()
    
    
pygame.quit()
quit()    
    