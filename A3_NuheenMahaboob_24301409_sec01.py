from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
# Camera-related variables
camera_pos = (0, 300, 500)
cam_angle = 90
cam_rad = 300
cam_height = 500
cam_rot_speed = 2
cam_height_speed = 10

fovY = 120  # Field of view
aspectRatio = WINDOW_WIDTH/WINDOW_HEIGHT
znear = 0.1
zfar = 1500
GRID_LENGTH = 600  # Length of grid lines

# displayinfo
life = 5
score = 0
missedbullets = 0


# floor
tile_size = 60
side = 13
tile_colour1 = (1, 1, 1)
tile_colour2 = (0.7, 0.5, 0.95)
boundary_height = 50
right_boundary_color = (0, 1, 0)
left_boundary_color = (0, 0, 1)
top_boundary_color = (0, 1, 1)
bottom_boundary_color = (1, 1, 1)

# playerdraw
player_x = 0
player_y = 0
player_z = 0
player_speed = 2000
player_angle = 0
player_rot_speed = 10
playerrad = 35

# bulletdraw
bullets = []
bullet_size = 8
bullet_speed = 600
bulletcolor = (1, 0, 0)
max_bulletmiss = 10

# enemydraw
enemies = []
enemycount = 20
enemy_speed = 15
enemy_base_rad = 25
pulsing = 2
enemy_headcolor = (1, 0, 0)
enemy_bodycolor = (0, 0, 0)

# Gamer imp var
gameover = False
first_POV = False
cheatmode = False
cheat_enemy_view = False
cheatrotate = 90
cheat_shoot = 0.2
cheat_shoot_time = 0
cheatangle = 4
enemyfollowangle = 0
last_time = time.time()
delta_time = 0


def draw_player():
    glPushMatrix()  # Save the current matrix state
    glTranslatef(player_x, player_y, player_z)
    glRotatef(player_angle, 0, 0, 1)
    # pura player shrink
    glScalef(0.5, 0.5, 0.5)
    if gameover:
        glTranslatef(0, 0, 60)
        glRotatef(-90, 1, 0, 0)
    # body
    glColor3f(0.333, 0.420, 0.184)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(60, 45, 100)
    glutSolidCube(1)  # Take cube size as the parameter
    glPopMatrix()  # Restore the previous matrix state
    # head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 115)
    # parameters are: quadric, radius, slices, stacks
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()
   # leftarm
    glColor3f(1.0, 0.878, 0.741)
    glPushMatrix()
    glTranslatef(-25, 20, 80)
    glRotatef(-90, 1, 0, 0)  # parameters are: angle, x, y, z
    # parameters are: quadric, base radius, top radius, height, slices, stacks
    gluCylinder(gluNewQuadric(), 8, 3, 30, 12, 12)
    glPopMatrix()
    # rightarm
    glPushMatrix()
    glTranslatef(25, 20, 80)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 3, 30, 12, 12)
    glPopMatrix()
    # gun
    glColor3f(0.753, 0.753, 0.753)
    glPushMatrix()
    glTranslatef(0, 20, 80)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 3, 80, 12, 12)
    glPopMatrix()
    # leftleg
    glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(-25, 0, -50)
    gluCylinder(gluNewQuadric(), 8, 14, 50, 12, 12)
    glPopMatrix()
    # rightleg
    glPushMatrix()
    glTranslatef(25, 0, -50)
    gluCylinder(gluNewQuadric(), 8, 14, 50, 12, 12)
    glPopMatrix()

    glPopMatrix()  # same world


