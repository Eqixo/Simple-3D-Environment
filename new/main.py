import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from player import Player
from world import World
from renderer import Renderer
from settings import *

def main():
    pygame.init()
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    renderer = Renderer()
    player = Player()
    world = World()
    wireframe = False

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            if event.type == KEYDOWN and event.key == K_w:
                wireframe = not wireframe
                if wireframe:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                else:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Calculer le delta time (en secondes)
        delta_time = clock.tick(60) / 1000.0  # Temps écoulé depuis la dernière frame

        keys = pygame.key.get_pressed()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        player.update(keys, mouse_dx, mouse_dy, world, delta_time)  # Passer delta_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        renderer.setup_camera(player)
        world.render(player.position)
        pygame.display.flip()

if __name__ == "__main__":
    main()