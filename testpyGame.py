import pygame

pygame.init()

#resolution
gameDisplay = pygame.display.set_mode((800,600))

#name of the display
pygame.display.set_caption('A bit Racey')

#imposes the time to everything in the game
clock = pygame.time.Clock()

#when we start we haven't crashed yet
crashed = False

while not crashed:
    
    # what key are they pressing?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # you've crashed
            crashed = True
            
        print(event)

    pygame.display.update()
    
    #frame per second #how fast things move
    clock.tick(60)

pygame.quit()
quit()
