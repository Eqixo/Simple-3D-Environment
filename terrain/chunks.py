import numpy as np
from OpenGL.GL import *

def generate_vertices_and_colors(heights, occlusion, num_points, config):
    vertices_global = []
    global_vertices = []
    global_colors = []
    global_normals = []
    global_vertex_map = {}
    global_min_y = float('inf')
    global_max_y = float('-inf')

    for i in range(num_points):
        for j in range(num_points):
            x = i * config.TERRAIN_RES - config.TERRAIN_SIZE / 2
            z = j * config.TERRAIN_RES - config.TERRAIN_SIZE / 2
            y = heights[i, j]
            vertices_global.append((x, y, z))
            global_vertex_map[(i, j)] = len(global_vertices)
            global_vertices.append((x, y, z))
            global_normals.append((0.0, 0.0, 0.0))
            global_min_y = min(global_min_y, y)
            global_max_y = max(global_max_y, y)

            # Définir les couleurs selon l'altitude
            if y < -10:
                base_color = (0.0, 0.0, 0.2)
            elif y < -2.5:
                base_color = (0.0, 0.1, 0.4)
            elif y < -0.5:
                base_color = (0.1, 0.2, 0.6)
            elif y < 0.5:
                base_color = (0.87, 0.81, 0.62)
            elif y < 2.5:
                base_color = (0.0, 0.4, 0.0)
            elif y < 3:
                base_color = (0.4, 0.2, 0.1)
            elif y < 7.5:
                base_color = (0.3, 0.3, 0.3)
            else:
                base_color = (1.0, 1.0, 1.0)
            ao_factor = occlusion[i, j]
            global_colors.append((
                min(max(base_color[0] * ao_factor, 0.0), 1.0),
                min(max(base_color[1] * ao_factor, 0.0), 1.0),
                min(max(base_color[2] * ao_factor, 0.0), 1.0)
            ))

    return vertices_global, global_vertex_map, global_vertices, global_colors, global_normals, global_min_y, global_max_y

def compute_normals(global_vertices, global_vertex_map, num_points, chunk_points, chunks_per_side):
    normal_accumulator = {key: np.array([0.0, 0.0, 0.0]) for key in global_vertex_map}
    for ci in range(chunks_per_side):
        for cj in range(chunks_per_side):
            start_i = ci * (chunk_points - 1)
            start_j = cj * (chunk_points - 1)
            for i in range(chunk_points - 1):
                for j in range(chunk_points - 1):
                    global_i = start_i + i
                    global_j = start_j + j
                    if global_i >= num_points - 1 or global_j >= num_points - 1:
                        continue
                    top_left = global_vertex_map.get((global_i, global_j))
                    top_right = global_vertex_map.get((global_i, global_j + 1))
                    bottom_left = global_vertex_map.get((global_i + 1, global_j))
                    bottom_right = global_vertex_map.get((global_i + 1, j + 1))
                    if None in (top_left, top_right, bottom_left, bottom_right):
                        continue
                    v0 = np.array(global_vertices[top_left])
                    v1 = np.array(global_vertices[bottom_left])
                    v2 = np.array(global_vertices[top_right])
                    u = v1 - v0
                    v = v2 - v0
                    normal = np.cross(u, v)
                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                    normal_accumulator[(global_i, global_j)] += normal
                    normal_accumulator[(global_i + 1, global_j)] += normal
                    normal_accumulator[(global_i, global_j + 1)] += normal
                    v0 = np.array(global_vertices[top_right])
                    v1 = np.array(global_vertices[bottom_left])
                    v2 = np.array(global_vertices[bottom_right])
                    u = v1 - v0
                    v = v2 - v0
                    normal = np.cross(u, v)
                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                    normal_accumulator[(global_i, global_j + 1)] += normal
                    normal_accumulator[(global_i + 1, global_j)] += normal
                    normal_accumulator[(global_i + 1, j + 1)] += normal
    return normal_accumulator

def generate_chunk(ci, cj, chunk_points, num_points, global_vertices, global_colors, global_normals, global_vertex_map, config):
    chunk_vertices = []
    chunk_colors = []
    chunk_normals = []
    chunk_indices = []
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    min_z = float('inf')
    max_z = float('-inf')

    start_i = ci * (chunk_points - 1)
    start_j = cj * (chunk_points - 1)

    chunk_vertex_map = {}
    for i in range(chunk_points):
        for j in range(chunk_points):
            global_i = start_i + i
            global_j = start_j + j
            if global_i >= num_points or global_j >= num_points:
                continue
            global_idx = global_vertex_map[(global_i, global_j)]
            chunk_vertex_map[(i, j)] = len(chunk_vertices)
            chunk_vertices.append(global_vertices[global_idx])
            chunk_colors.append(global_colors[global_idx])
            chunk_normals.append(global_normals[global_idx])
            x, y, z = global_vertices[global_idx]
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)

    for i in range(chunk_points - 1):
        for j in range(chunk_points - 1):
            top_left = chunk_vertex_map.get((i, j))
            top_right = chunk_vertex_map.get((i, j + 1))
            bottom_left = chunk_vertex_map.get((i + 1, j))
            bottom_right = chunk_vertex_map.get((i + 1, j + 1))
            if None in (top_left, top_right, bottom_left, bottom_right):
                continue
            chunk_indices.extend([top_left, bottom_left, top_right])
            chunk_indices.extend([top_right, bottom_left, bottom_right])

    vertices_array = np.array(chunk_vertices, dtype=np.float32)
    colors_array = np.array(chunk_colors, dtype=np.float32)
    normals_array = np.array(chunk_normals, dtype=np.float32)
    indices_array = np.array(chunk_indices, dtype=np.uint32)

    vbo_vertex = glGenBuffers(1)
    vbo_color = glGenBuffers(1)
    vbo_normal = glGenBuffers(1)
    vbo_index = glGenBuffers(1)
    vao = glGenVertexArrays(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertex)
    glBufferData(GL_ARRAY_BUFFER, vertices_array.nbytes, vertices_array, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_color)
    glBufferData(GL_ARRAY_BUFFER, colors_array.nbytes, colors_array, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(2)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_normal)
    glBufferData(GL_ARRAY_BUFFER, normals_array.nbytes, normals_array, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_index)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_array.nbytes, indices_array, GL_STATIC_DRAW)

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    return {
        'vbo_vertex': vbo_vertex,
        'vbo_color': vbo_color,
        'vbo_normal': vbo_normal,
        'vbo_index': vbo_index,
        'vao': vao,
        'num_indices': len(chunk_indices),
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'min_z': min_z,
        'max_z': max_z
    }

def get_terrain_height(x, z, vertices, num_points):
    from config import Config
    grid_x = (x + Config.TERRAIN_SIZE / 2) / Config.TERRAIN_RES
    grid_z = (z + Config.TERRAIN_SIZE / 2) / Config.TERRAIN_RES
    i = int(grid_x)
    j = int(grid_z)
    u = grid_x - i
    v = grid_z - j
    if i < 0 or i >= num_points - 1 or j < 0 or j >= num_points - 1:
        return 0.0
    idx00 = i * num_points + j
    idx10 = (i + 1) * num_points + j
    idx01 = i * num_points + (j + 1)
    idx11 = (i + 1) * num_points + (j + 1)
    y00 = vertices[idx00][1]
    y10 = vertices[idx10][1]
    y01 = vertices[idx01][1]
    y11 = vertices[idx11][1]
    y0 = y00 * (1 - u) + y10 * u
    y1 = y01 * (1 - u) + y11 * u
    height = y0 * (1 - v) + y1 * v
    return height