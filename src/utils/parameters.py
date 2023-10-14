import math
import pygame
import random
import pygame.font
import pygame_gui

# Game
WIDTH, HEIGHT = 900, 600
FPS = 60

# Speed
speed_multipliers = [0.25, 0.5, 0.75, 1, 2, 4, 8, 10]
speed_index = 3  # Index of 1 in the list
