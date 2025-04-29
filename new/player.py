import math
import pygame
from pygame.locals import *
import numpy as np
from settings import *

class Player:
    def __init__(self):
        self.position = np.array([0.0, 5.0, 0.0])  # x, y, z
        self.yaw = 0.0  # Rotation horizontale
        self.pitch = 0.0  # Rotation verticale
        self.direction = np.array([0.0, 0.0, -1.0])  # Vecteur direction initial
        self.height_offset = 1.0  # Hauteur du joueur au-dessus du terrain

    def update(self, keys, mouse_dx, mouse_dy, world=None, delta_time=1.0/60.0):
        # Mise à jour de l'orientation avec la souris
        self.yaw -= mouse_dx * MOUSE_SENSITIVITY * delta_time * 60.0  # Ajuster pour la sensibilité
        self.pitch -= mouse_dy * MOUSE_SENSITIVITY * delta_time * 60.0  # Ajuster pour la sensibilité
        self.pitch = max(-math.pi / 2, min(math.pi / 2, self.pitch))  # Limiter le pitch

        # Calculer le vecteur direction
        self.direction = np.array([
            math.cos(self.pitch) * math.sin(self.yaw),
            math.sin(self.pitch),
            math.cos(self.pitch) * math.cos(self.yaw)
        ])

        # Mouvement avec les touches (AZERTY)
        move = np.array([0.0, 0.0, 0.0])
        if keys[K_z]:
            move += np.array([math.sin(self.yaw), 0, math.cos(self.yaw)])  # Avancer
        if keys[K_s]:
            move -= np.array([math.sin(self.yaw), 0, math.cos(self.yaw)])  # Reculer
        if keys[K_q]:
            move += np.array([math.cos(self.yaw), 0, -math.sin(self.yaw)])  # Strafe gauche
        if keys[K_d]:
            move -= np.array([math.cos(self.yaw), 0, -math.sin(self.yaw)])  # Strafe droite

        if np.linalg.norm(move) > 0:
            move = move / np.linalg.norm(move) * PLAYER_SPEED * delta_time
            self.position += move

        # Ajuster la hauteur du joueur en fonction du terrain
        if world:
            terrain_height = world.get_terrain_height(self.position[0], self.position[2])
            self.position[1] = terrain_height + self.height_offset