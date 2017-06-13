import tdl

class Level(object):
    def __init__(self, width, height):
        self.data = tdl.Console(width, height)

    def draw_char(self, x, y, fg=Ellipsis, bg=Ellipsis):
        self.data.draw_char(x, y, fg, bg)

    def get_char(self, x, y):
        return self.data.get_char(x, y)

    def draw(self, console):
        console.blit(self.data)
