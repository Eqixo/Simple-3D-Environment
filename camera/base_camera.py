import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from rendering import build_perspective_matrix, build_view_matrix

class BaseCamera:
    def __init__(self, pos, yaw, pitch, config):
        self.pos = pos
        self.yaw = yaw
        self.pitch = pitch
        self.velocity = [0.0, 0.0, 0.0]
        self.config = config

    def rotate(self):
        if pygame.mouse.get_focused():
            rel = pygame.mouse.get_rel()
            if rel == (0, 0):
                pygame.mouse.set_pos(pygame.display.get_surface().get_width() // 2, pygame.display.get_surface().get_height() // 2)
            else:
                self.yaw += rel[0] * self.config.MOUSE_SENSITIVITY
                self.pitch -= rel[1] * self.config.MOUSE_SENSITIVITY
                self.pitch = np.clip(self.pitch, -90, 90)

    def update(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75, 1600 / 900, 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])
        proj_matrix = build_perspective_matrix(75, 1600/900, 0.1, 500.0)
        model_matrix = build_view_matrix(self.pos, self.yaw, self.pitch)
        return proj_matrix, model_matrix