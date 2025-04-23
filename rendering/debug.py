from OpenGL.GL import *
from .matrices import is_box_in_frustum
import pygame

def render_bounding_boxes(chunks, planes, model_view_matrix, player_pos=None):
    glDisable(GL_LIGHTING)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixf(model_view_matrix.T.flatten())

    glColor3f(1.0, 0.0, 0.0) if player_pos is not None else glColor3f(0.0, 1.0, 0.0)
    for chunk in chunks:
        if is_box_in_frustum(planes, chunk['min_x'], chunk['max_x'], chunk['min_y'], chunk['max_y'], chunk['min_z'], chunk['max_z']):
            min_x, max_x = chunk['min_x'], chunk['max_x']
            min_y, max_y = chunk['min_y'], chunk['max_y']
            min_z, max_z = chunk['min_z'], chunk['max_z']
            glBegin(GL_LINE_LOOP)
            glVertex3f(min_x, min_y, min_z)
            glVertex3f(max_x, min_y, min_z)
            glVertex3f(max_x, min_y, max_z)
            glVertex3f(min_x, min_y, max_z)
            glEnd()
            glBegin(GL_LINE_LOOP)
            glVertex3f(min_x, max_y, min_z)
            glVertex3f(max_x, max_y, min_z)
            glVertex3f(max_x, max_y, max_z)
            glVertex3f(min_x, max_y, max_z)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(min_x, min_y, min_z)
            glVertex3f(min_x, max_y, min_z)
            glVertex3f(max_x, min_y, min_z)
            glVertex3f(max_x, max_y, min_z)
            glVertex3f(max_x, min_y, max_z)
            glVertex3f(max_x, max_y, max_z)
            glVertex3f(min_x, min_y, max_z)
            glVertex3f(min_x, max_y, max_z)
            glEnd()
    
    if player_pos is not None:
        glPointSize(10.0)
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_POINTS)
        glVertex3f(player_pos[0], player_pos[1], player_pos[2])
        glEnd()
    
    glPopMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_LIGHTING)

def render_coordinates(active_pos, frozen_pos, fps, frame_time, font, visible_chunks=None):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1600, 900, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_FOG)
    text = f"Active: X: {active_pos[0]:.2f}, Y: {active_pos[1]:.2f}, Z: {active_pos[2]:.2f}"
    if frozen_pos is not None:
        text += f" | Frozen: X: {frozen_pos[0]:.2f}, Y: {frozen_pos[1]:.2f}, Z: {frozen_pos[2]:.2f}"
    text += f" | FPS: {fps:.2f} | Frame Time: {frame_time:.2f} ms"
    if visible_chunks is not None:
        text += f" | Chunks: {visible_chunks}"
    surface = font.render(text, True, (255, 255, 255))
    data = pygame.image.tostring(surface, "RGBA", True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2i(10, 880)
    glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)
    glDisable(GL_BLEND)
    glEnable(GL_FOG)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def render_light_trajectory(light_trajectory):
    glDisable(GL_LIGHTING)
    glPointSize(3.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    for pos in light_trajectory:
        glVertex3fv(pos)
    glEnd()
    if light_trajectory:
        glPointSize(10.0)
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3fv(light_trajectory[-1])
        glEnd()
    glEnable(GL_LIGHTING)