import numpy as np
import math

def smooth_heights(heights, biome_noise_map, num_points, config):
    smoothed_heights = np.copy(heights)
    for i in range(1, num_points - 1):
        for j in range(1, num_points - 1):
            if biome_noise_map[i, j] < 2.5:
                neighbor_sum = (
                    heights[i-1, j-1] + heights[i-1, j] + heights[i-1, j+1] +
                    heights[i, j-1] + heights[i, j] + heights[i, j+1] +
                    heights[i+1, j-1] + heights[i+1, j] + heights[i+1, j+1]
                )
                avg_neighbor = neighbor_sum / 9.0
                smoothed_heights[i, j] = (
                    (1.0 - config.SMOOTHING_FACTOR) * heights[i, j] +
                    config.SMOOTHING_FACTOR * avg_neighbor
                )
    return smoothed_heights

def compute_occlusion(heights, num_points, config):
    occlusion = np.ones((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            center_x = i * config.TERRAIN_RES - config.TERRAIN_SIZE / 2
            center_z = j * config.TERRAIN_RES - config.TERRAIN_SIZE / 2
            center_y = heights[i, j]
            ao_sum = 0.0
            for sample in range(config.AO_SAMPLES):
                theta = 2.0 * math.pi * sample / config.AO_SAMPLES
                dist = config.AO_RADIUS * math.sqrt(sample / config.AO_SAMPLES)
                sample_x = center_x + dist * math.cos(theta)
                sample_z = center_z + dist * math.sin(theta)
                grid_x = (sample_x + config.TERRAIN_SIZE / 2) / config.TERRAIN_RES
                grid_z = (sample_z + config.TERRAIN_SIZE / 2) / config.TERRAIN_RES
                i_n = int(grid_x)
                j_n = int(grid_z)
                if i_n < 0 or i_n >= num_points - 1 or j_n < 0 or j_n >= num_points - 1:
                    continue
                u = grid_x - i_n
                v = grid_z - j_n
                y00 = heights[i_n, j_n]
                y10 = heights[i_n + 1, j_n]
                y01 = heights[i_n, j_n + 1]
                y11 = heights[i_n + 1, j_n + 1]
                y0 = y00 * (1 - u) + y10 * u
                y1 = y01 * (1 - u) + y11 * u
                sample_y = y0 * (1 - v) + y1 * v
                height_diff = sample_y - center_y
                if height_diff > 0:
                    distance = math.sqrt((sample_x - center_x)**2 + (sample_z - center_z)**2)
                    if distance < 1e-6:
                        distance = 1e-6
                    ao_contribution = height_diff / distance
                    ao_sum += ao_contribution
            ao_sum = min(ao_sum * config.AO_STRENGTH / config.AO_SAMPLES, 0.5)
            occlusion[i, j] = 1.0 - ao_sum
    return occlusion