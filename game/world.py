import pygame as pg
import random
import noise
from .settings import TILE_SIZE, RED
from .buildings import Building
from .city import City


class World:
    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.perlin_scale = grid_length_x / 2

        self.grass_tiles = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.cities = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None
        self.examine_tile = None
        self.start_click_grid_pos = None


    def build(self, grid_pos):
        if self.hud.selected_tile["name"] == "city":
            ent = City(grid_pos)
            self.entities.append(ent)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent

        elif "name" in self.hud.selected_tile:
            ent = Building(grid_pos)
            self.entities.append(ent)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent

        self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
        self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
        self.hud.selected_tile = None


    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]

                # draw world tiles
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                # draw buildings
                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

                # draw cities
                city = self.cities[x][y]
                if city is not None:
                    screen.blit(city.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (city.image.get_height() - TILE_SIZE) + camera.scroll.y))


        # DRAW THE "GHOST" IMAGE IN WORLD (OF THE BUILD HUD)
        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, RED, iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)

        if (perlin >= 45) or (perlin <= -45):
            tile = "tree"
        else:
            if r == 1:
                tile = "tree"
            elif r == 2:
                tile = "rock"
            else:
                tile = ""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True
        }

        return out


    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x

        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y


    def load_images(self):
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()
        city = pg.image.load("assets/graphics/hut_X3.png").convert_alpha()

        images = {
            "tree": tree,
            "rock": rock,
            "block": block,
            "city": city
        }

        return images


    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False


    def mouse_click(self, mouse_pos, camera):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        self.start_click_grid_pos = grid_pos


    def mouse_up(self, mouse_pos, camera):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        print(f"{grid_pos} VS {self.start_click_grid_pos}")
        if grid_pos == self.start_click_grid_pos:
            collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
            if self.hud.selected_tile is not None and not collision:
                if self.can_place_tile(grid_pos):
                    self.build(grid_pos)
            else:
                self.examine_grid_pos(grid_pos)


    def examine_grid_pos(self, grid_pos):
        building = self.buildings[grid_pos[0]][grid_pos[1]]
        if building is not None:
            self.examine_tile = grid_pos
            self.hud.examined_tile = building
            print(f"{building} has been examined.")
