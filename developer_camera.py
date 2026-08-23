from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math


class DeveloperCamera:

    def __init__(self):

        # Developer mode starts OFF
        self.enabled = False

        # =====================================================
        # CAMERA TARGET
        # This is the point the camera rotates around
        # =====================================================

        self.target_x = 0
        self.target_y = 0
        self.target_z = 0

        # =====================================================
        # ORBIT CAMERA SETTINGS
        # =====================================================

        # Distance from camera to target
        self.distance = 700

        # Horizontal and vertical viewing angles
        self.yaw = 45
        self.pitch = 35

        # =====================================================
        # MOUSE TRACKING
        # =====================================================

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # Track whether left mouse button is being held
        self.left_mouse_pressed = False

    # =========================================================
    # TOGGLE DEVELOPER MODE
    # =========================================================

    def toggle(self):

        self.enabled = not self.enabled

        if self.enabled:
            print("Developer Mode: ON")

        else:
            print("Developer Mode: OFF")

    # =========================================================
    # MOUSE BUTTON
    # =========================================================

    def mouse_button(self, button, state, x, y):

        if not self.enabled:
            return

        # =====================================================
        # LEFT MOUSE BUTTON
        # =====================================================

        if button == GLUT_LEFT_BUTTON:

            if state == GLUT_DOWN:

                self.left_mouse_pressed = True

                self.last_mouse_x = x
                self.last_mouse_y = y

            elif state == GLUT_UP:

                self.left_mouse_pressed = False

        # =====================================================
        # MOUSE WHEEL = ZOOM
        # =====================================================

        if state == GLUT_DOWN:

            # Wheel forward
            if button == 3:

                self.distance -= 30

            # Wheel backward
            elif button == 4:

                self.distance += 30

        # Prevent camera from getting too close
        self.distance = max(10, self.distance)

    # =========================================================
    # MOUSE DRAGGING
    # =========================================================

    def mouse_motion(self, x, y):

        if not self.enabled:
            return

        # Only move camera while left mouse button is pressed
        if not self.left_mouse_pressed:
            return

        # Mouse movement
        dx = x - self.last_mouse_x
        dy = y - self.last_mouse_y

        # Get modifier keys
        modifiers = glutGetModifiers()

        # =====================================================
        # ALT + LEFT MOUSE = ORBIT
        # =====================================================

        if modifiers & GLUT_ACTIVE_ALT:

            self.yaw += dx * 0.5
            self.pitch += dy * 0.5

            # Prevent camera from flipping completely
            self.pitch = max(
                -89,
                min(89, self.pitch)
            )

        # =====================================================
        # LEFT MOUSE ONLY = PAN
        # =====================================================

        else:

            self.pan(
                dx,
                dy
            )

        # Update last mouse position
        self.last_mouse_x = x
        self.last_mouse_y = y

    # =========================================================
    # PAN CAMERA
    # =========================================================

    def pan(self, dx, dy):

        # Convert yaw angle to radians
        yaw_rad = math.radians(self.yaw)

        # =====================================================
        # CAMERA'S LOCAL RIGHT DIRECTION
        # =====================================================

        right_x = math.cos(yaw_rad)
        right_y = math.sin(yaw_rad)

        # Pan speed depends on zoom distance
        pan_speed = self.distance * 0.002

        # Move target sideways
        self.target_x -= dx * right_x * pan_speed
        self.target_y -= dx * right_y * pan_speed

        # Move target vertically
        self.target_z += dy * pan_speed

    # =========================================================
    # CALCULATE CAMERA POSITION
    # =========================================================

    def get_camera_position(self):

        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        # Camera position calculated around the target
        camera_x = (
            self.target_x
            + self.distance
            * math.cos(pitch_rad)
            * math.cos(yaw_rad)
        )

        camera_y = (
            self.target_y
            + self.distance
            * math.cos(pitch_rad)
            * math.sin(yaw_rad)
        )

        camera_z = (
            self.target_z
            + self.distance
            * math.sin(pitch_rad)
        )

        return (
            camera_x,
            camera_y,
            camera_z
        )

    # =========================================================
    # APPLY CAMERA
    # =========================================================

    def apply_camera(self):

        # Calculate current camera position
        camera_x, camera_y, camera_z = self.get_camera_position()

        # Look at the target
        gluLookAt(

            camera_x,
            camera_y,
            camera_z,

            self.target_x,
            self.target_y,
            self.target_z,

            0,
            0,
            1
        )
