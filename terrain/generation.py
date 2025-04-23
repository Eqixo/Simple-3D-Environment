import noise
import numpy as np
from .chunks import generate_vertices_and_colors, compute_normals, generate_chunk, get_terrain_height
from .occlusion import compute_occlusion, smooth_heights

def generate_heights(num_points, config):
    heights = np.zeros((num_points, num_points))
    biome_noise_map = np.zeros((num_points, num_points))
    global_min_y = float('inf')
    global_max_y = float('-inf')

    for i in range(num_points):
        for j in range(num_points):
            x = i * config.TERRAIN_RES - config.TERRAIN_SIZE / 2
            z = j * config.TERRAIN_RES - config.TERRAIN_SIZE / 2

            # Bruit de biome
            biome_noise = 0.0
            amplitude = 1.0
            frequency = 1.0
            for _ in range(config.OCTAVES):
                biome_noise += amplitude * noise.pnoise2(
                    x * frequency * config.BIOME_SCALE + config.SEED,
                    z * frequency * config.BIOME_SCALE + config.SEED,
                    base=config.SEED
                )
                amplitude *= config.PERSISTENCE
                frequency *= config.LACUNARITY
            biome_noise = (biome_noise + 1.0) / 2.0
            biome_noise_map[i, j] = biome_noise

            # Bruit de hauteur de base
            base_height = 0.0
            amplitude = 1.0
            frequency = 1.0
            for _ in range(config.OCTAVES):
                base_height += amplitude * noise.pnoise2(
                    x * frequency * config.BASE_HEIGHT_SCALE + config.SEED + 1000,
                    z * frequency * config.BASE_HEIGHT_SCALE + config.SEED + 1000,
                    base=config.SEED
                )
                amplitude *= config.PERSISTENCE
                frequency *= config.LACUNARITY
            base_height = (base_height + 1.0) / 2.0

            # Bruit de détail
            detail_noise = 0.0
            amplitude = 1.0
            frequency = 1.0
            for _ in range(config.OCTAVES):
                detail_noise += amplitude * noise.pnoise2(
                    x * frequency * config.DETAIL_SCALE + config.SEED + 2000,
                    z * frequency * config.DETAIL_SCALE + config.SEED + 2000,
                    base=config.SEED
                )
                amplitude *= config.PERSISTENCE
                frequency *= config.LACUNARITY

            # Déterminer le biome et ajuster la hauteur
            y = base_height
            if biome_noise < 0.3:  # Océan
                y = -1.0 - config.OCEAN_DEPTH * abs(detail_noise)
            elif biome_noise < 0.6:  # Plaine
                y = 0.3 + config.PLAINS_FLATNESS * abs(detail_noise)
            else:  # Montagne
                y = 1.0 + config.MOUNTAIN_INTENSITY * detail_noise

            y = y * config.HEIGHT_SCALE - 10.0
            y = max(-64.0, min(64.0, y))
            heights[i, j] = y
            global_min_y = min(global_min_y, y)
            global_max_y = max(global_max_y, y)

    return heights, biome_noise_map, global_min_y, global_max_y

def generate_terrain():
    from config import Config
    config = Config()
    num_points = int(config.TERRAIN_SIZE / config.TERRAIN_RES) + 1
    chunk_points = int(config.CHUNK_SIZE / config.TERRAIN_RES) + 1
    chunks_per_side = int(config.TERRAIN_SIZE / config.CHUNK_SIZE)

    # Générer hauteurs et biome
    heights, biome_noise_map, global_min_y, global_max_y = generate_heights(num_points, config)
    heights = smooth_heights(heights, biome_noise_map, num_points, config)
    occlusion = compute_occlusion(heights, num_points, config)

    # Générer vertices et couleurs
    vertices_global, global_vertex_map, global_vertices, global_colors, global_normals, _, _ = generate_vertices_and_colors(heights, occlusion, num_points, config)

    # Calculer les normales
    normal_accumulator = compute_normals(global_vertices, global_vertex_map, num_points, chunk_points, chunks_per_side)
    for (i, j), idx in global_vertex_map.items():
        normal = normal_accumulator[(i, j)]
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm
        else:
            normal = np.array([0.0, 1.0, 0.0])
        global_normals[idx] = tuple(normal)

    # Générer les chunks
    chunks = []
    for ci in range(chunks_per_side):
        for cj in range(chunks_per_side):
            chunk = generate_chunk(ci, cj, chunk_points, num_points, global_vertices, global_colors, global_normals, global_vertex_map, config)
            chunks.append(chunk)

    return vertices_global, num_points, chunks