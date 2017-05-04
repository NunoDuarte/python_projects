import pygame
# import everything
from pygame.locals import *

# import everything
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),  
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),         
    (6, 3),
    (6, 4), 
    (6, 7),
    (5, 1), 
    (5, 4),
    (5, 7), 
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
def main():
    pygame.init()
    display = (800, 600)
    # specifying DOUBLEBUFF double buffer and openGL 
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # 45 degree field of view
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    # -5 is the zoom at which we are looking at (0 -  would mean that we would be viewing right in your face)
    glTranslatef(0.0, 0.0, -5)
    
    glRotate(0, 0, 0, 0)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # to rotate the cube
        # 1 degree
        # x = 3
        # y = 1
        # z = 1
        glRotate(1, 3, 1, 1)        
                
        # you need to clear between each frame (just like in pygame)
        # we are telling openGL what exactly we want to clear
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # run code
        Cube()
        # pygame.update does not work here so pygame.flip does the job
        pygame.display.flip()
        
        pygame.time.wait(10)
        
        
main()
                
# this shows us a perspective of a 3D cube
# this is 3D but we could have done this with just pygame drawing some 2D lines (but that would be just a pseudo 3D) 





