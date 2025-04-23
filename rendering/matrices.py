import numpy as np
import math

def build_perspective_matrix(fovy, aspect, z_near, z_far):
    f = 1.0 / math.tan(math.radians(fovy) / 2)
    matrix = np.zeros((4, 4))
    matrix[0, 0] = f / aspect
    matrix[1, 1] = f
    matrix[2, 2] = (z_near + z_far) / (z_near - z_far)
    matrix[2, 3] = (2 * z_near * z_far) / (z_near - z_far)
    matrix[3, 2] = -1
    return matrix

def build_view_matrix(pos, yaw, pitch):
    cos_x = np.cos(np.radians(pitch))
    sin_x = np.sin(np.radians(pitch))
    cos_y = np.cos(np.radians(yaw))
    sin_y = np.sin(np.radians(yaw))
    forward = np.array([cos_x * sin_y, sin_x, -cos_x * cos_y])
    up = np.array([0, 1, 0])
    right = np.cross(forward, up)
    up = np.cross(right, forward)
    right /= np.linalg.norm(right)
    up /= np.linalg.norm(up)
    forward /= np.linalg.norm(forward)
    matrix = np.identity(4)
    matrix[0, 0:3] = right
    matrix[1, 0:3] = up
    matrix[2, 0:3] = -forward
    matrix[0:3, 3] = -np.dot(np.array([right, up, -forward]), pos)
    return matrix

def extract_frustum_planes(proj_matrix, model_matrix):
    clip = np.dot(proj_matrix, model_matrix)
    planes = np.zeros((6, 4))
    planes[0] = clip[3] + clip[0]
    planes[1] = clip[3] - clip[0]
    planes[2] = clip[3] + clip[1]
    planes[3] = clip[3] - clip[1]
    planes[4] = clip[3] + clip[2]
    planes[5] = clip[3] - clip[2]
    for i in range(6):
        norm = np.sqrt(planes[i, 0]**2 + planes[i, 1]**2 + planes[i, 2]**2)
        if norm > 0:
            planes[i] /= norm
    return planes

def is_box_in_frustum(planes, min_x, max_x, min_y, max_y, min_z, max_z):
    for plane in planes:
        px = max_x if plane[0] > 0 else min_x
        py = max_y if plane[1] > 0 else min_y
        pz = max_z if plane[2] > 0 else min_z
        distance = plane[0] * px + plane[1] * py + plane[2] * pz + plane[3]
        if distance < -0.2:
            return False
    return True