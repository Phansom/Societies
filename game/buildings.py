import pygame as pg
from .settings import D_POPULATION

class Household:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/hut_X3.png")
        self.image = image
        self.name = "household"
        self.rect = self.image.get_rect(topleft=pos)

        self.population = D_POPULATION

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()


    def update(self):
        pass


class Stonemasonry:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/building02.png")
        self.image = image
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.player_resources['stone'] += 1
            self.resource_cooldown = now
