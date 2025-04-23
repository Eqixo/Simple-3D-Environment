import pygame
import numpy as np
from .base_camera import BaseCamera
from terrain import get_terrain_height

class Camera(BaseCamera):
    def __init__(self, config):
        super().__init__([0.0, 1.0, 0.0], 0.0, 0.0, config)
        self.velocity = [0.0, 0.0, 0.0]
        self.can_jump = True
        self.accumulated_time = 0.0  # Temps accumulé pour la physique

    def move(self, keys, vertices, num_points, dt):
        # Accumuler le temps écoulé
        self.accumulated_time += dt

        # Pas de temps fixe pour la physique
        physics_step = self.config.PHYSICS_STEP

        # Exécuter les étapes physiques tant qu'il y a assez de temps accumulé
        while self.accumulated_time >= physics_step:
            # Calculer le mouvement basé sur les touches
            move = [0.0, 0.0, 0.0]
            cos_x = np.cos(np.radians(self.pitch))
            cos_y = np.cos(np.radians(self.yaw))
            sin_y = np.sin(np.radians(self.yaw))
            if keys[pygame.K_z]:
                move[0] += cos_x * sin_y * self.config.CAMERA_SPEED
                move[2] -= cos_x * cos_y * self.config.CAMERA_SPEED
            if keys[pygame.K_s]:
                move[0] -= cos_x * sin_y * self.config.CAMERA_SPEED
                move[2] += cos_x * cos_y * self.config.CAMERA_SPEED
            if keys[pygame.K_d]:
                move[0] += cos_y * self.config.CAMERA_SPEED
                move[2] += sin_y * self.config.CAMERA_SPEED
            if keys[pygame.K_q]:
                move[0] -= cos_y * self.config.CAMERA_SPEED
                move[2] -= sin_y * self.config.CAMERA_SPEED
            if keys[pygame.K_LSHIFT]:
                move[1] -= self.config.CAMERA_SPEED

            # Appliquer la gravité avec le pas de temps fixe
            self.velocity[1] -= self.config.GRAVITY * physics_step

            # Appliquer le frottement et le mouvement (proportionnel au pas de temps)
            friction = 0.9 ** (physics_step / 0.016)  # Ajuster le frottement pour le pas fixe
            self.velocity = [v * friction + m * physics_step for v, m in zip(self.velocity, move)]

            # Mettre à jour la position
            self.pos = [p + v * physics_step for p, v in zip(self.pos, self.velocity)]

            # Vérifier la collision avec le terrain
            terrain_height = get_terrain_height(self.pos[0], self.pos[2], vertices, num_points)
            if self.pos[1] < terrain_height + 0.5:
                self.pos[1] = terrain_height + 0.5
                self.velocity[1] = 0.0
                self.can_jump = True
            else:
                self.can_jump = False

            # Réduire le temps accumulé
            self.accumulated_time -= physics_step

    def jump(self):
        if self.can_jump:
            self.velocity[1] += self.config.JUMP_SPEED
            self.can_jump = False