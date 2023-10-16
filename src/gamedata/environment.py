import random
import pygame
import math
import pygame.font
import pygame_gui
from utils.constants import Colors
import utils.parameters
import gamedata.items

Parameters = utils.parameters
ItemsDatabase = gamedata.items

class GenerateEnvironment:
    def __init__(self):
        self.food_items = ItemsDatabase
    
    def randomly_spawn_food(self):
        for food in self.food_items:
            if food.spawns_naturally:
                food.rect.x = random.randint(0, Parameters.WIDTH)
                food.rect.y = random.randint(0, Parameters.HEIGHT)
