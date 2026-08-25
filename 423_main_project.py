from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
import math

# Import the temporary developer camera
from developer_camera import DeveloperCamera


last_time = time.time()

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800

center_x = WINDOW_WIDTH // 2
center_y = WINDOW_HEIGHT // 2

window_x = (MONITOR_WIDTH - WINDOW_WIDTH) // 2
window_y = (MONITOR_HEIGHT - WINDOW_HEIGHT) // 2
# room details

ROOM_WIDTH = 800
ROOM_DEPTH = 800

WALL_HEIGHT = 150
WALL_THICKNESS = 20

# player details
player_x = 0
player_y = ROOM_DEPTH/2 - 30
player_z = 0
player_angle = 180
leg_height = 100
body_height = 100
head_rad = 20
player_height = leg_height+body_height+(head_rad/2)
leg_angle = 0
walk_phase = 0
walk_speed = 12  # leg swing speed

move_speed = 100
moving = False

mouse_locked = True
mouse_speed = 0.2

# player movement
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

# =========================================================
# Camera-related variables
# =========================================================

# Alien details
alien_x = 100
alien_y = 0
alien_z = 10+player_height/4
alien_angle = 0

human_alien_x = -100
human_alien_y = 0
human_alien_z = 10 + player_height/4
human_alien_angle = 0

CAMERA_HEIGHT = 70
# For first-person:
CAMERA_DISTANCE = 40
# For 3rd
# CAMERA_DISTANCE = 120

camera_pos = (player_x, player_y, CAMERA_HEIGHT)

fovY = 120
GRID_LENGTH = 600


# =========================================================
# Developer Camera
# =========================================================

developer_camera = DeveloperCamera()


