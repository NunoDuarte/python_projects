import pygame
import random
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

# adding a ground is very similar to adding a cube
ground_vertices = (
    (-10, -1.1, 20),
    (10, -1.1, 20),
    (-10, -1.1, -300),
    (10, -1.1, -300),
    )

# just adding some vertices to make a boundary of some width but infinite length
def ground():
    glBegin(GL_QUADS)
    
    for vertex in ground_vertices:
        glColor3fv((0,0.5,0.5))
        glVertex3fv(vertex)
        
    glEnd()


# set vertices for every cube
def set_vertices(max_distance):
    x_value_change = random.randrange(-10,10)
    y_value_change = random.randrange(-10,10)
    z_value_change = random.randrange(-1*max_distance,-20)
    
    new_vertices = []
    
    for vert in vertices:
        new_vert = []
        
        # get new values for a new cube
        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change
        
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        
        new_vertices.append(new_vert)
        
    return new_vertices        


def Cube(vertices):
    
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
    
    glTranslatef(random.randrange(-5,5), random.randrange(-5,5), -40) # relation to our object
    
    # rotate the cube (x,y,z, theta)
    #glRotate(25, 4, 1, 0)
    
    x_move = 0
    y_move = 0
    
    max_distance = 300
    cube_dict = {}
    
    for x in range(75):
        cube_dict[x] = set_vertices(max_distance)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.3
                if event.key == pygame.K_RIGHT:
                    x_move = -0.3
                if event.key == pygame.K_UP:
                    y_move = -0.3
                if event.key == pygame.K_DOWN:
                    y_move = 0.3
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        print(x)
        
        camera_z = x[3][2] # new z position (it is the position that will be printed and it can't be avoided)
        camera_y = x[3][1]
        camera_x = x[3][0]
        

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move, y_move,0.5)
        
        ground()

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        pygame.display.flip()     
        pygame.time.wait(10)
        
      
main()
pygame.quit()
quit()                
                
# this shows us a perspective of a 3D cube
# this is 3D but we could have done this with just pygame drawing some 2D lines (but that would be just a pseudo 3D) 





