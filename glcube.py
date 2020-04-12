#!/usr/bin/env python

# https://github.com/pygame/pygame/blob/master/examples/glcube.py
# LGPL license

"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unoptimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""

import pygame
from pygame.locals import OPENGL, DOUBLEBUF, QUIT, KEYDOWN, K_ESCAPE, KEYDOWN, FULLSCREEN, K_LEFT, K_RIGHT, K_UP, K_DOWN

try:
    from OpenGL.GL import glBegin, glEnable,glColor3f, glColor3fv, glVertex3fv, glEnd, glMatrixMode, glLoadIdentity, glTranslatef, glRotatef, glClear, glRasterPos3d, glDrawPixels, GL_QUADS, GL_LINES, GL_DEPTH_TEST, GL_PROJECTION, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_RGBA, GL_UNSIGNED_BYTE
    from OpenGL.GLU import gluPerspective
except ImportError:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit



#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge


CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
)

# connect together points for each face
# face 1 connects points 0,1,2,3 etc
CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

fullscreen = False
outlines = True
fullscreen_res = None # set in main()
windowed_res = (640,480)
current_res = windowed_res
fov = 45.0


def drawText(position, textString):
    font = pygame.font.Font (None, 64)
    textSurface = font.render(textString, True, (255,255,255,255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def init_gl_stuff():
    global current_res, fov

    # tells opengl to use the depth buffer, so things are drawn in the correct order
    glEnable(GL_DEPTH_TEST)        #use our zbuffer

    #setup the camera
    glMatrixMode(GL_PROJECTION)
    # resets the matrix back to the origin
    glLoadIdentity()
    # defining a view frustrum
    gluPerspective(
            fov, # vertical field of view (deg)
            float(current_res[0])/current_res[1], # aspect ratio
            0.1, # zNear, the near clipping plane, don't render things closer than this
            100.0 # zFar, the far clipping plane, don't render things beyond this
    )
    # move the camera back three units
    glTranslatef(0.0, 0.0, -5.0)
    # orbit higher to view the subject at a better angle
    glRotatef(25, 1, 0, 0)



def drawcube(offset=0):
    "draw the cube"
    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))

    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:
            pos, color = allpoints[vert]
            glColor3fv(color)
            glVertex3fv(tuple(x+offset for x in pos))
    glEnd()

    if outlines:
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for line in CUBE_EDGES:
            for vert in line:
                pos, color = allpoints[vert]
                glVertex3fv(tuple(x+offset for x in pos))
    
        glEnd()


def toggle_fullscreen():
    global fullscreen, windowed_res, current_res
    if not fullscreen:
        print("Changing to FULLSCREEN {}x{}".format(*fullscreen_res))
        current_res = fullscreen_res
        pygame.display.set_mode(current_res, OPENGL | DOUBLEBUF | FULLSCREEN)
    else:
        print("Changing to windowed mode {}x{}".format(*windowed_res))
        current_res = windowed_res
        pygame.display.set_mode(windowed_res, OPENGL | DOUBLEBUF)
    fullscreen = not fullscreen
    init_gl_stuff()


def main():
    "run the demo"
    global fullscreen, fullscreen_res, windowed_res, fov, outlines
    #initialize pygame and setup an opengl display
    pygame.init()

    display_info = pygame.display.Info()
    fullscreen_res = (display_info.current_w, display_info.current_h)

    pygame.display.set_mode(windowed_res, OPENGL | DOUBLEBUF)

    init_gl_stuff()

    going = True
    speed,x,z,offset,second_cube = 0,0,0,0.5,False
    while going:
        #check for quit'n events
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (
                    event.type == KEYDOWN and (
                        event.key == K_ESCAPE or event.key == pygame.K_q
                    )
                ):
                going = False

            elif event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    toggle_fullscreen()
                if event.key == K_RIGHT:
                    speed += 1
                    print(speed,x,z,fov)
                if event.key == K_LEFT:
                    speed -= 1
                    print(speed,x,z,fov)
                if event.key == K_UP:
                    x += 1
                    print(speed,x,z,fov)
                    if not speed: speed = 1
                if event.key == K_DOWN:
                    x -= 1
                    print(speed,x,z,fov)
                    if not speed: speed = 1
                if event.key == pygame.K_r:
                    speed,x,z = 0,0,0
                    print(speed,x,z)
                    init_gl_stuff()
                if event.key == pygame.K_w:
                    fov += -1
                    init_gl_stuff()
                if event.key == pygame.K_s:
                    fov -= -1
                    init_gl_stuff()
                if event.key == pygame.K_o:
                    outlines = not outlines
                if event.key == pygame.K_z:
                    outlines = False
                    speed,x,y,fov = 2,1,0,8.0
                    init_gl_stuff()
                if event.key == pygame.K_a:
                    second_cube = not second_cube
                if event.key == pygame.K_d:
                    offset -= 0.25
                if event.key == pygame.K_e:
                    offset += 0.25

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #orbit camera around
        if speed:
            glRotatef(speed, x, 1, z)

        drawcube()
        if second_cube:
            drawcube(offset=offset)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__': main()