def draw_alien(human):
    global alien_x, alien_y, alien_z
    global human_alien_x, human_alien_y, human_alien_z, human_alien_angle

    glPushMatrix()  # Save the current matrix state
    if human:
        glTranslatef(human_alien_x, human_alien_y, human_alien_z)
        glRotatef(human_alien_angle, 0, 0, 1)
    else:
        glTranslatef(alien_x, alien_y, alien_z)
        glRotatef(alien_angle, 0, 0, 1)

    # pura alien shrink
    glScalef(0.3, 0.3, 0.3)

    glPushMatrix()
    if human:
        glColor3f(0, 1, 0)
    else:
        glColor3f(1, 0, 0)

    glutSolidCube(100)

    glColor3f(1, 1, 0)
    glTranslatef(28, 50, 30)
    glRotatef(-135, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)

    glColor3f(1.0, 0.5, 0.0)
    glTranslatef(0, 3, 5)
    gluCylinder(gluNewQuadric(), 3, 0, 12, 20, 20)
    glTranslatef(0, -3, -5)
    glRotatef(135, 0, 1, 0)
    glTranslatef(-56, 0, 0)
    glRotatef(135, 0, 1, 0)

    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)

    glColor3f(1.0, 0.5, 0.0)
    glTranslatef(0, 3, 5)
    gluCylinder(gluNewQuadric(), 3, 0, 12, 20, 20)
    glTranslatef(0, -3, -5)
    glRotatef(-135, 0, 1, 0)

    # lower teeth
    glColor3f(1, 1, 0)
    glTranslatef(4, 0, -70)
    glRotatef(-45, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)

    # upper teeth
    glRotatef(45, 1, 0, 0)
    glTranslatef(6, 0, 30)
    glRotatef(-135, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(-12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(-12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(-12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(-12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glTranslatef(-12, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 0, 30, 20, 20)
    glPopMatrix()
    glPopMatrix()


def draw_player():
    global leg_height, body_height, head_rad, leg_angle

    glPushMatrix()  # Save the current matrix state
    glTranslatef(player_x, player_y, player_z)
    glRotatef(player_angle, 0, 0, 1)

    # pura player shrink+ektu baka
    glScalef(0.2, 0.2, 0.2)
    glRotatef(20, 0, 0, 1)
    glTranslatef(50, 0, 0)

    # if gameover:
    #     glTranslatef(0, 0, 60)
    #     glRotatef(-90, 1, 0, 0)
    # body
    glColor3f(0.333, 0.420, 0.184)
    glPushMatrix()
    glTranslatef(0, 0, leg_height)
    # parameters are: quadric, base radius, top radius, height, slices, stacks
    gluCylinder(gluNewQuadric(), 20, 35, body_height, 12, 12)
    glPopMatrix()  # Restore the previous matrix state
    # head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, (leg_height+body_height+head_rad))
    # parameters are: quadric, radius, slices, stacks
    gluSphere(gluNewQuadric(), head_rad, 20, 20)
    glPopMatrix()
   # leftarm
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(-40, 0, body_height+leg_height-15)
    # parameters are: quadric, radius, slices, stacks
    gluSphere(gluNewQuadric(), 15, 20, 20)

    glColor3f(1.0, 0.878, 0.741)
    glTranslatef(0, 15, 0)
    glRotatef(-90, 1, 0, 0)  # parameters are: angle, x, y, z
    glRotatef(45, 0, 1, 0)  # parameters are: angle, x, y, z
    # parameters are: quadric, base radius, top radius, height, slices, stacks
    gluCylinder(gluNewQuadric(), 8, 5, 60, 12, 12)
    glPopMatrix()

    # rightarm
    # right arm er ball
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(40, 0, body_height+leg_height-15)
    # parameters are: quadric, radius, slices, stacks
    gluSphere(gluNewQuadric(), 15, 20, 20)

    # gun
    glColor3f(0, 0, 0)
    glTranslatef(-40, 50, 10)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 5, 40, 12, 12)

    glTranslatef(0, -10, 5)
    gluCylinder(gluNewQuadric(), 5, 3, 20, 12, 12)
    glColor3f(1, 1, 1)
    glTranslatef(0, 0, 18)
    gluSphere(gluNewQuadric(), 3, 20, 20)

    glTranslatef(0, 0, -18)
    glTranslatef(0, 10, -5)
    glRotatef(90, 1, 0, 0)
    glTranslatef(+40, -50, -10)
    # main right arm
    glColor3f(1.0, 0.878, 0.741)
    glTranslatef(0, 15, 0)
    glRotatef(-90, 1, 0, 0)  # parameters are: angle, x, y, z
    glRotatef(-45, 0, 1, 0)
    # parameters are: quadric, base radius, top radius, height, slices, stacks
    gluCylinder(gluNewQuadric(), 8, 5, 60, 12, 12)
    glPopMatrix()

    # left leg
    glColor3f(0.2, 0.2, 0.2)

    glPushMatrix()

    glTranslatef(-12, 0, leg_height)
    glRotatef(leg_angle, 1, 0, 0)
    glRotatef(180, 1, 0, 0)

    gluCylinder(gluNewQuadric(), 8, 15, leg_height, 12, 12)

    glPopMatrix()


# right leg
    glPushMatrix()

    glTranslatef(12, 0, leg_height)
    glRotatef(-leg_angle, 1, 0, 0)
    glRotatef(180, 1, 0, 0)

    gluCylinder(gluNewQuadric(), 8, 15, leg_height, 12, 12)

    glPopMatrix()
    glPopMatrix()


def draw_room():

    global ROOM_WIDTH, ROOM_DEPTH, WALL_HEIGHT, WALL_THICKNESS

    # =========================================================
    # FLOOR
    # =========================================================

    glColor3f(0.25, 0.25, 0.25)

    glBegin(GL_QUADS)

    glVertex3f(
        -ROOM_WIDTH / 2,
        -ROOM_DEPTH / 2,
        0
    )

    glVertex3f(
        ROOM_WIDTH / 2,
        -ROOM_DEPTH / 2,
        0
    )

    glVertex3f(
        ROOM_WIDTH / 2,
        ROOM_DEPTH / 2,
        0
    )

    glVertex3f(
        -ROOM_WIDTH / 2,
        ROOM_DEPTH / 2,
        0
    )

    glEnd()

    # =========================================================
    # Celing
    # =========================================================

    glColor3f(0.25, 0.25, 0.25)

    glBegin(GL_QUADS)

    glVertex3f(
        -ROOM_WIDTH / 2,
        -ROOM_DEPTH / 2,
        WALL_HEIGHT
    )

    glVertex3f(
        ROOM_WIDTH / 2,
        -ROOM_DEPTH / 2,
        WALL_HEIGHT
    )

    glVertex3f(
        ROOM_WIDTH / 2,
        ROOM_DEPTH / 2,
        WALL_HEIGHT
    )

    glVertex3f(
        -ROOM_WIDTH / 2,
        ROOM_DEPTH / 2,
        WALL_HEIGHT
    )

    glEnd()

    # =========================================================
    # BACK WALL
    # =========================================================

    glPushMatrix()

    glColor3f(0.35, 0.35, 0.35)

    glTranslatef(
        0,
        ROOM_DEPTH / 2,
        WALL_HEIGHT / 2
    )

    glScalef(
        ROOM_WIDTH,
        WALL_THICKNESS,
        WALL_HEIGHT
    )

    glutSolidCube(1)

    glPopMatrix()

    # =========================================================
    # LEFT WALL
    # =========================================================

    glPushMatrix()

    glColor3f(0.30, 0.30, 0.30)

    glTranslatef(
        -ROOM_WIDTH / 2,
        0,
        WALL_HEIGHT / 2
    )

    glScalef(
        WALL_THICKNESS,
        ROOM_DEPTH,
        WALL_HEIGHT
    )

    glutSolidCube(1)

    glPopMatrix()

    # =========================================================
    # RIGHT WALL
    # =========================================================

    glPushMatrix()

    glColor3f(0.30, 0.30, 0.30)

    glTranslatef(
        ROOM_WIDTH / 2,
        0,
        WALL_HEIGHT / 2
    )

    glScalef(
        WALL_THICKNESS,
        ROOM_DEPTH,
        WALL_HEIGHT
    )

    glutSolidCube(1)

    glPopMatrix()

    # =========================================================
    # FRONT WALL
    # =========================================================

    glPushMatrix()

    glColor3f(0.35, 0.35, 0.35)

    glTranslatef(
        0,
        -ROOM_DEPTH / 2,
        WALL_HEIGHT / 2
    )

    glScalef(
        ROOM_WIDTH,
        WALL_THICKNESS,
        WALL_HEIGHT
    )

    glutSolidCube(1)

    glPopMatrix()


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
    global w_pressed, s_pressed, a_pressed, d_pressed
    global mouse_locked

    if key == b'w':
        w_pressed = True

    if key == b's':
        s_pressed = True

    if key == b'a':
        a_pressed = True

    if key == b'd':
        d_pressed = True

    # cursor lock/unlock by pressing ESC
    if key == b'\x1b':       # ESC key
        mouse_locked = not mouse_locked

        if mouse_locked:
            glutSetCursor(GLUT_CURSOR_NONE)
            glutWarpPointer(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        else:
            glutSetCursor(GLUT_CURSOR_LEFT_ARROW)

    # =====================================================
    # Toggle Developer Mode
    # =====================================================

    if key == b'l' or key == b'L':
        developer_camera.toggle()
        glutPostRedisplay()
        return

    glutPostRedisplay()

# Extra add kortesi


def keyboardUpListener(key, x, y):
    global w_pressed, s_pressed, a_pressed, d_pressed, moving

    if key == b'w':
        w_pressed = False
        moving = False

    if key == b's':
        s_pressed = False
        moving = False

    if key == b'a':
        a_pressed = False
        moving = False

    if key == b'd':
        d_pressed = False
        moving = False


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

# Extra add kortesi


def mouseMotion(x, y):
    global player_angle, center_x, center_y

    global mouse_locked, mouse_speed

    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2

    if not mouse_locked:
        return

    dx = x - center_x

    if dx != 0:
        player_angle -= dx * mouse_speed

    glutWarpPointer(center_x, center_y)

    if developer_camera.enabled:

        developer_camera.mouse_motion(
            x,
            y
        )


def setupCamera():
    """
    Configures the camera's projection and view settings.
    """
    global camera_pos, CAMERA_DISTANCE, CAMERA_HEIGHT
    # =====================================================
    # Projection Matrix
    # =====================================================

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        fovY,
        WINDOW_WIDTH/WINDOW_HEIGHT,
        0.1,
        2000
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

    angle = math.radians(player_angle)

    # Player's forward direction
    forward_x = -math.sin(angle)
    forward_y = math.cos(angle)

    # Camera goes BEHIND the player
    camera_x = player_x - forward_x * CAMERA_DISTANCE
    camera_y = player_y - forward_y * CAMERA_DISTANCE
    camera_z = CAMERA_HEIGHT

    camera_pos = (
        camera_x,
        camera_y,
        camera_z
    )

    # Look some distance in front of the player
    look_distance = 100

    target_x = player_x
    target_y = player_y
    target_z = 70

    gluLookAt(
        camera_x,
        camera_y,
        camera_z,

        target_x,
        target_y,
        target_z,

        0,
        0,
        1
    )


def idle():
    global player_x, player_y, walk_phase, leg_angle, walk_speed
    global move_speed, moving
    global last_time
    global camera_pos

    # player movement
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    # Prevent huge jumps if the program freezes
    if delta_time > 0.1:
        delta_time = 0.1

    angle = math.radians(player_angle)

    # Player's forward direction
    #
    # player_angle = 0
    #       ↓
    #       +Y
    #
    forward_x = -math.sin(angle)
    forward_y = math.cos(angle)

    # Player's right direction
    right_x = math.cos(angle)
    right_y = math.sin(angle)

    moving = False
    # mouse er shathe shathe change jeno hoi

    # -------------------------
    # W = FORWARD
    # -------------------------

    if w_pressed:
        player_x += forward_x * move_speed * delta_time
        player_y += forward_y * move_speed * delta_time

        moving = True

    # -------------------------
    # S = BACKWARD
    # -------------------------

    if s_pressed:
        player_x -= forward_x * move_speed * delta_time
        player_y -= forward_y * move_speed * delta_time

        moving = True

    # -------------------------
    # D = RIGHT
    # -------------------------

    if d_pressed:
        player_x += right_x * move_speed * delta_time
        player_y += right_y * move_speed * delta_time

        moving = True

    # -------------------------
    # A = LEFT
    # -------------------------

    if a_pressed:
        player_x -= right_x * move_speed * delta_time
        player_y -= right_y * move_speed * delta_time

        moving = True

    # Walking animation
    if moving:
        walk_phase += walk_speed * delta_time
        leg_angle = 30 * math.sin(walk_phase)
    else:
        leg_angle = 0

    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene.
    """

    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    # Set viewport size
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Configure camera
    setupCamera()

    # =====================================================
    # Display Game Information
    # =====================================================
    x, y, z = camera_pos
    draw_text(10, 770, f"{x} {y} {z}")

    # =====================================================
    # Draw Shapes
    # =====================================================

    # draw_shapes()
    draw_room()
    draw_alien(False)
    draw_alien(True)
    draw_player()

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

    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    glutInitWindowPosition(window_x, window_y)

    glutCreateWindow(
        b"3D OpenGL Intro"
    )

    # =====================================================
    # Register Callbacks
    # =====================================================
    glutDisplayFunc(showScreen)

    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)  # Extra add kortesi

    glutSpecialFunc(specialKeyListener)

    glutMouseFunc(mouseListener)

    # Needed for dragging the mouse
    glutMotionFunc(mouseMotion)  # Extra add kortesi
    glutPassiveMotionFunc(mouseMotion)  # Extra add kortesi

    glutIdleFunc(idle)

    # Enter the GLUT main loop
    glutMainLoop()


if __name__ == "__main__":
    main()
