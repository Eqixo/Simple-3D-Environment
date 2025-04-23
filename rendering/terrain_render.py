from OpenGL.GL import *
from .matrices import is_box_in_frustum
import numpy as np

def render_terrain(chunks, planes, shader_program, model_view_matrix, proj_matrix, config, wireframe, camera_pos):
    glUseProgram(shader_program)

    # Passer les matrices
    model_view_loc = glGetUniformLocation(shader_program, "modelViewMatrix")
    proj_loc = glGetUniformLocation(shader_program, "projectionMatrix")
    glUniformMatrix4fv(model_view_loc, 1, GL_FALSE, model_view_matrix.T.flatten())
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, proj_matrix.T.flatten())

    # Passer les paramètres de lumière
    light_pos_loc = glGetUniformLocation(shader_program, "lightPosition")
    light_color_loc = glGetUniformLocation(shader_program, "lightColor")
    ambient_light_loc = glGetUniformLocation(shader_program, "ambientLight")
    glUniform3fv(light_pos_loc, 1, config.LIGHT_POSITION)
    glUniform3fv(light_color_loc, 1, config.LIGHT_COLOR)
    glUniform3fv(ambient_light_loc, 1, config.AMBIENT_LIGHT)

    # Passer les paramètres du brouillard
    fog_color_loc = glGetUniformLocation(shader_program, "fogColor")
    fog_start_loc = glGetUniformLocation(shader_program, "fogStart")
    fog_end_loc = glGetUniformLocation(shader_program, "fogEnd")
    glUniform3fv(fog_color_loc, 1, config.FOG_COLOR[:3])
    glUniform1f(fog_start_loc, config.FOG_START)
    glUniform1f(fog_end_loc, config.FOG_END)

    # Activer/désactiver le mode fil de fer
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)

    visible_chunks = 0
    total_chunks = len(chunks)
    camera_x, camera_z = camera_pos[0], camera_pos[2]
    view_distance = config.VIEW_DISTANCE
    chunk_size = config.CHUNK_SIZE

    # Pré-filtrer les chunks dans un rectangle en XZ
    min_chunk_x = int((camera_x - view_distance) / chunk_size)
    max_chunk_x = int((camera_x + view_distance) / chunk_size) + 1
    min_chunk_z = int((camera_z - view_distance) / chunk_size)
    max_chunk_z = int((camera_z + view_distance) / chunk_size) + 1

    filtered_chunks = []
    for chunk in chunks:
        chunk_center_x = (chunk['min_x'] + chunk['max_x']) / 2
        chunk_center_z = (chunk['min_z'] + chunk['max_z']) / 2
        chunk_x = int(chunk_center_x / chunk_size)
        chunk_z = int(chunk_center_z / chunk_size)
        if min_chunk_x <= chunk_x <= max_chunk_x and min_chunk_z <= chunk_z <= max_chunk_z:
            filtered_chunks.append(chunk)

    # Traiter les chunks filtrés
    view_distance_sq = view_distance ** 2
    for chunk in filtered_chunks:
        min_x, max_x = chunk['min_x'], chunk['max_x']
        min_y, max_y = chunk['min_y'], chunk['max_y']
        min_z, max_z = chunk['min_z'], chunk['max_z']

        # Calculer le point le plus proche de la boîte englobante
        closest_x = max(min_x, min(max_x, camera_pos[0]))
        closest_y = max(min_y, min(max_y, camera_pos[1]))
        closest_z = max(min_z, min(max_z, camera_pos[2]))

        # Calculer la distance au carré
        distance_sq = (
            (camera_pos[0] - closest_x) ** 2 +
            (camera_pos[1] - closest_y) ** 2 +
            (camera_pos[2] - closest_z) ** 2
        )

        # Ne pas rendre si le chunk est trop loin
        if distance_sq > view_distance_sq:
            continue

        # Vérifier si le chunk est dans le frustum
        if is_box_in_frustum(planes, min_x, max_x, min_y, max_y, min_z, max_z):
            glBindVertexArray(chunk['vao'])
            glDrawElements(GL_TRIANGLES, chunk['num_indices'], GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
            visible_chunks += 1

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glUseProgram(0)

    # Débogage
    # print(f"Chunks filtrés : {len(filtered_chunks)}/{total_chunks}, rendus : {visible_chunks}")

    return visible_chunks