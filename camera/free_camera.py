import numpy as np
import pygame
from .base_camera import BaseCamera

class FreeCamera(BaseCamera):
    def __init__(self, pos, yaw, pitch, config):
        super().__init__(pos, yaw, pitch, config)
        self.accumulated_time = 0.0  # Temps accumulé pour la physique

    def move(self, keys, dt):
        # Accumuler le temps écoulé
        self.accumulated_time += dt
        physics_step = self.config.PHYSICS_STEP

        # Exécuter les étapes physiques
        while self.accumulated_time >= physics_step:
            move = [0.0, 0.0, 0.0]
            cos_x = np.cos(np.radians(self.pitch))
            cos_y = np.cos(np.radians(self.yaw))
            sin_y = np.sin(np.radians(self.yaw))
            if keys[pygame.K_z]:
                move[0] += cos_x * sin_y * self.config.FREECAM_SPEED
                move[2] -= cos_x * cos_y * self.config.FREECAM_SPEED
            if keys[pygame.K_s]:
                move[0] -= cos_x * sin_y * self.config.FREECAM_SPEED
                move[2] += cos_x * cos_y * self.config.FREECAM_SPEED
            if keys[pygame.K_d]:
                move[0] += cos_y * self.config.FREECAM_SPEED
                move[2] += sin_y * self.config.FREECAM_SPEED
            if keys[pygame.K_q]:
                move[0] -= cos_y * self.config.FREECAM_SPEED
                move[2] -= sin_y * self.config.FREECAM_SPEED
            if keys[pygame.K_SPACE]:
                move[1] += self.config.FREECAM_SPEED
            if keys[pygame.K_LSHIFT]:
                move[1] -= self.config.FREECAM_SPEED

            # Appliquer le frottement et le mouvement
            friction = 0.9 ** (physics_step / 0.016)
            self.velocity = [v * friction + m * physics_step for v, m in zip(self.velocity, move)]
            self.pos = [p + v * physics_step for p, v in zip(self.pos, self.velocity)]

            self.accumulated_time -= physics_step