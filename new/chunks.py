from OpenGL.GL import *
import numpy as np
from noise import pnoise2
from settings import *

class Chunk:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.vertices = []
        self.colors = []
        self.indices = []
        self.vbo = None
        self.cbo = None
        self.ibo = None
        self.generate_terrain()
        self.setup_vbo()

    def generate_terrain(self):
        # Générer une grille de CHUNK_SIZE + 1 x CHUNK_SIZE + 1 vertices
        for i in range(CHUNK_SIZE + 1):
            for j in range(CHUNK_SIZE + 1):
                x = self.x * CHUNK_SIZE + i
                z = self.z * CHUNK_SIZE + j
                # Noise pour le biome
                biome_noise = pnoise2(x * BIOME_NOISE_SCALE, z * BIOME_NOISE_SCALE)
                # Déterminer le biome en fonction de la noise
                biome_index = int((biome_noise + 1) / 2 * len(BIOMES))  # Normaliser [0, 1] et mapper
                biome_index = min(biome_index, len(BIOMES) - 1)  # Limiter à l'index max
                biome = BIOMES[biome_index]
                
                # Calculer la hauteur avec la noise, modulée par le biome
                height_noise = pnoise2(x * NOISE_SCALE, z * NOISE_SCALE)
                y = height_noise * WORLD_HEIGHT / 2 * biome["height_scale"] + WORLD_HEIGHT / 2
                self.vertices.append((i, y, j))

                # Déterminer la couleur en fonction de la hauteur
                for b in BIOMES:
                    if y <= b["max_height"]:
                        self.colors.append(b["color"])
                        break

        # Créer les indices pour les triangles
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                v0 = i * (CHUNK_SIZE + 1) + j
                v1 = v0 + 1
                v2 = (i + 1) * (CHUNK_SIZE + 1) + j
                v3 = v2 + 1
                # Deux triangles par quad
                self.indices.extend([v0, v1, v2, v1, v3, v2])

    def setup_vbo(self):
        # Convertir les vertices et couleurs en tableaux numpy
        vertex_array = np.array(self.vertices, dtype=np.float32).flatten()
        color_array = np.array(self.colors, dtype=np.float32).flatten()
        index_array = np.array(self.indices, dtype=np.uint32)

        # Créer le VBO pour les vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_array.nbytes, vertex_array, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # Créer le CBO pour les couleurs
        self.cbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
        glBufferData(GL_ARRAY_BUFFER, color_array.nbytes, color_array, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # Créer le IBO pour les indices
        self.ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_array.nbytes, index_array, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def render(self):
        glPushMatrix()
        glTranslatef(self.x * CHUNK_SIZE, 0, self.z * CHUNK_SIZE)
        
        # Configurer le VBO pour les vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glEnableClientState(GL_VERTEX_ARRAY)

        # Configurer le CBO pour les couleurs
        glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
        glColorPointer(3, GL_FLOAT, 0, None)
        glEnableClientState(GL_COLOR_ARRAY)

        # Configurer le IBO et dessiner
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        # Désactiver les états
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        
        glPopMatrix()