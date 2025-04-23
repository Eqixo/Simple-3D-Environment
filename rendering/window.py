import pygame
from pygame.locals import *
from OpenGL.GL import *
from shaders import create_shader_program
from config import Config

def init_window():
    config = Config()
    pygame.init()
    display = (1600, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Jeu 3D - Paysage Multinoise avec Shaders")
    glEnable(GL_DEPTH_TEST)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    font = pygame.font.SysFont("arial", 16)

    # Activer le brouillard
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, config.FOG_COLOR)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, config.FOG_START)
    glFogf(GL_FOG_END, config.FOG_END)

    # Initialiser le programme shader
    shader_program = create_shader_program('shaders/terrain.vert', 'shaders/terrain.frag')

    return shader_program, font