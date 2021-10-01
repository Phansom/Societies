import pygame as pg

class Camera:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.scroll = pg.Vector2(0,0)
        self.dx = 0
        self.dy = 0
        self.drag = False
        self.mouse_pos = pg.mouse.get_pos()
        self.old_mouse_pos = pg.mouse.get_pos()

    def handle_mouse(self):
        mouse_pos = self.mouse_pos

        if self.drag:
            self.dx = (self.mouse_pos[0] - self.old_mouse_pos[0])
            self.dy = (self.mouse_pos[1] - self.old_mouse_pos[1])
            self.scroll.x += self.dx
            self.scroll.y += self.dy

        self.old_mouse_pos = mouse_pos


    def update(self):
        self.mouse_pos = pg.mouse.get_pos()
        if self.mouse_pos != self.old_mouse_pos:
            self.handle_mouse()
