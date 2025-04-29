from chunks import Chunk
from settings import *

class World:
    def __init__(self):
        self.chunks = {}

    def get_chunk_key(self, x, z):
        return (int(x // CHUNK_SIZE), int(z // CHUNK_SIZE))

    def get_terrain_height(self, x, z):
        # Trouver le chunk correspondant
        chunk_x, chunk_z = self.get_chunk_key(x, z)
        key = (chunk_x, chunk_z)
        if key not in self.chunks:
            self.chunks[key] = Chunk(chunk_x, chunk_z)

        chunk = self.chunks[key]
        # Coordonnées locales dans le chunk
        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE

        # Trouver les indices des vertices entourant la position
        i0 = int(local_x)
        j0 = int(local_z)
        i1 = min(i0 + 1, CHUNK_SIZE)
        j1 = min(j0 + 1, CHUNK_SIZE)

        # Interpolation bilinéaire
        frac_x = local_x - i0
        frac_z = local_z - j0

        # Récupérer les hauteurs des quatre vertices
        v00 = chunk.vertices[i0 * (CHUNK_SIZE + 1) + j0][1]  # y de (i0, j0)
        v01 = chunk.vertices[i0 * (CHUNK_SIZE + 1) + j1][1]  # y de (i0, j1)
        v10 = chunk.vertices[i1 * (CHUNK_SIZE + 1) + j0][1]  # y de (i1, j0)
        v11 = chunk.vertices[i1 * (CHUNK_SIZE + 1) + j1][1]  # y de (i1, j1)

        # Interpolation en x pour les deux paires de vertices
        y0 = v00 * (1 - frac_x) + v10 * frac_x
        y1 = v01 * (1 - frac_x) + v11 * frac_x

        # Interpolation finale en z
        height = y0 * (1 - frac_z) + y1 * frac_z
        return height

    def render(self, player_pos):
        player_chunk_x, player_chunk_z = self.get_chunk_key(player_pos[0], player_pos[2])

        # Générer ou récupérer les chunks à proximité
        for cx in range(player_chunk_x - RENDER_DISTANCE, player_chunk_x + RENDER_DISTANCE + 1):
            for cz in range(player_chunk_z - RENDER_DISTANCE, player_chunk_z + RENDER_DISTANCE + 1):
                key = (cx, cz)
                if key not in self.chunks:
                    self.chunks[key] = Chunk(cx, cz)
                self.chunks[key].render()