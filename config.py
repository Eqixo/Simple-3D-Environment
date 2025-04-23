class Config:
    # Paramètres du terrain
    TERRAIN_SIZE = 1024
    TERRAIN_RES = 1.0
    CHUNK_SIZE = 16
    BIOME_SCALE = 0.005
    BASE_HEIGHT_SCALE = 0.01
    DETAIL_SCALE = 0.05
    OCTAVES = 8
    PERSISTENCE = 0.6
    LACUNARITY = 2.5
    HEIGHT_SCALE = 10.0
    OCEAN_DEPTH = 0.5
    PLAINS_FLATNESS = 0.5
    MOUNTAIN_INTENSITY = 1.0
    SMOOTHING_FACTOR = 1.0
    SEED = 42

    # Paramètres de l'occlusion ambiante
    AO_RADIUS = 3.0
    AO_STRENGTH = 1.0
    AO_SAMPLES = 16

    # Paramètres de la caméra
    CAMERA_SPEED = 9.81
    FREECAM_SPEED = CAMERA_SPEED * 10
    MOUSE_SENSITIVITY = 0.1
    GRAVITY = 29.43
    JUMP_SPEED = 9.81
    PHYSICS_STEP = 1.0 / 60.0

    # Paramètres de la lumière
    LIGHT_POSITION = [0.0, 50.0, 50.0]
    LIGHT_COLOR = [1.0, 1.0, 1.0]
    AMBIENT_LIGHT = [1.0, 1.0, 1.0]
    MAX_TRAJECTORY_POINTS = 1000

    # Paramètres du brouillard
    VIEW_DISTANCE = 8 * CHUNK_SIZE
    FOG_START = VIEW_DISTANCE - CHUNK_SIZE  # Distance où le brouillard commence
    FOG_END = VIEW_DISTANCE   # Distance où le brouillard est complet
    FOG_COLOR = [0.53, 0.81, 0.98, 1.0]  # Même couleur que le fond bleu ciel

    # Paramètre de débogage
    DEBUG_MODE = False