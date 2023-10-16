import sys

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


camera_x = 0
camera_y = 0
camera_z = 0

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    
    #Your Code Here
    glMatrixMode(GL_PROJECTION)
    #glOrtho(-10, 10, -10, 10, -5, 100)
    #gluPerspective(90, 1, 1, 512)
    #glTranslated(0,0,-10)
    glMatrixMode(GL_MODELVIEW)
    

    
    
    drawHouse()

    
    glFlush()
    

def keyboard(key, x, y):
    
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'w':
        glMatrixMode(GL_PROJECTION)
        glTranslated(0,0,1)
        print("W is pressed, go forward")

    if key == b'a':
        glMatrixMode(GL_PROJECTION)
        glTranslated(1,0,0)
        print("A is pressed, go left")

    if key == b's':
        glMatrixMode(GL_PROJECTION)
        glTranslated(0,0,-1)
        print("S is pressed, go back")

    if key == b'd':
        glMatrixMode(GL_PROJECTION)
        glTranslated(-1,0,0)
        print("D is pressed, go right")

    if key == b'r':
        glTranslated(0,-1,0)
        print("R is pressed, go up")

    if key == b'f':
        glTranslated(0,1,0)
        print("F is pressed, go down")

    if key == b'q':
        glRotated(-1,0,1,0)
        print("Q is pressed, rotate right")

    if key == b'e':
        glRotated(1,0,1,0)
        print("E is pressed, rotate left")

    if key == b'h':
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1, 1, 512)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        print("H is pressed, return home")

    if key == b'o':
        glMatrixMode(GL_PROJECTION)
        glOrtho(-1, 1, -1, 1, 1, 200)
        print("O is pressed, orthographic projection")

    if key == b'p':
        glMatrixMode(GL_PROJECTION)
        gluPerspective(0,1,1,512)
        print("P is pressed, perspective projection")
  
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
