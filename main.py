import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from config import Config
from terrain import generate_terrain
from camera import FreeCamera, Camera
from rendering import *

def main():
    config = Config()
    shader_program, font = init_window()
    vertices, num_points, chunks = generate_terrain()
    player_camera = Camera(config)
    active_camera = player_camera
    is_freecam = False
    freecam = None
    player_pos_frozen = None
    player_yaw_frozen = 0.0
    player_pitch_frozen = 0.0
    wireframe = False
    debug_mode = False
    running = True
    clock = pygame.time.Clock()
    light_trajectory = []
    last_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000.0
        last_time = current_time
        fps = 1.0 / dt if dt > 0.00001 else 0.0
        frame_time = dt * 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    wireframe = not wireframe
                if event.key == pygame.K_SPACE and not is_freecam:
                    player_camera.jump()
                if event.key == pygame.K_f:
                    is_freecam = not is_freecam
                    if is_freecam:
                        freecam = FreeCamera(player_camera.pos, player_camera.yaw, player_camera.pitch, config)
                        active_camera = freecam
                        player_pos_frozen = player_camera.pos[:]
                        player_yaw_frozen = player_camera.yaw
                        player_pitch_frozen = player_camera.pitch
                    else:
                        player_camera.pos = freecam.pos[:]
                        player_camera.yaw = freecam.yaw
                        player_camera.pitch = freecam.pitch
                        player_camera.velocity = [0.0, 0.0, 0.0]
                        active_camera = player_camera
                        freecam = None
                        player_pos_frozen = None
                if event.key == pygame.K_F3:
                    debug_mode = not debug_mode

        active_camera.rotate()
        keys = pygame.key.get_pressed()
        if is_freecam:
            active_camera.move(keys, dt)
        else:
            active_camera.move(keys, vertices, num_points, dt)

        glClearColor(0.53, 0.81, 0.98, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        proj_matrix, model_view_matrix = active_camera.update()

        proj_player = build_perspective_matrix(75, 1600/900, 0.1, 500.0)
        model_player = build_view_matrix(
            player_pos_frozen if is_freecam else player_camera.pos,
            player_yaw_frozen if is_freecam else player_camera.yaw,
            player_pitch_frozen if is_freecam else player_camera.pitch
        )
        planes_player = extract_frustum_planes(proj_player, model_player)

        # Rendre le terrain et obtenir le nombre de chunks visibles
        visible_chunks = render_terrain(
            chunks,
            planes_player if is_freecam else extract_frustum_planes(proj_matrix, model_view_matrix),
            shader_program,
            model_view_matrix,
            proj_matrix,
            config,
            wireframe,
            active_camera.pos
        )

        if debug_mode:
            # Pré-filtrer les chunks pour render_bounding_boxes
            view_distance = config.VIEW_DISTANCE
            chunk_size = config.CHUNK_SIZE
            camera_x, camera_z = active_camera.pos[0], active_camera.pos[2]
            min_chunk_x = int((camera_x - view_distance) / chunk_size)
            max_chunk_x = int((camera_x + view_distance) / chunk_size) + 1
            min_chunk_z = int((camera_z - view_distance) / chunk_size)
            max_chunk_z = int((camera_z + view_distance) / chunk_size) + 1

            visible_chunks_list = []
            for chunk in chunks:
                chunk_center_x = (chunk['min_x'] + chunk['max_x']) / 2
                chunk_center_z = (chunk['min_z'] + chunk['max_z']) / 2
                chunk_x = int(chunk_center_x / chunk_size)
                chunk_z = int(chunk_center_z / chunk_size)
                if min_chunk_x <= chunk_x <= max_chunk_x and min_chunk_z <= chunk_z <= max_chunk_z:
                    min_x, max_x = chunk['min_x'], chunk['max_x']
                    min_y, max_y = chunk['min_y'], chunk['max_y']
                    min_z, max_z = chunk['min_z'], chunk['max_z']
                    closest_x = max(min_x, min(max_x, active_camera.pos[0]))
                    closest_y = max(min_y, min(max_y, active_camera.pos[1]))
                    closest_z = max(min_z, min(max_z, active_camera.pos[2]))
                    distance_sq = (
                        (active_camera.pos[0] - closest_x) ** 2 +
                        (active_camera.pos[1] - closest_y) ** 2 +
                        (active_camera.pos[2] - closest_z) ** 2
                    )
                    if distance_sq <= view_distance ** 2:
                        visible_chunks_list.append(chunk)

            render_bounding_boxes(
                visible_chunks_list,
                planes_player if is_freecam else extract_frustum_planes(proj_matrix, model_view_matrix),
                model_view_matrix,
                player_pos_frozen if is_freecam else None
            )
            render_light_trajectory(light_trajectory)
            render_coordinates(
                active_camera.pos,
                player_pos_frozen if is_freecam else None,
                fps=fps,
                frame_time=frame_time,
                font=font,
                visible_chunks=visible_chunks  # Passer le nombre de chunks visibles
            )

        pygame.display.flip()
        clock.tick(-1)

    for chunk in chunks:
        glDeleteBuffers(1, [chunk['vbo_vertex']])
        glDeleteBuffers(1, [chunk['vbo_color']])
        glDeleteBuffers(1, [chunk['vbo_normal']])
        glDeleteBuffers(1, [chunk['vbo_index']])
        glDeleteVertexArrays(1, [chunk['vao']])
    glDeleteProgram(shader_program)
    pygame.quit()

if __name__ == "__main__":
    main()