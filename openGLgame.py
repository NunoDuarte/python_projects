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
    # paramters: camera_x and camera_y is to define where we are in the 3D environment
def set_vertices(max_distance, min_distance=-20, camera_x = 0, camera_y = 0):
    
    camera_x = -1*int(camera_x)
    camera_y = -1*int(camera_y)
    
    x_value_change = random.randrange(camera_x-75, camera_x+75)
    y_value_change = random.randrange(camera_y-75, camera_y+75)
    z_value_change = random.randrange(-1*max_distance,min_distance)
    
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
    
    max_distance = 100
    min_distance = -20
    
    gluPerspective(45, (display[0]/display[1]), 0.1, max_distance)
    
    glTranslatef(0, 0, -40) # relation to our object
    
    x_move = 0
    y_move = 0
    
    cur_x = 0
    cur_y = 0
    
    #speed of the game
    game_speed = 2
    direction_speed = 2
    
    cube_dict = {}
    
    for x in range(75):
        cube_dict[x] = set_vertices(max_distance, min_distance)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = -1*direction_speed
                if event.key == pygame.K_UP:
                    y_move = -1*direction_speed
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print(x)
        
        camera_z = x[3][2] # new z position (it is the position that will be printed and it can't be avoided)
        camera_y = x[3][1]
        camera_x = x[3][0]
        
        cur_x += x_move
        cur_y += y_move

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move, y_move, game_speed)
        
        ground()

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        # what this does is get the cubes that have passed the screen and give them new vertices now in front of your view
        # as the while loop goes again it will generate the same cubes but with new vertices. This simulates the creation and elimination
        # of old cubes        
        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                #print('passed cube')                
                new_max = int(-1*(camera_z-(max_distance*2)))
                cube_dict[each_cube] = set_vertices(new_max, int(camera_z-max_distance), cur_x, cur_y)
                

        pygame.display.flip()     
        #pygame.time.wait(10)
        
      
main()
pygame.quit()
quit()                
                
# this shows us a perspective of a 3D cube
# this is 3D but we could have done this with just pygame drawing some 2D lines (but that would be just a pseudo 3D) 





