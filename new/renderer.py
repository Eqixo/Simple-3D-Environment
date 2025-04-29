from OpenGL.GL import *
from OpenGL.GLU import *
from settings import *

class Renderer:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.7, 1.0, 1.0)  # Ciel bleu clair
        self.setup_perspective()

    def setup_perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, RENDER_DISTANCE * CHUNK_SIZE * 2)
        glMatrixMode(GL_MODELVIEW)

    def setup_camera(self, player):
        glLoadIdentity()
        gluLookAt(
            player.position[0], player.position[1], player.position[2],
            player.position[0] + player.direction[0],
            player.position[1] + player.direction[1],
            player.position[2] + player.direction[2],
            0, 1, 0
        )