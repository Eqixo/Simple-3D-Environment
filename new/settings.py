CHUNK_SIZE = 16  # Taille d'un chunk (16x16 blocs)
RENDER_DISTANCE = 8  # Nombre de chunks rendus autour du joueur
WORLD_HEIGHT = 32  # Hauteur maximale du monde
NOISE_SCALE = 0.1  # Échelle pour la génération de bruit (hauteur)
BIOME_NOISE_SCALE = 0.05  # Échelle pour la génération de bruit (biomes)
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FOV = 60  # Champ de vision pour la projection
PLAYER_SPEED = 1.5  # Vitesse de déplacement du joueur
MOUSE_SENSITIVITY = 0.002  # Sensibilité de la souris

# Seuils de hauteur et couleurs pour les biomes
BIOMES = [
    {
        "name": "plaines",
        "max_height": WORLD_HEIGHT * 0.6,  # Jusqu'à 40% de la hauteur max
        "color": (0.18, 0.46, 0.2),  # Vert pour les plaines
        "height_scale": 0.25  # Terrain plus plat
    },
    {
        "name": "collines",
        "max_height": WORLD_HEIGHT * 0.7,  # Jusqu'à 70% de la hauteur max
        "color": (0.33, 0.23, 0.09),  # Brun pour les collines
        "height_scale": 0.5  # Terrain modéré
    },
    {
        "name": "montagnes",
        "max_height": WORLD_HEIGHT,  # Jusqu'à la hauteur max
        "color": (0.28, 0.28, 0.27),  # Gris pour les montagnes
        "height_scale": 1.0  # Terrain plus accidenté
    }
]