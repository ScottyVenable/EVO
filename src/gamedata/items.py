import random
import pygame
from utils.constants import Colors

class Item:
    def __init__(self, name, description, weight, item_type, sprite):
        self.name = name
        self.description = description
        self.weight = weight
        self.sprite = sprite
        self.item_type = item_type # The type of item (organic, mineral, glass, metalic, fabric, ceramic, etc)

class Food(Item):
    def __init__(self, name, description, weight, item_type, nutrients, spawns_naturally, spawn_probability, sprite):
        super().__init__(name, description, weight, item_type, sprite)
        self.nutrients = nutrients
        self.spawns_naturally = spawns_naturally
        self.spawn_probability = spawn_probability
        self.sprite = sprite

        self.rect = self.sprite.get_rect()

class Material(Item):
    def __init__(self, name, description, weight, item_type, sprite):
        super().__init__(name, description, weight, item_type, sprite)

        self.rect = self.sprite.get_rect()

class Foods:

    berry_sprite = pygame.Surface((3, 3))
    berry_sprite.fill(Colors.RED)

    hazelnut_sprite = pygame.Surface((3, 3))
    hazelnut_sprite.fill(Colors.BROWN)


    berry = Food("Berry", "A sweet berry", 0.5, "fruit", 3, True, 0.01, berry_sprite)
    hazelnut = Food("Hazelnut", "A delicious nut", 0.8, "nut", 5, True, 0.0003, hazelnut_sprite)

def main():
    #Create Sprite Groups
    food_sprites = pygame.sprite.Group()
    populator = PopulateItems()
    sprites_list = create_sprites()
    food_list, material_list = populator.populate_all()
    create_sprites()

