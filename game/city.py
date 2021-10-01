import pygame as pg
import random
from .settings import D_POPULATION, ECONOMY_COOLDOWN
from .resource_manager import ResourceManager

# TODO: Finish City class and use it to make a new City entity in world class.
class City:

    def __init__(self, pos):
        self.name = generate_name()
        self.population = D_POPULATION
        self.businesses = None
        self.resource_manager = ResourceManager()
        self.pos = pos
        self.image = pg.image.load("assets/graphics/hut_X3.png")

        self.consumption_rate = 0.01
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > ECONOMY_COOLDOWN:
            self.resource_manager.update_resource_data()





def generate_name():
    return random.choice(["city1", "city2", "city3", "city4", "city5"])


