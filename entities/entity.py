class Entity(object):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        self.char = char
        self.position = position
        self.fg = fg
        self.bg = bg

    def draw(self, console):
        if self.position in console:
            console.draw_char(*self.position, self.char, self.fg, self.bg)

    def update(self):
        pass

    def handle_events(self, event):
        pass