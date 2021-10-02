import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .camera import Camera
from .hud import Hud
from .resource_manager import ResourceManager
from .city import City


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.entities = []
        self.resource_manager = ResourceManager()
        self.hud = Hud(self.resource_manager, self.width, self.height)
        self.world = World(self.resource_manager, self.entities, self.hud, 50, 50, self.width, self.height)
        self.camera = Camera(self.width, self.height)
        self.has_changed = True


    def run(self):
        self.clock.tick(60)
        self.events()
        self.update()
        if self.has_changed:
            self.draw()
            self.has_changed = False


    def events(self):

        for event in pg.event.get():
            self.has_changed = True
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.world.mouse_click(pg.mouse.get_pos(), self.camera)
                self.camera.drag = True
            if event.type == pg.MOUSEBUTTONUP:
                self.world.mouse_up(pg.mouse.get_pos(), self.camera)
                self.camera.drag = False


    def update(self):
        self.camera.update()
        for e in self.entities:
            e.update()
        self.hud.update()


    def draw(self):
        self.screen.fill((0,0,0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255,255,255),
            (10,10)
        )

        pg.display.flip()
