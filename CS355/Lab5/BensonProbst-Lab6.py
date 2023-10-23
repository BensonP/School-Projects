import sys
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
CAMERA_X = 0
CAMERA_Y = 0
CAMERA_Z = -10
ANGLE = 0
PERSP = True
CAR_X = 0
TIRE_ROTATION = 0

def timer(value):
    global CAR_X
    global TIRE_ROTATION
    CAR_X += .08
    TIRE_ROTATION -= 2
    glutPostRedisplay()
    glutTimerFunc(30, timer, 0)


def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

 
def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()

def drawStreet():
    for i in range(5):
        if i != 0:
            glTranslated(20,0,0)
        drawHouse()

def drawNeighborHood():
    glPushMatrix()
    glTranslated(0,0,-25)
    drawStreet()
    glPushMatrix()
    glRotated(-90,0,1,0)
    glTranslated(20,0,-20)
    drawHouse()
    glPopMatrix()
    glRotated(180,0,1,0)
    glTranslated(0,0,-40)
    drawStreet()
    glPopMatrix()

def drawMovingCar():
    glPushMatrix()
    glTranslated(CAR_X - 15,0,0)
    drawCar()
    for i in range(4):
        glPushMatrix()
        drawMovingWheels(i)
        glPopMatrix()
    glPopMatrix()

def drawMovingWheels(i):
    if i == 0:
        glTranslated(-2, 0, -1.5)
    if i == 1:
        glTranslated(-2, 0, 1.5)
    if i == 2:
        glTranslated(2,0,-1.5)
    if i == 3:
        glTranslated(2,0,1.5)
    glRotated(TIRE_ROTATION,0,0,1)
    drawTire()

        

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    
    glLoadIdentity()
    if(PERSP):
        gluPerspective(90, 1, 1, 512)
    else:
        glOrtho(-10, 10, -10, 10, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(ANGLE,0,1,0)
    glTranslated(CAMERA_X,CAMERA_Y,CAMERA_Z)

    drawNeighborHood()
    drawMovingCar()
    
    glFlush()
    

def keyboard(key, x, y):
    global CAMERA_X
    global CAMERA_Y
    global CAMERA_Z
    global ANGLE
    global PERSP
    
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'w':
        CAMERA_Z += math.sin(math.radians(ANGLE + 90))
        CAMERA_X += math.cos(math.radians(ANGLE + 90))

    if key == b's':
        CAMERA_Z -= math.sin(math.radians(ANGLE + 90))
        CAMERA_X -= math.cos(math.radians(ANGLE + 90))
        

    if key == b'a':
        CAMERA_Z += math.sin(math.radians(ANGLE))
        CAMERA_X += math.cos(math.radians(ANGLE))

    if key == b'd':
        CAMERA_Z -= math.sin(math.radians(ANGLE))
        CAMERA_X -= math.cos(math.radians(ANGLE))

    if key == b'r':
        CAMERA_Y -=1

    if key == b'f':
        CAMERA_Y +=1

    if key == b'e':
        ANGLE +=1

    if key == b'q':
        ANGLE -=1

    if key == b'h':
        CAMERA_X = 0
        CAMERA_Y = 0
        CAMERA_Z = -10
        ANGLE = 0

    if key == b'o':
        PERSP = False

    if key == b'p':
        PERSP = True
  
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, timer, 0)
glutMainLoop()
