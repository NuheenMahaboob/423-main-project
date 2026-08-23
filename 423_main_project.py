from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Import the temporary developer camera
from developer_camera import DeveloperCamera


# =========================================================
# Camera-related variables
# =========================================================

camera_pos = (0, 500, 500)

fovY = 120
GRID_LENGTH = 600
rand_var = 423


# =========================================================
# Developer Camera
# =========================================================

developer_camera = DeveloperCamera()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)


def draw_shapes():

    glPushMatrix()  # Save the current matrix state

    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)
    glutSolidCube(60)

    glTranslatef(0, 0, 100)
    glColor3f(0, 1, 0)
    glutSolidCube(60)

    glColor3f(1, 1, 0)
    glScalef(2, 2, 2)

    gluCylinder(
        gluNewQuadric(),
        40,
        5,
        150,
        10,
        10
    )

    glTranslatef(100, 0, 100)
    glRotatef(90, 0, 1, 0)

    gluCylinder(
        gluNewQuadric(),
        40,
        5,
        150,
        10,
        10
    )

    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100)

    gluSphere(
        gluNewQuadric(),
        80,
        10,
        10
    )

    glPopMatrix()  # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation,
    camera updates, cheat mode toggles, and developer mode.
    """

    # =====================================================
    # Toggle Developer Mode
    # =====================================================

    if key == b'l' or key == b'L':
        developer_camera.toggle()
        glutPostRedisplay()
        return

    # =====================================================
    # Normal Game Controls
    # =====================================================

    # Move forward
    # if key == b'w':

    # Move backward
    # if key == b's':

    # Rotate gun left
    # if key == b'a':

    # Rotate gun right
    # if key == b'd':

    # Toggle cheat mode
    # if key == b'c':

    # Toggle cheat vision
    # if key == b'v':

    # Reset the game
    # if key == b'r':

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    """
    Handles special key inputs.
    """

    global camera_pos

    # Don't allow normal camera controls
    # while Developer Mode is active
    if developer_camera.enabled:
        return

    x, y, z = camera_pos

    # Move camera up
    # if key == GLUT_KEY_UP:

    # Move camera down
    # if key == GLUT_KEY_DOWN:

    # Moving camera left
    if key == GLUT_KEY_LEFT:
        x -= 1

    # Moving camera right
    if key == GLUT_KEY_RIGHT:
        x += 1

    camera_pos = (x, y, z)

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs.
    """

    # =====================================================
    # Developer Mode Mouse Controls
    # =====================================================

    if developer_camera.enabled:

        developer_camera.mouse_button(
            button,
            state,
            x,
            y
        )

        return

    # =====================================================
    # Normal Game Mouse Controls
    # =====================================================

    # Left mouse button fires a bullet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

    # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

    pass


def mouseMotion(x, y):
    """
    Handles mouse dragging for Developer Mode.
    """

    if developer_camera.enabled:

        developer_camera.mouse_motion(
            x,
            y
        )


def setupCamera():
    """
    Configures the camera's projection and view settings.
    """

    # =====================================================
    # Projection Matrix
    # =====================================================

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        fovY,
        1.25,
        0.1,
        1500
    )

    # =====================================================
    # Model View Matrix
    # =====================================================

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # =====================================================
    # Developer Camera
    # =====================================================

    if developer_camera.enabled:

        developer_camera.apply_camera()

        return

    # =====================================================
    # Normal Game Camera
    # =====================================================

    x, y, z = camera_pos

    gluLookAt(
        x, y, z,        # Camera position
        0, 0, 0,        # Look-at target
        0, 0, 1         # Up vector
    )


def idle():
    """
    Idle function that runs continuously.
    """

    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene.
    """

    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    # Set viewport size
    glViewport(0, 0, 1000, 800)

    # Configure camera
    setupCamera()

    # =====================================================
    # Draw a random point
    # =====================================================

    glPointSize(20)

    glBegin(GL_POINTS)

    glVertex3f(
        -GRID_LENGTH,
        GRID_LENGTH,
        0
    )

    glEnd()

    # =====================================================
    # Draw the grid (game floor)
    # =====================================================

    glBegin(GL_QUADS)

    glColor3f(1, 1, 1)

    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)

    glColor3f(0.7, 0.5, 0.95)

    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)

    glEnd()

    # =====================================================
    # Display Game Information
    # =====================================================

    draw_text(
        10,
        770,
        f"A Random Fixed Position Text"
    )

    draw_text(
        10,
        740,
        f"See how the position and variable change?: {rand_var}"
    )

    # =====================================================
    # Draw Shapes
    # =====================================================

    draw_shapes()

    # Swap buffers
    glutSwapBuffers()


# =========================================================
# Main Function
# =========================================================

def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )

    glutInitWindowSize(1000, 800)

    glutInitWindowPosition(0, 0)

    glutCreateWindow(
        b"3D OpenGL Intro"
    )

    # =====================================================
    # Register Callbacks
    # =====================================================

    glutDisplayFunc(showScreen)

    glutKeyboardFunc(keyboardListener)

    glutSpecialFunc(specialKeyListener)

    glutMouseFunc(mouseListener)

    # Needed for dragging the mouse
    glutMotionFunc(mouseMotion)

    glutIdleFunc(idle)

    # Enter the GLUT main loop
    glutMainLoop()


if __name__ == "__main__":
    main()
