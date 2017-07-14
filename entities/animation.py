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