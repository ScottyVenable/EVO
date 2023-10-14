import math
import pygame
import random
import pygame.font
import pygame_gui

class Colors:
    # Basic Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Neutral Colors
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)

    # Warm Colors
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)

    # Cool Colors
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    PURPLE = (128, 0, 128)

    # Pastel Colors
    PINK = (255, 182, 193)
    LAVENDER = (230, 230, 250)
    TURQUOISE = (64, 224, 208)
    MINT_GREEN = (152, 255, 152)

    # Earthy Colors
    SAND = (244, 164, 96)
    FOREST_GREEN = (34, 139, 34)
    SKY_BLUE = (135, 206, 235)

    # Vibrant Colors
    GOLD = (255, 215, 0)
    LIME = (0, 255, 0)
    TANGERINE = (255, 165, 0)
    ROSE = (255, 0, 127)
    INDIGO = (75, 0, 130)

    # Gradients
    SUNSET = [(255, 0, 0), (255, 165, 0), (255, 255, 0)]
    OCEAN = [(0, 0, 128), (0, 0, 255), (0, 128, 255)]
    FIRE = [(255, 0, 0), (255, 69, 0), (255, 165, 0)]

    # Random Colors
    RANDOM1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    RANDOM2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
