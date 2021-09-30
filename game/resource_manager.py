import pygame as pg


class ResourceManager:

    def __init__(self):
        self.player_resources = {
            "wood": 5,
            "stone": 5,
            "food": 5
        }

        self.resources = {
            "wood": {"local": 10, "supply": 0, "demand": 0},
            "stone": {"local": 10, "supply": 0, "demand": 0},
            "food": {"local": 10, "supply": 0, "demand": 0}
        }

        # costs
        self.costs = {
            "household": {"wood": 1, "stone": 1, "food": 3},
            "stonemasonry": {"wood": 2, "stone": 1}
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.player_resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.player_resources[resource]:
                affordable = False
        return affordable

    def update_resource_data(self):
        for resource in self.resources:
            pass




