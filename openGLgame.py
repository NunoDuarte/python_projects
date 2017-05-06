import pygame
# import everything
from pygame.locals import *

# import everything
from OpenGL.GL import *
from OpenGL.GLU import *

# the order is important! (for all vertices)
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

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)            
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1), 
    )

def Cube():
    
    glBegin(GL_QUADS)
    x = 0
    glColor3fv((0,1,0)) #putting here (it is a constant color)
    for surface in surfaces:
        x+=1
        glColor3fv((0,0,1)) #putting here (it is a constant for each surface)
        for vertex in surface:
            glVertex3fv(vertices[vertex])
            #glColor3fv(colors[x]) #putting here (it is a constant for each vertex)
            
    glEnd()
    
    
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
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    glTranslatef(0.0, 0.0, -40) # relation to our object
    
    # rotate the cube (x,y,z, theta)
    #glRotate(25, 4, 1, 0)
    
    object_passed = False
    
    while not object_passed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, -0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 0.5, 0)

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        print(x)
        
        camera_z = x[3][2] # new z position (it is the position that will be printed and it can't be avoided)
        camera_y = x[3][1]
        camera_x = x[3][0]
        
        # if the object passed our screen then we have avoided it
        if camera_z < -1:
            object_passed = True

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(0,0,0.5)

        Cube()
        pygame.display.flip()     
        pygame.time.wait(10)
        
for x in range(10):        
    main()
pygame.quit()
quit()                
                
# this shows us a perspective of a 3D cube
# this is 3D but we could have done this with just pygame drawing some 2D lines (but that would be just a pseudo 3D) 