def draw_floor_and_boundary():
    global tile_size, side, tile_colour1, tile_colour2
    global boundary_height
    # ground
    box = -(side*tile_size)/2
    for row in range(side):
        for col in range(side):
            x1 = box + col * tile_size
            y1 = box + row * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size

            if (row+col) % 2 == 0:
                glColor3f(*tile_colour1)
            else:
                glColor3f(*tile_colour2)
            glBegin(GL_QUADS)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
            glEnd()
    # walls
    sidelength = side * tile_size
    half = sidelength/2

    # left
    glColor3f(*right_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(-half,  half, 0)
    glVertex3f(-half, -half, 0)
    glVertex3f(-half, -half, boundary_height)
    glVertex3f(-half,  half, boundary_height)
    glEnd()
   # right
    glColor3f(*left_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(half, -half, 0)
    glVertex3f(half,  half, 0)
    glVertex3f(half,  half, boundary_height)
    glVertex3f(half, -half, boundary_height)
    glEnd()
    # bottom
    glColor3f(*top_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(half, -half, 0)
    glVertex3f(-half, -half, 0)
    glVertex3f(-half, -half, boundary_height)
    glVertex3f(half, -half, boundary_height)
    glEnd()
    # top
    glColor3f(*bottom_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(-half, half, 0)
    glVertex3f(half, half, 0)
    glVertex3f(half, half, boundary_height)
    glVertex3f(-half, half, boundary_height)
    glEnd()


def enemy_rad(enemy):
    return enemy_base_rad * (0.8 + 0.2 * math.sin(enemy['phase']))


def random_enemy_position():
    limit = (side * tile_size) / 2 - 40
    while True:
        x = random.uniform(-limit, limit)
        y = random.uniform(-limit, limit)
        dx = x - player_x
        dy = y - player_y
        if math.sqrt(dx*dx + dy*dy) > 200:
            return x, y


def respawn(enemy):
    x, y = random_enemy_position()
    enemy['x'] = x
    enemy['y'] = y
    enemy['phase'] = random.uniform(0, 2 * math.pi)


def spawnenmy():
    global enemies
    enemies = []
    for i in range(enemycount):
        x, y = random_enemy_position()
        enemies.append(
            {'x': x, 'y': y, 'phase': random.uniform(0, 2 * math.pi)})


def draw_enemies():
    for enemy in enemies:
        rad = enemy_rad(enemy)
        glPushMatrix()
        glTranslatef(enemy['x'], enemy['y'], rad)
        glColor3f(*enemy_headcolor)
        gluSphere(gluNewQuadric(), rad, 20, 20)
        glColor3f(*enemy_bodycolor)
        glTranslatef(0, 0, rad)
        gluSphere(gluNewQuadric(), rad * 0.5, 20, 20)

        glPopMatrix()


def draw_bullets():
    glColor3f(*bulletcolor)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['x'], bullet['y'], bullet['z'])
        glutSolidCube(bullet_size)
        glPopMatrix()


def gundirect():
    angle = math.radians(player_angle)
    return -math.sin(angle), math.cos(angle)


def fire_bullet():
    if gameover:
        return
    dir_x, dir_y = gundirect()
    bullets.append({'x': player_x + dir_x * 35,
                    'y': player_y + dir_y * 35,
                    'z': player_z + 30,
                    'dx': dir_x,
                    'dy': dir_y})
    print("Player Bullet fired!")


def enemyinsight():
    dir_x, dir_y = gundirect()
    for enemy in enemies:
        ex = enemy['x'] - player_x
        ey = enemy['y'] - player_y
        distance = math.sqrt(ex*ex + ey*ey)
        if distance == 0:
            return True
        dot = (dir_x * ex + dir_y * ey) / distance
        dot = max(-1, min(1, dot))
        if math.degrees(math.acos(dot)) < cheatangle:
            return True
    return False


def update_cheatmode(delta):
    global player_angle, cheat_shoot_time, enemyfollowangle
    if not cheatmode:
        return
    player_angle = (player_angle + cheatrotate * delta) % 360
    if cheat_enemy_view:
        enemyfollowangle = player_angle

    cheat_shoot_time -= delta
    if cheat_shoot_time <= 0 and enemyinsight():
        fire_bullet()
        cheat_shoot_time = cheat_shoot


def update_bullets(delta):

    global missedbullets
    limit = (side * tile_size) / 2
    leftb = []
    for bullet in bullets:
        bullet['x'] += bullet['dx'] * bullet_speed * delta
        bullet['y'] += bullet['dy'] * bullet_speed * delta
        if abs(bullet['x']) > limit or abs(bullet['y']) > limit:
            missedbullets += 1
            print("Bullet missed:", missedbullets)
        else:
            leftb.append(bullet)

    bullets[:] = leftb


def update_enemies(delta):
    for enemy in enemies:
        enemy['phase'] += pulsing * delta
        dx = player_x - enemy['x']
        dy = player_y - enemy['y']
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            enemy['x'] += (dx / distance) * enemy_speed * delta
            enemy['y'] += (dy / distance) * enemy_speed * delta


def check_bullet_enemy_collision():
    global score
    leftb = []
    for bullet in bullets:
        hit = False
        for enemy in enemies:
            rad = enemy_rad(enemy)
            dx = bullet['x'] - enemy['x']
            dy = bullet['y'] - enemy['y']
            dz = bullet['z'] - rad
            if (dx*dx + dy*dy + dz*dz)**0.5 < rad + bullet_size:  # eucledeand distancetaken
                hit = True
                score += 1
                respawn(enemy)
                break
        if not hit:
            leftb.append(bullet)
    bullets[:] = leftb  # removing porer bullet


def check_player_enemy_collision():
    global life
    for enemy in enemies:
        rad = enemy_rad(enemy)
        dx = player_x - enemy['x']
        dy = player_y - enemy['y']
        if math.sqrt(dx*dx + dy*dy) < rad + playerrad:
            life -= 1
            print("Remaining Player Life:", life)
            respawn(enemy)


def update_game(delta):
    global gameover
    if gameover:
        return
    update_cheatmode(delta)
    update_bullets(delta)
    update_enemies(delta)
    check_bullet_enemy_collision()
    check_player_enemy_collision()
    if life <= 0 or missedbullets >= max_bulletmiss:
        gameover = True


def reset():
    global life, score, missedbullets
    global player_x, player_y, player_z, player_angle
    global gameover, cheatmode, cheat_enemy_view, cheat_shoot_time
    global enemyfollowangle
    life = 5
    score = 0
    missedbullets = 0
    player_x = 0
    player_y = 0
    player_z = 0
    player_angle = 0
    gameover = False
    cheatmode = False
    cheat_enemy_view = False
    cheat_shoot_time = 0
    enemyfollowangle = 0
    bullets[:] = []
    spawnenmy()
    print("Remaining Player Life:", life)


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

   # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

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


def keyboardListener(key, x, y):
    global player_x, player_y
    global player_angle
    global cheatmode, cheat_enemy_view, enemyfollowangle
    if key == b'r':
        reset()
        return
    if key == b'c':
        cheatmode = not cheatmode
        if not cheatmode:
            cheat_enemy_view = False
    if key == b'v':
        if cheatmode:
            cheat_enemy_view = not cheat_enemy_view
            enemyfollowangle = player_angle
    if gameover:
        return

    dir_x, dir_y = gundirect()
    movement = (side * tile_size) / 2 - 40

    if key == b'w':
        player_x += dir_x * player_speed * delta_time
        player_y += dir_y * player_speed * delta_time

    if key == b's':
        player_x -= dir_x * player_speed * delta_time
        player_y -= dir_y * player_speed * delta_time

    if key == b'a' and not cheatmode:
        player_angle = (player_angle + player_rot_speed) % 360

    if key == b'd' and not cheatmode:
        player_angle = (player_angle - player_rot_speed) % 360

    player_x = max(-movement, min(movement, player_x))
    player_y = max(-movement, min(movement, player_y))


def specialKeyListener(key, x, y):
    global camera_pos, cam_angle, cam_height
    if key == GLUT_KEY_UP:
        cam_height += cam_height_speed

    if key == GLUT_KEY_DOWN:
        cam_height -= cam_height_speed

    if key == GLUT_KEY_LEFT:
        cam_angle -= cam_rot_speed

    if key == GLUT_KEY_RIGHT:
        cam_angle += cam_rot_speed

    angle = math.radians(cam_angle)
    camera_x = cam_rad * math.cos(angle)
    camera_y = cam_rad * math.sin(angle)
    camera_pos = (camera_x, camera_y, cam_height)


def mouseListener(button, state, x, y):
    global first_POV
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_POV = not first_POV


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    # Think why aspect ration is 1.25?
    gluPerspective(fovY, aspectRatio, znear, zfar)
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    if first_POV:

        if cheatmode and not cheat_enemy_view:
            view_angle = player_angle
        else:
            view_angle = player_angle
        angle = math.radians(view_angle)
        dir_x = -math.sin(angle)
        dir_y = math.cos(angle)
        eye_x = player_x + dir_x * 30
        eye_y = player_y + dir_y * 30
        eye_z = player_z + 90
        gluLookAt(eye_x, eye_y, eye_z,
                  eye_x + dir_x * 200, eye_y + dir_y * 200, eye_z - 40,
                  0, 0, 1)
        return
    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    if delta_time > 0.05:
        delta_time = 0.05

    update_game(delta_time)
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setupCamera()  # Configure camera perspective
    draw_floor_and_boundary()
    if gameover:
        draw_text(10, 770, "GAMEOVER. Your Score is " + str(score) + ".")
        draw_text(10, 740, "Press R to reset the Game.")
    else:
        draw_text(10, 770, f"Player Life Remaining: {life}")
        draw_text(10, 740, f"Game Score : {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missedbullets}")
    draw_player()
    draw_enemies()
    draw_bullets()
    glutSwapBuffers()

# Main function to set up OpenGL window and loop


def main():
    glutInit()
    # Double buffering, RGB color, depth test
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    spawnenmy()
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    # Register the idle function to move the bullet automatically
    glutIdleFunc(idle)

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
