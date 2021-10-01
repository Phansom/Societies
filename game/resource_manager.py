import pygame as pg

class ResourceManager:

    def __init__(self):
        self.resources = {
            "wood": 10,
            "stone": 10,
            "food": 10
        }

        self.resource_data = {
            "production": 0,
            "consumption": 0
        }

        # costs
        self.costs = {
            "city": {"wood": 1, "stone": 1, "food": 1},
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def update_resource_data(self):
        for resource in self.resources:
            for _ in self.resource_data:
                self.resources[resource] += (self.resource_data["production"] - self.resource_data["consumption"])






