import tdl

import scene

from entities import entity

class Animation(entity.Entity):
    def __init__(self):
        self.parent = None

    def draw(self, console):
        pass

    def update(self, time):
        if self.parent:
            pass

    def handle_events(self, event):
        pass


class FlashBackground(Animation):
    def __init__(self, bg=(255, 255, 255), interval=0.25, repeat=2):
        super().__init__()
        self.time = 0
        self.interval = interval
        self.times_flashed = 0
        self.times_to_flash = repeat * 2
        self.bg = bg
        self.current_bg = bg

    def update(self, time):
        self.time += time
        if self.time > self.interval:
            self.time = 0
            self.times_flashed += 1

            if self.current_bg == self.bg:
                self.current_bg = self.parent.bg
            else:
                self.current_bg = self.bg

        if self.times_flashed > self.times_to_flash:
            self.parent.children.remove(self)

    def draw(self, console):
        if not self.parent.visible:
            return

        pos = self.parent.position
        char = self.parent.char
        fg = self.parent.fg

        console.draw_char(*pos, char, fg, self.current_bg)

class ThrowMotion(Animation):
    def __init__(self, parent, source, dest, time):
        super().__init__()
        self.parent = parent
        self.points = tdl.map.bresenham(*source, *dest)
        self.time = time
        self.time_to_next = 0
        self.frame_time = time / len(self.points)
        self.current_point = self.points.pop(0)

    def update(self, time):
        self.time_to_next += time
        if self.time_to_next >= self.frame_time:
            self.time_to_next = 0

            if self.points:
                self.current_point = self.points.pop(0)

            else:
                self.parent.children.remove(self)

    def draw(self, console):
        if not scene.Scene.current_scene.check_visibility(*self.current_point):
            return

        level = scene.Scene.current_scene.level
        #dx = self.parent.position[0] + level.x
        #dy = self.parent.position[1] + level.y
        #ch, fg, bg = level.get_char(dx, dy)

        p = self.parent
        #console.draw_char(*self.parent.position, ch, fg, bg)
        console.draw_char(*self.current_point, p.char, p.fg, p.bg)
