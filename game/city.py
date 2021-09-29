import pygame as pg
import random
from .settings import D_POPULATION, D_FOOD

class City:
    def __init__(self):
        self.name = generate_name()
        self.population = D_POPULATION
        self.businesses = None

        self.food = D_FOOD
        self.consumption = None
        self.production = None


def generate_name():
    return random.choice(["city1", "city2"])


