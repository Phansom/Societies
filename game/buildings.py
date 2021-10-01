import pygame as pg
from .settings import D_POPULATION, ECONOMY_COOLDOWN


# TODO: Might end up replacing this with the city.py code; unsure if will be using buildings in the future. Possibly
# TODO: might use this as a constructable section (ie villages, cropland, rangeland, woodland).
class Building:

    def __init__(self, name, pos, city, img):
        self.image = img
        self.name = name
        self.pos = pos
        self.city = city
        self.rect = self.image.get_rect(topleft=pos)
        self.update_cooldown = pg.time.get_ticks()

    def update(self, update_method):
        now = pg.time.get_ticks()
        if now - self.update_cooldown > ECONOMY_COOLDOWN:
            # TODO: update the building as needed here

            self.update_cooldown = now


building_list = {
    "name": str,
    "pos": (int,int)



}